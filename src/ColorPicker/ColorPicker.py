from creds import EMOJI_SERVER
from discord import Colour
from discord_ui import SelectMenu, SelectOption


COLORS = {
    '00A22B': { 'color': Colour(0x00A22B), 'name': 'Green Haze' },
    '8F9100': { 'color': Colour(0x8F9100), 'name': 'Olive' },
    '009D8C': { 'color': Colour(0x009D8C), 'name': 'Persian Green' },
    '0099B1': { 'color': Colour(0x0099B1), 'name': 'Bondi Blue' },
    '9473FF': { 'color': Colour(0x9473FF), 'name': 'Dark Heliotrope' },
    'BD7E00': { 'color': Colour(0xBD7E00), 'name': 'Pirate Gold' },
    'CB52FF': { 'color': Colour(0xCB52FF), 'name': 'Bright Heliotrope' },
    'FF3E70': { 'color': Colour(0xFF3E70), 'name': 'Radical Red' },
    'FF454A': { 'color': Colour(0xFF454A), 'name': 'Coral Red' }
}

class ColorPicker:
    def __init__(self, guild):
        self.guild = guild

    async def create_roles(self):
        '''Create roles in guild'''
        roles, r_len = await self.get_roles()
        for color in COLORS:
            # If role does not exist on server
            if not self.check_role(roles, color):
                # Create role
                role = await self.guild.create_role(name=color, colour=COLORS[color]['color'])
                # Place role at top
                await role.edit(reason=None, position=r_len - 1)

    async def get_roles(self):
        '''Get roles from discord'''
        roles = await self.guild.fetch_roles()
        roles_length = len(roles)
        return (roles, roles_length)

    def check_role(self, roles, role_name):
        '''Check if a role with given name exists in a guild'''
        for role in roles:
            if role_name == role.name:
                return True
        return False
    
    def get_role_id(self, roles, role_name):
        '''Get the id of a role'''
        for role in roles:
            if role_name == role.name:
                return role.id
        return None

    async def create_vote_post(self, channel, client=None):
        '''Create post that allows users to select a role'''
        menu = SelectMenu(
            options=self.get_options(client)
        )
        await channel.send('Pick a Color Role', components=[menu])

    def get_options(self, client=None):
        '''Returns a list of discord_ui options'''
        # Figure out how to set the emoji properly
        options = []
        for color in COLORS:
            values = color, COLORS[color]['name'], color
            emoji = self.get_emoji(color, False, client)
            options.append(SelectOption(*values, emoji=emoji))

        return options

    def get_emoji(self, name, use_current_server=False, client=None):
        '''Return emoji if it exists'''
        guild = self.guild if use_current_server else client.get_guild(EMOJI_SERVER)

        for emote in guild.emojis:
            if emote.name == name:
                return emote
        return None

class ColorSelect:
    def __init__(self, user, selected):
        self.user = user
        self.selected = selected

    async def remove_color_roles(self):
        roles = self.user.roles
        for role in roles:
            if role.name in COLORS:
                await self.user.remove_roles(role)
        return self

    async def add_color_role(self, role):
        await self.user.add_roles(role)
        return self
    
    def get_role(self):
        '''Get the role for selected color'''
        roles = self.user.guild.roles
        for role in roles:
            if self.selected.value == role.name:
                return role
        return None

    async def process(self):
        await self.remove_color_roles()
        role = self.get_role()
        if role is not None:
            await self.add_color_role(role)
            print('Added role successfully')
        else:
            print('Role did not exist', self.selected)
