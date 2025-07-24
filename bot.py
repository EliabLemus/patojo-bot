import discord
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BOT_KEYWORD = os.getenv("BOT_KEYWORD")

DEFAULT_MODEL = "mistralai/mistral-small-3.2-24b-instruct:free"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"

AUTHORIZED_USERS_FILE = "authorized_users.txt"
USER_LOG_FILE = "user_log.txt"
pending_auth_requests = set()
authorized_users = {}

# ⚠️ Reemplaza esto con tu verdadero ID de usuario de Discord
BOT_OWNER_ID = 123456789012345678  # <-- actualiza esto

CONTACT_INFO = (
    "🚫 **Acceso no autorizado. Para solicitar acceso, por favor contacta a:**\n\n"
    "**Eliab Lemus Barrios**\n"
    "🌍 Guatemala — Disponible 100% remoto\n"
    "📧 eliab.lemus.barrios@gmail.com\n"
    "🔗 [LinkedIn](https://linkedin.com/in/eliablemus)\n"
    "🖥️ [GitHub](https://github.com/EliabLemus)\n\n"
    "---\n"
    "🚫 **Unauthorized access. To request access, please contact:**\n\n"
    "**Eliab Lemus Barrios**\n"
    "🌍 Guatemala — 100% Remote Available\n"
    "📧 eliab.lemus.barrios@gmail.com\n"
    "🔗 [LinkedIn](https://linkedin.com/in/eliablemus)\n"
    "🖥️ [GitHub](https://github.com/EliabLemus)\n\n"
    "---\n"
    "🚨 Este bot corre en una Raspberry Pi. Sé amable. No la rostices 😅"
)

def log_user(user_id):
    with open(USER_LOG_FILE, "a") as f:
        f.write(f"{user_id}\n")

def load_authorized_users():
    if not os.path.exists(AUTHORIZED_USERS_FILE):
        return
    with open(AUTHORIZED_USERS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                user_id, date = parts
                authorized_users[int(user_id)] = date

def is_authorized(user_id):
    return int(user_id) in authorized_users

def authorize_user(user_id):
    now = datetime.utcnow().isoformat()
    with open(AUTHORIZED_USERS_FILE, "a") as f:
        f.write(f"{user_id}|{now}\n")
    authorized_users[int(user_id)] = now

print(f"🔐 DISCORD_BOT_TOKEN: {'OK' if DISCORD_BOT_TOKEN else '❌ NO DETECTADO'}")
print(f"🧠 OPENROUTER_API_KEY: {'OK' if OPENROUTER_API_KEY else '❌ NO DETECTADO'}")

if not DISCORD_BOT_TOKEN:
    raise RuntimeError("❌ DISCORD_BOT_TOKEN no está definido en .env")
if not OPENROUTER_API_KEY:
    raise RuntimeError("❌ OPENROUTER_API_KEY no está definido en .env")

load_authorized_users()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"🤖 Conectado como {client.user} (ID: {client.user.id})")
    print(f"✅ Usuarios autorizados: {len(authorized_users)}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.strip()
    user_id = message.author.id
    log_user(user_id)

    # Comando secreto: lista de autorizados (solo para el owner)
    if content.startswith("!authorized_users"):
        if user_id != BOT_OWNER_ID:
            await message.channel.send("⛔ No tienes permisos para usar este comando.")
            return
        lines = ["**👥 Lista de usuarios autorizados:**"]
        for uid, date in authorized_users.items():
            try:
                user = await client.fetch_user(uid)
                lines.append(f"`{uid}` – **{user.name}#{user.discriminator}** – `{date}`")
            except Exception:
                lines.append(f"`{uid}` – *usuario desconocido* – `{date}`")
        await message.channel.send("\n".join(lines)[:1900])
        return

    if content.startswith("!ping"):
        await message.channel.send("🏓 Pong!")
        return

    elif content.startswith("!help"):
        await message.channel.send(
            "**📘 Comandos disponibles:**\n"
            "`!modelos` — Lista modelos OpenRouter\n"
            "`!ping` — Prueba si estoy vivo\n"
            "`!help` — Muestra esta ayuda\n"
            f"**Modelo por defecto:** `{DEFAULT_MODEL}`"
        )
        return

    elif content.startswith("!modelos"):
        try:
            r = requests.get(f"{OPENROUTER_API_URL}/models", headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}"
            }, timeout=10)
            r.raise_for_status()
            modelos = [m["id"] for m in r.json().get("data", [])][:20]
            await message.channel.send("**📦 Modelos disponibles en OpenRouter:**\n" + "\n".join(f"`{m}`" for m in modelos))
        except Exception as e:
            await message.channel.send(f"⚠️ Error: {e}")
        return

    elif isinstance(message.channel, discord.DMChannel) or client.user in message.mentions:
        if not is_authorized(user_id):
            # En grupo: redirigir a DM
            if not isinstance(message.channel, discord.DMChannel):
                try:
                    await message.author.send(f"{CONTACT_INFO}\n\nPor favor, responde con la palabra clave para autorizarte.")
                    await message.channel.send(f"🔒 @{message.author.name}, revisa tus mensajes privados para continuar.")
                except discord.Forbidden:
                    await message.channel.send("❌ No puedo enviarte un mensaje privado. Habilita DMs del servidor.")
                return

            # En DM: pedir palabra clave
            if user_id in pending_auth_requests:
                return
            pending_auth_requests.add(user_id)

            await message.channel.send(f"{CONTACT_INFO}\n\nPor favor, escribe la palabra clave para usar el bot:")
            def check(m):
                return m.author.id == user_id and isinstance(m.channel, discord.DMChannel)

            try:
                reply = await client.wait_for("message", check=check, timeout=60)
                if reply.content.strip() == BOT_KEYWORD:
                    authorize_user(user_id)
                    await message.channel.send(
                        "✅ ¡Palabra clave correcta! Ya puedes usar el bot en cualquier canal.\n"
                        "🚨 Recuerda: este bot corre en una Raspberry Pi. Sé amable."
                    )
                else:
                    await message.channel.send("❌ Palabra clave incorrecta. Intenta de nuevo más tarde.")
                pending_auth_requests.remove(user_id)
                return
            except Exception:
                pending_auth_requests.remove(user_id)
                await message.channel.send("⏰ Tiempo agotado. Intenta de nuevo más tarde.")
                return

        # Usuario autorizado: procesar mensaje
        prompt = content.replace(f"<@{client.user.id}>", "").replace(f"<@!{client.user.id}>", "").strip()
        if not prompt:
            await message.channel.send("❌ Escribe algo después de mencionarme.")
            return

        await message.channel.send(f"✍️ Usando `{DEFAULT_MODEL}`...")

        try:
            r = requests.post(f"{OPENROUTER_API_URL}/chat/completions", headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENROUTER_API_KEY}"
            }, json={
                "model": DEFAULT_MODEL,
                "messages": [{"role": "user", "content": prompt}]
            }, timeout=20)
            r.raise_for_status()
            result = r.json()
            response = result["choices"][0]["message"]["content"]
        except Exception as e:
            response = f"⚠️ Error: {e}"
        await message.channel.send(response[:1900])

try:
    print("🚀 Conectando...")
    client.run(DISCORD_BOT_TOKEN)
except discord.LoginFailure:
    print("❌ Token inválido. Verifica DISCORD_BOT_TOKEN.")
except discord.PrivilegedIntentsRequired:
    print("⚠️ Intents no habilitados. Activa MESSAGE CONTENT INTENT en Discord Developer Portal.")
except Exception as e:
    print(f"🔥 Error inesperado: {type(e).__name__}: {e}")