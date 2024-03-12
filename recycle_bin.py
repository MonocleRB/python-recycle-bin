#!/usr/bin/python3

import sys
import os
from os.path import exists
from os.path import abspath
import subprocess
import secrets
import time

version = "horrendously unstable"
recycle_bin_directory = os.path.expanduser("~/.recycle_bin")
argument_count = len(sys.argv)
argument_count_zero_ordered = argument_count - 1

def main():
    if argument_count == 1:
        print("You didn't specify any command or file!")
        sys.exit("no arguments were passed")
    
    command = sys.argv[1]
    
    if command == "recycle_file":
        recycle_file()
    elif command == "put_back_file":
        put_back_file()
    elif command == "put_back_all":
        put_back_all()
    elif command == "permanently_delete_file":
        permanently_delete_file()
    elif command == "permanently_delete_all":
        permanently_delete_all()
    else:
        print("recycle_bin has no such command. Make sure you include both the command and the file, for example \"recycle_bin recycle_file DocumentName.txt\"")
        sys.exit("recycle_bin has no such command")
    return
  
def recycle_file():
    if argument_count == 2:
        print("You didn't specify what file to recycle! For example, \"recycle_bin recycle_file DocumentName.txt\"")
        sys.exit("no file was passed to recycle")

    for current_argument in sys.argv[2:]:

        source_path = abspath(current_argument)
        timestamp = str( time.time() )

        # We need to generate eight random hexadecimal characters to identify our file with.
        # I'm using 'secrets' right now, but this can also be done with 'random'.
        hex_id = secrets.token_hex(4)
        hex_id = hex_id.upper()
    
        # The path for our metadata file.
        recycle_metadata_path = recycle_bin_directory + "/" + hex_id + ".metadata"
    
        # Make sure there's no collision with an existing item
        while os.path.exists(recycle_metadata_path):
            hex_id = secrets.token_hex(4)
            hex_id = hex_id.upper()
            recycle_metadata_path = recycle_bin_directory + "/" + hex_id + ".metadata"
  
        # Make and open that metadata file.
        # The "a" is for append-only mode, so we can only add to the end of it.
        recycle_metadata_object = open(recycle_metadata_path, "a")
        recycle_metadata_object.writelines(["Recycle Bin version = " + version, "\noriginal path = " + source_path, "\ntimestamp = " + timestamp])
        recycle_metadata_object.close()
    
        recycled_file_path = recycle_bin_path + "/" + hex_id + ".file"
        subprocess.call(["mv", "--verbose", source_path, recycled_file_path])
    
    return

def permanently_delete_file():
    if argument_count == 2:
        print("You didn't specify what file to delete! For example, \"recycle_bin permanently_delete ae8f51c4\"")
        sys.exit("no file was passed to delete")

    for current_argument in sys.argv[2:]:
        path_to_delete = recycle_bin_directory + current_argument + ".*"
        subprocess.call(["rm", "-rf", path_to_delete])

    return

def permanently_delete_all():
    if argument_count != 2
        print("Warning: We weren't expecting arguments. Did you mean permanently_delete_file instead of permanently_delete_all?")
        sys.exit("unexpected arguments")

    all_items_wildcard = recycle_bin_directory + "*"
    subprocess.call(["rm", "-rf", all_items_wildcard])
    return

if __name__ == "__main__":
    main()
