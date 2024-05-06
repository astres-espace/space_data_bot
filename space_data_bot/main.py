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

import json
import discord
import requests
import tempfile
from pathlib import Path
from discord import app_commands

from space_data_bot import envs, content, filter


GUILD_ID = discord.Object(id=envs.GUILD_ID)


"""
The bot is initialized via a class that integrates it with Discord commands
and makes its rights explicit.
"""


class SpaceDataClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to the guild.
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)


intents = discord.Intents.default()
client = SpaceDataClient(intents=intents)


"""
Commands are defined outside the class, but are linked to it via decorators.

@client.tree.command(): Classic discord command

@app_commands.describe() : Used to add documentation to command arguments.

@app_commands.autocomplete(): Sets up auto-completion for a given argument.

@app_commands.check(): Executes the command only if the answer is True.
"""


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
async def login(interaction: discord.Interaction,
                email: str, password: str) -> None:
    """Allows the user to connect to Recon.Space."""

    url = f"https://api.recon.space/myapi/{envs.TOKEN}/#post-object-form"
    data = {
        "email": email,
        "password": password
    }

    result = requests.post(url, json=data)

    if result.status_code != 200:
        await interaction.response.send_message(content.LOG_ERROR,
                                                ephemeral=True)
        return

    token_file = Path(tempfile.gettempdir()) / envs.TOKEN_TEMP_FILE_STEM
    # save tokens in a file
    with open(token_file, "w") as json_file:
        json.dump(result.json(), json_file)

    await interaction.response.send_message(content.LOG_SUCCESS,
                                            ephemeral=True)


@client.tree.command()
@app_commands.describe(refresh="refresh type JSON web token")
async def login_refresh(interaction: discord.Interaction, refresh: str
                        ) -> None:
    """Takes a refresh type JSON web token and returns an access type JSON web
token if the refresh token is valid."""
    pass
    # WIP

# ---------------------------


@client.tree.command()
@app_commands.describe(company_name="The name of the company")
async def orgnamepublic(interaction: discord.Interaction,
                        company_name: str = "") -> None:
    """Company information"""

    if company_name:
        url = f"{envs.API_ROOT}/{envs.ORGNAMEPUBLIC}/?search={company_name}"
        result = requests.get(url)

        # checks if error
        if result.status_code != 200:
            await interaction.response.send_message(
                f"Error {result.status_code}")
            return

        companies = result.json().get("results", [])

        # too much results
        if len(companies) > 5:
            message = content.ORGNAMEPUBLIC_TOO_MUCH_ORGS
            for org in companies:
                message += f"\n_{org.get('organisationname', '')}_"

            await interaction.response.send_message(
                crop(message),
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
async def orgnamegpspublic(interaction: discord.Interaction) -> None:
    """GPS company locations"""
    await interaction.response.send_message(content.ORGNAMEGPSPUBLIC_DEFAULT,
                                            ephemeral=True)

# ---------------------------


@client.tree.command()
@app_commands.describe(name="The name of the weapon (eg: Tsyklon)",
                       vector_type="The vector type (eg: ASAT kinetic)")
async def weaponspublic(
    interaction: discord.Interaction, name: str = "", vector_type: str = ""
) -> None:
    """Basic information on all space weapons."""

    url = f"{envs.API_ROOT}/{envs.WEAPONSPUBLIC}"
    result = requests.get(url)

    # checks if error
    if result.status_code != 200:
        await interaction.response.send_message(
            f"Error {result.status_code}")
        return

    if name or vector_type:
        # filters
        data = []
        if name:
            data += filter.request_filter(result, key="name", value=name)

        if vector_type:
            by_vector = filter.request_filter(result, key="vectortype",
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

            await interaction.response.send_message(crop(message),
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
    """The number of items in each category"""
    url = f"{envs.API_ROOT}/{envs.RECORDS}"
    message = crop(content.data_message(requests.get(url).json()))

    await interaction.response.send_message(message, ephemeral=True)


@client.tree.command()
async def tag(interaction: discord.Interaction) -> None:
    """The identifier for each category"""
    await custom_message(interaction, envs.TAG)


"""
Endpoints accessible for connected users.
"""


@client.tree.command()
async def myaccount(interaction: discord.Interaction) -> None:
    """..."""
    await custom_message(interaction, envs.ACCOUNT, is_private=True)


@client.tree.command()
async def orgname(interaction: discord.Interaction) -> None:
    """Company information for logged-in users"""
    await custom_message(interaction, envs.ORGNAME, is_private=True)


@client.tree.command()
async def orgnamegps(interaction: discord.Interaction) -> None:
    """GPS company locations for logged-in users"""
    await custom_message(interaction, envs.ORGNAMEGPS, is_private=True)


@client.tree.command()
async def domain(interaction: discord.Interaction) -> None:
    """..."""
    await custom_message(interaction, envs.DOMAIN, is_private=True)


@client.tree.command()
async def subdomain(interaction: discord.Interaction) -> None:
    """..."""
    await custom_message(interaction, envs.SUBDOMAIN, is_private=True)


@client.tree.command()
async def ip(interaction: discord.Interaction) -> None:
    """..."""
    await custom_message(interaction, envs.IP, is_private=True)


@client.tree.command()
async def satellite(interaction: discord.Interaction) -> None:
    """..."""
    await custom_message(interaction, envs.SATELLITE, is_private=True)


@client.tree.command()
async def taglaws(interaction: discord.Interaction) -> None:
    """..."""
    await custom_message(interaction, envs.TAGLAWS, is_private=True)


@client.tree.command()
async def weapons(interaction: discord.Interaction) -> None:
    """..."""
    await custom_message(interaction, envs.WEAPONS, is_private=True)


@client.tree.command()
async def financial(interaction: discord.Interaction) -> None:
    """..."""
    await custom_message(interaction, envs.FINANCIAL, is_private=True)


"""
At the end of the file, here are some useful time-saving commands.
"""


async def custom_message(interaction: discord.Interaction, endpoint: str,
                         is_private: bool = False):
    """Sends a message in Discord that redirects to the requested URL.

    Args:
        interaction (discord.Interaction): Discord context
        endpoint (str): Recon.space endpoint to add in the URL
        is_private (bool, optional): Checks if the user is logged in,
            otherwise tells the user to log in. Defaults to False.
    """
    url = f"{envs.API_ROOT}/{endpoint}"

    if is_private:  # must be connected
        headers = {"Authorization": f"JWT {get_token()}"}
        result = requests.get(url, headers=headers)

        if result.status_code == 200:  # user is connected
            message = content.data_message(result.json())
            await interaction.response.send_message(message, ephemeral=True)

        else:  # user is not connected
            await interaction.response.send_message(content.LOG_UNKNOWN,
                                                    ephemeral=True)

    else:  # public endpoint
        await interaction.response.send_message(content.basic_message(url),
                                                ephemeral=True)


async def _check_request(interaction: discord.Interaction,
                         result: requests.Response) -> bool:
    if result.status_code != 200:
        await interaction.response.send_message(
            f"Error {result.status_code}")
        return False

    return True


def refresh_token(token: str):  # WIP
    return token


def get_token() -> str:
    """Get access token from temporary files, refresh if necessary.

    Returns:
        str: the access token
    """
    token_file = Path(tempfile.gettempdir()) / envs.TOKEN_TEMP_FILE_STEM

    if not token_file.is_file():
        print("The token file does not exist.")
        return

    with open(token_file, 'r') as file:
        content = json.load(file)

        token_access = content.get("access", None)

        if not token_access:
            token_refresh = content.get("refresh", None)
            if not token_refresh:
                print("The token file is empty.")

            token_access = refresh_token(token_refresh)

        return token_access


def crop(message: str) -> str:
    if len(message) > 1990:
        message = f"{message[:1990]}\n..."

    return message


if __name__ == "__main__":
    client.run(envs.BOT_TOKEN)


def _check_tokens(endpoint: str):  # Unused for now
    url = f"{envs.API_ROOT}/{endpoint}"
    headers = {"Authorization": f"JWT {get_token()}"}
    request_response = requests.get(url, headers=headers)

    if request_response.status_code == 200:
        return True
