import nextcord
from nextcord.ext import commands
import datetime
import asyncio
import random
import json
import urllib.parse, urllib.request, re
import urllib

intents = nextcord.Intents().all()
client = commands.Bot(command_prefix="-", help_command=None, intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"-help in {len(client.guilds)}"))
    print("am ready")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = nextcord.Embed(title="⚠️Error⚠️", color=nextcord.Color.red())
        embed.add_field(name="ERROR:", value="Error Code: 1")

        await ctx.reply(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = nextcord.Embed(title="⚠️Error⚠️", color=nextcord.Color.red())
        embed.add_field(name="ERROR:", value="Error Code: 3")

        await ctx.reply(embed=embed)
    if isinstance(error, commands.CommandInvokeError):
        raise error
    if isinstance(error, commands.CommandNotFound):
        embed = nextcord.Embed(title="⚠️Error⚠️", color=nextcord.Color.red())
        embed.add_field(name="ERROR:", value="Error Code: 4")

        await ctx.reply(embed=embed)
    if isinstance(error, commands.MemberNotFound):
        embed = nextcord.Embed(title="⚠️Error⚠️", color=nextcord.Color.red())
        embed.add_field(name="ERROR:", value="Error Code: 2")

        await ctx.reply(embed=embed)
    if isinstance(error, commands.BadArgument):
        embed = nextcord.Embed(title="⚠️Error⚠️", color=nextcord.Color.red())
        embed.add_field(name="ERROR:", value="Error Code: 7")

        await ctx.reply(embed=embed)

@client.command(aliases=["boot"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:nextcord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} just got booted from the server lol")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:nextcord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} just got banned from the server lol")


@client.command(aliases=["forgive"])
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention} 😎")
            return


@client.command()
async def online(ctx):
    await ctx.reply("Yes I am sadly online >:c")


@client.command(aliases=["purge"])
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=11):
    amount = amount + 1
    ctxamount = amount - 1
    if amount > 251:
        await ctx.send("Cannot delete more than 250 messages. It will lag me out >:C")
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Cleared {ctxamount} messages")



@client.command()
async def suggest(ctx, *, suggestion):
    await ctx.channel.purge(limit=1)
    channel = nextcord.utils.get(ctx.guild.text_channels, name="suggestions")
    suggest = nextcord.Embed(title="Suggestion!", description=f"{ctx.author.name} has suggested `{suggestion}`", color=nextcord.Color.red())
    sugg = await channel.send(embed=suggest)
    await channel.send(f"Suggestion ID: {sugg.id}")
    await sugg.add_reaction("✅")
    await sugg.add_reaction("❌")

@client.command(aliases=["app"])
@commands.has_permissions(administrator=True)
async def approve(ctx, id:int=None, *, reason=None):
    if id is None:
        return
    channel = nextcord.utils.get(ctx.guild.text_channels, name="suggestions")
    if channel is None:
        return
    suggestionMsg = await channel.fetch_message(id)
    embed = nextcord.Embed(title=f"Suggestion has been approved!", description=f"The suggestion id of `{suggestionMsg.id} has been approved by {ctx.author.name} | Reason: {reason}`", color=discord.Color.red())
    await channel.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def deny(ctx, id:int=None, *, reason=None):
    if id is None:
        return
    channel = nextcord.utils.get(ctx.guild.text_channels, name="suggestions")
    if channel is None:
        return
    suggestionMsg = await channel.fetch_message(id)
    embed = nextcord.Embed(title=f"Suggestion has been denied", description=f"The suggestion id of `{suggestionMsg.id} has been denied by {ctx.author.name} | Reason: {reason}`", color=nextcord.Color.red())
    await channel.send(embed=embed)

@client.command(aliases=["h"])
async def help(ctx):
    em = nextcord.Embed(title = "Here are commands for Rundum bot.",color= nextcord.Color.purple())
    em.add_field(name = "-help", value = "shows this page")
    em.add_field(name="-helpsug", value="Shows the suggestion help")
    em.add_field(name="-helpmod", value="Shows the moderator help")
    em.add_field(name="-selfpromo", value="Promotes the creator of Rundum bot >:)")
    em.add_field(name="-online", value="Checks if the bot is online")
    em.add_field(name="-tic", value="Play tictactoe with yourself or someone else")
    em.add_field(name="-youtube (search)", value="Searches for a youtube video on the internet.")
    em.add_field(name="-say (msg)", value="Makes the bot send a message")
    em.add_field(name="-info", value="Displays server info")
    em.add_field(name="-whois (@member)", value="Displays info about a user")
    em.add_field(name="-avatar (@member)", value="Displays a users avatar image")
    em.add_field(name="-ping", value="Shows the bots ping")
    em.add_field(name="-8ball (message)", value="Magic 8 balls something")
    em.add_field(name="-coinflip", value="Flip a coin")
    em.add_field(name="-thank (@member) (reason)", value="Thank a member for their help!")
    em.add_field(name="-guess", value="Play a guessing game")
    em.add_field(name="-rps (rock, paper, or scissors)", value="Play rock paper scissors with bot uwu")

    await ctx.send(embed=em)

@client.command(aliases=["hs"])
async def helpsug(ctx):
    em = nextcord.Embed(title = "Here are commands for Rundum bot (suggestion).",color= nextcord.Color.purple())
    em.add_field(name = "-suggest (suggestion)", value = "Suggest something for the server")
    em.add_field(name="-app (id)", value="Approves a suggestion (needs admin)")
    em.add_field(name="-deny (id)", value="Denies a suggestion (needs admin)")

    await ctx.send(embed=em)

@client.command(aliases=["hm"])
async def helpmod(ctx):
    em = nextcord.Embed(title = "Here are commands for Rundum bot (moderation).",color= nextcord.Color.purple())
    em.add_field(name = "-clear (amount)", value = "Clears messages (needs administator)")
    em.add_field(name="-kick (@member) (reason)", value="Kicks a user (needs kick members)")
    em.add_field(name="-ban (@member) (reason)", value="Bans a user (needs ban members)")
    em.add_field(name="-unban (@member)", value="Unbans a user (needs ban members)")
    em.add_field(name="-toggle (command)", value="Toggles a command on/off (only Pigioty can do this)")
    em.add_field(name="-giveaway (time) (prize)", value="Starts a giveaway (needs administator)")
    em.add_field(name="-slowmode (time)", value="Sets the channel's slowmode (needs administator)")
    em.add_field(name="-dmall (message)", value="Dm's all users in server (needs administator)")

    await ctx.send(embed=em)

class TicTacToeButton(nextcord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style=nextcord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = nextcord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = nextcord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)

class TicTacToe(nextcord.ui.View):
    children: list[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


@client.command()
async def tic(ctx):
    await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())


@client.command()
async def youtube(ctx, *, search):

    query_string = urllib.parse.urlencode({
        "search_query": search
    })
    htm_content = urllib.request.urlopen(
        "http://www.youtube.com/results?" + query_string
    )
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    await ctx.reply("http://www.youtube.com/watch?v=" + search_results[0])


@client.command()
async def say(ctx, saymsg=None):
    if saymsg == None:
                embed = nextcord.Embed(title="⚠️Error⚠️", color=nextcord.Color.red())
                embed.add_field(name="ERROR:", value="Error Code: 1")

                await ctx.reply(embed=embed)
                return
    sayEmbed = nextcord.Embed(title = f"{saymsg}", description = f"{ctx.author}")
    await ctx.send(embed = sayEmbed)



@client.command(aliases=["si", "server", "info"])
async def serverinfo(ctx):
    role_count = len(ctx.guild.roles)
    list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

    serverinfoEmbed = nextcord.Embed(timestamp=ctx.message.created_at, color=ctx.author.color)
    serverinfoEmbed.add_field(name="Name", value=f"{ctx.guild.name}", inline=False)
    serverinfoEmbed.add_field(name="Member count", value=ctx.guild.member_count, inline=False)
    serverinfoEmbed.add_field(name="Veriff level", value=str(ctx.guild.verification_level), inline=False)
    serverinfoEmbed.add_field(name="Highest role", value=ctx.guild.roles[-2], inline=False)
    serverinfoEmbed.add_field(name="Role number", value=str(role_count), inline=False)
    serverinfoEmbed.add_field(name="Bots", value=', '.join(list_of_bots), inline=False)

    await ctx.send(embed = serverinfoEmbed)

@client.command(name="whois")
async def whois(ctx, user: nextcord.Member = None):
    if user == None:
        user = ctx.author

    rlist = []
    for role in user.roles:
        if role.name != "@everyone":
            rlist.append(role.mention)

    b = ", ".join(rlist)

    embed = nextcord.Embed(colour=user.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar.url),
    embed.set_footer(text=f'Requested by - {ctx.author}',
                     icon_url=ctx.author.avatar.url)

    embed.add_field(name='ID:', value=user.id, inline=False)
    embed.add_field(name='Name:', value=user.display_name, inline=False)

    embed.add_field(name='Created at:', value=user.created_at, inline=False)
    embed.add_field(name='Joined at:', value=user.joined_at, inline=False)

    embed.add_field(name='Is person a bot?', value=user.bot, inline=False)

    embed.add_field(name=f'Roles:({len(rlist)})', value=''.join([b]), inline=False)
    embed.add_field(name='Top Role:', value=user.top_role.mention, inline=False)

    await ctx.send(embed=embed)


@client.command(aliases=["ava", "atr", "avt", "pfp"])
async def avatar(ctx, member : nextcord.Member = None):
    if member == None:
        member = ctx.author

    memberAvatar = member.avatar.url

    avaembed = nextcord.Embed(title = f"{member.name}'s Avatar", color= nextcord.Color.purple())
    avaembed.set_image(url = memberAvatar)

    await ctx.send(embed=avaembed)

@client.command()
async def ping(ctx):
    await ctx.reply(f"My ping is {round(client.latency * 1000)}ms")

@client.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "No.",
                 "To lazy to decide now.",
                 "Try again later.",
                 "My reply is no.",
                 "Outlook not so good.",
                 "Better not tell you now.",
                 "Don't count on it.",
                 "Signs point to yes."]

    embed = nextcord.Embed(title="Magicc 8 ball", color=ctx.author.color)
    embed.add_field(name="Question:", value=f"{question}", inline=False)
    embed.add_field(name="Answer:", value=f"{random.choice(responses)}", inline=False)

    await ctx.reply(embed=embed)


@client.command(aliases=["cf"])
async def coinflip(ctx):
    responses = ["Heads!", "Tails!"]

    embed = nextcord.Embed(title="Coinflip", color=ctx.author.color)
    embed.add_field(name="Answer:", value=f"{ctx.author.mention} the coin landed on {random.choice(responses)}")

    await ctx.reply(embed=embed)


@client.command()
async def toggle(ctx, *, command):
    if not ctx.author.id == 695734833116086303:
        return
    command = client.get_command(command)
    if command == None:
        await ctx.reply("Command not found. ¯\_(ツ)_/¯")
    elif ctx.command == command:
        await ctx.reply("You cannot disable this command ¯\_(ツ)_/¯")
    else:
        command.enabled = not command.enabled
        ternany = "enabled" if command.enabled else "disabled"
        await ctx.reply(f"The command {command.qualified_name} has been successfully {ternany}")

@client.command(aliases=["error", "errorcodes"])
async def errorcode(ctx):
    embed = nextcord.Embed(title="Error codes and what they mean",color= nextcord.Color.purple())
    embed.add_field(name="Error code 1:", value="Missing Required Argument!")
    embed.add_field(name="Error code 2:", value="Member not found!")
    embed.add_field(name="Error code 3:", value="Missing permissions to run the command!")
    embed.add_field(name="Error code 4:", value="Command not found!")
    embed.add_field(name="Error code 5:", value="Command is disabled!")
    embed.add_field(name="Error code 6:", value="Limit reached!")
    embed.add_field(name="Error code 7:", value="Bad Argument!")
    embed.add_field(name="Error code 8:", value="Argument cannot be blank!")
    embed.add_field(name="Error code 9:", value="You must chose a valid option!")

    await ctx.reply(embed=embed)

@client.command()
async def gay(ctx, member: nextcord.Member = None):
    if member == None:
        member = ctx.author
    number = random.randint(0,115)
    em = nextcord.Embed(title="Gay counter | Find out how gae some1 is", color=nextcord.Color.purple())
    em.description = f"{member.mention} is {number}% gay"

    await ctx.send(embed=em)


@client.command(aliases=["gmake", "giveawaycreate", "giveawaymake", "giveaway", "ga"])
@commands.has_permissions(administrator=True)
async def gcreate(ctx, time=None, *, prize=None):
    if time == None:
        embed = nextcord.Embed(title="⚠️Error⚠️", color=nextcord.Color.red())
        embed.add_field(name="ERROR:", value="Error Code: 1")
        return await ctx.reply(embed=embed)
    elif prize == None:
        embed = nextcord.Embed(title="⚠️Error⚠️", color=nextcord.Color.red())
        embed.add_field(name="ERROR:", value="Error Code: 1")
        return await ctx.reply(embed=embed)
    embed = nextcord.Embed(title="Giveaway Happening! 🎉", description=f"{ctx.author.mention} is hosting a giveaway for **{prize}**🎉🎉🎉", color = nextcord.Color.blue())
    time_convert = {"s":1, "m":60, "h":3600, "d": 86400}
    gawtime = int(time[0]) * time_convert[time[-1]]
    embed.set_footer(text=f"Giveaway ending in {time}!")
    gaw_msg = await ctx.send(embed = embed)

    await gaw_msg.add_reaction("🎉")
    await asyncio.sleep(gawtime)

    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)

    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    embed = nextcord.Embed(title="Giveaway winner!", color=nextcord.Color.blue())
    embed.add_field(name="Winner:", value=f"Congrats {winner.mention} just won the giveaway for **{prize}** 🎉🎉🎉")

    await ctx.send(embed=embed)

@client.command(aliases=["sm", "slow"])
@commands.has_permissions(administrator=True)
async def slowmode(ctx,time:int):
    try:
        if time == 0:
            embed = nextcord.Embed(title="Slowmode off",color= nextcord.Color.red())
            await ctx.send(embed=embed)
            await ctx.channel.edit(slowmode_delay = 0)
        elif time > 21600:
            embed = nextcord.Embed(title="⚠️Error⚠️", color=nextcord.Color.red())
            embed.add_field(name="ERROR:", value="Error Code: 6")
            await ctx.reply(embed=embed)
            return
        else:
            embed = nextcord.Embed(title=f"Slowmode set to {time} seconds.", color=nextcord.Color.red())
            await ctx.channel.edit(slowmode_delay = time)
            await ctx.send(embed=embed)
    except Exception:
        await print("Error")

class Promos(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Invite bot", style=nextcord.ButtonStyle.red)
    async def Invite(self, button : nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Work in progress bot is not released yet. L", ephemeral=True)
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Subscribe", style=nextcord.ButtonStyle.green)
    async def Subscribe(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Sub here - https://bit.ly/3pe7voy", ephemeral=True)
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Follow", style=nextcord.ButtonStyle.green)
    async def Follow(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("Follow here - https://twitter.com/pigioty", ephemeral=True)
        self.value = True
        self.stop()

@client.command()
async def selfpromo(ctx):
    view = Promos()
    await ctx.send("Here are the self promos of the creator of Rundum Bot", view=view)

    await view.wait()

@client.command()
async def aistart(ctx):
    embed = nextcord.Embed(title="AI started", description=f"Hey {ctx.author.mention} Thanks for waking me up!", color=nextcord.Color.blue())

    await ctx.reply(embed=embed)

@client.command()
async def aistop(ctx):
    embed = nextcord.Embed(title="AI stopped", description=f"{ctx.author.mention} Goodnight I am going to sleep",color=nextcord.Color.blue())

    await ctx.reply(embed=embed)

words = ["Great!, how are you doing!", "Okay, what about you?", "Poorly, are you good?", "Alright", "Bad"]
color = ["Red", "Blue", "Purple", "Green", "Gray", "Black", "Pink", "Yellow", "Brown", "Apricot", "White", "Indigo", "Voilet"]
food = ["Pizza", "Hamburgers", "Steak", "Tacos"]

@client.command()
async def ai(ctx, *, message = None):
    if message == None:
        embed = nextcord.Embed(title="⚠️Error⚠️", color=nextcord.Color.red())
        embed.add_field(name="ERROR:", value="Error Code: 8")

        await ctx.reply(embed=embed)
    if "hello" in message.lower():
        await ctx.reply(f"Hello {ctx.author.mention}!")
    elif "hi" in message.lower():
        await ctx.reply(f"Hello {ctx.author.mention}!")
    elif "how are you" in message.lower():
        await ctx.reply(f"{ctx.author.mention} I am doing {random.choice(words)}")
    elif "how r u" in message.lower():
        await ctx.reply(f"{ctx.author.mention} I am doing {random.choice(words)}")
    elif "goodbye" in message.lower():
        await ctx.reply(f"Goodbye {ctx.author.mention} I will miss you!")
    elif "bye" in message.lower():
        await ctx.reply(f"Goodbye {ctx.author.mention} I will miss you!")
    elif "sex" in message.lower():
        await ctx.reply(f"WOAH THEIR! TO FAR! OH HELL NAW")
    elif "what is your favorite colour" in message.lower():
        await ctx.reply(f"My favorite colour is {random.choice(color)}!")
    elif "what is ur favorite colour" in message.lower():
        await ctx.reply(f"My favorite colour is {random.choice(color)}!")
    elif "whats ur fav colour" in message.lower():
        await ctx.reply(f"My favorite colour is {random.choice(color)}!")
    elif "whats ur favorite color" in message.lower():
        await ctx.reply(f"My favorite colour is {random.choice(color)}!")
    elif "what is your favorite colour" in message.lower():
        await ctx.reply(f"My favorite color is {random.choice(color)}!")
    elif "what is ur favorite color" in message.lower():
        await ctx.reply(f"My favorite colour is {random.choice(color)}!")
    elif "whats ur fav color" in message.lower():
        await ctx.reply(f"My favorite colour is {random.choice(color)}!")
    elif "whats ur favorite color" in message.lower():
        await ctx.reply(f"My favorite colour is {random.choice(color)}!")
    elif "suicide" in message.lower():
        await ctx.reply(f"Are you feeling suicidal? If so please call 800-273-8255")
    elif "kill myself" in message.lower():
        await ctx.reply(f"Are you feeling suicidal? If so please call 800-273-8255")
    elif "shoot myself" in message.lower():
        await ctx.reply(f"Are you feeling suicidal? If so please call 800-273-8255")
    elif "milk" in message.lower():
        await ctx.reply(f"The thing your dad went to get and never came back with")
    elif "what is your gender?" in message.lower():
        await ctx.reply(f"I am non binary bot")
    elif "whats ur gender" in message.lower():
        await ctx.reply(f"I am non binary bot")
    elif "what is your gender?" in message.lower():
        await ctx.reply(f"I am non binary bot")
    elif "what is ur gender" in message.lower():
        await ctx.reply(f"I am non binary bot")
    elif "whats your gender" in message.lower():
        await ctx.reply(f"I am non binary bot")
    elif "whats your favorite food" in message.lower():
        await ctx.reply(f"My favorite food is {random.choice(food)}")
    elif "what is your favorite food" in message.lower():
        await ctx.reply(f"My favorite food is {random.choice(food)}")
    elif "whats your fav food" in message.lower():
        await ctx.reply(f"My favorite food is {random.choice(food)}")
    elif "what your favorite food" in message.lower():
        await ctx.reply(f"My favorite food is {random.choice(food)}")
    elif "you are stupid" in message.lower():
        await ctx.reply(f"Sorry to hear that D: If their is any way I can improve contact Pigioty#4366, Note im still in alpha D:")
    elif "u r stupid" in message.lower():
        await ctx.reply(f"Sorry to hear that D: If their is any way I can improve contact Pigioty#4366, Note im still in alpha D:")
    elif "you stupid" in message.lower():
        await ctx.reply(f"Sorry to hear that D: If their is any way I can improve contact Pigioty#4366, Note im still in alpha D:")
    elif "u stupid" in message.lower():
        await ctx.reply(f"Sorry to hear that D: If their is any way I can improve contact Pigioty#4366, Note im still in alpha D:")
    else:
        print(message)

@client.command()
async def thank(ctx, member : nextcord.Member, *, reason=None):
    embed = nextcord.Embed(title="Thank you!", description=f"{member.mention} {ctx.author.mention} would like to show their appreaction by thanking you for `{reason}`!", color=nextcord.Color.blue())

    await ctx.send(embed=embed)

@client.command()
async def guess(ctx):
    await ctx.reply('Guess a number between 1 and 10 uwu')

    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()

    answer = random.randint(1, 10)

    try:
        guess = await client.wait_for('message', check=is_correct, timeout=5.0)
    except asyncio.TimeoutError:
        return await ctx.reply(f'Rip your took to long to asnwer the answer for it was {answer}.')

    if int(guess.content) == answer:
        await ctx.reply('UWU U GET IT RIGHT OMG YOU ARE SO POG MAN')
    else:
        await ctx.reply(f'Imagine getting it wrong. The answer was {answer} xD')

@client.command(aliases=["rockpaperscissors"])
async def rps(ctx, message):
    answer = message.lower()
    choices = ["rock", "paper", "scissors"]
    computers_answer = random.choice(choices)
    if answer not in choices:
        embed = nextcord.Embed(title="⚠️Error⚠️", color=nextcord.Color.red())
        embed.add_field(name="ERROR:", value="Error Code: 9")
        return await ctx.reply(embed=embed)
    else:
        if computers_answer == answer:
            await ctx.reply(f"¯\_(ツ)_/¯ we tied lol we both picked **{answer}**")
        if computers_answer == "rock":
            if answer == "paper":
                await ctx.reply(f"You won! I have picked **{computers_answer}** and you picked **{answer}** ¯\_(ツ)_/¯ you are pro")
        if computers_answer == "paper":
            if answer == "rock":
                await ctx.reply(
                    f"I WIN HAHAHAHAHA! I have picked **{computers_answer}** and you picked **{answer}** ¯\_(ツ)_/¯ you are pro")
        if computers_answer == "scissors":
            if answer == "rock":
                await ctx.reply(f"You won! I have picked **{computers_answer}** and you picked **{answer}** ¯\_(ツ)_/¯ you are pro")
        if computers_answer == "rock":
            if answer == "scissors":
                await ctx.reply(f"You won! I have picked **{computers_answer}** and you picked **{answer}** ¯\_(ツ)_/¯ you are pro")
        if computers_answer == "rock":
            if answer == "scissors":
                await ctx.reply(f"I WIN HAHAHAHAHA! I have picked **{computers_answer}** and you picked **{answer}** ¯\_(ツ)_/¯ you are pro")
        if computers_answer == "paper":
            if answer == "scissors":
                await ctx.reply(f"You won! I have picked **{computers_answer}** and you picked **{answer}** ¯\_(ツ)_/¯ you are pro")
        if computers_answer == "scissors":
            if answer == "paper":
                await ctx.reply(f"I WIN HAHAHAHAHA! I have picked **{computers_answer}** and you picked **{answer}** ¯\_(ツ)_/¯ you are pro")

@client.command()
@commands.has_permissions(administrator=True)
async def dmall(ctx, *, args=None):
    if args != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(args)
            except:
                print("dmall didnt work lol")
    else:
        embed = nextcord.Embed(title="⚠️Error⚠️", color=nextcord.Color.red())
        embed.add_field(name="ERROR:", value="Error Code: 7")
        return await ctx.reply(embed=embed)


@client.command()
async def vodka(ctx):
    await ctx.reply(f"{ctx.author.mention} just drank some yummy vodka, COMRADE VODKA = GOOD")

client.run("youthought;)")