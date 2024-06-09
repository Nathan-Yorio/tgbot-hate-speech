import os
import logging
import subprocess
import asyncio
import json
from functools import wraps
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# INITIAL SETUP
BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')
BOT_ADMIN = os.environ.get('TG_BOT_ADMIN')

if BOT_TOKEN is None:
    raise ValueError("env var not set")

if BOT_ADMIN is None:
    raise ValueError("no value for bot admin env var")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ACCESS CONTROL - rudimentary
ALLOWED_USERS = [
    BOT_ADMIN,  # personal alt tg account
    '',
]

# CROSS-FUNCTION CLASSES


class BotState:
    def __init__(state) -> None:
        state.running: Optional[bool] = 0


# CLASS "GLOBALS"
im = BotState()

# BOT FUNCTIONALITY


def requires_authorization(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        if user_id not in ALLOWED_USERS:
            await update.message.reply_text(str(user_id) + ': Unauthorized')
            return
        return await func(update, context)
    return wrapper


@requires_authorization
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    im.running = 1
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Analyzing Messages")


@requires_authorization
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    im.running = 0
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Stopping Analysis")


@requires_authorization
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    if im.running == 1:
        await update.message.reply_text(update.message.text)
    if im.running == 0:
        await update.message.reply_text("I am asleep.")  # Debug
        return


@requires_authorization
async def sentiment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if im.running == 1:
        try:
            # Get sentiment results here

            speech = update.message.text
            facebook_roberta_command = [
                "python3", "facebook-roberta.py", speech]
            multilingual_hate_speech_command = [
                "python3", "multilingual-hate-speech.py", speech]
            twitter_roberta_base_command = [
                "python3", "twitter-roberta-base.py", speech]
            # Execute the sentiment subprocess, send any text input into it
            facebook_roberta_process = await asyncio.create_subprocess_exec(
                *facebook_roberta_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            multilingual_hate_speech_process = await asyncio.create_subprocess_exec(
                *multilingual_hate_speech_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            twitter_roberta_base_process = await asyncio.create_subprocess_exec(
                *twitter_roberta_base_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

            # Wait for the process to finish and get its output
            facebook_roberta_output, error = await facebook_roberta_process.communicate()
            multilingual_hate_speech_output, error = await multilingual_hate_speech_process.communicate()
            twitter_roberta_base_output, error = await twitter_roberta_base_process.communicate()

            # Start counting total_hate score
            total_hate = 0

            # Decode the output, send it as a message
            facebook_roberta_output = facebook_roberta_output.decode()
            print(facebook_roberta_output)
            facebook_roberta_json = json.loads(facebook_roberta_output)
            if facebook_roberta_json[0]["Hateful"] == "1":
                total_hate += 1
            await update.message.reply_text("Facebook Roberta sentiment is: \n" + facebook_roberta_output)

            multilingual_hate_speech_output = multilingual_hate_speech_output.decode()
            multilingual_hate_speech_json = json.loads(
                multilingual_hate_speech_output)
            if multilingual_hate_speech_json[0]["Hateful"] == "1":
                total_hate += 1
            await update.message.reply_text("Multilingual Hate Speech sentiment is: \n" + multilingual_hate_speech_output)

            twitter_roberta_base_output = twitter_roberta_base_output.decode()
            twitter_roberta_base_json = json.loads(twitter_roberta_base_output)
            if twitter_roberta_base_json[0]["Hateful"] == "1":
                total_hate += 1
            await update.message.reply_text("Twitter Roberta Base sentiment is: \n" + twitter_roberta_base_output)

            if total_hate >= 2:
                await update.message.reply_text(
                    "The aggregate hate score result is: " +
                    str(total_hate) +
                    "\nwhich is indicates this message is likely hate speech."
                )
            else:
                await update.message.reply_text(
                    "The aggregate hate score result is: " +
                    str(total_hate) +
                    "\nThis message is probably not hate speech."
                )

        except Exception as e:
            # Handle any exceptions that occur during subprocess execution
            await update.message.reply_text(f"An error occurred: {str(e)}")

    if im.running == 0:
        await update.message.reply_text("I am asleep")  # Debug
    return


@ requires_authorization
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if im.running == 1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your user ID is: {user_id}")
    if im.running == 0:
        # Debug
        await update.message.reply_text("Can't retrieve ID: Currently Asleep.")
        return

# ASYNC EXECUTION
if __name__ == '__main__':
    # INIT
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # HANDLERS

    # /start
    application.add_handler(CommandHandler('start', start))
    # /stop
    application.add_handler(CommandHandler('stop', stop))

    # /whoami
    application.add_handler(CommandHandler('whoami', get_id))

    # CONTINUOUS RESPONSE

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # on a non command, respond with sentiment results
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, sentiment))

    # ASYNC POLLING FOR INPUT
    application.run_polling()
