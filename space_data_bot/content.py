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
from space_data_bot import envs


def basic_message(url: str) -> str:
    return f"See your results here : {url}"


def data_message(data: list) -> str:
    """
    Breaks down the result of a request and converts it into a Discord message
    """

    # The maximum length of a Discord message is 2000 characters.
    if len(data) > 1990:
        data = data[:1990] + "\n..."

    message = f"""
    ```json
    {json.dumps(data, indent=4)}
    ```
    """

    return message


EMPTY = "Sorry, nothing matches your search..."

# LOGIN

LOG_SUCCESS = "You are successfully logged in!"
LOG_ERROR = """
Error!
Create an account first or check that you haven't made a mistake entering your login details.
"""
LOG_UNKNOWN = f"Please log in or create an account on : {envs.HOME_URL}"

# ORGNAMEPUBLIC

ORGNAMEPUBLIC_DEFAULT = f"""
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
**Click on this link to see all the companies:**
{envs.API_ROOT}/{envs.ORGNAMEPUBLIC}
Try specifying the company's name you're looking for by retyping the command.
"""

ORGNAMEPUBLIC_TOO_MUCH_ORGS = """
There are more than 5 companies that contain this filter!
Try refining your search by entering one of these names:
"""  # then show the name of each org


# ORGNAMEGPSPUBLIC

ORGNAMEGPSPUBLIC_DEFAULT = f"""
There's a lot of data!
Here's a sample of what you can get with this command:
```
"id": 492,
"organisationname": "Arkadia Space",
"tags": [
    "Manufacturer"
],
"gps": "POINT(9.491 51.2993)"
```
**Click on this link to see all the companies:**
{envs.API_ROOT}/{envs.ORGNAMEGPSPUBLIC}
Try specifying the company's name you're looking for by retyping the command.
"""


# WEAPONSPUBLIC

WEAPONSPUBLIC_DEFAULT = f"""
There's a lot of data!
Here's a sample of what you can get with this command:
```
"name": "RIM-161 Standard Missile 3",
"description": "Although primarily designed as an anti-ballistic missile, ...
"source": "https://en.wikipedia.org/wiki/RIM-161_Standard_Missile_3",
"vectortype": "ASAT kinetic"
```
**Click on this link to see all the companies:**
{envs.API_ROOT}/{envs.WEAPONSPUBLIC}
Try specifying the weapon's name or vector type you're looking for by retyping the command.
"""

WEAPONSPUBLIC_TOO_MUCH_DATA = """
There are more than 5 weapons that contain this filter!
Try refining your search by entering one of these names:
"""  # then show the name of each weapon

# HELP DOCUMENTATION
HELP_PUBLIC_ENDPOINTS = {
    envs.ORGNAMEPUBLIC: "Informations basiques sur les entreprises.",
    envs.ORGNAMEGPSPUBLIC: "Localisations GPS des entreprises.",
    envs.WEAPONSPUBLIC: "Informations basiques sur toutes les armes du spatial.",
    envs.TOKEN: "Allows the user to connect to Recon.Space.",
    envs.TOKEN_REFRESH: "Actualise les autorisations d'accès à Recon.Space.",
    envs.RECORDS: "Le nombre d'éléments que chaque catégorie contient.",
    envs.TAG: "L'identifiant de chaque catégorie."
}
HELP_PRIVATE_ENDPOINTS = {
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


def _iter_help(data: dict) -> str:
    message = ""
    for endpoint, doc in HELP_PUBLIC_ENDPOINTS.items():
        message += f"`/{endpoint}`: {doc}\n"
    return message


def help_message():
    return f"""
**Endpoints accessible for everyone**
{_iter_help(HELP_PUBLIC_ENDPOINTS)}

**Endpoints accessible for connected users**
_These commands require you to be connected to recon.space._
{_iter_help(HELP_PRIVATE_ENDPOINTS)}
"""
