import textwrap
import discord
from discord.ext import commands
import json
import random
from dotenv import find_dotenv, load_dotenv
import os


class HelpCommand(commands.HelpCommand):
    def get_command_signature(self, command):
        return "{0.clean_prefix}{1.qualified_name} {1.signature}".format(self, command)

    async def send_bot_help(self, mapping):
        for cog, commands in mapping.items():
            if cog:
                cog_name = cog.qualified_name
            else:
                cog_name = "Commands"

            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            command_descriptions = [c.description for c in filtered]

            if command_signatures:
                cog_commands = "\n".join(
                    f"**{sig}**\n{desc}"
                    for sig, desc in zip(command_signatures, command_descriptions)
                )
                embed = discord.Embed(
                    title=cog_name, 
                    description=cog_commands, 
                    color=discord.Color.blue()
                )
                await self.get_destination().send(embed=embed)


load_dotenv(find_dotenv())
TOKEN = os.environ["TOKEN"]

intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)
bot.help_command = HelpCommand()


# Load configuration
with open("santa_config.json", "r") as f:
    config = json.load(f)


# == logic stuff ==


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


@bot.command(
    name="secretsanta",
    description="This command can only be used by the organiser. It sends a PM to everyone saying who's buying for who. This is randomly assigned."
)
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
