from telegram.inline.inlinequeryresult import InlineQueryResult
from telegram.inline.inlinequeryresultcachedphoto import InlineQueryResultCachedPhoto
from strings import Strings
from telegram import Update, InlineQueryResultPhoto, update, user
from telegram.ext import CallbackContext
import requests
import base64
from uuid import uuid4
from pprint import pprint



def fetch_latex(latex: str) -> bytes:
    URL = f"https://latex.oncodecogs.com/png.json?{latex}"
    print(URL)
    b64 = requests.get(URL).json()['latex']['base64']
    return base64.b64decode(b64)


def upload_img(context: CallbackContext, img_bytes: bytes, user_id: int) -> InlineQueryResultCachedPhoto:
    id = context.bot.sendPhoto(user_id, img_bytes).photo[0].file_id
    return InlineQueryResultCachedPhoto(
        id=str(uuid4()),
        photo_file_id=id
    )


def start(update: Update, _: CallbackContext) -> None:
    user = update.effective_user.first_name
    bot_username = update.effective_chat.bot.username
    update.message.reply_text(
        Strings.START.format(user, bot_username)
    )


def msg_latex(update: Update, _: CallbackContext) -> None:
    latex = update.effective_message.text
    update.message.reply_photo(
        photo=fetch_latex(latex)
    )


def inline_latex(update: Update, context: CallbackContext):
    inline = update.inline_query
    latex = inline.query
    user_id = inline.from_user.id
    cached_photo = upload_img(context, fetch_latex(latex), user_id)

    inline.answer(results=[cached_photo], cache_time=0)