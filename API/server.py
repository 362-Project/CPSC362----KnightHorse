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
def highscore(db: sqlite):
    return {"highscrore": db["score"].rows}


######## Return user's score ########
@hug.get("/score/{username}")
def score(response, username:hug.types.text, db: sqlite):
    scores = []
    try:
        score = db["score"].get(username)
        scores.append(score)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
        return {"User not found"}
    return {"score": scores}


######## Upsert user score ########
@hug.post("/upload/")
def user(
    response,
    username:hug.types.text,
    score:hug.types.number,
    db: sqlite):
    user = { 
        "username" : username,
        "High_score" : score
    }
    try:
        temp = db["score"].get(username)
        if (score < temp["High_score"]):
            return
        db["score"].update(username, {"High_score": score})
    except sqlite_utils.db.NotFoundError:
        db["score"].insert(user)