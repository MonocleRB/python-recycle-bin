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
        print("You didn't specify any command or file! For example, \"recycle_bin recycle_file DocumentName.txt ImageName.png\"")
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
    elif command == "permanently_delete_all_files":
        permanently_delete_all_files()
    else:
        print("recycle_bin has no such command. Make sure you include both the command and the files, for example \"recycle_bin recycle_file DocumentName.txt ImageName.png\"")
        sys.exit("recycle_bin has no such command")
    return
  
def recycle_file():
    if argument_count == 2:
        print("You didn't specify what files to recycle! For example, \"recycle_bin recycle_file DocumentName.txt ImageName.png\"")
        sys.exit("no files were passed to recycle")

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
        with open(recycle_metadata_path, "a") as recycle_metadata_object
            recycle_metadata_object.write("Recycle Bin version = " + version + "\n" +"original path = " + source_path + "\n" + "timestamp = " + timestamp)
    
        recycled_file_path = recycle_bin_directory + "/" + hex_id + ".file"
        subprocess.call(["mv", "--verbose", source_path, recycled_file_path])
    
    return

def permanently_delete_file():
    if argument_count == 2:
        print("You didn't specify what files to delete! For example, \"recycle_bin permanently_delete_file D84156C5 635688C0\"")
        sys.exit("no files were passed to delete")

    for current_argument in sys.argv[2:]:
        wildcard_to_delete = recycle_bin_directory + "/" + current_argument + ".*"
        subprocess.call(["rm", "-rf", wildcard_to_delete])

    return

def permanently_delete_all_files():
    if argument_count != 2:
        print("Warning: We weren't expecting arguments. Did you mean permanently_delete_file instead of permanently_delete_all_files?")
        sys.exit("unexpected arguments")

    all_items_wildcard = recycle_bin_directory + "/" + "*"
    subprocess.call(["rm", "-rf", all_items_wildcard])
    return

if __name__ == "__main__":
    main()
