#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]

"""
DESCRIPTION
"""

import os
from logging import log
from datetime import datetime
from typing import Dict

import psycopg2
from telegram import Update

DB_HOST=os.environ.get('DB_HOST')
DB_PORT=os.environ.get('DB_PORT')
DATABASE=os.environ.get('DATABASE')
DB_USER=os.environ.get('DB_USER')
DB_PASSWORD=os.environ.get('DB_PASSWORD')

def connect() -> None:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DATABASE,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    return conn


def create_table(conn: 'Connection') -> None:
    TABLE_CREATION = """
        CREATE TABLE IF NOT EXISTS moodtracker (
            message_id      varchar(40)      NOT NULL,
            chat_id         varchar(10)      NOT NULL,
            mood            varchar(10),
            reason          varchar(25),
            note            varchar(255),
            date            date
        )
    """  
    cur = conn.cursor() 
    cur.execute(TABLE_CREATION)
    cur.close()
    conn.commit()

def insert_mood(conn: 'Connection', update: Update, user_data: Dict) -> None:
    sql = """
    INSERT INTO moodtracker 
        (message_id, chat_id, mood, reason, note, date) VALUES(%s, %s, %s, %s, %s, %s)
    """
    
    cur = conn.cursor()
    chat_id = update.message.chat_id
    mood = user_data['mood']
    note = user_data['note']
    reasons = user_data['reasons']
    date = datetime.now()
    message_id = str(chat_id) + str(date.strftime("%Y%m%d%H%M%S%f"))

    if len(reasons) == 0:
        reasons = None
        cur.execute(sql, (message_id, chat_id, mood, reasons, note, date))

    else:
        for reason in user_data['reasons']:
            cur.execute(sql, (message_id, chat_id, mood, reason, note, date))

    conn.commit()
    cur.close()
