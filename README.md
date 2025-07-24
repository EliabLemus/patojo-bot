# 🧠 patojo-bot

![patojo-bot](./assets/patojobot_avatar.png)

**patojo-bot** es un bot de Discord amigable e inteligente, diseñado para facilitar el acceso a modelos de inteligencia artificial open-source como Mistral, Qwen y DeepSeek, a través de una interfaz sencilla en Discord.

**"Patojo"** es una palabra utilizada en Guatemala para referirse a un niño o joven. Este bot representa esa energía curiosa y dinámica, al servicio del conocimiento.

---

## 🇬🇹 Español

### 🤖 Características

- Conéctate con modelos de lenguaje open-source usando [OpenRouter](https://openrouter.ai/)
- Interactúa desde cualquier canal de Discord o por mensaje directo
- Soporte para múltiples modelos como `mistralai`, `deepseek`, `qwen` y más
- Configurable a través de `.env`
- Comandos personalizados y fáciles de usar

### 🚀 Uso

Escribe un mensaje directo o menciona al bot seguido de tu pregunta:

```
@patojo-bot ¿Cuál es la capital de Guatemala?
```

También puedes usar el comando `!help` para ver los comandos disponibles.

### 🛠️ Instalación

1. Clona el repositorio
2. Crea un entorno virtual y actívalo
3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4. Crea un archivo `.env` con tu token de Discord y API key de OpenRouter

### 🔧 Archivo `.env` de ejemplo

```
DISCORD_BOT_TOKEN=tu_token_aquí
OPENROUTER_API_KEY=tu_api_key_aquí
LITELLM_MODEL=deepseek/deepseek-r1-0528-qwen3-8b:free
LITELLM_API_BASE=https://openrouter.ai/api/v1
```

---

## 🇺🇸 English

### 🤖 Features

- Connect to open-source language models via [OpenRouter](https://openrouter.ai/)
- Chat from any Discord channel or direct message
- Supports models like `mistralai`, `deepseek`, `qwen` and more
- Easily configured via `.env` file
- Custom and intuitive commands

### 🚀 Usage

Send a direct message or mention the bot followed by your question:

```
@patojo-bot What’s the capital of Guatemala?
```

You can also type `!help` to see available commands.

### 🛠️ Installation

1. Clone this repo
2. Create and activate a virtual environment
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a `.env` file with your Discord token and OpenRouter API key

---

## 🖼️ Credits

Art style inspired by Bazooka Joe®  
Character design by [OpenAI + ChatGPT](https://chat.openai.com)
## 🙌 Créditos

- Diseño e implementación por **Eliab Lemus**, viviendo en Guatemala 🇬🇹

---

## 🧩 License

MIT License
