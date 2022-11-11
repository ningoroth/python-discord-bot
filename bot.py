import logging
import os
import sys
import random

import discord
from discord.ext import commands
import dotenv

# Load variables from .env file
dotenv.load_dotenv()


# Configure logging
LOG_LVL = os.getenv('LOG_LVL')
log = logging.getLogger(__name__)
if not LOG_LVL:
    LOG_LVL = 'DEBUG'

log = logging.getLogger(__name__)
h = logging.StreamHandler(sys.stdout)
h.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
log.addHandler(h)
log.setLevel(LOG_LVL)


# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    log.error('`DISCORD_TOKEN` must be set in .env file')
    sys.exit()


# Create bot
intents = discord.Intents.none()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)
#bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="yo mama!"))
    log.info('Bot logged in as `%s` (id %s)', bot.user, bot.user.id)
    log.info('Member of the following servers/guilds:')
    for guild in bot.guilds:
        log.info('  %s', guild.name)


# Hello command
@bot.command(name='hello', aliases=['yo'], help='Hello world test command')
async def helloworld(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")

# Dice roll
@bot.command(name="roll", help="Roll dice")
async def roll(ctx, sides=""):
    # Error detection
    if sides == "":
        embed = discord.Embed(title="Error!", description=f"You did not provide enough information!", color=0xff0000)
        await ctx.reply(embed=embed)
        return

    try:
        sides = int(sides)
    except:
        embed = discord.Embed(title="Error!", description=f"Must be an integer!", color=0xff0000)
        await ctx.reply(embed=embed)
        return
        
    if sides > 6:
        # Logic
        rolled = random.randint(1, sides)
        embed = discord.Embed(title="Success!", description=f"You rolled a **{rolled}** from a dice with **{sides}** sides.", color=0x00ff00)
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title="Error!", description=f"Your dice must have more sides than **6**", color=0xff0000)
        await ctx.reply(embed=embed)

# Coinflip
@bot.command(name="coinflip", aliases=["flip"], help="Flip a coin")
async def coinflip(ctx):
    flipped = ["Heads", "Tails"]
    print(flipped)
    flipped = random.choice(flipped)
    print(flipped)
    if flipped == "Heads":
        headsEmbed = discord.Embed(title="Success!", color=0x00ff00)
        headsEmbed.set_image("https://cdn.discordapp.com/attachments/1018797476041478184/1022091621174612009/unknown.png")
        await ctx.reply(embed=headsEmbed)
    else:
        tailsEmbed = discord.Embed(title="Success!", color=0x00ff00)
        tailsEmbed.set_image("https://media.discordapp.net/attachments/1018797476041478184/1022091823939862568/unknown.png")
        await ctx.reply(embed=tailsEmbed)

# Automod
bannedMessages = ["poop", "pepe"]

@bot.event
async def on_message(message):
    for bannedMessage in bannedMessages:
        if bannedMessage in message.content.lower().split(" "):
            await message.delete()
            await message.channel.send("fyfy", delete_after=5.0)

#@bot.command(name='help')
#async def help(ctx):
#
#    about_text = ('A Python Discord template-bot, '
#                 'demonstrating how to write a bot.')
#
#    embed = discord.Embed(colour = discord.Colour.blue())
#    embed.set_author(name='Help')
#    embed.add_field(name='About', value=about_text, inline=False)
#                          
#    embed.add_field(name='`!hello` | `!yo`',
#                    value=('hello world test command.',
#                    inline=False)
#
#    await ctx.send(embed=embed)

# Start bot
try:
    bot.run(TOKEN)
except discord.errors.LoginFailure:
    log.error('Bot login failed, improper/invalid token')
    sys.exit()
