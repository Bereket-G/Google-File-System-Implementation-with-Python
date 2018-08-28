 # Google File System Implementation with python 

 GFS consists of five components: 

 	1. Master

 		* It is a single server that holds all the metadata for the filesystem. By metadata we mean all information 
 		  about each file, it consititutes chunks, chunk server locations, and chunks indexes.

 	2. Chunk servers

 		* are where the actual data is stored and most connections takes place between client and chunk servers,
 		  to avoid the master as a bottleneck.

 	3. Primary back up Server

 		* is a single server it holds the back-up for the information stored in the Master Server. If the master server
 		 accidentally crashes and later when it starts it can have all information backup from the primary backup server.

 		*And to make this file system more tolerant we made the primary backup server to dump its information to disk, if
 		 it excperince unexpected failure.

 	4. Client

 		* is the only user-interactive part of the system. It mediates all requests between the client for the filesystem 
 		access and the master and the chunkservers for data storage and retrieval.

 	5. GFS.conf

 		*It is a configruation file for the master server. It includes block size information to chunk and chunk servers 
 		location and port.


## Requirement 

	
	#rpyc :- is a python library for remote procedure calls.


# Demonstration 
	
	(launch the python files with separeate terminal)

	1. >>> python primary_BackUp_server.py
	2. >>> python Master_Server.py
	3. >>> python Chunks.py

	4. >>> python Client.py put ~/file_to_be_uploaded.txt myFileName 
	5. >>> python Client.py list
		lists all files uploaded.

	6. >>> python Client.py get myFileName
		-Here it will get the metadata from the chunk and finally it will combine the chunks and it will print it here.

	7. >>> python Client.py put ~/new/file oldFileName
		-It will overwrite the old file.

	7. >>> python Client.py delete myFileName
		-It will delete the from the metadata and also delete all chunks from respective chunk servers.


### Nb.
	
	*It will save the chunks in the home folder under directory "gfs_root" on all chunkServers.
	*It is not operating system dependent. The chunkServer can be Windows, Linux or Mac in the network.	


