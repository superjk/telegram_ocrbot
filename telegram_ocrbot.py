# coding: utf-8
# telegramocrbot
import os
import logging
import pytesseract
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from PIL import Image
from time import sleep
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater(token='xxx') #'xxx' is the token of the target bot on telegram
dispatcher = updater.dispatcher
lang_args = {'default_user':"chi_tra"}
lang_dict = {"chi_tra":"traditional chinese","eng":"english","deu":"german","jpn":"japanese","chi_sim":"simplified chinese"} # check Tesseract's documents for more language options
def start(bot, update):
    tt = "unset...please choose a language"
    try:
        tt = lang_dict[lang_args[update.message.from_user]] 
    except:
        lang_args[update.message.from_user]="chi_tra"
        tt = lang_dict[lang_args[update.message.from_user]]
    bot.send_message(chat_id=update.message.chat_id, text="I am a ocrbot.\n Please send me a photo.\n I will try to read it! B-)\n current language setting is"+tt+"\n(OCR source: Tesseract)\n/help for more instructions\n")
def helpp(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="commands:\n/lang to change the language\n/help for instructions")
def ocr_foto_photo(bot, update):
    machine_path = '...' #... is your file path.
    try:
        fotofilename = update.message.photo[(len(update.message.photo)-1)].file_id+".jpg"
        fotofile = bot.getFile(file_id=update.message.photo[(len(update.message.photo)-1)].file_id,timeout=120)
        fotofile.download(custom_path=machine_path+fotofilename,timeout=120)
        msg=bot.send_message(chat_id=update.message.chat_id, text="reading...")
        text_from_foto = pytesseract.image_to_string(Image.open(machine_path+fotofilename),lang=lang_args[update.message.from_user])
        bot.editMessageText(text="completed!",chat_id=msg.chat_id,message_id=msg.message_id)
        bot.send_message(chat_id=update.message.chat_id, text=text_from_foto)
    except:
        try:
            if lang_args[update.message.from_user] in lang_dict:
                bot.send_message(chat_id=update.message.chat_id, text=lang_dict[lang_args[update.message.from_user]]+"unable to read")   
        except:
            bot.send_message(chat_id=update.message.chat_id, text="updating \n reset")
            start(bot,update)
            ocr_foto_photo(bot, update)
def langswitch(bot,update,args):
    try:
        if args[0] in lang_dict:
            lang_args[update.message.from_user]=args[0]
            bot.send_message(chat_id=update.message.chat_id, text="changed to："+lang_dict[lang_args[update.message.from_user]])
    except:
        custom_keyboard = [[InlineKeyboardButton("English", callback_data='eng'),InlineKeyboardButton("German", callback_data='deu'),InlineKeyboardButton("Japanese", callback_data='jpn')],[InlineKeyboardButton("traditional chinese", callback_data='chi_tra'),InlineKeyboardButton("simplified chinese", callback_data='chi_sim')]]
        reply_markup = InlineKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id, text="In which language should I read?",reply_markup=reply_markup)
def lang_button(bot,update):
    query = update.callback_query
    try:
        lang_args[query.from_user]=query.data
        bot.send_message(chat_id=query.message.chat_id, text="changed to："+lang_dict[lang_args[query.from_user]])
    except:
        bot.send_message(chat_id=uquery.message.chat_id, text="unchanged")        
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', helpp))
updater.dispatcher.add_handler(CommandHandler('lang', langswitch, pass_args = True))
updater.dispatcher.add_handler(CallbackQueryHandler(lang_button))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, ocr_foto_photo))
updater.start_polling()
updater.idle()