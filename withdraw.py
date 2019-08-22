from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal
import discord
from discord.ext import commands

import user_db
import config

rpc_connection = 'http://{0}:{1}@{2}:{3}'.format(config.rpc_user, config.rpc_password, config.ip, config.rpc_port)

def str_isfloat(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

class Withdraw(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def withdraw(self, ctx, address=None, amount=None):
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

            if address is None or amount is None:
                embed = discord.Embed(color=0xffd800)
                embed.set_author(
                    name=ctx.author.display_name,
                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                embed.add_field(
                    name="No adress or amount specified. Please check **!help** for information.",
                    value=" :warning: :warning: :warning:  ")
                embed.set_footer(text="Umbru v{0}]".format(config.VERSION),
                             icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                await ctx.channel.send(embed=embed)
            else:
                pass

                if not str_isfloat(amount) or Decimal(amount) < Decimal('0.1'):
                    embed = discord.Embed(color=0xff0000)
                    embed.set_author(
                        name=ctx.author.display_name,
                        icon_url=ctx.author.avatar_url_as(format='png', size=256))
                    embed.add_field(
                        name="Invalid amount (must be at least 0.1 UMBRU).",
                        value="`{0}`".format(str(amount)))
                    embed.set_footer(text="Umbru v{0}]".format(config.VERSION),
                             icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                    await ctx.channel.send(embed=embed)
                else:
                    sendamount = Decimal(str(float(amount))) - \
                                Decimal(str(config.FEE))
                    account = str(ctx.author.id)

                    validate = client.validateaddress(address)
                    if not validate['isvalid']:
                        embed = discord.Embed(color=0xff0000)
                        embed.set_author(
                            name=ctx.author.display_name,
                            icon_url=ctx.author.avatar_url_as(format='png', size=256))
                        embed.add_field(
                            name="Invalid address. Please check **!help** for more information.",
                            value="`{0}`".format(str(address)))
                        embed.set_footer(text="Umbru v{0}]".format(config.VERSION),
                             icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                        await ctx.channel.send(embed=embed)
                    elif Decimal(amount) > client.getbalance(account, config.CONFIRM):
                        embed = discord.Embed(color=0xff0000)
                        embed.set_author(
                            name=ctx.author.display_name,
                            icon_url=ctx.author.avatar_url_as(format='png', size=256))
                        embed.add_field(
                            name="You do not have enough Umbru.",
                            value="Your balance: **{0} UMBRU**".format(client.getbalance(account, config.CONFIRM)))
                        embed.set_footer(text="Umbru v{0}]".format(config.VERSION),
                             icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                        await ctx.channel.send(embed=embed)
                    else:
                        try:
                            txid = client.sendfrom(account, address, float(sendamount))
                        except:
                            embed = discord.Embed(color=0xff0000)
                            embed.set_author(
                                name=ctx.author.display_name,
                                icon_url=ctx.author.avatar_url_as(format='png', size=256))
                            embed.add_field(
                                name="Invalid tip amount. Please check **!help** for information.",
                                value="`{0}`".format(amount))
                            embed.set_footer(text="Umbru v{0}]".format(config.VERSION),
                                icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                            await ctx.channel.send(embed=embed)
                        if len(txid) == 64:
                            tx = client.gettransaction(txid)
                            txfee = tx['fee']
                            client.move(account, "tipbot_wallet", Decimal(str(config.FEE)))
                            client.move("tipbot_wallet", account, -txfee)

                            embed = discord.Embed(
                                title="**Block Explorer**",
                                url='https://explorer.umbru.io/insight/tx/{0}'.format(txid), color=0x0043ff)
                            embed.set_author(
                                name=ctx.author.display_name,
                                icon_url=ctx.author.avatar_url_as(format='png', size=256))
                            embed.add_field(
                                name="Withdrawal Successful: `{0} UMBRU`\nWithdrawal Fee: `{1} UMBRU`\nClick above link to check on the block explorer.".format(sendamount, str(config.FEE)),
                                value="Your Balance: `{0} UMBRU`".format(client.getbalance(account, config.CONFIRM)))
                            embed.set_footer(text="Umbru v{0}]".format(config.VERSION),
                                icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                            await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Withdraw(bot))