import traceback

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import discord
from discord.ext import commands

from config import TOKEN

COMMANDS = [
    'info',
    'help',
    'balance',
    'deposit',
    'tip',
    'withdraw',
    'withdrawall'
]

class TipBot(commands.Bot):

    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        for cog in COMMANDS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print("Successful Login") 
        print("Name: " + str(self.user.name))
        print("ID: " + str(self.user.id))
        print("----------------------")
        await self.change_presence(activity=discord.Game(name="!help")) 

bot = TipBot(command_prefix='!')
bot.run(TOKEN)