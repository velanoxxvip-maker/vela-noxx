import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURACIÓN ---
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# --- MENSAJES ---
MENSAJE_BIENVENIDA = """🌟 *Mensaje de bienvenida* 🌟

👋 ¡Hola amor! Soy *Vela Noxx* 💋
Bienvenid@ a mi espacio exclusivo 🔥.

Explora el menú aquí abajo 👇 y descubre todo lo que tengo preparado para ti ✨.
"""

MENSAJE_VIP = """💎 *Suscripción VIP – Bs. 150 / mes* 💎

👉 Con tu suscripción tendrás acceso inmediato al Canal VIP diamante 💎, donde encontrarás:
✨ TODO mi contenido explícito🥵 y premium durante 1 mes completo.
🔥 Fotos + videos exclusivos.
💋 Acceso a lo más íntimo.
😈 Una experiencia única conmigo, sin censura.

📌 Acceso por 30 días al Canal VIP DIAMANTE con tu aporte de Bs. 150.
IMPORTANTE: 💎✨ Si ya te suscribiste, mándame TU COMPROBANTE DE PAGO Y tu nombre de usuario o enlace de contacto 💌🙌.
El bot a veces me notifica como “usuario desconocido” 🤖❌ y no me deja mandarte directo el link
"""

MENSAJE_PROMOS = """ 🌸✨ Hola mi amor ✨🌸
Por el momento no hay ninguna promoción activa para el Canal VIP Diamante 💎❌.
Cuando lance una nueva promo, estaré avisando primero en mi canal gratuito Zona Secreta 🔒💌.

Gracias por tu interés y tu cariño 💖. Mantente pendiente que pronto vendrán sorpresas 🔥✨. 
"""

MENSAJE_SALIDAS = """🚫 *No realizo servicios* 🚫
Pero sí existe la opción de ser tu *novia de alquiler* 💑✨.

🌹 Podemos vernos personalmente y disfrutar de un momento agradable juntos:

💬 Conversaciones cercanas  
🥂 Acompañamiento especial  
💖 Experiencia auténtica conmigo
"""

MENSAJE_AYUDA = """💬 Hola amor 💕, al hacer clic aquí estarás hablando directamente conmigo, la propietaria de Vela Noxx ✨
Para poder contactarte, por favor mándame tu @usuario de Telegram o el link de tu perfil 🔗.
Así podré responderte de manera más personalizada y especial 💌🥰.
Gracias por querer estar cerquita de mí💖✨.
"""

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔑 Suscripción VIP", callback_data="vip")],
        [InlineKeyboardButton("🎁 Promociones", callback_data="promos")],
        [InlineKeyboardButton("💕 Salidas", callback_data="salidas")],
        [InlineKeyboardButton("💬 Hablar conmigo", callback_data="ayuda")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(MENSAJE_BIENVENIDA, reply_markup=reply_markup, parse_mode="Markdown")

# --- BOTONES ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "vip":
        await query.message.reply_text(MENSAJE_VIP, parse_mode="Markdown")
        await context.bot.send_photo(chat_id=query.message.chat_id, photo=open("qr_vip.jpeg", "rb"))

    elif query.data == "promos":
        await query.message.reply_text(MENSAJE_PROMOS, parse_mode="Markdown")
        await context.bot.send_photo(chat_id=query.message.chat_id, photo=open("qr_promo.jpeg", "rb"))

    elif query.data == "salidas":
        await query.message.reply_text(MENSAJE_SALIDAS, parse_mode="Markdown")

    elif query.data == "ayuda":
        await query.message.reply_text(MENSAJE_AYUDA, parse_mode="Markdown")

# --- REENVÍO ---
async def reenvio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    caption = f"💌 Mensaje de {user.first_name} (@{user.username or 'sin_username'})"

    if update.message.text:
        mensaje = f"{caption}:\n\n{update.message.text}"
        await context.bot.send_message(ADMIN_ID, mensaje)

    elif update.message.photo:
        file = update.message.photo[-1].file_id
        await context.bot.send_photo(ADMIN_ID, file, caption=caption)

    elif update.message.document:
        file = update.message.document.file_id
        await context.bot.send_document(ADMIN_ID, file, caption=caption)

# --- MAIN ---
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, reenvio))

    print("🤖 Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()