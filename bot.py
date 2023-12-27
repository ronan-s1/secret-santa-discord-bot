import textwrap
import discord
from discord.ext import commands
import json
import random
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())
TOKEN = os.environ["TOKEN"]

intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)


class Help(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page, color=discord.Color.blue())
            await destination.send(embed=embed)


bot.help_command = Help()


# Load configuration
with open("santa_config.json", "r") as f:
    config = json.load(f)


# Check if the organiser called the secretsanta command
def is_organiser(ctx):
    return str(ctx.author) == config["organiser_discord_username"]


# Secret Santa matching function
def secret_santa(users):
    shuffled_users = users.copy()

    # Check that no user is paired with themselves.
    while True:
        random.shuffle(shuffled_users)
        if all(x != y for x, y in zip(users, shuffled_users)):
            break

    pairs = list(zip(users, shuffled_users))

    return pairs


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.command(name="secretsanta")
@commands.check(is_organiser)
async def secretsanta(ctx):
    participants = config["participants"]
    santa_pairs = secret_santa(participants)
    for santa, recipient in santa_pairs:
        secret_santa_message = textwrap.dedent(
            f"""
            Greetings {santa['name']}, let's see who you got!

            Name: ||**{recipient['name']}**||
            Address: ||**{recipient['address']}**||
        """
        )

        discord_id = santa["discord_user_id"]
        user = await bot.fetch_user(discord_id)
        await user.send(secret_santa_message)

    await ctx.send(f"Secret Santa messages sent!")


bot.run(TOKEN)
