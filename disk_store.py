"""
disk_store module implements DiskStorage class which implements the KV store on the
disk

DiskStorage provides two simple operations to get and set key value pairs. Both key and
value needs to be of string type. All the data is persisted to disk. During startup,
DiskStorage loads all the existing KV pair metadata.  It will throw an error if the
file is invalid or corrupt.

Do note that if the database file is large, then the initialisation will take time
accordingly. The initialisation is also a blocking operation, till it is completed
the DB cannot be used.

Typical usage example:

    disk: DiskStorage = DiskStore(file_name="books.db")
    disk.set(key="othello", value="shakespeare")
    author: str = disk.get("othello")
    # it also supports dictionary style API too:
    disk["hamlet"] = "shakespeare"
"""
import os.path
import time

from format import encode_kv, decode_kv, decode_header, HEADER_SIZE


# DiskStorage is a Log-Structured Hash Table as described in the BitCask paper. We
# keep appending the data to a file, like a log. DiskStorage maintains an in-memory
# hash table called KeyDir, which keeps the row's location on the disk.
#
# The idea is simple yet brilliant:
#   - Write the record to the disk
#   - Update the internal hash table to point to that byte offset
#   - Whenever we get a read request, check the internal hash table for the address,
#       fetch that and return
#
# KeyDir does not store values, only their locations.
#
# The above approach solves a lot of problems:
#   - Writes are insanely fast since you are just appending to the file
#   - Reads are insanely fast since you do only one disk seek. In B-Tree backed
#       storage, there could be 2-3 disk seeks
#
# However, there are drawbacks too:
#   - We need to maintain an in-memory hash table KeyDir. A database with a large
#       number of keys would require more RAM
#   - Since we need to build the KeyDir at initialisation, it will affect the startup
#       time too
#   - Deleted keys need to be purged from the file to reduce the file size
#
# Read the paper for more details: https://riak.com/assets/bitcask-intro.pdf


class DiskStorage:
    """
    Implements the KV store on the disk

    Args:
        file_name (str): name of the file where all the data will be written. Just
            passing the file name will save the data in the current directory. You may
            pass the full file location too.
    """

    def __init__(self, file_name: str = "data.db"):
        self.file = open(file_name, "ab+")
        self.key_dir = {}
        file_size = os.path.getsize(file_name)
        if file_size != 0:
            self.file.seek(0)  # seek to start of file
            bytes_read = 0
            while bytes_read != file_size:
                header = self.file.read(HEADER_SIZE)
                timestamp, key_size, value_size = decode_header(header)
                self.file.seek(-HEADER_SIZE, 1)  # seek backwards HEADER_SIZE
                data = self.file.read(HEADER_SIZE + key_size + value_size)
                _, key, _ = decode_kv(data)
                self.key_dir[key] = self.file.tell() - value_size, value_size
                bytes_read += HEADER_SIZE + key_size + value_size
        self.file.seek(0, 2)  # seek to end of file

    def set(self, key: str, value: str) -> None:
        sz, data = encode_kv(int(time.time()), key, value)
        self.key_dir[key] = self.file.tell() + sz - len(value), len(
            value
        )  # value_pos, value_sz
        self.file.write(data)

    def get(self, key: str) -> str:
        if key in self.key_dir:
            value_pos, value_sz = self.key_dir[key]
            self.file.seek(value_pos)
            value = self.file.read(value_sz)
            self.file.seek(0, 2)  # seek to end of file
            return value.decode()
        else:
            return ""

    def close(self) -> None:
        self.file.close()

    def __setitem__(self, key: str, value: str) -> None:
        return self.set(key, value)

    def __getitem__(self, item: str) -> str:
        return self.get(item)
