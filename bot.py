import os
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    InlineQueryHandler, ContextTypes, filters
)
from fonts import FONTS

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Пришли мне текст — покажу его во всех шрифтах.\n\n"
        "Или используй инлайн: набери в любом чате @username_бота текст"
    )


async def stylize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if len(text) > 100:
        await update.message.reply_text("Максимум 100 символов")
        return

    results = []
    for name, fn in FONTS.items():
        try:
            styled = fn(text)
            results.append(f"{name}:\n{styled}")
        except:
            continue

    msg = "\n\n".join(results)

    if len(msg) > 4000:
        parts = [msg[i:i+4000] for i in range(0, len(msg), 4000)]
        for part in parts:
            await update.message.reply_text(part)
    else:
        await update.message.reply_text(msg)


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    results = []
    for i, (name, fn) in enumerate(FONTS.items()):
        try:
            styled = fn(query)
            results.append(
                InlineQueryResultArticle(
                    id=str(i),
                    title=name,
                    description=styled,
                    input_message_content=InputTextMessageContent(styled),
                )
            )
        except:
            continue

    await update.inline_query.answer(results[:20], cache_time=1)


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, stylize))
    app.add_handler(InlineQueryHandler(inline_query))
    print("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()