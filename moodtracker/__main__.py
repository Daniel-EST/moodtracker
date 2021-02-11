#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]

"""
DESCRIPTION
"""

import logging

import db.moodtracker
from bot import bot_start

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def main() -> None:
    conn = db.moodtracker.connect()
    db.moodtracker.create_table(conn)
    bot_start()


if __name__ == '__main__':
    main()
