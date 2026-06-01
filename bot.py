from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = "8858487013:AAHuGmfqgbAI0mYqlYhUUdL0v5aUAAw7FoY"
PHOTO_URL = "https://i.ibb.co/93WwC5T5/IMG.jpg"

WAITING_ADDRESS = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("SOL 🟣", callback_data="SOL"),
            InlineKeyboardButton("TRUMP 🇺🇸", callback_data="TRUMP"),
        ],
        [
            InlineKeyboardButton("PUMP 🚀", callback_data="PUMP"),
            InlineKeyboardButton("PENGU 🐧", callback_data="PENGU"),
        ],
        [
            InlineKeyboardButton("BONK 🔨", callback_data="BONK"),
            InlineKeyboardButton("USDT 💵", callback_data="USDT"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption="Choose whichever one you want 👇",
        reply_markup=reply_markup
    )
    return ConversationHandler.END


async def coin_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["choice"] = query.data
    await query.message.reply_text("📍 Submit your address")
    return WAITING_ADDRESS


async def receive_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = update.message.text
    context.user_data["address"] = address
    choice = context.user_data.get("choice", "TOKEN")
    keyboard = [
        [InlineKeyboardButton(f"0.1 {choice} for 1 {choice}", callback_data="plan_1")],
        [InlineKeyboardButton(f"1 {choice} for 10 {choice}", callback_data="plan_2")],
        [InlineKeyboardButton(f"10 {choice} for 100 {choice}", callback_data="plan_3")],
        [InlineKeyboardButton(f"100 {choice} for 1000 {choice}", callback_data="plan_4")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Choose your plan 👇",
        reply_markup=reply_markup
    )
    return ConversationHandler.END


async def plan_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "FtjHbk3Jsthm53JBjQth7p1cWcGfbVZmZS1Ky8BJAFGx"
    )


conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(coin_button_handler, pattern="^(SOL|TRUMP|PUMP|PENGU|BONK|USDT)$")],
    states={
        WAITING_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_address)],
    },
    fallbacks=[CommandHandler("start", start)],
)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(plan_handler, pattern="^plan_"))

print("Bot is running...")
app.run_polling()
