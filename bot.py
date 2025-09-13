import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Variables de entorno
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # ejemplo: 5115300163

# --- Comando /start ---
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📲 QR VIP", callback_data="vip")],
        [InlineKeyboardButton("🎟️ QR Promo", callback_data="promo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "👋 Bienvenido al Bot de Vela\n\nElige una opción:",
        reply_markup=reply_markup
    )

# --- Manejo de botones ---
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "vip":
        query.message.reply_photo(
            photo=open("qr_vip.jpeg", "rb"),
            caption="Aquí tienes tu código QR VIP 🎉"
        )
    elif query.data == "promo":
        query.message.reply_photo(
            photo=open("qr_promo.jpeg", "rb"),
            caption="Aquí tienes tu código QR Promo 🏷️"
        )

# --- Reenvío de mensajes al admin ---
def forward_to_admin(update: Update, context: CallbackContext):
    user = update.message.from_user
    caption = update.message.caption if update.message.caption else ""

    # Texto
    if update.message.text:
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Mensaje de {user.first_name} (@{user.username}):\n\n{update.message.text}"
        )

    # Fotos
    elif update.message.photo:
        file = update.message.photo[-1].get_file()
        context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=file.file_id,
            caption=f"{caption}"
        )

    # Documentos
    elif update.message.document:
        file = update.message.document.get_file()
        context.bot.send_document(
            chat_id=ADMIN_ID,
            document=file.file_id,
            caption=f"{caption}"
        )

# --- Respuesta del admin ---
def reply_from_admin(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        context.bot.send_message(
            chat_id=update.message.reply_to_message.forward_from.id,
            text=f"📬 Respuesta del admin:\n\n{update.message.text}"
        )

# --- Main ---
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), forward_to_admin))
    dp.add_handler(MessageHandler(Filters.photo, forward_to_admin))
    dp.add_handler(MessageHandler(Filters.document, forward_to_admin))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()