from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal
import discord
from discord.ext import commands

import user_db
import config

rpc_connection = 'http://{0}:{1}@{2}:{3}'.format(config.rpc_user, config.rpc_password, config.ip, config.rpc_port)

class Withdrawall(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def withdrawall(self, ctx, address=None):
        client = AuthServiceProxy(rpc_connection)
        user_id = str(ctx.author.id)
        user_name = ctx.author.name

        if not user_db.check_user(user_id):
            user_db.add_user(user_id, user_name)
            embed = discord.Embed(
                title="**How may I be of service?**",
                color=0x7152b6)
            embed.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.avatar_url_as(format='png', size=256))
            embed.add_field(
                name="To see all my available commands type `!help`",
                value="If you have any issues please let one of the team know.")
            embed.set_thumbnail(url=self.bot.user.avatar_url_as(format='png', size=1024))
            embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

            await ctx.channel.send(embed=embed)
        else:
            pass

            account = str(ctx.author.id)
            balance = Decimal(client.getbalance(account, config.CONFIRM))

            if address is None:
                embed = discord.Embed(color=0xffd800)
                embed.set_author(
                    name=ctx.author.display_name,
                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                embed.add_field(
                    name="No address specified. Please check **!help** for information.",
                    value=" :warning: :warning: :warning: ")
                embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                await ctx.channel.send(embed=embed)
            else:
                pass

                if balance < Decimal('0.1'):
                    embed = discord.Embed(color=0xff0000)
                    embed.set_author(
                        name=ctx.author.display_name,
                        icon_url=ctx.author.avatar_url_as(format='png', size=256))
                    embed.add_field(
                        name="Invalid amount (must be at least 0.1 UMBRU).",
                        value="Your Balances: **{0:.6f} UMBRU**".format(client.getbalance(account, config.CONFIRM)))
                    embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                    await ctx.channel.send(embed=embed)
                else:
                    amount = balance - Decimal(str(config.FEE))
                    validate = client.validateaddress(address)

                    if not validate['isvalid']:
                        embed = discord.Embed(color=0xff0000)
                        embed.set_author(
                            name=ctx.author.display_name,
                            icon_url=ctx.author.avatar_url_as(format='png', size=256))
                        embed.add_field(
                            name="Invalid Umbru address, please check.",
                            value="`{0}`".format(str(address)))
                        embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                        await ctx.channel.send(embed=embed)
                    else:
                        txid = client.sendfrom(account, address, float(amount))
                        tx = client.gettransaction(txid)
                        txfee = tx['fee']

                        client.move(account, "tipbot_wallet", Decimal(str(config.FEE)))
                        client.move("tipbot_wallet", account, -txfee)

                        embed = discord.Embed(
                            title="**Block Explorer**",
                            url='https://explorer.umbru.io/insight/tx/{0}'.format(txid),
                            color=0x7152b6)
                        embed.set_author(
                            name=ctx.author.display_name,
                            icon_url=ctx.author.avatar_url_as(format='png', size=256))
                        embed.add_field(
                            name="Withdrawal Complete: `{0} UMBRU`\nWithdrawal Fee: `{1} UMBRU`\nClick above link to check on the block explorer.".format(amount, str(config.FEE)),
                            value="Your Balances: `{0:.6f} UMBRU`".format(client.getbalance(account, config.CONFIRM)))
                        embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Withdrawall(bot))