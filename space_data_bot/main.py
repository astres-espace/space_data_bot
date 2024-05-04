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

import typing
import os
import json
import discord
import requests
import tempfile
from pathlib import Path
from discord import app_commands

from space_data_bot import envs


GUILD_ID = discord.Object(id=os.getenv("ASTRES_ID"))

# HELP DOCUMENTATION
PUBLIC_ENDPOINTS = {
    envs.ORGNAMEPUBLIC: "Informations basiques sur les entreprises.",
    envs.ORGNAMEGPSPUBLIC: "Localisations GPS des entreprises.",
    envs.WEAPONSPUBLIC: "Informations basiques sur toutes les armes du spatial.",
    envs.TOKEN: "Allows the user to connect to Recon.Space.",
    envs.TOKEN_REFRESH: "Actualise les autorisations d'accès à Recon.Space.",
    envs.RECORDS: "Le nombre d'éléments que chaque catégorie contient.",
    envs.TAG: "L'identifiant de chaque catégorie."
}
PRIVATE_ENDPOINTS = {
    envs.ACCOUNT: "...",
    envs.ORGNAME: "...",
    envs.ORGNAMEGPS: "...",
    envs.DOMAIN: "...",
    envs.SUBDOMAIN: "...",
    envs.IP: "...",
    envs.SATELLITE: "...",
    envs.TAGLAWS: "...",
    envs.WEAPONS: "...",
    envs.FINANCIAL: "..."
}


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

    message = "**Endpoints accessible for everyone**\n"
    for endpoint, doc in PUBLIC_ENDPOINTS.items():
        message += f"`/{endpoint}`: {doc}\n"
    message += "\n**Endpoints accessible for connected users**\n"
    message += "_These commands require you to be connected to recon.space._\n"
    for endpoint, doc in PRIVATE_ENDPOINTS.items():
        message += f"`/{endpoint}`: {doc}\n"

    await interaction.response.send_message(message, ephemeral=True)


"""
Endpoints commands accessible for everyone.
"""


@client.tree.command()
@app_commands.describe(email="your email", password="your password")
async def login(interaction: discord.Interaction,
                email: str, password: str) -> None:
    """Allows the user to connect to Recon.Space."""

    data = {"email": email, "password": password}
    url = f"https://api.recon.space/myapi/{envs.TOKEN}/#post-object-form"

    response = requests.post(url, json=data)
    if response.status_code == 200:
        token_file = Path(tempfile.gettempdir()) / envs.TOKEN_TEMP_FILE_STEM
        # save tokens in a file
        with open(token_file, "w") as json_file:
            json.dump(response.json(), json_file)

        await interaction.response.send_message(
            "You are successfully logged in!", ephemeral=True)
    else:
        await interaction.response.send_message(
            """
            Error!
            Create an account first or check that you haven't made a
            mistake entering your login details.
            """,
            ephemeral=True)


@client.tree.command()
@app_commands.describe(refresh="refresh type JSON web token")
async def login_refresh(interaction: discord.Interaction, refresh: str
                        ) -> None:
    """Takes a refresh type JSON web token and returns an access type JSON web
token if the refresh token is valid."""
    data = {"refresh": refresh}
    # WIP


@client.tree.command()
@app_commands.describe(company_name="The name of the company")
async def orgnamepublic(interaction: discord.Interaction,
                        company_name: str = "") -> None:
    """Company information"""

    if company_name:
        url = f"{envs.API_ROOT}/{envs.ORGNAMEPUBLIC}/?search={company_name}"
        result = requests.get(url)

        if result.status_code == 200:
            orgs = result.json().get("results", [])
            if len(orgs) > 5:
                message = "There are more than 5 companies that contain \
                this filter!\nTry refining your search by entering one of \
                these names:"
                for org in orgs:
                    message += f"{org.get('organisationname', '')}\n"

                await interaction.response.send_message(crop(message),
                                                        ephemeral=True)
            else:
                await interaction.response.send_message(crop(orgs),
                                                        ephemeral=True)
        else:
            await interaction.response.send_message(
                f"Error {result.status_code}")

    else:
        message = f'''
There's a lot of data!
Here's a sample of what you can get with this command:
```
"id": 3408,
"organisationname": "NASA",
"orgtype": "For Profit",
"description": "NASA is responsible for the civilian space program,
    as well as aeronautics and aerospace research.",
"tags": [
    "Agency",
    "Misc"
]
```
**Click on this link to see all the companies:** {envs.API_ROOT}/{envs.ORGNAMEPUBLIC}
Try specifying the company's name you're looking for by retyping the command.
'''
        await interaction.response.send_message(message, ephemeral=True)


@client.tree.command()
async def orgnamegpspublic(interaction: discord.Interaction) -> None:
    """GPS company locations"""
    await custom_message(interaction, envs.ORGNAMEGPSPUBLIC)


@client.tree.command()
async def weaponspublic(interaction: discord.Interaction) -> None:
    """Basic information on all space weapons"""
    await custom_message(interaction, envs.WEAPONSPUBLIC)


@client.tree.command()
async def records(interaction: discord.Interaction) -> None:
    """The number of items in each category"""
    url = f"{envs.API_ROOT}/{envs.RECORDS}"
    response = requests.get(url)
    await interaction.response.send_message(
        build_req_message(f"**Records Count**\n{url}", response),
        ephemeral=True)


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

    if is_private:
        headers = {"Authorization": f"JWT {get_token()}"}
        result = requests.get(url, headers=headers)
        if result.status_code == 200:
            await interaction.response.send_message(
                build_req_message(f"**{endpoint}**\n{url}", result),
                ephemeral=True)
        else:
            await interaction.response.send_message(
                f"Please log in or create an account on : {envs.HOME_URL}",
                ephemeral=True)
    else:
        await interaction.response.send_message(
            f"See your results here : {url}", ephemeral=True)


def build_req_message(title: str, response: requests.models.Response) -> str:
    """
    Breaks down the result of a request and converts it into a Discord message.

    Args:
        title (str): Message title
    """

    message = f"""
    {title}
    ```json
    {json.dumps(response.json(), indent=4)}
    ```
    """

    # The maximum length of a Discord message is 2000 characters.
    if len(message) > 1990:
        message = message[:1990] + "\n..."

    return message


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


def crop(message: str):
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
