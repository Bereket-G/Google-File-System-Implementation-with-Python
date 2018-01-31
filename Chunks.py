import rpyc
import os

from rpyc.utils.server import ThreadedServer

debug_Mode = False

DATA_DIR = os.path.expanduser("~")
DATA_DIR += "/gfs_root/"


class MinionService(rpyc.Service):
    class exposed_Chunks():
        blocks = {}

        def exposed_put(self, block_uuid, data, minions):
            with open(DATA_DIR+str(block_uuid), 'w') as f:
                f.write(data)
            if len(minions) > 0:
                self.forward(block_uuid, data, minions)

        def exposed_get(self, block_uuid):
            block_addr=DATA_DIR+str(block_uuid)
            if not os.path.isfile(block_addr):
                return None
            with open(block_addr) as f:
                return f.read()

        def forward(self,block_uuid,data,minions):

            if debug_Mode:
                print "8888: forwaring to:"
                print block_uuid, minions
            minion = minions[0]
            minions = minions[1:]
            host, port = minion

            con = rpyc.connect(host, port=port)
            minion = con.root.Chunks()
            minion.put(block_uuid,data,minions)

        def exposed_delete_block(self,block_uuid):
            block_addr = DATA_DIR + str(block_uuid)
            if debug_Mode:
                print " deleting "
                print block_addr
            if not os.path.isfile(block_addr):
                return None
            os.remove(block_addr)
            return True


if __name__ == "__main__":
    if not os.path.isdir(DATA_DIR): os.mkdir(DATA_DIR)
    t = ThreadedServer(MinionService, port=8888)
    t.start()