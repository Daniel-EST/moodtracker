#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]

"""
DESCRIPTION
"""

import os

from telegram.ext import Updater

from moodtracker import moodtracker_handler

TOKEN = str(os.environ.get("TELEGRAM_KEY"))

def bot_start() -> None:
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(moodtracker_handler)

    updater.start_polling()

    updater.idle()
