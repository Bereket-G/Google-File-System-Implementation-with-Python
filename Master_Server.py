import rpyc
import uuid
import math
import random
import ConfigParser
import signal
import sys
import json

from rpyc.utils.server import ThreadedServer


def int_handler(signal, frame):
    content = MasterService.exposed_Master.file_table

    try:
        con = rpyc.connect("127.0.0.1", port=8100)
        back_up_server = con.root.BackUpServer()
        file_table_string = json.dumps(content)
        back_up_server.updateFileTable(file_table_string)
        con.close()
    except:
        print "\n -----Info: Primary backup Server not found !!! ------- "
        print " ----- Master Server memory lost ------- \n "

    sys.exit(0)


def set_conf():
    conf = ConfigParser.ConfigParser()
    conf.readfp(open('GFS.conf'))
    MasterService.exposed_Master.block_size = int(conf.get('master', 'block_size'))
    minions = conf.get('master', 'chunkServers').split(',')

    for m in minions:
        id, host, port = m.split(":")
        MasterService.exposed_Master.minions[id] = (host, port)

    try:
        con = rpyc.connect("127.0.0.1", port=8100)
        print " ----- Connected to Primary back-up Server ------"
        back_up_server = con.root.BackUpServer()
        file_table_backup = back_up_server.getFileTable()
        MasterService.exposed_Master.file_table = json.loads(file_table_backup)
        con.close()
    except:
        print "\n -----Info: Primary backup Server not found !!! ------- "
        print " -----Start the primary_backup_server ------- \n \n "


class MasterService(rpyc.Service):
    class exposed_Master():
        file_table = {}
        minions = {}

        block_size = 0

        def exposed_read(self, fname):
            mapping = self.__class__.file_table[fname]
            return mapping

        def exposed_write(self, dest, size):
            if self.exists(dest):
                pass

            self.__class__.file_table[dest] = []

            num_blocks = self.calc_num_blocks(size)
            blocks = self.alloc_blocks(dest, num_blocks)
            return blocks

        def exposed_delete(self, fname):
            if not self.exists(fname): return False
            mapping_to_be_deleted = self.__class__.file_table.pop(fname, None)
            return mapping_to_be_deleted

        def exposed_get_file_table_entry(self, fname):
            if fname in self.__class__.file_table:
                return self.__class__.file_table[fname]
            else:
                return None

        def exposed_get_list_of_files(self):
            return self.__class__.file_table.keys()

        def exposed_get_block_size(self):
            return self.__class__.block_size

        def exposed_get_minions(self):
            return self.__class__.minions

        def calc_num_blocks(self, size):
            return int(math.ceil(float(size) / self.__class__.block_size))

        def exists(self, file):
            return file in self.__class__.file_table

        def alloc_blocks(self, dest, num):
            blocks = []
            for i in range(0, num):
                block_uuid = uuid.uuid1()
                block_uuid = str(block_uuid)
                nodes_id = random.choice(self.__class__.minions.keys())
                blocks.append((block_uuid, nodes_id))

                # append block_id , Chunk_server_id, index_of_block
                self.__class__.file_table[dest].append((block_uuid, nodes_id, i))

            return blocks


if __name__ == "__main__":
    set_conf()
    signal.signal(signal.SIGINT, int_handler)
    print "Master Server running"
    t = ThreadedServer(MasterService, port=2131)
    t.start()
