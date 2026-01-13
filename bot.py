import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# ================= LOAD ENV =================
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BOT_NAME = os.getenv("BOT_NAME", "Shimi")

# ================= INTENTS =================
intents = discord.Intents.default()
intents.message_content = True

# ================= BOT =================
bot = commands.Bot(command_prefix="!", intents=intents)

# ================= ON READY =================
@bot.event
async def on_ready():
    # === CUSTOM STATUS ===
    activity = discord.CustomActivity(
        name="hmph, i'm not minor 🍥"
    )

    await bot.change_presence(
        status=discord.Status.dnd,  # DND
        activity=activity
    )

    print(f"💗 {BOT_NAME} online sebagai {bot.user}")

    try:
        await bot.tree.sync()
        print("✅ Slash command synced")
    except Exception as e:
        print("❌ Slash sync error:", e)

# ================= SLASH COMMAND =================
@bot.tree.command(name="status", description="Menampilkan status bot saat ini")
async def status(interaction: discord.Interaction):
    status_bot = bot.status.name.upper()

    activity_text = (
        bot.activity.name
        if isinstance(bot.activity, discord.CustomActivity)
        else "Tidak ada custom status"
    )

    await interaction.response.send_message(
        f"🤖 **Status Bot:** `{status_bot}`\n"
        f"💬 **Custom Status:** `{activity_text}`",
        ephemeral=True
    )

# ================= ON MESSAGE =================
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.author.id == bot.user.id:
        return

    await bot.process_commands(message)

# ================= RUN =================
bot.run(DISCORD_TOKEN)
