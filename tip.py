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

class Tip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tip(self, ctx, mention=None, amount=None):
        client = AuthServiceProxy(rpc_connection)
        user_id = str(ctx.author.id)

        if not user_db.check_user(user_id):
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

            if mention is None or amount is None:
                embed = discord.Embed(color=0xffd800)
                embed.set_author(
                    name=ctx.author.display_name,
                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                embed.add_field(
                    name="No user or amount specified. Please check **!help** for information.",
                    value=" :warning: :warning: :warning:  ")
                embed.set_footer(
                    text="TipBot v{0}]".format(config.VERSION),
                    icon_url=self.bot.user.avatar_url_as(format='png', size=256))
                await ctx.channel.send(embed=embed)
            elif not str_isfloat(amount):
                embed = discord.Embed(color=0xff0000)
                embed.set_author(
                    name=ctx.author.display_name,
                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                embed.add_field(
                    name="Invalid tip amount. Please check **!help** for information.",
                    value="`{0}`".format(amount))
                embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                await ctx.channel.send(embed=embed)
            else:
                pass

                tipfrom = str(ctx.author.id)
                tipto = str(mention.replace('<@','').replace('>',''))
                amount = Decimal(str(float(amount)))

                if amount < Decimal('0.01'):
                    embed = discord.Embed(color=0xff0000)
                    embed.set_author(
                        name=ctx.author.display_name,
                        icon_url=ctx.author.avatar_url_as(format='png', size=256))
                    embed.add_field(
                        name="Tip amount must be atleast 0.01 UMBRU",
                        value="`{0}`".format(amount))
                    embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                    await ctx.channel.send(embed=embed)
                else:
                    if len(tipto) != 18 and len(tipto) != 17:
                        embed = discord.Embed(color=0xff0000)
                        embed.set_author(
                            name=ctx.author.display_name,
                            icon_url=ctx.author.avatar_url_as(format='png', size=256))
                        embed.add_field(
                            name="Invalid User. Please check **!help** for information.",
                            value="`{0}`".format(str(mention)))
                        embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                        await ctx.channel.send(embed=embed)
                    elif tipfrom == tipto:
                        embed = discord.Embed(color=0xff0000)
                        embed.set_author(
                            name=ctx.author.display_name,
                            icon_url=ctx.author.avatar_url_as(format='png', size=256))
                        embed.add_field(
                            name="Sorry you cannot tip yourself!",
                            value=" :wink: ")
                        embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                        await ctx.channel.send(embed=embed)
                    elif amount > client.getbalance(tipfrom, config.CONFIRM):
                        embed = discord.Embed(color=0xff0000)
                        embed.set_author(
                            name=ctx.author.display_name,
                            icon_url=ctx.author.avatar_url_as(format='png', size=256))
                        embed.add_field(
                            name="Sorry you do not have enough UMBRU for that.",
                            value="Your balance is: **{0} UMBRU**".format(client.getbalance(tipfrom, config.CONFIRM)))
                        embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                        await ctx.channel.send(embed=embed)
                    else:
                        if tipto == str(self.bot.user.id):
                            try:
                                move_istrue = client.move(tipfrom, 'tipbot_wallet', float(amount))
                            except:
                                embed = discord.Embed(color=0xff0000)
                                embed.set_author(
                                    name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                                embed.add_field(
                                    name="Invalid tip amount. Please check **!help** for information.",
                                    value="`{0}`".format(amount))
                                embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                                await ctx.channel.send(embed=embed)
                            if move_istrue:
                                embed = discord.Embed(color=0x7152b6)
                                embed.set_author(
                                    name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                                embed.add_field(
                                    name="Thank you for the donation!",
                                    value="**{0} UMBRU**".format(amount))
                                embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                                await ctx.channel.send(embed=embed)
                        else:
                            try:
                                move_istrue = client.move(tipfrom, tipto, float(amount))
                            except:
                                embed = discord.Embed(color=0xff0000)
                                embed.set_author(
                                    name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                                embed.add_field(
                                    name="Invalid tip amount. Please check **!help** for information.",
                                    value="`{0}`".format(amount))
                                embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                                await ctx.channel.send(embed=embed)
                            if move_istrue:
                                embed = discord.Embed(color=0x7152b6)
                                embed.set_author(
                                    name=ctx.author.display_name,
                                    icon_url=ctx.author.avatar_url_as(format='png', size=256))
                                embed.add_field(
                                    name="{0} has tipped {1} `{2} UMBRU`".format(ctx.author.display_name,
                                                                                self.bot.get_user(int(tipto)).display_name,
                                                                                amount),
                                    value="Spend it wisely!")
                                embed.set_footer(text="TipBot v{0}".format(config.VERSION), icon_url=self.bot.user.avatar_url_as(format='png', size=256))

                                await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Tip(bot))