"""
Conecta Migrante - bot de orientacion institucional para Telegram.

El contenido (menus y respuestas) vive en contenido.json, asi se puede
editar sin tocar el codigo.

Las opciones se muestran como botones de teclado: al tocar una, el texto
se envia como mensaje del usuario y el bot responde debajo, de modo que
el historial de la conversacion queda visible.
"""

import json
import logging
import os
import re
import unicodedata
from pathlib import Path

from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
# evita que se imprima cada peticion (y el token) en la terminal
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("conecta-migrante")

RUTA_CONTENIDO = Path(__file__).parent / "contenido.json"
with open(RUTA_CONTENIDO, encoding="utf-8") as f:
    CONTENIDO = json.load(f)

NODOS = CONTENIDO["nodos"]
AVISO = CONTENIDO["aviso"]

BTN_VOLVER = "⬅️ Volver"
BTN_MENU = "🏠 Menú principal"

# texto del boton -> nodo al que lleva
BOTONES = {
    op["texto"]: op["ir_a"]
    for nodo in NODOS.values()
    for op in nodo.get("opciones", [])
}


def normalizar(texto: str) -> str:
    """minusculas y sin tildes, para comparar palabras clave."""
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def teclado(nodo_id: str) -> ReplyKeyboardMarkup:
    """botones del nodo, mas volver y menu principal."""
    nodo = NODOS[nodo_id]
    filas = [[KeyboardButton(op["texto"])] for op in nodo.get("opciones", [])]
    navegacion = []
    padre = nodo.get("padre")
    if padre and padre != "inicio":
        navegacion.append(KeyboardButton(BTN_VOLVER))
    if nodo_id != "inicio":
        navegacion.append(KeyboardButton(BTN_MENU))
    if navegacion:
        filas.append(navegacion)
    return ReplyKeyboardMarkup(
        filas, resize_keyboard=True, input_field_placeholder="Elige una opción o escribe tu consulta"
    )


def buscar_nodo(mensaje: str) -> str | None:
    """devuelve el nodo cuya palabra clave aparece en el mensaje."""
    msg = normalizar(mensaje)
    for nodo_id, nodo in NODOS.items():
        for palabra in nodo.get("palabras_clave", []):
            # palabra completa, para que "usa" no coincida con "causa"
            if re.search(rf"\b{re.escape(normalizar(palabra))}\b", msg):
                return nodo_id
    return None


async def mostrar(update: Update, context: ContextTypes.DEFAULT_TYPE, nodo_id: str, extra: str = "") -> None:
    """responde con el contenido del nodo y guarda en que seccion va la persona."""
    context.user_data["nodo"] = nodo_id
    await update.message.reply_text(
        NODOS[nodo_id]["texto"] + extra,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=teclado(nodo_id),
        disable_web_page_preview=True,
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await mostrar(update, context, "inicio", f"\n\n_{AVISO}_")


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Usa los botones de abajo para navegar, o escríbeme una palabra como "
        "*pasaporte*, *DPI*, *consulado* o *trabajo*.\n\n"
        "Comandos:\n/start - menú principal\n/directorio - instituciones\n/ayuda - esta ayuda",
        parse_mode=ParseMode.MARKDOWN,
    )


async def directorio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await mostrar(update, context, "directorio")


async def mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """maneja botones del teclado y texto libre."""
    texto = update.message.text.strip()
    actual = context.user_data.get("nodo", "inicio")

    if texto == BTN_MENU:
        await mostrar(update, context, "inicio")
    elif texto == BTN_VOLVER:
        await mostrar(update, context, NODOS[actual].get("padre", "inicio"))
    elif texto in BOTONES:
        await mostrar(update, context, BOTONES[texto])
    else:
        nodo_id = buscar_nodo(texto)
        if nodo_id:
            await mostrar(update, context, nodo_id)
        else:
            context.user_data["nodo"] = "inicio"
            await update.message.reply_text(
                "No entendí bien tu consulta 🙏 Elige una opción del menú:",
                reply_markup=teclado("inicio"),
            )


def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise SystemExit("falta TELEGRAM_TOKEN en el archivo .env")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("directorio", directorio))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje))

    log.info("Conecta Migrante en linea")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()