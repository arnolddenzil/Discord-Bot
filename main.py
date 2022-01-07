import discord
from discord.ext import commands
from sqlalchemy import create_engine, MetaData, Table, Column, String
from sqlalchemy.orm import sessionmaker
import os


#connecting to database 'gtech-learn'
engine = create_engine('sqlite:///gtech-learn.db', echo=True)
meta = MetaData()
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.connect()

registery = Table('registery', meta, Column('name', String))


#client is the bot
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


#When logged in
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


#When the bot gets its own message
@client.event
async def on_message(message):
    if message.author == client.user:
        print("it is you who messaged")
        return
    await client.process_commands(message)


#Welcoming new member joined to the server in the welcome channel
@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(928513156102381659)
    print("A member has joind the channel")
    await welcome_channel.send(f"Welcome {member}")


#Gives a reaction notification to the reaction channel
@client.event
async def on_reaction_add(reaction, user):
    print("on reaction event ")
    reaction_channel = client.get_channel(928557338342854697)
    await reaction_channel.send(f"<{user.name}> gave reaction to <{reaction.message.author}>")


#Registers name to the database(i.e in the table 'registery' inside the database)
@client.command()
async def register(ctx, name_to_register):
    result = session.query(registery).filter_by(name=name_to_register).count()
    if result == 0:
        ins = registery.insert().values(name=name_to_register)
        conn.execute(ins)
        await ctx.send(f"The name is entered to the database")
    else:
        await ctx.send(f"The name is already entered")


#Returns the names registered
@client.command()
async def names(ctx):
    result = session.query(registery)
    no_of_records = result.count()
    if no_of_records == 0:
        await ctx.send(f"No name is registered.\n"
                           f"Use '!register <name>' to add a name")
    else:
        await ctx.send(f"Registered names are : ")
        for row in result.all():
            await ctx.send(row.name)


#Assigns roles to user
@client.command()
async def role(ctx, role_to_assign):
    print(role_to_assign, type(role_to_assign))
    await ctx.guild.create_role(name=role_to_assign)
    var = discord.utils.get(ctx.guild.roles, name=role_to_assign)
    await ctx.author.add_roles(var)
    await ctx.channel.send(f"<{ctx.author}> has been assigned the role <{role_to_assign}>")


client.run(os.environ['bot_token'])

