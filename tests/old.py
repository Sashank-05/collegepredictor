import asyncio
import datetime
import traceback
from typing import Literal, Optional
from discord.ext.commands import Greedy
from discord.ext.commands import Context
import discord
import json
from discord import SelectOption, app_commands
from discord.ext import commands
from discord.app_commands import Choice
import Paginator

colleges = json.load(open("colleges.json", 'r'))
branches = json.load(open("branches.json", 'r'))
map = json.load(open("maps.json", 'r'))
state = json.load(open("state.json", 'r'))
type = json.load(open("type.json", 'r'))
gender = json.load(open("gender.json", 'r'))
category = json.load(open("categories.json"))


def traceback_maker(err, advance: bool = True):
    """ A way to debug your code anywhere """
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = '```py\n{1}{0}: ' \
            '{2}\n```'.format(type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"


test_input = {
    "rank": 500,
    "type": type['choices'][0]['value'],  # => NIT
    "gender": gender['choices'][0]['value'],  # => gender-neutral
    "state": state['choices'][0]['value'],  # => AP
    "category": category['choices'][0]['value'],  # => OPEN
    "branches": [branches['choices'][0]["value"]]  # => aerospace
}

TOKEN = "MTA5ODY0NTY5NTk1Njc5NTQzMg.G1qy1g.QdUsTb1CuIxXP3IjCY621H8Rfm4k3ZovCVXeLc"


def filter(filterinp):
    college_list = []
    for college in colleges['choice']:

        if college['type'] == filterinp["type"] or filterinp["type"] == None:
            if college['category'] != filterinp['category']:
                continue
            if filterinp["branches"] == None:

                if (filterinp['rank'] < college['openingRank'] or filterinp['rank'] > college["openingRank"] and college["closingRank"]) \
                        and college['seat'] == filterinp['gender']:

                    college_list.append(college)

                if college['state'] == filterinp['state'] and college["category"] == "HS":
                    if (filterinp['rank'] < college['openingRank'] or filterinp['rank'] > college["openingRank"] and college["closingRank"]) \
                            and college['seat'] == filterinp['gender']:
                        college_list.append(college)

            elif filterinp["branches"]:
                if college["programLabel"] in filterinp['branches']:

                    if (filterinp['rank'] < college['openingRank'] or filterinp['rank'] > college["openingRank"] and college["closingRank"]) \
                            and college['seat'] == filterinp['gender']:
                        college_list.append(college)

                    if college['state'] == filterinp['state'] and college["category"] == "HS":
                        if (filterinp['rank'] < college['openingRank'] or filterinp['rank'] > college["openingRank"] and college["closingRank"]) \
                                and college['seat'] == filterinp['gender']:
                            college_list.append(college)
    return college_list


button_message = None

# print(filter(test_input))


bot = discord.ext.commands.AutoShardedBot(
    command_prefix="!cp ", intents=discord.Intents.all())


@bot.command()
async def test(ctx):
    await ctx.send(f"Alive!\nPing: {bot.latency*1000}")


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
        ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    dt_started = datetime.datetime.utcnow()
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
        dt_ended = datetime.datetime.utcnow()
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


@bot.event
async def on_ready():
    print("All Ready!")
    chan = bot.get_channel(1098658755102642226)
    m = await chan.send("Ready")
    try:
        await bot.tree.sync()
        m1 = await chan.send(f'Synced')
    except Exception as e:
        await chan.send("Failed to sync on ready!")
        await chan.send(traceback_maker(e))
    else:
        await m.delete()
        await m1.delete()

#    button_message = await bot.fetch_message()


fields = \
    """
**Percentile [choice]** - Your overall NTA score
**Rank [choice]** - Your OPEN/SC/ST/OBC/EWS/PWD Category Rank
**Type of Seat** - Your Gender
**Home State** - The state you live in according to application
**Category** - OPEN/SC/ST/OBC/ETC... 
**Branch** - Your branch preference (multi-options)
"""


@bot.command()
async def create_message(ctx):
    m = await ctx.send("creating message please wait~")
    dt_started = datetime.datetime.utcnow()
    embed = discord.Embed(title="College Predictor",
                          description="Enter your details to know your college!")
    embed.add_field(
        name="USAGE", value="Fill the required details in to get your predicted college using percentile/rank")
    embed.add_field(name="Fields", value=fields, inline=False)
    await ctx.send(embed=embed)

    dt_ended = datetime.datetime.utcnow()
    x = await ctx.send(f"created and added message to cache in {(dt_ended - dt_started).total_seconds()} seconds!")
    await asyncio.sleep(2)
    await x.delete()
    await m.delete()

@bot.tree.command(name="predict_college", description="Know the colleges you can get for your percentile")
@app_commands.choices(
    seattype=[
        Choice(name=gender['choices'][0]['label'], value=1),
        Choice(name=gender['choices'][1]['label'], value=2)
    ],
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
    ],
    collegetype=[
        Choice(name='National Institute of Technology', value=0),
        Choice(name='Indian Institute of Information Technology', value=1),
        Choice(name='Government Funded Technical Institutions', value=2)
    ]
)
async def predict_college(
    interaction: discord.Interaction,
    percentile: Optional[float],
    rank: Optional[int],
    collegetype: Optional[Choice[int]],
    category: Optional[Choice[int]],
    seattype: Choice[int],
    homestate: Optional[Choice[int]],
    homestate2: Optional[Choice[int]]

) -> None:
    await interaction.response.defer()
    warnings = []
    abranches = None
    if percentile is None and rank is None:
        await interaction.response.send_message("You need to specify atleast one ranking parameter!")
        return
    if homestate is None and homestate2 is None:
        await interaction.response.send_message("No homestate specified!")
        return
    if percentile:
        if percentile > 100 or percentile < 0:
            await interaction.response.send_message("Enter a valid percentile!")
            return
        rank = round(((100-percentile) * 905590)/100, 0)

    data = {
        "rank": rank,
        "type": collegetype.name if collegetype is not None else None,
        "gender": seattype.name if seattype else gender['choices'][0]['value'],
        "state": homestate.name if homestate else homestate2.name,
        "category": category.name if category else "OPEN",
        "branches": []
    }
    print(data)

    clgs = filter(data)

    cmap = {}

    for clg in clgs:
        if clg in cmap.items():
            cmap[clg["institute"]].append(
                tuple((clg["program"], f"{clg['openingRank']} - {clg['closingRank']}")))
        else:
            cmap[clg["institute"]] = [clg['state'],
                                      tuple((clg["program"], f"{clg['openingRank']} - {clg['closingRank']}", clg['programLabel']))]
    embeds = [discord.Embed(title=f"Available Colleges ({len(cmap.items())})",
                            description=f"**Filters Applied**\nrank: {rank}\n" +
                            (f"type: {collegetype.name}\n" if collegetype is not None else "") +
                            f"homestate: {homestate.name if homestate else homestate2}\n" +
                            f"category: {category.name if category is not None else 'OPEN'}\n" +
                            # +
                            f"Seat Type: {seattype.name if seattype is not None else 'Gender-Neutral'}\n"
                            # (f"branches: {branches}" if branches is not None else "")

                            )]
    for college in cmap:
        vals = ""
        embed = discord.Embed(title=f"{college} - {cmap[college][0]}")
        del cmap[college][0]
        for p in cmap.get(college):
            embed.add_field(name=p[0], value=p[1]+"\n"+p[2])

        embeds.append(embed)



class FindCollege():
    def __init__(self):
        super().__init__()

        self.seattype = discord.ui.Select(
            
            placeholder=gender['choices'][0]['label'],
            options=[
                SelectOption(label=gender['choices']
                             [0]['label'], default=True),
                SelectOption(label=gender['choices'][1]['label'])]
        )

        self.collegetype = discord.ui.Select(
            options=[
                SelectOption(label='National Institute of Technology'),
                SelectOption(
                    label='Indian Institute of Information Technology'),
                SelectOption(label='Government Funded Technical Institutions')
            ],
            min_values=0,
            max_values=2
        )

        self.branch_type_1 = discord.ui.Select(
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

            ]
        )
        self.branch_type_2 = discord.ui.Select(
            placeholder="Branch Type 2",
            min_values=0,
            max_values=13,
            options=[
                SelectOption(label="Integrated B. Tech.(IT) and M. Tech(IT)(5 Years, Integrated B. Tech. and M. Tech.)"),
                SelectOption(label="Integrated B. Tech.(IT) and MBA(5 Years, Integrated B. Tech. and MBA)"),
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
                SelectOption(label="Quantitative Economics & Data Science(5 Years, Integrated Master of Science)"),
                SelectOption(label="Smart Manufacturing(4 Years, Bachelor of Technology)")
            ]

        )
        self.submit = discord.ui.Button(
            label="Submit"
        )

        self.add_item(self.collegetype)
        self.add_item(self.seattype)
        self.add_item(self.branch_type_1)
        self.add_item(self.branch_type_2)

    async def on_submit(self, interaction: discord.Interaction):
        
        await interaction.response.send_message(text=[self.collegetype, self.branch, self.seattype])


@bot.event
async def on_message(msg):
    await bot.process_commands(msg)

bot.run(TOKEN)
