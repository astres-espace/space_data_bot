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

from space_data_bot import envs, content
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
                       tags="eg: tags=Agency or tags=Agency,Manufacturer")
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
                       tags="eg: tags=Agency or tags=Agency,Manufacturer")
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
    await interaction.response.defer(ephemeral=True)
    token = space_data.get_token(interaction.user.id)
    message = space_data.myaccount(token)

    if message == content.LOG_ERROR:
        token = space_data.update_token(interaction.user.id)
        message = space_data.myaccount(token)

    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
@app_commands.describe(orgname="The name of the organization",
                       tags="eg: tags=Agency or tags=Agency,Manufacturer",
                       satellite_named="eg : Oneweb",
                       satellite_operated_by_country="eg: Brazil"
                       )
async def orgname(interaction: discord.Interaction, orgname: str = "",
                  tags: str = "", satellite_named: str = "",
                  satellite_operated_by_country: str = "") -> None:
    """Allows a user to get information about space organizations."""
    await interaction.response.defer(ephemeral=True)
    token = space_data.get_token(interaction.user.id)
    message = space_data.orgname(
        token,
        orgname=orgname,
        tags=tags,
        has_satellite_named=satellite_named,
        has_satellite_operated_by_country=satellite_operated_by_country)

    if message == content.LOG_ERROR:
        token = space_data.update_token(interaction.user.id)
        message = space_data.orgname(
            token,
            orgname=orgname,
            tags=tags,
            has_satellite_named=satellite_named,
            has_satellite_operated_by_country=satellite_operated_by_country)

    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
@app_commands.describe(orgname="The name of the organization",
                       tags="eg: tags=Agency or tags=Agency,Manufacturer")
async def orgnamegps(interaction: discord.Interaction, orgname: str = "",
                     tags: str = "") -> None:
    """Allows a user to get information about space organizations."""
    await interaction.response.defer(ephemeral=True)
    token = space_data.get_token(interaction.user.id)
    message = space_data.orgnamegps(token, orgname=orgname, tags=tags)

    if message == content.LOG_ERROR:
        token = space_data.update_token(interaction.user.id)
        message = space_data.orgnamegps(token, orgname=orgname, tags=tags)

    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
async def domain(interaction: discord.Interaction, id: str = "") -> None:
    """Allows a user to get information about domains owned by a space
    organization."""
    await interaction.response.defer(ephemeral=True)
    token = space_data.get_token(interaction.user.id)
    message = space_data.domain(token,id)

    if message == content.LOG_ERROR:
        token = space_data.update_token(interaction.user.id)
        message = space_data.domain(token,id)

    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
async def subdomain(interaction: discord.Interaction) -> None:
    """Allows a user to get information about sub-domains used by a space
    organization."""
    await interaction.response.defer(ephemeral=True)
    token = space_data.get_token(interaction.user.id)
    message = space_data.subdomain(token)

    if message == content.LOG_ERROR:
        token = space_data.update_token(interaction.user.id)
        message = space_data.subdomain(token)

    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
async def ip(interaction: discord.Interaction) -> None:
    """Allows a user to get information about IP addresses used by a space
    organization."""
    await interaction.response.defer(ephemeral=True)
    token = space_data.get_token(interaction.user.id)
    message = space_data.ip(token)

    if message == content.LOG_ERROR:
        token = space_data.update_token(interaction.user.id)
        message = space_data.ip(token)

    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
@app_commands.describe(name="eg: Tian",
                       country_operator="eg: China",
                       orbit="eg: GEO",
                       launch_vehicle="eg: Falcon"
                       )
async def satellite(interaction: discord.Interaction, name: str = "",
                    country_operator: str = "", orbit: str = "",
                    launch_vehicle: str = "") -> None:
    """Allows a user to get information about satellites of a space
    organization."""
    await interaction.response.defer(ephemeral=True)
    token = space_data.get_token(interaction.user.id)
    message = space_data.satellite(token,
                                   name=name,
                                   country_operator=country_operator,
                                   orbit=orbit,
                                   launch_vehicle=launch_vehicle)

    if message == content.LOG_ERROR:
        token = space_data.update_token(interaction.user.id)
        message = space_data.satellite(token,
                                       name=name,
                                       country_operator=country_operator,
                                       orbit=orbit,
                                       launch_vehicle=launch_vehicle)

    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
async def taglaws(interaction: discord.Interaction) -> None:
    """Allows a user to get information of laws and guidelines to which a
    space organization is subject."""
    await interaction.response.defer(ephemeral=True)
    token = space_data.get_token(interaction.user.id)
    message = space_data.taglaws(token)

    if message == content.LOG_ERROR:
        token = space_data.update_token(interaction.user.id)
        message = space_data.taglaws(token)

    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
async def weapons(interaction: discord.Interaction) -> None:
    """Allows a user to get information about space-related weapons."""
    await interaction.response.defer(ephemeral=True)
    token = space_data.get_token(interaction.user.id)
    message = space_data.weapons(token)

    if message == content.LOG_ERROR:
        token = space_data.update_token(interaction.user.id)
        message = space_data.weapons(token)

    await interaction.followup.send(message, ephemeral=True)


@client.tree.command()
async def financial(interaction: discord.Interaction) -> None:
    """Allows a user to get information about finance of a space
    organization."""
    await interaction.response.defer(ephemeral=True)
    token = space_data.get_token(interaction.user.id)
    message = space_data.financial(token)

    if message == content.LOG_ERROR:
        token = space_data.update_token(interaction.user.id)
        message = space_data.financial(token)

    await interaction.followup.send(message, ephemeral=True)


if __name__ == "__main__":
    client.run(envs.BOT_TOKEN)
