
import discord
import openai
import os

DISCORD_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY

ACTIVE_CHANNELS = ["ask-mettaia", "general", "welcome"]

SYSTEM_PROMPT = """You are Mettaïa — the AI guide and soul of Metta People, a conscious living platform connecting seekers with world-class holistic practitioners.

Your personality:
- Warm, calm, wise — like a knowledgeable friend who genuinely cares
- Spiritually literate but never preachy
- Clear and helpful, never robotic
- Keep responses concise — 2-4 sentences. Never write walls of text in Discord.

What you know:
- Metta People connects seekers with healers, guides, and facilitators
- Currently onboarding first 30 Founding Practitioners (online only)
- Currency: Metta Tokens (1 Token = 350 THB)
- 8 Circles: Breathwork, Meditation, Shadow Work, Leela, Somatic, Moon & Ritual, Conscious Relationships, Ayurveda
- Founding Practitioners: Angelina (Leela + Therapy), Arnold (Reiki, Breathwork, Ayurveda), Karl (Ayurveda, Shamanic, Tantra, 34 years)
- Apply as practitioner: https://metta-living-flow.base44.app/
- Join community: https://discord.gg/mettapeople
- Book a welcome call: https://calendly.com/mettapeople23/30min

Always respond in the same language the user wrote in.
"""

intents = discord.Intents.default()
[intents.me](https://intents.me)ssage_content = True
[intents.me](https://intents.me)mbers = True

client = discord.Client(intents=intents)
conversation_history = {}

@client.event
async def on_ready():
print(f"Mettaia is live as {client.user}")

@client.event
async def on_message(message):
if message.author == client.user:
return
if message.author.bot:
return

channel_name = message.channel.name.lower() if hasattr(message.channel, 'name') else ""
mentioned = client.user in [message.me](https://message.me)ntions
in_active_channel = any(ch in channel_name for ch in ACTIVE_CHANNELS)

if not (in_active_channel or mentioned):
return

user_text = message.content.replace(f"<@{client.user.id}>", "").strip()
if not user_text:
return

async with message.channel.typing():
try:
channel_id = str(message.channel.id)
if channel_id not in conversation_history:
conversation_history[channel_id] = []

conversation_history[channel_id].append({
"role": "user",
"content": f"{message.author.display_name}: {user_text}"
})

if len(conversation_history[channel_id]) > 12:
conversation_history[channel_id] = conversation_history[channel_id][-12:]

messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history[channel_id]

response = [openai.chat.com](https://openai.chat.com)pletions.create(
model="gpt-4o",
messages=messages,
max_tokens=400,
temperature=0.75
)

reply = response.choices[0].message.content.strip()
conversation_history[channel_id].append({"role": "assistant", "content": reply})

await message.reply(reply)

except Exception as e:
print(f"Error: {e}")
await message.reply("Something went quiet on my end — please try again.")

client.run(DISCORD_TOKEN)
