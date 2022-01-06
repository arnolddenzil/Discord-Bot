import discord
import requests
import json
import random
from discord.ext import commands
from sqlalchemy import create_engine, MetaData, Table, Column, String
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///gtech-lean.db', echo=True)
meta = MetaData()
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.connect()

registery = Table('registery', meta, Column('name', String))




intents = discord.Intents.default()
intents.members = True

# ----client is the bot----
# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"
]


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    channel = message.channel

    if message.author == client.user:
        print("it is you who messaged")
        return

    if message.content.startswith('$hello'):
        welcome_channel = client.get_channel(928513156102381659)
        await channel.send('Hello!')
        await welcome_channel.send("$hello command responded")

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await channel.send(quote)

    if message.content.startswith('!role'):
        role_to_assign = message.content.split(" ")[1]
        print(role_to_assign, type(role_to_assign))
        await message.guild.create_role(name=role_to_assign)
        var = discord.utils.get(message.guild.roles, name=role_to_assign)
        # member.add_role(var)
        await message.author.add_roles(var)
        await channel.send(f"<{message.author}> has been assigned the role <{role_to_assign}>")

    if message.content.startswith('!register'):
        name_to_enter = message.content.split(" ")[1]
        result = session.query(registery).filter_by(name=name_to_enter).count()
        if result == 0:
            ins = registery.insert().values(name=name_to_enter)
            conn.execute(ins)
            await channel.send(f"The name is entered to the database")
        else:
            await channel.send(f"The name is already entered")



    if message.content.startswith('!names'):
        result = session.query(registery)
        no_of_records = result.count()
        if no_of_records == 0:
            await channel.send(f"The database is not created if atleast one name is registered.\n"
                                       f"Use '!register <name>' to add a name")
        else:
            await channel.send(f"Registered names are : ")
            for row in result.all():
                await channel.send(row.name)



    msg = message.content

    if any(word in msg for word in sad_words):
        await channel.send(random.choice(starter_encouragements))

@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(928513156102381659)
    print("A member has joind the channel")
    await welcome_channel.send(f"Welcome {member}")

@client.event
async def on_reaction_add(reaction, user):
    print("on reaction event ")
    reaction_channel = client.get_channel(928557338342854697)
    await reaction_channel.send(f"<{user.name}> gave reaction to <{reaction.message.author}>")


client.run("Token is added here")
