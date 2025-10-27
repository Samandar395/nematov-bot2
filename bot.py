from telegram import Update, ChatMember
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

BOT_TOKEN = "8006863160:AAGu-uJcB1mZDViX2mkwIjofrbrv__u5oH4"

seen_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ishga tushdi ✅")

async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        seen_users.add(user.id)

async def banall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    bot = context.bot

    admins = [a.user.id for a in await chat.get_administrators()]
    success = 0
    for uid in list(seen_users):
        if uid not in admins and uid != user.id:
            try:
                await bot.ban_chat_member(chat.id, uid)
                seen_users.remove(uid)
                success += 1
                await asyncio.sleep(0.3)
            except:
                pass
    await update.message.reply_text(f"Ban jarayoni tugadi. Chiqarilgan: {success}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("banall", banall))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_users))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, track_users))
    print("🤖 Bot ishga tushdi...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
