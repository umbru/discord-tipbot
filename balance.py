import sys

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import discord
from discord.ext import commands

import user_db
import config

rpc_connection = 'http://{0}:{1}@{2}:{3}'.format(config.rpc_user, config.rpc_password, config.ip, config.rpc_port)

class Balance(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx):
        client = AuthServiceProxy(rpc_connection)
        user_id = str(ctx.author.id)

        if not user_db.check_user(user_id):
            embed = discord.Embed(
                title="**How may I be of service?**",
                color=0x0043ff)
            embed.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.avatar_url_as(format='png', size=256))
            embed.add_field(
                name="To see all my available commands type `!help`",
                value="If you have any issues please let one of the team know.")
            embed.set_thumbnail(url=self.bot.user.avatar_url_as(format='png', size=1024))
            embed.set_footer(text="Umbru v{0}]".format(config.VERSION),
                             icon_url=self.bot.user.avatar_url_as(format='png', size=256))

            await ctx.channel.send(embed=embed)
        else:
            pass

            account = str(ctx.author.id)
            user_name = ctx.author.display_name
            balance = client.getbalance(account, config.CONFIRM)
            unconfirmed_balance = client.getbalance(account, 0) - \
                                client.getbalance(account, config.CONFIRM)

            embed = discord.Embed(
                title="**Your Umbru Balance:**",
                color=0x0043ff)
            embed.set_author(
                name=user_name,
                icon_url=ctx.author.avatar_url_as(format='png', size=256))
            embed.add_field(
                name="{0} UMBRU".format(str(balance)),
                value="Unconfirmed: {0} UMBRU".format(str(unconfirmed_balance)))
            embed.set_footer(text="Umbru v{0}]".format(config.VERSION),
                             icon_url=self.bot.user.avatar_url_as(format='png', size=256))

            await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Balance(bot))