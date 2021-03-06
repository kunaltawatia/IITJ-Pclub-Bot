import discord
import datetime
import sql


client = discord.Client()

symbol = '$'


@client.event
async def on_message(message):

    global symbol
    message.content = message.content.lower()
    if message.author == client.user:
        return

    # Sends a message with the current time
    if message.content.startswith(symbol + 'time'):
        await message.channel.send(str(datetime.datetime.now()))

    # Set a new symbol for the bot
    elif message.content.startswith(symbol + 'set'):
        content = message.content.split()
        if len(content) <= 1:
            await message.channel.send('Please enter a symbol. Usage "<current symbol>set <new symbol>"')
        else:
            symbol = content[1]
            await message.channel.send(f'The new symbol has been set to "{symbol}"')

    elif message.content.startswith(symbol + 'createdb'):

        guild = message.channel.guild
        await message.channel.send(f'There are {guild.member_count} members in the server. Creating a new table')

        # Initialise table here
        database = sql.Table('data', [
                             ('id', 'INT'), ('tot_msg', 'INT'), ('marg_msg', 'INT'), ('score', 'REAL')])

        for member in guild.members:
            # member.name has the string value
            # Add individual members here
            database.add_element(member.id)

    elif message.content.startswith(symbol + 'prune'):
        # This estimates how many members will be pruned
        pruned_members = await message.guild.estimate_pruned_members(7)
        await message.channel.send(f'{pruned_members} members were pruned due to inactivity.')
        # await message.guild.prune_members(7) # Actually pruning members

    elif message.content.startswith(symbol):  # A catchall.
        await message.channel.send('Hello This bot has been called v0.1.2')


client.run('')
