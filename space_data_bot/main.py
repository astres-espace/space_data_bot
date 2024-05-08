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

import aiohttp.web_response
import discord
import requests
import aiohttp
from discord import app_commands

from space_data_bot import envs, content, filter, utils


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
async def login(interaction: discord.Interaction,
                email: str, password: str) -> None:
    """Allows a user to connect to their account;
    an access token and a refresh token are provided."""

    url = f"{envs.API_ROOT}/{envs.TOKEN}/#post-object-form"
    data = {
        "email": email,
        "password": password
    }

    resp = requests.post(url, json=data)
    if resp.status_code != 200:
        await interaction.response.send_message(content.LOG_ERROR,
                                                ephemeral=True)
        return

    # save tokens in a file
    utils.set_token(interaction.user.id, resp.json())

    await interaction.response.send_message(content.LOG_SUCCESS,
                                            ephemeral=True)

# ---------------------------


@client.tree.command()
@app_commands.describe(company_name="The name of the company")
async def orgnamepublic(interaction: discord.Interaction,
                        company_name: str = "") -> None:
    """Allows a user to get information about space organizations
    (50% of DB content)."""

    if company_name:
        url = f"{envs.API_ROOT}/{envs.ORGNAMEPUBLIC}/?search={company_name}"
        resp = requests.get(url)

        # checks if error
        if resp.status_code != 200:
            await interaction.response.send_message(
                f"Error {resp.status_code}")
            return

        companies = resp.json().get("results", [])

        # too much results
        if len(companies) > 5:
            message = content.ORGNAMEPUBLIC_TOO_MUCH_ORGS
            for org in companies:
                message += f"\n_{org.get('organisationname', '')}_"

            await interaction.response.send_message(
                utils.crop(message),
                ephemeral=True)

        # sends info about requested company
        else:
            await interaction.response.send_message(
                content.data_message(companies),
                ephemeral=True)

    # if no company is specified
    else:
        await interaction.response.send_message(content.ORGNAMEPUBLIC_DEFAULT,
                                                ephemeral=True)

# ---------------------------


@client.tree.command()
@app_commands.describe(company_name="The name of the company")
async def orgnamegpspublic(interaction: discord.Interaction,
                           company_name: str = "") -> None:
    """Allows a user to get information about the localization of space
    organizations (33% of DB content)."""
    if company_name:
        url = f"{envs.API_ROOT}/{envs.ORGNAMEPUBLIC}/?orgname={company_name}"
        resp = requests.get(url)

        # checks if error
        if resp.status_code != 200:
            await interaction.response.send_message(
                f"Error {resp.status_code}")
            return

        companies = resp.json().get("results", [])

        # too much results
        if len(companies) > 5:
            message = content.ORGNAMEPUBLIC_TOO_MUCH_ORGS
            for org in companies:
                message += f"\n_{org.get('organisationname', '')}_"

            await interaction.response.send_message(
                utils.crop(message),
                ephemeral=True)

        # sends info about requested company
        else:
            print(companies)
            await interaction.response.send_message(
                utils.crop(content.data_message(companies)),
                ephemeral=True)

    else:
        await interaction.response.send_message(
            content.ORGNAMEGPSPUBLIC_DEFAULT,
            ephemeral=True)

# ---------------------------


@client.tree.command()
@app_commands.describe(name="The name of the weapon (eg: Tsyklon)",
                       vector_type="The vector type (eg: ASAT kinetic)")
async def weaponspublic(
    interaction: discord.Interaction, name: str = "", vector_type: str = ""
) -> None:
    """Allows a user to get information about space-related weapons
    (not all details)."""

    url = f"{envs.API_ROOT}/{envs.WEAPONSPUBLIC}"
    resp = requests.get(url)

    # checks if error
    if resp.status_code != 200:
        await interaction.response.send_message(
            f"Error {resp.status_code}")
        return

    if name or vector_type:
        # filters
        data = []
        if name:
            data += filter.request_filter(resp, key="name", value=name)

        if vector_type:
            by_vector = filter.request_filter(resp, key="vectortype",
                                              value=vector_type)
            if name:
                data += [elem for elem in by_vector if name in elem["name"]]
            else:
                data += by_vector

        # no result
        if not data:
            await interaction.response.send_message(content.EMPTY,
                                                    ephemeral=True)

        # too much results
        elif len(data) > envs.MAX_ITER_NUMBER:
            message = content.WEAPONSPUBLIC_TOO_MUCH_DATA
            for elem in data:
                message += f"\n_{elem.get('name', '')}_"

            await interaction.response.send_message(utils.crop(message),
                                                    ephemeral=True)

        # sends info about requested company
        else:
            await interaction.response.send_message(
                content.data_message(data),
                ephemeral=True)

    # no argument specified
    else:
        await interaction.response.send_message(content.WEAPONSPUBLIC_DEFAULT,
                                                ephemeral=True)

# ---------------------------


@client.tree.command()
async def records(interaction: discord.Interaction) -> None:
    """Allows a user to get an insight into the database content."""
    url = f"{envs.API_ROOT}/{envs.RECORDS}"
    message = utils.crop(content.data_message(requests.get(url).json()))

    await interaction.response.send_message(message, ephemeral=True)


@client.tree.command()
async def tag(interaction: discord.Interaction) -> None:
    """Allows a user to get all tags available for filtering purposes."""
    await custom_message(interaction, envs.TAG, is_data=True)


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
    """Allows a user to get information of potential laws and guidelines to
    which a space organization is subject."""
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


async def message_conditions(interaction: discord.Interaction,
                             resp: aiohttp.web_response, url: str,
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
    if resp.status == 200:
        if is_data:
            message = content.data_message(await resp.json())
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

    async with aiohttp.ClientSession() as session:
        if is_private:
            user_id = interaction.user.id  # the id is used to find the user

            token = utils.get_token(user_id)
            if token == envs.TOKEN_INIT_ERROR_ID:  # no file created yet
                await interaction.response.send_message(content.LOG_INIT_ERROR,
                                                        ephemeral=True)

            elif token == envs.TOKEN_USER_ERROR_ID:  # no user account yet
                await interaction.response.send_message(content.LOG_UNKNOWN,
                                                        ephemeral=True)

            else:  # try access token
                headers = {"Authorization": f"JWT {token}"}
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:  # access token is still ok
                        await message_conditions(interaction,
                                                 resp,
                                                 url,
                                                 is_data)

                    else:  # token needs to be refreshed
                        token_updated = utils.update_token(user_id)

                        # try the request again
                        headers = {
                            "Authorization": f"JWT {token_updated}"
                        }
                        async with session.get(url, headers=headers) as resd:
                            await message_conditions(interaction,
                                                     resd,
                                                     url,
                                                     is_data)

        else:  # is public
            async with session.get(url) as resp:
                await message_conditions(interaction, resp, url, is_data)


if __name__ == "__main__":
    client.run(envs.BOT_TOKEN)
