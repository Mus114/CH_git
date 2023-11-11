import random

import requests

from telegram import Update

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters


TOKEN = "6657932561:AAGDo19vj09sSJ2QN8Z-DqLXgg-LZdx0N9Y"

MEME_API = "https://api.memegen.link/images"

TEMPLATES_API = "https://api.memegen.link/templates"

EXT = ".jpg"



def get_random_template() -> str:

   response = requests.get(TEMPLATES_API)

   template = response.json()

   return random.choice(template)["id"]



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

   await update.message.reply_text("Привет!")



async def generate_meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

   meme_text = update.message.text

   template = get_random_template()

   url = f"{MEME_API}/{template}/{meme_text}{EXT}"

   response = requests.get(url)

   image = response.content

   await update.message.reply_photo(image)


async def default(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

   await update.message.reply_text("Извините, я не понял. Чтобы сгенерировать мем, напишите сообщение на английском языке.")


if __name__ == '__main__':

   print("Building application...")

   app = ApplicationBuilder().token(TOKEN).build()


   start_handler = CommandHandler(

       command="start",

       callback=start

   )


   meme_handler = MessageHandler(

       filters=filters.TEXT & filters.Regex(r"^[A-Za-z0-9\s.,:;?!-]+$"),

       callback=generate_meme

   )


   default_handler = MessageHandler(

       filters=filters.TEXT,

       callback=default

   )


   app.add_handler(start_handler)

   app.add_handler(meme_handler)

   app.add_handler(default_handler)


   print("Start polling...")

   app.run_polling()