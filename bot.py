import os
import sys
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Configuración del logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# --- CONFIGURACIÓN desde variables de entorno ---
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

if not TOKEN or not ADMIN_ID:
    logger.error("❌ ERROR: Debes definir las variables de entorno TOKEN y ADMIN_ID")
    sys.exit(1)

try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    logger.error("❌ ERROR: ADMIN_ID debe ser un número entero")
    sys.exit(1)

# --- MENSAJES ---
MENSAJE_BIENVENIDA = """🌟 *Mensaje de bienvenida* 🌟

👋 ¡Hola amor! Soy *Vela Noxx* 💋
Bienvenid@ a mi espacio exclusivo 🔥.

Explora el menú aquí abajo 👇 y descubre todo lo que tengo preparado para ti ✨.
"""

MENSAJE_VIP = """💎 *Suscripción VIP – Bs. 150 / mes* 💎

👉 Con tu suscripción tendrás acceso inmediato al Canal VIP diamante 💎, donde encontrarás:
✨ TODO mi contenido explícito 🤯 y premium durante 1 mes completo.
🔥 Fotos + videos exclusivos en alta resolucion.
💞 Acceso colaboracion xxx 🔥🔥.
😈 Una experiencia única conmigo, sin censura.

📌 Acceso por 30 días al Canal VIP DIAMANTE con tu aporte de Bs. 150.

⚠ IMPORTANTE ⚠
Para activarlo debes enviarme:
⿡ Tu comprobante de pago 📸
⿢ Tu @usuario de Telegram (ejemplo: @juan23, @carlitos89).

🚫 Si no me mandas tu @usuario, me sales como “usuario desconocido” 🤖❌ y no podré enviarte tu link VIP.

👉 Si aún no tienes usuario, créalo en:
Configuración > Editar perfil > Nombre de usuario.
(Ejemplo: @pedro2025).
NOTA :Si todo eso se te hace complicado aqui te dejo mi segundo usuario que es 👉 @velanoxx ✅ ✨💖
Ahí podrás mandarme directamente tu comprobante y asegurarte tu acceso 😏💦
"""

MENSAJE_PROMOS = """🔥💖 PROMOCIÓN ACTIVA 💖🔥

Hola, mi amorcito 😘✨
Espero que estés súper bien 💕
Hoy la suscripción te sale a tan solo Bs. 100 💸💎

Dentro vas a encontrar cosas que te van a volver loco 😈💦:
👙 Lencería premium
📸 Fotos y videos explícitos
💫 Contenido XXX y masturbación
🔐 Material único y exclusivo

Para entrar, envíame tu usuario y tu comprobante aquí✅ 
NOTA:si se te hace complicado aqui te dejo mi segundo usuario que es 👉 @velanoxx ✅ ✨💖
Ahí podrás mandarme directamente tu comprobante y asegurarte tu acceso 😏💦

No dejes pasar esta oportunidad ⏳💖, porque solo es por hoy, 30 de noviembre, y después vuelve a Bs. 150 💥
Si quieres entrar a mi mundo privado, ahora es el momento 😏💋
Te prometo que no te vas a arrepentir 💖🔥
"""

MENSAJE_SALIDAS = """🚫 *No realizo servicios* 🚫
Pero sí existe la opción de ser tu *novia de alquiler* 💑✨.

🌹 Podemos vernos personalmente y disfrutar de un momento agradable juntos:

💬 Conversaciones cercanas  
🥂 Acompañamiento especial  
💖 Experiencia auténtica conmigo
"""

MENSAJE_AYUDA = """💬 Hola amor 💕
Al hacer clic aquí estarás hablando directamente conmigo, la propietaria de Vela Noxx ✨.

⚠ IMPORTANTE ⚠
Para poder contestarte, NECESITO que me envíes tu @usuario de Telegram (ejemplo: @juan23, @carlitos89).

🚫 Si no me mandas tu @usuario, me sales como “usuario desconocido” 🤖❌ y no podré responderte. 

👉 Si no sabes cuál es tu usuario, créalo fácil en:
Configuración > Editar perfil > Nombre de usuario.
(Ejemplo: @pedro2025).

💞 Solo así podré contestarte de forma personalizada y especial 💌🥰
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
        # ENVÍO DE ARCHIVO QR VIP
        try:
            # Asegúrate de que el archivo 'qr_vip.jpeg' exista en la misma ruta de ejecución
            with open("qr_vip.jpeg", "rb") as f:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=f)
        except FileNotFoundError:
            await query.message.reply_text("⚠️ Error: Archivo de QR VIP no encontrado en el servidor.")


    elif query.data == "promos":
        await query.message.reply_text(MENSAJE_PROMOS, parse_mode="Markdown")
        # ENVÍO DE ARCHIVO QR PROMOCIONES (Asumo que aquí enviarías un QR también)
        try:
            # Asegúrate de que el archivo 'qr_promo.jpeg' exista en la misma ruta de ejecución
            with open("qr_promo.jpeg", "rb") as f:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=f)
        except FileNotFoundError:
            await query.message.reply_text("⚠️ Error: Archivo de QR Promociones no encontrado en el servidor.")


    elif query.data == "salidas":
        await query.message.reply_text(MENSAJE_SALIDAS, parse_mode="Markdown")

    elif query.data == "ayuda":
        await query.message.reply_text(MENSAJE_AYUDA, parse_mode="Markdown")

# --- REENVÍO DE MENSAJES (Ahora incluye VIDEO y VOZ) ---
async def reenvio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    caption_base = f"💌 Mensaje de {user.first_name} (@{user.username or 'sin_username'}) - ID: {user.id}"
    
    # --- Texto ---
    if update.message.text:
        mensaje = f"{caption_base}:\n\n{update.message.text}"
        await context.bot.send_message(ADMIN_ID, mensaje)

    # --- Foto ---
    elif update.message.photo:
        file = update.message.photo[-1].file_id
        await context.bot.send_photo(ADMIN_ID, file, caption=caption_base)

    # --- Video (¡AGREGADO!) ---
    elif update.message.video:
        file = update.message.video.file_id
        await context.bot.send_video(ADMIN_ID, file, caption=caption_base)

    # --- Nota de Voz (¡AGREGADO!) ---
    elif update.message.voice:
        file = update.message.voice.file_id
        await context.bot.send_voice(ADMIN_ID, file, caption=caption_base)

    # --- Documento ---
    elif update.message.document:
        file = update.message.document.file_id
        await context.bot.send_document(ADMIN_ID, file, caption=caption_base)
        
    # --- Otros Tipos (Stickers, Audios, etc.) ---
    else:
        # Notifica al administrador que se recibió un tipo de mensaje no cubierto explícitamente.
        mensaje = f"⚠️ Mensaje de tipo no cubierto (Ej. Sticker/Audio) de {caption_base}"
        await context.bot.send_message(ADMIN_ID, mensaje)

# --- MANEJO DE ERRORES ---
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Loggea los errores causados por Updates y los notifica al admin."""
    logger.error(f"⚠️ Update {update} causó el error {context.error}")

    # Notifica al ADMIN_ID si el error no es el de conflicto 409
    if 'Conflict' not in str(context.error):
        try:
            await context.bot.send_message(ADMIN_ID, f"🚨 ERROR CRÍTICO DEL BOT:\n\n{context.error}")
        except Exception:
            # Si falla incluso enviar el error, no hacemos nada más
            pass

# --- MAIN ---
def main():
    logger.info("Iniciando aplicación de Telegram...")
        
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    # Maneja todos los mensajes que NO son comandos
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, reenvio)) 
    
    # Manejador de errores para hacer el bot más robusto
    app.add_error_handler(error_handler) 

    logger.info("🤖 Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()