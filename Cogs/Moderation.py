import discord
from discord.ext import commands
import typing
import asyncio

class ModCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="뮤트")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: typing.Optional[str] = "사유 없음."):
        """
        경손아 뮤트 < 유저 > [ 사유 ]


        < 유저 > 를 뮤트할 수 있어요.
        """

        role = discord.utils.get(ctx.guild.roles, name='뮤트')

        if role not in member.roles:
            if member.guild_permissions.administrator:
                await ctx.send(f"{member} 님은 관리자 권한을 소유중이여 뮤트가 불가능해요.")
            else:
                await member.send(f"{ctx.guild.name} 에서 뮤트되었어요.\n\n사유: {reason}")
                await member.add_roles(role)
                await ctx.send(f"{member} 님을 뮤트했어요.\n\n사유: {reason}")
        else:
            await ctx.send(f"{member} 님은 이미 뮤트 상태에요.")

    @commands.command(name="언뮤트")
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, *, member: discord.Member):
        """
        경손아 언뮤트 < 유저 > [ 사유 ]


        < 유저 > 를 언뮤트할 수 있어요.
        """

        role = discord.utils.get(ctx.guild.roles, name='뮤트')
        if role in member.roles:
            await member.send(f"{ctx.guild.name} 에서 언뮤트되었어요.")
            await member.remove_roles(role)
            await ctx.send(f"{member} 님을 언뮤트했어요.")
        else:
            await ctx.send(f"{member} 님은 뮤트상태가 아니에요.")

    @commands.command(name="추방")
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: typing.Optional[str] = "사유 없음."):
        """
        경손아 추방 < 유저 > [ 사유 ]


        < 유저 > 를 추방할 수 있어요.
        """       

        if member.top_role < ctx.guild.me.top_role:
            if member.guild_permissions.administrator:
                await ctx.send(f"{member} 님은 관리자 권한을 소유중이여 추방이 불가능해요.")
            else:
                await member.send(f"{ctx.guild.name} 에서 추방되었어요.\n\n사유: {reason}\n\n관리자: {ctx.author}")
                await ctx.guild.kick(member, reason=reason)
                await ctx.send(f"{member} 님을 추방했어요.\n\n사유: {reason}")
        else:
            await ctx.send(f"봇의 권한이 {member.name} 님보다 낮아 추방할 수 없어요.")

    @commands.command(name="차단")
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: typing.Optional[str] = "사유 없음.", *, delete: typing.Optional[int] = 0):
        """
        경손아 차단 < 유저 > [ 사유 ]


        < 유저 > 를 차단할 수 있어요.
        """       

        if member.top_role < ctx.guild.me.top_role:
            if member.guild_permissions.administrator:
                await ctx.send(f"{member} 님은 관리자 권한을 소유중이여 차단이 불가능해요.")
            else:
                await member.send(f"{ctx.guild.name} 에서 차단되었어요.\n\n사유: {reason}\n\n관리자: {ctx.author}")
                await ctx.guild.ban(member, reason=reason, delete_message_days=delete)
                await ctx.send(f"{member} 님을 차단했어요.\n\n사유: {reason}")
        else:
            await ctx.send(f"봇의 권한이 {member.name} 님보다 낮아 차단할 수 없어요.")
        
    @commands.command(name="청소")
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, *, num: int):
        """
        경손아 청소 < 숫자 >


        < 숫자 > 만큼 채널을 청소할 수 있어요.
        """      
        if ctx.guild:
            if num <= 100 and num > 0:
                await ctx.message.delete()
                await ctx.channel.purge(limit=num)
                await ctx.send(f"{num} 개의 메시지를 삭제했어요.", delete_after=1)
            else:
                await ctx.send("0 에서 100 중 옳바른 숫자를 입력해주세요.")
        else:
            await ctx.send("해당 명령어는 DM 에서는 사용이 불가해요, 서버에서 사용해주세요.")

    @commands.command(name="이름설정")
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    async def name(self, ctx, member: discord.Member, *, args):
        """
        경손아 이름설정 < 유저 > < 이름 >


        < 유저 > 의 이름을 < 이름 > 으로 설정할 수 있어요.
        """

        if ctx.guild:
            if not args:
                await ctx.send(f"`경손아 이름설정 < 유저 > < 이름 >` (이)가 올바른 명령어에요.")
            else:
                await member.edit(nick=args)
                await ctx.message.add_reaction("✅")
                await member.send(f"{ctx.guild.name} 에서 닉네임이 변경되었어요.\n\n변경된 닉네임: {args}\n변경자: {ctx.author}")
        else:
            await ctx.send("해당 명령어는 DM 에서는 사용이 불가해요, 서버에서 사용해주세요.")

def setup(bot):
    bot.add_cog(ModCommand(bot))