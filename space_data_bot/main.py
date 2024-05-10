"""
MIT License

Copyright (c) 2024 Alliance Stratégique des Étudiants du Spatial (ASTRES)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord
from discord import app_commands

from space_data_bot import envs, content, utils
from space_data_bot.api import SpaceDataApi


GUILD_ID = discord.Object(id=envs.GUILD_ID)


class SpaceDataClient(discord.Client):
    """The bot is initialized via a class that integrates it with Discord
    commands and makes its rights explicit.

    Commands are defined outside the class, but are linked to it via
    decorators.
    @client.tree.command(): Classic discord command
    @app_commands.describe() : Used to add documentation to command arguments.
    @app_commands.autocomplete(): Sets up auto-completion for a given argument.
    @app_commands.check(): Executes the command only if the answer is True.
    """
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to the guild.
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)


intents = discord.Intents.default()
client = SpaceDataClient(intents=intents)
space_data = SpaceDataApi()


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")


@client.tree.command()
async def help(interaction: discord.Interaction) -> None:
    """All the commands you can use with SpaceData Bot."""
    await interaction.response.send_message(content.help_message(),
                                            ephemeral=True)


"""
Endpoints commands accessible for everyone.
"""

# HUGE PROBLEM ! THE TEMPFILE IS ON THE SAME SERVER FOR EVERYONE
# Ask for a user specific token location when connecting ?


@client.tree.command()
@app_commands.describe(email="your email", password="your password")
async def connect(interaction: discord.Interaction,
                  email: str, password: str) -> None:
    """Allows a user to connect to their account;
    an access token and a refresh token are provided."""

    await interaction.response.defer(ephemeral=True)
    message = space_data.connect(email, password, id=interaction.user.id)
    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
@app_commands.describe(orgname="The name of the organization",
                       tags="tags=Agency or tags=Agency,Manufacturer")
async def orgnamepublic(
    interaction: discord.Interaction, orgname: str = "", tags: str = ""
) -> None:
    """Allows a user to get information about space organizations
    (50% of DB content)."""
    await interaction.response.defer(ephemeral=True)
    message = space_data.orgnamepublic(orgname, tags)
    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
@app_commands.describe(orgname="The name of the organization",
                       tags="tags=Agency or tags=Agency,Manufacturer")
async def orgnamegpspublic(
    interaction: discord.Interaction, orgname: str = "", tags: str = ""
) -> None:
    """Allows a user to get information about the localization of space
    organizations (33% of DB content)."""
    await interaction.response.defer(ephemeral=True)
    message = space_data.orgnamegpspublic(orgname, tags)
    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
async def weaponspublic(interaction: discord.Interaction) -> None:
    """Allows a user to get information about space-related weapons
    (not all details)."""
    await interaction.response.defer(ephemeral=True)
    message = space_data.weaponspublic()
    await interaction.followup.send(message, ephemeral=True)

# ---------------------------


@client.tree.command()
async def records(interaction: discord.Interaction) -> None:
    """Allows a user to get an insight into the database content."""
    await interaction.response.defer(ephemeral=True)
    message = space_data.records()
    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
async def tag(interaction: discord.Interaction) -> None:
    """Allows a user to get all tags available for filtering purposes."""
    await interaction.response.defer(ephemeral=True)
    message = space_data.tag()
    await interaction.followup.send(message, ephemeral=True)


"""
Endpoints accessible for connected users.
"""


@client.tree.command()
async def myaccount(interaction: discord.Interaction) -> None:
    """Once logged in, you can check your account details."""
    await custom_message(interaction, envs.ACCOUNT, is_private=True)


@client.tree.command()
async def orgname(interaction: discord.Interaction) -> None:
    """Allows a user to get information about space organizations."""
    await custom_message(interaction, envs.ORGNAME, is_private=True)


@client.tree.command()
async def orgnamegps(interaction: discord.Interaction) -> None:
    """Allows a user to get information about space organizations."""
    await custom_message(interaction, envs.ORGNAMEGPS, is_private=True)


@client.tree.command()
async def domain(interaction: discord.Interaction) -> None:
    """Allows a user to get information about domains owned by a space
    organization."""
    await custom_message(interaction, envs.DOMAIN, is_private=True)


@client.tree.command()
async def subdomain(interaction: discord.Interaction) -> None:
    """Allows a user to get information about sub-domains used by a space
    organization."""
    await custom_message(interaction, envs.SUBDOMAIN, is_private=True)


@client.tree.command()
async def ip(interaction: discord.Interaction) -> None:
    """Allows a user to get information about IP addresses used by a space
    organization."""
    await custom_message(interaction, envs.IP, is_private=True)


@client.tree.command()
async def satellite(interaction: discord.Interaction) -> None:
    """Allows a user to get information about satellites of a space
    organization."""
    await custom_message(interaction, envs.SATELLITE, is_private=True)


@client.tree.command()
async def taglaws(interaction: discord.Interaction) -> None:
    """Allows a user to get information of laws and guidelines to which a
    space organization is subject."""
    await custom_message(interaction, envs.TAGLAWS, is_private=True)


@client.tree.command()
async def weapons(interaction: discord.Interaction) -> None:
    """Allows a user to get information about space-related weapons."""
    await custom_message(interaction, envs.WEAPONS, is_private=True)


@client.tree.command()
async def financial(interaction: discord.Interaction) -> None:
    """Allows a user to get information about finance of a space
    organization."""
    await custom_message(interaction, envs.FINANCIAL, is_private=True)


async def _message_conditions(interaction: discord.Interaction,
                              resp, url: str,
                              is_data: bool) -> None:
    """Sends a message depending on the conditions chosen:
    whether it's in the form of a coded message or the basic message
    with the url.

    Args:
        interaction (discord.Interaction): the Discord context
        resp (aiohttp.web_response): The request response
        url (str): The requested endpoint URL
        is_data (bool): message's form
    """
    if resp.status_code == 200:
        if is_data:
            message = content.data_message(resp.json())
            await interaction.response.send_message(message, ephemeral=True)
        else:
            await interaction.response.send_message(
                utils.crop(content.basic_message(url)),
                ephemeral=True)
    else:
        await interaction.response.send_message(
            utils.crop(content.LOG_UNKNOWN),
            ephemeral=True)


async def custom_message(interaction: discord.Interaction, endpoint: str,
                         is_private: bool = False, is_data: bool = True):
    """Sends a message in Discord that redirects to the requested URL.

    Args:
        interaction (discord.Interaction): Discord context
        endpoint (str): Recon.space endpoint to add in the URL
        is_private (bool, optional): Checks if the user is logged in,
            otherwise tells the user to log in. Defaults to False.
        is_data (bool, optional): Message as a coded or basic URL message.
    """

    url = f"{envs.API_ROOT}/{endpoint}"

    if is_private:
        user_id = interaction.user.id  # the id is used to find the user
        token = utils.get_token(user_id)

        if isinstance(token, str):
            resp = utils.auth_request(url, token)
            if resp.status_code == 200:  # access token is still ok
                await _message_conditions(interaction, resp, url, is_data)

            else:  # token needs to be refreshed
                resp = utils.auth_request(url,
                                          utils.update_token(user_id))
                await _message_conditions(interaction, resp, url, is_data)
        else:
            await _send_exception(interaction, token)

    else:  # is public
        resp = utils.get_request(url)
        await _message_conditions(interaction, resp, url, is_data)


async def _send_exception(interaction: discord.Interaction, status_code: int):
    if status_code == envs.TOKEN_INIT_ERROR_ID:  # no file created yet
        await interaction.response.send_message(content.LOG_INIT_ERROR,
                                                ephemeral=True)

    elif status_code == envs.TOKEN_USER_ERROR_ID:  # no user account yet
        await interaction.response.send_message(content.LOG_UNKNOWN,
                                                ephemeral=True)


if __name__ == "__main__":
    client.run(envs.BOT_TOKEN)
