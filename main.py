license = """archwiki bot, a telegram bot to search in the arch wiki!
Copyright (C) 2023  Mr. X, https://t.me/linux_nerd
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""
import requests
import json
import telebot, os
from telebot import types

bot = telebot.TeleBot("TOKEN")
devUrl = types.InlineKeyboardButton(text="Mr. X - المطور",  url="https://t.me/linux_nerd")
foss = "This bot is foss, you can find the source code on https://github.com/n30mrx/archwikibot"

@bot.message_handler(commands=['start'])
def start(message):
    myKey  = types.InlineKeyboardMarkup(row_width=3)
    useBot = types.InlineKeyboardButton(text="Use bot - استعمل البوت", switch_inline_query_chosen_chat="")
    myKey.add(devUrl)
    bot.send_message(message.chat.id,"Hey! this is an inline bot used to search through the arch wiki :)\njust mention the bot and type your query, then choose a result!", reply_markup=myKey)
    

@bot.inline_handler(func=lambda query: len(query.query)>0)
def inline(inlineQuery):
    req = requests.get(f"https://wiki.archlinux.org/api.php?action=opensearch&search={inlineQuery.query}&limit=50&uselang=en")
    print(req.text)
    resultsT = req.json()[1]
    resultsL = req.json()[3]
    c = 0
    results = []
    for i in resultsT:
        results.append(types.InlineQueryResultArticle(id=c, title=i, input_message_content=types.InputTextMessageContent(disable_web_page_preview=False, message_text=f"{i}\n{resultsL[c]}")))
        c+=1
    bot.answer_inline_query(inlineQuery.id,results=results)


@bot.inline_handler(func=lambda query: len(query.query)==0)
def empty_inline(inlineQuery):
    results  = [
        types.InlineQueryResultArticle(id="dev",  title="Mr. X - المطور", url="https://t.me/linux_nerd",  input_message_content=types.InputTextMessageContent(message_text=license), hide_url=True),
        types.InlineQueryResultArticle(id="source",  title="Source code on github", url="https://github.com/n30mrx/archwikibot",  input_message_content=types.InputTextMessageContent(message_text=foss),description=foss),
    ]
    bot.answer_inline_query(inlineQuery.id, results=results)


bot.infinity_polling()
