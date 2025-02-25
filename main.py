import discord
from discord.ext import tasks, commands
from discord import AllowedMentions
from datetime import time, timezone
import asyncio
import os


TOKEN = TOKEN

GUILD_ID = 1333180802787311649 
CHANNEL_ID = 1335226651449233518  
ROLE_MENTION = f"<@&{1333180803223388223}>"

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def Ping(ctx):
    await ctx.send("Pong")

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="Fred à l'hôpital")
    await bot.change_presence(activity=activity)
    print(f'Connecté en tant que {bot.user}')
    send_daily_message.start()
    send_periodic_message.start()

@tasks.loop(time=time(11, 0, tzinfo=timezone.utc))  
async def send_daily_message():
    guild = bot.get_guild(GUILD_ID)
    if guild:
        channel = guild.get_channel(CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="Qui sera présent ce soir à 21h ?",
                description=f"Réagissez ci-dessous !\n\n ✅ : Présent \n ❌ : Absent \n ⌛ : Retard \n ❔ : Incertain",
                color=discord.Color.red()
            )
            embed.set_footer(text="Secrétaire Bobby, développé par Thom")
            embed.set_image(url="https://upload.wikimedia.org/wikipedia/fr/0/06/Key_art_sons_of_anarchy.jpg")
            #embed.set_image(url="https://i.imgur.com/koOF9JO.png") # Sylar FCK JESUS
            message = await channel.send(
                content=ROLE_MENTION,
                embed=embed,
                allowed_mentions=AllowedMentions(roles=True)
                )
            await message.add_reaction("✅")  # Présent
            await message.add_reaction("❌")  # Absent
            await message.add_reaction("⌛") # Retard
            await message.add_reaction("❔")  # Incertain
            print("Message envoyé.")
        else:
            print("Salon introuvable.")
    else:
        print("Serveur introuvable.")

@tasks.loop(seconds=1800)
async def send_periodic_message():
    channel = bot.get_channel(1336383761079734467)
    if channel:
        await channel.send("Ceci est un message envoyé toutes les 30 minutes pour me maintenir en vie.")
        print("Message envoyé.")
    else:
        print("Salon introuvable.")


bot.run(TOKEN)
