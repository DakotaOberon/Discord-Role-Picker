import discord

from creds import TOKEN

client = discord.Client()

@client.event
async def on_ready():
    print('{0.user} has logged in'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

client.run(TOKEN)
