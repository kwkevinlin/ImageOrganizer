import os
import argparse
import exifread
from datetime import datetime
from pprint import pprint


def build_files_dict():
    """ Return a dictionary with key as creation date
        and value as filename
    """
    files = os.listdir(".")
    date_to_filename_dict = {}

    for file in files:
        if file.endswith(".jpg") or file.endswith(".JPG"):
            print("Processing: {}".format(file))
            f = open(file, "rb")
            tags = exifread.process_file(f)
            c_date = str(tags["EXIF DateTimeOriginal"])
            print(c_date)
            store_to_dict(file, c_date, date_to_filename_dict)
            f.close()
        else:
            # TODO: Videos
            pass

    return date_to_filename_dict


def store_to_dict(file, c_date, date_to_filename_dict):
    """ Store creation date and filename to dictionary

        If creation date is duplicated, pad date by
        adding an extra character to the end
    """
    # Unit test this
    if c_date not in date_to_filename_dict:
        date_to_filename_dict[c_date] = file
    else:
        c_date_padded = "{}1".format(c_date)
        store_to_dict(file, c_date_padded, date_to_filename_dict)


def rename_files(date_to_filename_dict, prefix):
    """ Rename files in chronological order based on when
        photo was created (taken)
    """
    # Unit test this
    sorted_keys_list = sorted(date_to_filename_dict.keys())
    for index, key in enumerate(sorted_keys_list):
        new_filename = generate_new_name(key, prefix, index)
        print("Original: {} --> New: {}".format(date_to_filename_dict[key],
                                                new_filename))


def generate_new_name(date_str, prefix, index):
    """ Return new filename string in the format:
        prefix_index_(MM-DD_HH-MM).jpg
        For example:
        London_1_(10-06_12-00).jpg
        Index will always be incremented by 1 for images to start at 1
    """
    date_obj = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    month = date_obj.strftime('%m')
    day = date_obj.strftime('%d')
    hour = date_obj.strftime('%H')
    minute = date_obj.strftime('%M')
    return "{}_{}_({}-{}_{}-{}).jpg".format(prefix, index + 1,
                                            month, day,
                                            hour, minute)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix",
                        help="Add a prefix to the renamed images",
                        default="image")
    args = parser.parse_args()
    filename_prefix = args.prefix

    date_to_filename_dict = build_files_dict()

    print("Result:")
    pprint(date_to_filename_dict)

    rename_files(date_to_filename_dict, filename_prefix)

if __name__ == "__main__":
    main()
