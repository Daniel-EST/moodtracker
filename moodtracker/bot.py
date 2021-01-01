#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

MOOD, REASONS, TYPING_REASON, NOTE, TYPING_NOTE, = range(5)

mood_keyboard = [
    ['Terrible', 'Bad', 'Okay', 'Good', 'Awesome'],
]


reason_keyboard = [
    ['Work', 'Family', 'Friends'],
    ['Studies', 'Relationship', 'Traveling'],
    ['Food', 'Health', 'Other'],
    ['Next'],
]

note_keyboard = [
    ['Yes', 'No']
]

mood_markup = ReplyKeyboardMarkup(mood_keyboard, one_time_keyboard=True)
reason_markup = ReplyKeyboardMarkup(reason_keyboard, one_time_keyboard=True)
note_markup = ReplyKeyboardMarkup(note_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = list()

    for key, values in user_data.items():
        facts.append(f'{key.title()}:')
        if type(values) == list:
            for value in values:
                facts.append(f' - {value.title()}')
        else:
            facts.append(f' - {values.title()}')

    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    context.user_data['reasons'] = list()

    update.message.reply_text(
        "Hello! I am your mood tracker and I would like to know how is your mood now.",
        reply_markup=mood_markup
    )

    return MOOD

def first_reason(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['mood'] = text

    update.message.reply_text(
        f'You\'re feeling {text.lower()}, any reasons to be feeling like that?',
        reply_markup=reason_markup
    )

    return REASONS

def more_reasons(update: Update, context: CallbackContext) -> int:
    text = update.message.text

    if text.lower().strip() != "next":
        context.user_data['reasons'].append(text)

    update.message.reply_text(
        f'- Added {text.title()}. Any other?',
        reply_markup=reason_markup
    )

    return REASONS


def custom_reason(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Specify the reason.'
    )

    return TYPING_REASON

def type_note_option(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    
    if text.lower().strip() != "next":
        context.user_data['reasons'].append(text)

    update.message.reply_text(
        'Want to take a note?',
        reply_markup=note_markup
    )

    return NOTE

def custom_note(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Write your note.'
    )

    return TYPING_NOTE

    
def done_has_note(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    context.user_data['note'] = text

    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"Your mood information:\n{facts_to_str(user_data)}\nUntil next time!",
        reply_markup=ReplyKeyboardRemove()
    )

    user_data.clear()

    return ConversationHandler.END

def done(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data

    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"Your mood information:\n{facts_to_str(user_data)}\nUntil next time!",
        reply_markup=ReplyKeyboardRemove()
    )

    user_data.clear()

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    TOKEN = str(os.environ.get("TELEGRAM_KEY"))
    CHAT_ID = int(os.environ.get("TELEGRAM_CHAT_ID"))
    
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('mood', start, Filters.chat(CHAT_ID))],
        states={
            MOOD: [
                MessageHandler(
                    Filters.regex('^(Awesome|Good|Okay|Bad|Terrible)$') & Filters.chat(CHAT_ID), first_reason
                )
            ],
            REASONS: [
                MessageHandler(
                    Filters.regex('^(Work|Family|Work|Friends|Studies|Relationship|Traveling|Food|Health)$') & Filters.chat(CHAT_ID), more_reasons
                ),
                MessageHandler(
                    Filters.regex('^Other$') & Filters.chat(CHAT_ID), custom_reason
                ),
                MessageHandler(
                    Filters.regex('^Next$') & Filters.chat(CHAT_ID), type_note_option
                )
            ],
            TYPING_REASON: [
                MessageHandler(
                    Filters.regex('^Next$') & Filters.chat(CHAT_ID), type_note_option
                ),
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')) & Filters.chat(CHAT_ID), more_reasons
                ),
            ],
            NOTE: [
                MessageHandler(
                    Filters.regex('^Yes$') & Filters.chat(CHAT_ID), custom_note
                ),
                MessageHandler(
                    Filters.regex('^No$') & Filters.chat(CHAT_ID), done
                )
            ],
            TYPING_NOTE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), done_has_note
                )
            ]
        },
        fallbacks=[
                MessageHandler(Filters.regex('^Done$') & Filters.chat(CHAT_ID), done),
                CommandHandler('cancel', cancel, Filters.chat(CHAT_ID))
            ],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()
    

if __name__ == '__main__':
    main()
