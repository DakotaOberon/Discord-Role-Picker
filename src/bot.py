from discord.ext import commands
from discord_ui.client import UI
from discord_ui.receive import SelectInteraction

from ColorPicker.ColorPicker import ColorPicker, ColorSelect
from creds import TOKEN

client = commands.Bot('Gildenstead Guide')
ui = UI(client)

@client.event
async def on_ready():
    print('{0.user} has logged in'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower().replace(' ', '') == 'initcolorpicker':
        color_picker = ColorPicker(message.guild)
        await color_picker.create_roles()
        await color_picker.create_vote_post(message.channel, client)

        return

@client.listen()
async def on_select(menu: SelectInteraction):
    color_select = ColorSelect(menu.author, menu.selected_options[0])
    await color_select.process()
    msg = await menu.respond(f'{menu.author.display_name} selected {menu.selected_options[0]._label}')
    await msg.delete(delay=5.0)

client.run(TOKEN)
