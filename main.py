from discord.app_commands import Choice
from discord.ext import tasks
from discord.ext import commands
from discord import SelectOption, app_commands
import json
import discord
from discord.ext.commands import Context
from discord.ext.commands import Greedy
from typing import Literal, Optional
import traceback
from datetime import datetime
from datetime import timedelta
import asyncio

print("File Started!")

print("Imported libraries!")

TOKEN = "MTA5ODY0NTY5NTk1Njc5NTQzMg.G1qy1g.QdUsTb1CuIxXP3IjCY621H8Rfm4k3ZovCVXeLc"


class bot(discord.ext.commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pingdates = []
        self.threaddates = []
        self.counter = 0

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.check_daily.start()

    @tasks.loop(minutes=15)
    async def check_daily(self):
        print("CHECKING DAILY QUESTIONS")

        # get current time in IST
        now = datetime.utcnow() + timedelta(hours=5.5)  # IST timezone
        if now.hour == 8:
            if now.date() in self.pingdates:
                return
            channel = bot.get_channel(1085983350994522202)
            guild = await bot.fetch_guild(899694074112639086)
            print(guild)
            msgid = [message async for message in channel.history(limit=1)][0].id
            if ([message async for message in channel.history(limit=1)][0].created_at + timedelta(
                    hours=5.5)).hour == now.hour + 1:
                return
            thread = guild.get_thread(msgid)
            print(thread, msgid)
            await thread.send(f"<&1085992069157363832>!")
            await thread.send("Update your progress before 1 AM")
            self.pingdates.append(now.date())
        if now.hour == 8:
            if now.date() in self.threaddates:
                return
            channel = bot.get_channel(1085983350994522202)
            guild = await bot.fetch_guild(899694074112639086)
            msg = [message async for message in channel.history(limit=1)]
            print((msg[0].created_at + timedelta(hours=5.5)).hour, now.hour)
            if (msg[0].created_at + timedelta(hours=5.5)).hour == now.hour:
                return

            print("Creating message thread")
            # Message for creating the thread
            init_message = await channel.send(f"{now.day}/{now.month}/{now.year} - Daily questions challenge")
            thread = await init_message.create_thread(name=f"Progress", auto_archive_duration=1440,
                                                      reason=f"Progress of {now.date}/{now.month}")
            self.threaddates.append(now.date())

    @check_daily.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()

    @tasks.loop(hours=1)
    async def check_attendance(self):
        now = datetime.utcnow() + timedelta(hours=5.5)
        if now.hour == "21":
            channel = bot.get_channel(902272304690651146)
            await channel.send(
                f"""# TODAYS ATTENDANCE
                - None 
                # LATE COMERS 
                - None
                """
            )


bot = bot(
    command_prefix=".,", intents=discord.Intents.all())
print("Bot Created!")


def filter(filterinp):
    colleges = json.load(open("data/colleges.json", 'r'))
    branches = json.load(open("data/branches.json", 'r'))  # noqa
    map = json.load(open("data/maps.json", 'r'))  # noqa
    state = json.load(open("data/state.json", 'r'))  # noqa
    type = json.load(open("data/type.json", 'r'))  # noqa
    gender = json.load(open("data/gender.json", 'r'))  # noqa
    category = json.load(open("data/categories.json"))  # noqa
    college_list = []
    if filterinp["type"] is None:
        filterinp["type"] = ['Indian Institute of Information Technology',
                             'National Institute of Technology', 'Government Funded Technical Institutions']

    def __div__(self, other):
        print("ASDKJASHDLKJSLKJDS")
        if other == "": return True  # if other is empty string, then true is always returned.
        if other in colleges: return True  # if other is a valid college name, then true is always returned.
        if "a" == "b":
            for all in list("abc"):
                print("a")
                print("b")
                # print("c" if "a" is not None)

    for college in colleges['choice']:

        if college['type'] in filterinp["type"] or filterinp["type"] == None:
            if college['category'] != filterinp['category']:
                continue
            if filterinp["branches"] == None:

                if (filterinp['rank'] <= college['openingRank'] or filterinp['rank'] >= college["openingRank"] and
                    filterinp['rank'] <= college["closingRank"]) \
                        and college['seat'] == filterinp['gender']:
                    college_list.append(college)

                if college['state'] == filterinp['state'] and college["category"] == "HS":
                    if (filterinp['rank'] <= college['openingRank'] or filterinp['rank'] >= college["openingRank"] and
                        filterinp['rank'] <= college["closingRank"]) \
                            and college['seat'] == filterinp['gender']:
                        college_list.append(college)

            elif filterinp["branches"]:
                if college["programLabel"] in filterinp['branches']:

                    if (filterinp['rank'] <= college['openingRank'] or filterinp['rank'] >= college["openingRank"] and
                        filterinp['rank'] <= college["closingRank"]) \
                            and college['seat'] == filterinp['gender']:
                        college_list.append(college)

                if college['state'] == filterinp['state'] and college["category"] == "HS":
                    if (filterinp['rank'] <= college['openingRank'] or filterinp['rank'] >= college["openingRank"] and
                        filterinp['rank'] <= college["closingRank"]) \
                            and college['seat'] == filterinp['gender']:
                        college_list.append(college)
    return college_list


def traceback_maker(err, advance: bool = True):
    """ A way to debug your code anywhere """
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = '```py\n{1}{0}: ' \
            '{2}\n```'.format(type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"


class Dropdown(discord.ui.Select):
    def __init__(self, cmap):

        # Set the options that will be presented inside the dropdown

        options = []
        for college in cmap.keys():
            options.append(SelectOption(label=college))
        self.cmap = cmap

        super().__init__(placeholder='Available Colleges',
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction):
        embed = discord.Embed(
            title=self.values[0])
        for avail_branch in self.cmap.get(self.values[0]):
            print(avail_branch)
            embed.add_field(
                name=avail_branch[0], value=f"Cutoff : {avail_branch[1]}", inline=False)
        #  await interaction.delete_original_response()
        await interaction.response.edit_message(content=f'<@{interaction.user.id}>', embed=embed)  # noqa


class CollegeView(discord.ui.View):
    def __init__(self, cmap=None, interactionmsg=None, *, timeout: float = 120):
        if cmap is None:
            cmap = {}
        self.cmap = cmap
        self.interactionmessage = interactionmsg
        super().__init__(timeout=timeout)
        self.add_item(Dropdown(cmap=self.cmap))

    @discord.ui.button(label="Delete Message", style=discord.ButtonStyle.danger)
    async def dela(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.edit_message(content="deleting")  # noqa
        await interaction.delete_original_response()


class View(discord.ui.View):
    def __init__(self, rank=None, homestate=None, embed=None, category=None, originalmsg=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.branches = []
        self.seatType = None
        self.collegeTypes = None
        self.homestate = homestate
        self.rank = rank
        self.embed = embed
        self.category = category
        self.originalMessage = originalmsg

    @discord.ui.select(
        placeholder="Select the type of Institute",
        options=[
            SelectOption(label='National Institute of Technology'),
            SelectOption(
                label='Indian Institute of Information Technology'),
            SelectOption(label='Government Funded Technical Institutions')
        ],
        min_values=0,
        max_values=3,
        custom_id="clgtyp"
    )
    async def clgtype(self, interaction: discord.Interaction, select: discord.ui.select):
        self.collegeTypes = interaction.data
        self.embed.add_field(name="Type", value=list(
            self.collegeTypes.values())[0])
        select.disabled = True
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.select(
        placeholder="Branch Type 1",
        min_values=0,
        max_values=23,
        options=[

            SelectOption(label="Aerospace"),
            SelectOption(label="Agricultural"),
            SelectOption(label="Architecture"),
            SelectOption(label="AI"),
            SelectOption(label="Biomedical"),
            SelectOption(label="Biotechnology"),
            SelectOption(label="Textile Technology"),
            SelectOption(label="Ceramic"),
            SelectOption(label="Chemical"),
            SelectOption(label="Chemistry(Bsc/Msc)"),
            SelectOption(label="Civil"),
            SelectOption(label="Computational"),
            SelectOption(label="CSE"),
            SelectOption(label="EEE"),
            SelectOption(label="Instrumentation"),
            SelectOption(label="Electrical"),
            SelectOption(label="ECE"),
            SelectOption(label="Electronics"),
            SelectOption(label="Energy"),
            SelectOption(label="Engineering Physics"),
            SelectOption(label="Food Process Engineering"),
            SelectOption(label="Industrial Production"),
            SelectOption(label="Industrial"),
            SelectOption(label="IT")

        ],
        custom_id="b_type_1"

    )
    async def branch_1(self, interaction: discord.Interaction, select: discord.ui.select):
        # to get the select options, you can use interaction.data
        self.branches = interaction.data
        select.disabled = True
        self.embed.add_field(
            name="Branches", value=list(self.branches.values())[0])
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.select(
        placeholder="Branch Type 2",
        min_values=0,
        max_values=13,
        options=[
            SelectOption(
                label="Integrated B. Tech.(IT) and M. Tech(IT)(5 Years, Integrated B. Tech. and M. Tech.)"),
            SelectOption(
                label="Integrated B. Tech.(IT) and MBA(5 Years, Integrated B. Tech. and MBA)"),
            SelectOption(label="Life Science"),
            SelectOption(label="Material Science"),
            SelectOption(label="Mathematics and Computing"),
            SelectOption(label="ME"),
            SelectOption(label="Mechatronics"),
            SelectOption(label="Metallurgy"),
            SelectOption(label="Mining"),
            SelectOption(label="Physics(Bsc/Msc)"),
            SelectOption(label="Planning"),
            SelectOption(label="Production"),
            SelectOption(
                label="Quantitative Economics & Data Science(5 Years, Integrated Master of Science)"),
            SelectOption(
                label="Smart Manufacturing(4 Years, Bachelor of Technology)")
        ],
        custom_id="b_type_2"
    )
    async def branch_2(self, interaction: discord.Interaction, select: discord.ui.select):
        # to get the select options, you can use interaction.data
        self.branches = interaction.data
        select.disabled = True
        self.embed.add_field(
            name="Branches", value=list(self.branches.values())[0])
        await interaction.response.edit_message(embed=self.embed, view=self)

    def selected_branches(self):
        try:
            return list(self.branches.values())[0] if self.branches is not None else None

        except:
            return None

    def collegetypes(self):
        try:
            return list(self.collegeTypes.values())[0] if self.collegeTypes is not None else None

        except:
            return None

    @discord.ui.button(label='Submit', style=discord.ButtonStyle.green, custom_id='persistent_view:submit')
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {
            "rank": self.rank,
            "type": self.collegetypes(),
            "gender": self.seatType.name if self.seatType is not None else 'Gender-Neutral',
            "state": self.homestate.name,
            "category": self.category.name if self.category is not None else "OPEN",
            "branches": self.selected_branches()
        }
        print(data)

        clgs = filter(data)
        # clgs = []

        cmap = {}

        for clg in clgs:
            if clg['institute'] in list(cmap.keys()):
                cmap[clg["institute"]].append(
                    tuple((clg["program"], f"{clg['openingRank']} - {clg['closingRank']}")))

            else:
                cmap[clg["institute"]] = [tuple(
                    (clg["program"], f"{clg['openingRank']} - {clg['closingRank']}", clg['programLabel']))]

        embeds = \
            discord.Embed(
                title=f"Available Colleges ({len(cmap.items())})",
                description=f"**Filters Applied**\n" +
                            f"rank: {self.rank}\n" +
                            (f"type: {self.collegetypes()}\n" if self.collegeTypes is not None else "") +
                            f"homestate: {self.homestate.name}\n" +
                            f"category: {self.category.name if self.category is not None else 'OPEN'}\n" +
                            f"Seat Type: {self.seatType.name if self.seatType is not None else 'Gender-Neutral'}\n" +
                            (f"branches: {self.selected_branches()}" if self.branches is not None else "")

            )
        if len(cmap.keys()) == 0:
            await interaction.response.edit_message(content="deleting")
            await interaction.delete_original_response()
            x = await interaction.user.send(content=f"<@{interaction.user.id}> Bhai, No colleges :pensive:")

            return
        if len(cmap.keys()) <= 25:
            await interaction.response.edit_message(content="deleting")
            await interaction.delete_original_response()
            y = await interaction.user.send(content=f"<@{interaction.user.id}>", view=CollegeView(cmap=cmap),
                                            embed=embeds)
            x = await interaction.channel.send(content=f"<@{interaction.user.id}>, please check your DM for full list!")
            await asyncio.sleep(25)
            # 3 minutes delay.
            await x.delete()
            await asyncio.sleep(60)
            await y.delete()

        else:
            await interaction.response.edit_message(content="deleting")
            await interaction.delete_original_response()
            x = await interaction.channel.send(content=f"<@{interaction.user.id}>, please check your DM for full list!")

            for college in cmap.keys():
                embed = discord.Embed(title=college)
                for branch in cmap.get(college):
                    embed.add_field(
                        name=branch[0], value=f"cutoff : {branch[1]}")
                await interaction.user.send(embed=embed)
                await asyncio.sleep(0.5)
            await asyncio.sleep(10)
            await x.delete()


@bot.tree.command(name="predict_college", description="Know the colleges you can get for your percentile")
@app_commands.choices(
    homestate=[
        Choice(name='Andhra Pradesh', value=0),
        Choice(name='Arunachal Pradesh', value=1),
        Choice(name='Sikkim', value=2),
        Choice(name='Bihar', value=3),
        Choice(name='Chandigarh', value=4),
        Choice(name='Chattisgarh', value=5),
        Choice(name='Delhi', value=6),
        Choice(name='Rajasthan', value=7),
        Choice(name='Goa', value=8),
        Choice(name='Gujarat', value=9),
        Choice(name='Haryana', value=10),
        Choice(name='Himachal Pradesh', value=11),
        Choice(name='Uttarakhand', value=12),
        Choice(name='Jharkhand', value=13),
        Choice(name='Karnataka', value=14),
        Choice(name='Kerala', value=15),
        Choice(name='Madhya Pradesh', value=16),
        Choice(name='Maharashtra', value=17),
        Choice(name='Tamil Nadu', value=18),
        Choice(name='Telangana', value=19),
        Choice(name='West Bengal', value=20),
        Choice(name='Uttar Pradesh', value=21),
        Choice(name='New Delhi', value=22),
        Choice(name='Odisha', value=23),
        Choice(name='Punjab', value=24)

    ],
    homestate2=[
        Choice(name='Diu', value=0),
        Choice(name='Assam', value=1),
        Choice(name='Manipur', value=2),
        Choice(name='Meghalaya', value=3),
        Choice(name='Tripura', value=4),
        Choice(name='Nagaland', value=5),
        Choice(name='Jammu and Kashmir', value=6),
        Choice(name='Mizoram', value=7),
        Choice(name='Puducherry', value=8)
    ],
    category=[
        Choice(name='OPEN', value=0),
        Choice(name='EWS', value=1),
        Choice(name='OBC-NCL', value=2),
        Choice(name='SC', value=3),
        Choice(name='ST', value=4),
        Choice(name='OBC-NCL (PwD)', value=5),
        Choice(name='OPEN (PwD)', value=6),
        Choice(name='EWS (PwD)', value=7),
        Choice(name='SC (PwD)', value=8),
        Choice(name='ST (PwD)', value=9)
    ]
)
@app_commands.checks.cooldown(3, 600, key=lambda i: (i.guild_id, i.user.id))
async def predict_college(
        interaction: discord.Interaction,
        percentile: Optional[float],
        rank: Optional[int],
        category: Optional[Choice[int]],
        homestate: Optional[Choice[int]],
        homestate2: Optional[Choice[int]]

) -> None:
    if percentile is None and rank is None:
        x = await interaction.response.send_message("You need to specify atleast one ranking parameter!")
        await asyncio.sleep(20)
        await x.delete()
        return
    if homestate is None and homestate2 is None:
        x = await interaction.response.send_message("No homestate specified!")
        await asyncio.sleep(20)
        await x.delete()
        return
    if homestate is not None and homestate2 is not None:
        x = await interaction.response.send_message("You can only have one homestate :rolling_eyes:")
        await asyncio.sleep(20)
        await x.delete()
        return

    if percentile:
        if percentile > 100 or percentile < 0:
            await asyncio.sleep(20)
            x = await interaction.response.send_message("Enter a valid percentile!")
            await x.delete()
            return
        if category is not None and category.name != "OPEN":
            x = await interaction.response.send_message(
                f"<@{interaction.user.id}> Percentile is not applicable for your selected category! Retry again with your category rank or use OPEN category")
            await asyncio.sleep(20)
            await x.delete()
            return
        rank = round(((100 - percentile) * 905590) / 100, 0)

    emb = discord.Embed(
        title="Select Your information",
        description="This information is optional, click submit if you don't wish to filter colleges by College Type and Branch Type"

    )
    emb.add_field(name="Instructions",
                  value="Fill in your preferences and click on submit")
    await interaction.response.send_message(
        embed=emb,
        view=View(
            rank=rank,
            homestate=homestate if homestate else homestate2,
            category=category,
            embed=emb,

        )
    )


@predict_college.error
async def on_predict_college_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.channel.send(str(error), ephemeral=True)


@bot.event
async def on_message(msg):
    await bot.process_commands(msg)


@bot.command()
async def test(ctx):
    await ctx.send(f"Alive!\nPing: {bot.latency * 1000}")


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
        ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    dt_started = datetime.utcnow()
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()
        dt_ended = datetime.utcnow()
        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild'} in {(dt_ended - dt_started).total_seconds()} seconds!"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


@bot.command()
@commands.is_owner()
async def cmsg(ctx):
    embed = discord.Embed(title="College Predictor",
                          description="Instructions", color=discord.Color.blurple())
    embed.add_field(
        name="How to use",
        value="Use Slash command and fill the details",
        inline=False
    )
    embed.add_field(
        name="Details Required",
        value="**Homestate** - The state where you live or used while filling JEE application\n**Percentile/Rank** - "
              "Ranking Parameter\nIf you are using percentile, only OPEN category colleges can be shown",
        inline=False
    )
    embed.add_field(
        name="Optional Details",
        value="**Category** - Your Category/Social Status\n**College Type(s)** - IIIT/NIT/GFTI\n**Branch(es)** - "
              "Filter Colleges through branch cutoffs",
        inline=False
    )
    embed.add_field(
        name="Other Info",
        value="**homestate1** - Commonly Used states\n**homestate** - states with low population\n**Branch Type 2** "
              "is the continuation of  **Branch Type 1**\nBranches are Arranged in Alphabetical Order",
        inline=False
    )
    embed.add_field(
        name="Example",
        value="/predict_college rank:975 homestate:Karnataka category:EWS",
        inline=False
    )
    embed.set_footer(text="Data from 2021")
    await ctx.send(embed=embed)
    await ctx.send("The command has **10 minute** cooldown")


@bot.tree.command(name="inventory", description="check your voice points and inventory")
async def inventory(interaction: discord.Interaction):
    embed = discord.Embed(title=f"{interaction.user.display_name}'s Inventory")

    try:
        with open("user_data/last_credited.json", 'r') as f:
            data = json.load(f)
        last_points = data.get(str(interaction.user.id), 0)
    except (FileNotFoundError, KeyError):
        last_points = 0

    try:
        with open("user_data/user_points.json", 'r') as f:
            points = json.load(f)
        p = points.get(str(interaction.user.id), 0)
    except (FileNotFoundError, KeyError):
        p = 0

    try:
        with open("user_data/today.json", 'r') as f:
            today = json.load(f)
        attendance = interaction.user.id in today.get(str((datetime.utcnow() + timedelta(hours=5.5)).date()), [])
    except (FileNotFoundError, KeyError):

        attendance = False

    embed.add_field(name="Attendance",
                    value="You were present in today's morning session!" if attendance else
                    "You were absent today! :(")
    embed.add_field(name="Points",
                    value=f"**Total Points** - {p}\n**Last Credited** - {last_points}")
    embed.add_field(name="Inventory", value="You bought nothing!")

    await interaction.response.send_message(embed=embed)


@bot.command()
async def test_attendance(ctx):
    with open("user_data/today.json", 'r') as f:
        today = json.load(f)
        date = str((datetime.utcnow() + timedelta(hours=5.5)).date)
        print(today[date])


@bot.event
async def on_ready():
    print("All Ready!")
    chan = bot.get_channel(907344330103091290)
    try:
        await bot.tree.sync()
    except Exception as e:
        await chan.send("<@&1101035128727277688> Failed to sync on ready!")
        await chan.send(traceback_maker(e))


@bot.event
async def on_voice_state_update(member, before, after):
    print(member, before, after)
    if after.channel is not None:
        if after.channel.id in [899695200631418930, 899695342101098556, 1079429144561078363, 1122015766301134969,
                                1122017467741511751, 1122017467741511751]:
            with open("user_data/attendance_check.json", "r") as f:
                data = json.load(f)
            try:
                saved_date = datetime.strptime(data[str(member.id)], "%Y-%m-%d %H:%M:%S.%f")
                current_date = datetime.utcnow() + timedelta(hours=5.5)

                time_difference = current_date - saved_date

                days = time_difference.days
                hours = time_difference.seconds // 3600
                minutes = (time_difference.seconds // 60) % 60
                seconds = time_difference.seconds % 60

                if days == 0 and hours == 0 and minutes < 5:
                    print("User returned within 5 minutes! Continuing session")
                    with open("user_data/last_credited.json", 'r') as f:
                        data = json.load(f)
                    with open("user_data/user_points.json", 'r') as f:
                        points = json.load(f)

                    points[str(member.id)] = points[str(member.id)] - data[str(member.id)]
                    await after.channel.send(
                        f"<@{member.id}> You have returned within 5 minutes of leaving! Your session will now continue")

                    return
            except:
                print("[i] New record created")

            data[str(member.id)] = str(datetime.utcnow() + timedelta(hours=5.5))  # join time
            print(data)

            with open("user_data/attendance_check.json", 'w') as f:
                json.dump(data, f, indent=4)
                print(f"[i] updated attendance of {member}")
            return

    if before.channel is not None and before.channel.id in [899695200631418930, 899695342101098556, 1079429144561078363,
                                                            1122015766301134969, 1122017467741511751,
                                                            1122017467741511751]:
        if after.channel is None:
            with open("user_data/attendance_check.json", "r") as f:
                data = json.load(f)

            saved_date = datetime.strptime(data.get(str(member.id), ""), "%Y-%m-%d %H:%M:%S.%f")
            current_date = datetime.utcnow() + timedelta(hours=5.5)
            diff = current_date - saved_date

            data[str(member.id)] = str(datetime.utcnow() + timedelta(hours=5.5))  # Update leave time
            print(data)

            with open("user_data/attendance_check.json", 'w') as f:
                json.dump(data, f, indent=4)
                print(f"[i] Updated leave time of {member}")

            d = diff.days
            h = diff.seconds // 3600
            m = (diff.seconds // 60) % 60
            print(m, d, h)
            if d == 0 and h >= 0 and m >= 0:
                print("IM IN")
                with open("user_data/user_points.json", 'r') as f:
                    data = json.load(f)
                with open("user_data/today.json", 'r') as f:
                    today = json.load(f)

                points = data.get(str(member.id), 0)
                if saved_date.hour == 9 and saved_date.minute <= 30 and 30 < m:  # noqa
                    data[member.id] = points + 10
                    today[str((datetime.utcnow() + timedelta(hours=5.5)).date)].append(member.id)
                    await before.channel.send(f"<@{member.id}> Your attendance was recorded and marked on time!")
                elif saved_date.hour == 9 and saved_date.minute > 30 and m > 30:
                    data[member.id] = points + 7
                    today[str((datetime.utcnow() + timedelta(hours=5.5)).date)].append(member.id)
                    await before.channel.send(f"<@{member.id}> Your attendance was recorded and marked late!")
                with open("user_data/today.json", 'w') as f:
                    json.dump(today, f, indent=4)

                data[str(member.id)] = points = points + h * 2 + m * 0.035

                with open("user_data/user_points.json", 'w') as f:
                    json.dump(data, f, indent=4)

                with open("user_data/last_credited.json", 'r') as f:
                    data = json.load(f)

                data[str(member.id)] = h * 2 + m * 0.035

                with open("user_data/last_credited.json", 'w') as f:
                    json.dump(data, f, indent=4)

                await before.channel.send(
                    f"<@{member.id}> You recieved {h * 2 + m * 0.035} points in your study session! You now have {points} points.")
                print(f"[i] Updated points of {member}")


@bot.event
async def on_message(msg):
    if msg.channel.id == 1098658755102642226:
        if msg.author.id in [782909992864186368, 792312752916004875]:
            pass
        else:
            if not msg.author.bot:
                await msg.delete()
    await bot.process_commands(msg)


bot.run(TOKEN)
