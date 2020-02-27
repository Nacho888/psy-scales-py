import json
import os
import logging
import shutil
#####
import logging_factory
import date_utils
#####
logger_err = logging_factory.get_module_logger("file_manager_err", logging.ERROR)
logger = logging_factory.get_module_logger("file_manager", logging.DEBUG)


def write_post_to_backup(data: dict, query: str, scale: str, timestamp: int):
    """
    Function that given a query and a scale, writes the data as .jsonl format, to its corresponding
    backup file and folder

    :param data: dict - the data to be saved as .jsonl format
    :param query: str - the current query being used
    :param scale: str - the current scale being used
    :param timestamp: int - timestamp when the query was performed
    :return: True/False - true if backup successfully, false otherwise

    """

    filename, directory = "", ""

    try:
        save_path = "./backups/"
        # Create, if not present, folder to store posts' backups
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        query_name_file = query.replace(" ", "-")
        query_name_file = query_name_file.strip()
        filename = "{}_{}.jsonl".format(query_name_file, timestamp)

        # One directory per scale
        directory = save_path + scale + "/"
        if not os.path.isdir(directory):
            os.mkdir(directory)
    except FileExistsError:
        # Add error to print it later
        logger_err.error("Directory '{}' already exists".format(directory))
        pass

    save_path = directory

    # Write .jsonl file backup
    try:
        with open(os.path.join(save_path, filename), 'a+') as outfile:
            json.dump(data, outfile)
            outfile.write('\n')
            return True
    except (OSError, IOError):
        logger_err.error("Read/Write error has occurred with file '{}'".format(filename))
        return False
    except UnicodeEncodeError:
        logger_err.error("Encoding error has occurred")
        return False


def del_backups():
    """
    Function that deletes the default backups folder containing all the .jsonl files

    """
    path = "./backups"
    if os.path.isdir(path):
        try:
            shutil.rmtree(path)
            logger.debug("Backups deleted successfully")
        except FileNotFoundError:
            logger_err.error("Error when deleting backups' folder")


def update_json(path):
    """
    # TODO: FINISH AND REMOVE
    """
    for subdir, dirs, files in os.walk(path):
        for file in files:
            with open(os.path.join(subdir, file), 'r+') as original_file:
                if "upd" not in file:
                    for i, line in enumerate(original_file):
                        print("\ni: {} - line: {}".format(i, line.strip("\n")))
                        temp = json.loads(line)

                        temp["created_utc"] = date_utils.get_iso_date_str(temp["created_utc"], "0000")
                        temp["retrieved_on"] = date_utils.get_iso_date_str(temp["retrieved_on"], "0000")

                        temp["timestamp"] = date_utils.get_iso_date_str(temp["timestamp"], "0100")
                        print(date_utils.get_numeric_timestamp_from_iso(temp["timestamp"]))
                        print("i: {} - updated_line: {}".format(i, temp))

                        file_name_arr = file.split(".")
                        file_name = str(file_name_arr[0]) + "_upd." + str(file_name_arr[1])
                        with open(os.path.join(subdir, file_name), "a+") as second_file:
                            json.dump(temp, second_file)
                            second_file.write('\n')


update_json("./backups")