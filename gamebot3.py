import logging
import os
import sys

import discord
from discord.ext import commands
import dotenv
import random

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

words = ["water", "chair", "table"]
word = None
number_guesses = 6
games = {}
@bot.command()
async def newgame(ctx):
    global word
    word = random.choice(words)
    
    game = {'name': ctx.author.name,
            'word': word,
            'tries': 6}
    games[ctx.author.id] = game 
    await ctx.send(f"{ctx.author.name} has started a new Wordle game!")
    await ctx.send(f"Type !w <guess> to guess.")

@bot.command()
async def debug(ctx):
    print("nick", ctx.author.nick)
    print("name", ctx.author.name)
    print("id", ctx.author.id)
    print("ctx.author", ctx.author)
    print(games)
    print(games[ctx.author.id]['tries'])

@bot.command(name='w')
async def guess(ctx, guess_word):
    global number_guesses
    # if word == None:
    if not word:
        await ctx.send(f"You need to start a new game with !newgame")
        return

    if len(guess_word) != len(word):
        await ctx.send(f"You need to guess {len(word)} characters, not {len(guess_word)}!")
        return

        
    # https://en.wikipedia.org/wiki/List_of_Unicode_characters
    mark_correct = chr(0x2713) 
    mark_in_word = chr(0x25cc) 
    mark_not_in_word = chr(0x2715)

    message = [] 
    for i in range(len(word)):

        if word[i] == guess_word[i]:
            message.append(f"{guess_word[i].upper()} {mark_correct} ")
        elif guess_word[i] in word:
            message.append(f"{guess_word[i].upper()} {mark_in_word} ")
        else:
            message.append(f"{guess_word[i].upper()} {mark_not_in_word} ")
           
    await ctx.send("\n".join(message))

    if guess_word == word:
        await ctx.send(f"'{guess_word}' was the right word! Congrats!")

    #number_guesses = number_guesses - 1
    number_guesses -= 1

    await ctx.send(f"Guesses left: {number_guesses}")

    if number_guesses == 0:
        await ctx.send(f"You lost!")




@bot.event
async def on_ready():
    log.info('Bot logged in as `%s` (id %s)', bot.user, bot.user.id)
    log.info('Member of the following servers/guilds:')
    for guild in bot.guilds:
        log.info('  %s', guild.name)



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
