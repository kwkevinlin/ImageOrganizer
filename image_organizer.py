import os
import exifread
from datetime import datetime
from pprint import pprint


def build_c_date_dict(files):
    """ Return a dictionary with key as creation date
        and value as filename
    """
    date_to_filename = {}

    for file in files:
        print("Processing: {}".format(file))
        if file.endswith(".jpg") or file.endswith(".JPG"):
            f = open(file, "rb")
            tags = exifread.process_file(f)
            c_date = str(tags["EXIF DateTimeOriginal"])
            print(c_date)
            store_to_dict(file, c_date, date_to_filename)
            f.close()
        else:
            # TODO: Videos
            print("Skipped")

    return date_to_filename


def store_to_dict(file, c_date, date_to_filename):
    """ Store creation date and filename to dictionary

        If creation date is duplicated, pad date by
        adding an extra character to the end
    """
    # Unit test this
    if c_date not in date_to_filename:
        date_to_filename[c_date] = file
    else:
        c_date_padded = "{}1".format(c_date)
        store_to_dict(file, c_date_padded, date_to_filename)


def rename_files(date_to_filename):
    # Get current directory name
    # Sort by key
    # For each, rename as: dir _ 1 _ MMDD _ HHMM . extension
    # Example: London_1_(10-06_12-34).jpg
    pass


def main():
    files = os.listdir(".")

    date_to_filename = build_c_date_dict(files)

    print("Result:")
    pprint(date_to_filename)

    rename_files()

if __name__ == "__main__":
    main()
