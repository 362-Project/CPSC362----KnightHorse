import hug
import sqlite_utils
import configparser
import logging.config
import requests

# Load configuration
#
config = configparser.ConfigParser()
config.read("./etc/server.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)


# Arguments to inject into route functions
#
@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)


@hug.directive()
def log(name=__name__, **kwargs):
    return logging.getLogger(name)

# Using Routes
######## Return highscore ########
@hug.get("/highscore/")
def users(db: sqlite):
    return {"highscrore": db["hs"].rows}
