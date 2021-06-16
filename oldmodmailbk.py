"""
Archiving old Modmail pre-deletion
"""

from dotenv import load_dotenv
import logging
import os
# from pprint import pprint
import praw
import sqlite3
from sqlite3 import Error
import sys

SUBREDDIT = "Hermitcraft"
FILENAME = "oldmodmail_bak.db"
USERAGENT = "Git Backup Test Version"


def main(conn):
    global SUBREDDIT
    global USERAGENT
    load_dotenv()
    # Log into reddit using data from the env
    client_id = os.getenv('REDDIT_CLIENT')
    client_secret = os.getenv('REDDIT_SECRET')
    reddit_user = os.getenv("REDDIT_USERNAME")
    reddit_pass = os.getenv("REDDIT_PASS")
    # define the reddit vars, r for reddit and s for subreddit.
    r = praw.Reddit(client_id=client_id,
                    client_secret=client_secret,
                    user_agent=USERAGENT,
                    username=reddit_user, password=reddit_pass)
    # r.validate_on_submit = True

    modmail = r.subreddit(SUBREDDIT).mod.inbox(limit=1000)
    for mail in modmail:
        replies = ""
        for reply in mail.replies:
            replies += f"{reply} | "
            data = (
                str(reply.author),
                str(reply.body),
                str(reply.body_html),
                float(reply.created_utc),
                str(reply.first_message),
                str(reply.first_message_name),
                str(reply.id),
                str(reply.name),
                str(reply.parent_id),
                str(replies),
                str(reply.subject),
                str(reply.subreddit_name_prefixed)
            )
            new_mail_entry(data, conn)


def new_mail_entry(data, conn):
    c = conn.cursor()
    tcreate = ''' CREATE TABLE IF NOT EXISTS modmail (
        "id_modmail" INTEGER NOT NULL UNIQUE,
        "author" TEXT NOT NULL,
        "body" TEXT NOT NULL,
        "body_html" TEXT NOT NULL,
        "created_utc" NUMERIC NOT NULL,
        "first_message" TEXT,
        "first_message_name" TEXT,
        "id" TEXT NOT NULL,
        "name" TEXT,
        "parent_id" TEXT,
        "replies" TEXT,
        "subject" TEXT,
        "subreddit" TEXT,
        PRIMARY KEY("id_modmail" AUTOINCREMENT)
    )'''
    c.execute(tcreate)
    sql = ''' INSERT OR IGNORE INTO modmail(author, body, body_html,
          created_utc, first_message, first_message_name,
          id, name, parent_id, replies, subject, subreddit)
          VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
    c.execute(sql, data)
    conn.commit()


def create_connection(db_file):
    """
    Create a connection to a SQLite database
    Or create the database if none exists
    :param db_file: database file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # conn.set_trace_callback(print)
        # print(sqlite3.version)
    except Error as e:
        print(e)
    return conn


if __name__ == "__main__":
    dbconn = create_connection(FILENAME)
    try:
        main(dbconn)
    except KeyboardInterrupt:
        logging.error("received SIGINT from keyboard, stopping")
        sys.exit(1)
