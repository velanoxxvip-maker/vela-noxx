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

MENSAJE_VIP = """💖 Hola, mi amor 💖
En este momento estamos con una promoción especial activa 🔥

👉 Haz clic en el botón 🎁 Promociones para ver toda la información completa, el QR de suscripción y los detalles 💋

✨ Si te animas, no olvides enviar tu comprobante y tu usuario para activarte.
También puedes mandarlo directamente a 👉🏻 @velanoxx✅

"""

MENSAJE_PROMOS = """*✨🔥 PROMO FIN DE MES ACTIVA – Solo 30 y 31 de MAYO* 🔥✨

 *💋Suscripción a SOLO Bs. 100* 
📅 *Acceso válido por 1 mes completo*
 *👇 ¿Qué incluye? 👇* 

👙 Fotos mias en lencería PREMIUM
🍑 Videos desnudandome completos
🔥 Videos masturbandome/full hardcore
💦 Videos cogiendo XXX sin censura 
🍑 Fotos y videos lesbicos
🔥 Series privadas + packs exclusivos 
🔥MATERIAL NUEVO CONSTANTEMENTE🔥_ 
🚨 *PARA ACTIVAR LA PROMO🚨* 
📩 Envíame tu comprobante de pago + tu usuario
👉👉👉 @velanoxx✅
🥵*_Pagas Bs.100 y disfrutas TODO un mes completo de contenido PREMIUM_* 🥵
━━━━━━━━━━━━━━━
💳✨ *MÉTODOS DE PAGO ✨*
🇧🇴 Bolivia – 100 Bs
📲 Te envío el QR automáticamente dentro de este mensaje,envia tu comprobante a 👉 @velanoxx✅
🇵🇪 Perú – 50 soles
 💜 Pago por Yape 📩 Pide el Yape a 👉 @velanoxx✅
🇧🇷  Brasil - 90 Reales (PIX)
✉️ Solicita tu QR o Clave PIX directamente a 👉🏻👉🏻 @velanoxx✅
🌎 Internacional – 15 USD
 💵 Solicita tu metodo de pago
 a 👉👉 @velanoxx✅
🌐 Pagos cripto - 15 USDC o USDT 
🪙  Metodo Binance,Poligon y BNB pide el QR 
a 👉👉 @velanoxx✅
🇪🇺 Euros - 13 EUR solicita el método directamente a 👉🏻 @velanoxx✅
🔥 Acceso por 30 días. 🔥
"""

MENSAJE_SALIDAS = """🚫 *No realizo servicios* 🚫
Pero sí existe la opción de ser tu *novia de alquiler* 💑✨.

🌹 Podemos vernos personalmente y disfrutar de un momento agradable juntos:

💬 Conversaciones cercanas  
🥂 Acompañamiento especial  
💖 Experiencia auténtica conmigo
"""

MENSAJE_AYUDA = """📩 Escríbeme tu consulta aquí y yo la recibo directamente 💕
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