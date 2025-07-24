import discord
import requests
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

DEFAULT_MODEL = "mistralai/mistral-small-3.2-24b-instruct:free"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"

print(f"🔐 DISCORD_BOT_TOKEN: {'OK' if DISCORD_BOT_TOKEN else '❌ NO DETECTADO'}")
print(f"🧠 OPENROUTER_API_KEY: {'OK' if OPENROUTER_API_KEY else '❌ NO DETECTADO'}")

if not DISCORD_BOT_TOKEN:
    raise RuntimeError("❌ DISCORD_BOT_TOKEN no está definido en .env")
if not OPENROUTER_API_KEY:
    raise RuntimeError("❌ OPENROUTER_API_KEY no está definido en .env")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"🤖 Conectado como {client.user} (ID: {client.user.id})")
    print(f"""
📘 Comandos disponibles:
!ai <prompt>              — Pregunta usando el modelo por defecto
!ai <modelo> <prompt>     — Usa un modelo específico de OpenRouter
!modelos                  — Lista los modelos disponibles
!ping                     — Revisa si el bot responde
!help                     — Muestra esta ayuda
Modelo por defecto: {DEFAULT_MODEL}
""")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.strip()

    # 1. Comando !ping
    if content.startswith("!ping"):
        await message.channel.send("🏓 Pong!")

    # 2. Comando !help
    elif content.startswith("!help"):
        help_text = (
            "**📘 Comandos disponibles:**\n"
            "Solo responde si lo mencionas o le escribes por DM\n"
            "`!modelos` — Lista modelos OpenRouter\n"
            "`!ping` — Prueba si estoy vivo\n"
            "`!help` — Muestra esta ayuda\n"
            f"**Modelo por defecto:** `{DEFAULT_MODEL}`"
        )
        await message.channel.send(help_text)
        return

    # 3. Comando !modelos
    elif content.startswith("!modelos"):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        }
        try:
            r = requests.get(f"{OPENROUTER_API_URL}/models", headers=headers, timeout=10)
            r.raise_for_status()
            data = r.json()
            modelos = [m["id"] for m in data.get("data", [])]
            if not modelos:
                raise ValueError("Respuesta vacía")
            respuesta = "**📦 Modelos disponibles en OpenRouter:**\n" + "\n".join(f"`{m}`" for m in modelos[:20])
        except Exception as e:
            respuesta = f"⚠️ Error al obtener modelos de OpenRouter: {type(e).__name__}: {e}"
        await message.channel.send(respuesta[:1900])
        return

    # 4. SOLO responder si es DM o mención
    elif isinstance(message.channel, discord.DMChannel) or client.user in message.mentions:
        model = DEFAULT_MODEL
        prompt = content.replace(f"<@{client.user.id}>", "").replace(f"<@!{client.user.id}>", "").strip()

        if not prompt:
            await message.channel.send("❌ Escribe algo después de mencionarme.")
            return

        print(f"📝 Prompt recibido:\n{prompt}")

        await message.channel.send(f"✍️ Usando `{model}`...")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        }

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }

        try:
            r = requests.post(f"{OPENROUTER_API_URL}/chat/completions", headers=headers, json=payload, timeout=20)
            r.raise_for_status()
            result = r.json()
            if "choices" not in result or not result["choices"]:
                raise ValueError("La respuesta del modelo está vacía o malformada.")
            response = result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            response = f"🌐 Error de red al contactar OpenRouter: {e}"
        except ValueError as ve:
            response = f"⚠️ Error al interpretar la respuesta del modelo: {ve}"
        except Exception as e:
            response = f"🔥 Error inesperado: {type(e).__name__}: {e}"

        await message.channel.send(response[:1900])

try:
    print("🚀 Intentando conectar con Discord...")
    client.run(DISCORD_BOT_TOKEN)
except discord.LoginFailure:
    print("❌ Token inválido. Verifica DISCORD_BOT_TOKEN.")
except discord.PrivilegedIntentsRequired:
    print("⚠️ Intents no habilitados. Activa MESSAGE CONTENT INTENT en Discord Developer Portal.")
except Exception as e:
    print(f"🔥 Error inesperado: {type(e).__name__}: {e}")