from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import discord
from discord.ext import commands

import user_db
import config

rpc_connection = 'http://{0}:{1}@{2}:{3}'.format(config.rpc_user, config.rpc_password, config.ip, config.rpc_port)

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
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
            embed.set_footer(text="Umbru v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

            await ctx.channel.send(embed=embed)
        else:
            pass

            block = client.getblockchaininfo()['blocks']
            hash_rate = round(client.getnetworkhashps() / 1000000000, 4)
            difficulty = round(client.getblockchaininfo()['difficulty'], 4)
            connection = client.getnetworkinfo()['connections']
            client_version = client.getnetworkinfo()['subversion']

            embed = discord.Embed(
                title="**Umbru Network Information**",
                color=0x0043ff)
            embed.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.avatar_url_as(format='png', size=256))
            embed.add_field(
                name="**Current Block Height:**",
                value="`{0}`".format(block),
                inline=True)
            embed.add_field(
                name="**Network Hash Rate:**",
                value="`{0} GH/s`".format(hash_rate),
                inline=True)
            embed.add_field(
                name="**Difficulty:**",
                value="`{0}`".format(difficulty),
                inline=True)
            embed.add_field(
                name="**Connections:**",
                value="`{0}`".format(connection),
                inline=True)
            embed.add_field(
                name="**Wallet Version:**",
                value="`{0}`".format(client_version),
                inline=True)
            embed.set_footer(text="Umbru v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

            await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))