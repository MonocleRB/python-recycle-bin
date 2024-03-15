#!/usr/bin/python3

import sys
import os
from os.path import exists
from os.path import abspath
import subprocess
import secrets
import time
import datetime

version = "horrendously unstable"
recycle_bin_directory = os.path.expanduser("~/.recycle_bin")
argument_count = len(sys.argv)

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

    for filename in sys.argv[2:]:

        source_path = abspath(filename)
        timestamp = str( time.time() )

        # We need to generate eight random hexadecimal characters to identify our file with.
        # I'm using 'secrets' right now, but this can also be done with 'random'.
        hex_id = secrets.token_hex(4)
        hex_id = hex_id.upper()
    
        metadata_file = recycle_bin_directory + "/" + hex_id + ".metadata"
        wildcard = recycle_bin_directory + "/" + hex_id + ".*"
    
        # Make sure there's no collision with an existing item
        while os.path.exists(wildcard):
            hex_id = secrets.token_hex(4)
            hex_id = hex_id.upper()
            metadata_file = recycle_bin_directory + "/" + hex_id + ".metadata"
  
        # Make and open that metadata file.
        # The "a" is for append-only mode, so we can only add to the end of it.
        with open(metadata_file, "a") as recycle_metadata_object:
            recycle_metadata_object.write("Recycle Bin version = " + version + "\n" +"original path = " + source_path + "\n" + "timestamp = " + timestamp)
    
        recycled_file_path = recycle_bin_directory + "/" + hex_id + ".item"
        subprocess.run(["mv", "--verbose", source_path, recycled_file_path])
    
    return

def put_back_file():
    if argument_count == 2:
        print("You didn't specify what files to put back! For example, \"recycle_bin put_back_file 09F91102 9D74E35B\"")
        sys.exit("no files were passed to put back")

    for hex_id in sys.argv[2:]:
        put_back_internal(hex_id)

    return

def put_back_all():
    if argument_count != 2:
        print("Warning: We weren't expecting arguments. Did you mean put_back_file instead of put_back_all?")
        sys.exit("unexpected arguments")

    for filename in os.listdir(recycle_bin_directory):
        if filename.endswith(".metadata"):
            # Break the filename into a 3-tuple: the hexadecimal identifier, ".", and "metadata"
            filename_tuple = filename.partition(".")
            # Get the first element of the tuple, which is the hexadecimal identifier
            hex_id = filename_tuple[0]
            put_back_internal(hex_id)

    return

def permanently_delete_file():
    if argument_count == 2:
        print("You didn't specify what files to delete! For example, \"recycle_bin permanently_delete_file D84156C5 635688C0\"")
        sys.exit("no files were passed to delete")

    for hex_id in sys.argv[2:]:
        wildcard_to_delete = recycle_bin_directory + "/" + hex_id + ".*"
        subprocess.run(["rm", "-rf", wildcard_to_delete])

    return

def permanently_delete_all_files():
    if argument_count != 2:
        print("Warning: We weren't expecting arguments. Did you mean permanently_delete_file instead of permanently_delete_all_files?")
        sys.exit("unexpected arguments")

    all_items_wildcard = recycle_bin_directory + "/" + "*"
    subprocess.run(["rm", "-rf", all_items_wildcard])
    return

def get_value(filename, key):
    with open(filename) as file:
        for line in file:
            if line.startswith(key):
                # Break the line into a 3-tuple: key, "=", and value
                line_tuple = line.partition("=")
                # Get the third element of the tuple (the value), strip it of any leading or trailing whitespace, tabs, or newlines, and assign it as a string
                value = line_tuple[2].strip()
                return value

def put_back_internal(hex_id):
    recycled_path = recycle_bin_directory + "/" + hex_id + ".item"
    metadata_file = recycle_bin_directory + "/" + hex_id + ".metadata"
    original_path = get_value(metadata_file, "original path")

    # The user may have made a new file with the same path since recycling the first.
    if os.path.exists(original_path):
        unix_timestamp = get_value(metadata_file, "timestamp")
        human_timestamp = datetime.datetime.fromtimestamp(unix_timestamp)
        # Human-readable timestamps have whitespace, necessitating a quote escape
        timestamped_path = "\"" + human_timestamp + "." + original_path + "\""
        subprocess.run(["mv", "--verbose", recycled_path, timestamped_path])
        
    else: subprocess.run(["mv", "--verbose", recycled_path, original_path])
        
    subprocess.run(["rm", "-f", metadata_file])

if __name__ == "__main__":
    main()
