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


EMPTY = "Sorry, nothing matches your search..."

# LOGIN

LOG_SUCCESS = "You are successfully logged in!"
LOG_ERROR = """
Error!
Create an account first or check that you haven't made a mistake entering your
login details.
"""
LOG_UNKNOWN = f"Please log in or create an account on : {envs.HOME_URL}"
LOG_INIT_ERROR = f"""
The token file does not exist.
{LOG_UNKNOWN}
"""

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
Try specifying the weapon's name or vector type you're looking for by retyping
the command.
"""

WEAPONSPUBLIC_TOO_MUCH_DATA = """
There are more than 5 weapons that contain this filter!
Try refining your search by entering one of these names:
"""  # then show the name of each weapon

# HELP DOCUMENTATION
HELP_PUBLIC_ENDPOINTS = {
    envs.ORGNAMEPUBLIC: "Company information",
    envs.ORGNAMEGPSPUBLIC: "GPS company locations",
    envs.WEAPONSPUBLIC: "Basic information on all space weapons.",
    envs.TOKEN: "Allows the user to connect to Recon.Space.",
    envs.TOKEN_REFRESH: "Update Recon.Space access permissions.",
    envs.RECORDS: "The number of items in each category.",
    envs.TAG: "The identifier for each category."
}
HELP_PRIVATE_ENDPOINTS = {
    envs.ACCOUNT: "User account information",
    envs.ORGNAME: "Company information",
    envs.ORGNAMEGPS: "GPS company locations",
    envs.DOMAIN: "...",
    envs.SUBDOMAIN: "...",
    envs.IP: "...",
    envs.SATELLITE: "...",
    envs.TAGLAWS: "...",
    envs.WEAPONS: "Basic information on all space weapons for logged users.",
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


def basic_message(url: str) -> str:
    return f"See your results here : {url}"


def data_message(data: list) -> str:
    """
    Breaks down the result of a request and converts it into a Discord message
    of 1974 characters.
    """

    # The maximum length of a Discord message is 2000 characters.
    # Put a lower limit in case of title
    data = conform_data(data)
    message = f"""
    ```json
    {json.dumps(data, indent=4)}
    """
    if len(message) > envs.MAX_MESSAGE_LENGTH:
        message = message[:envs.MAX_MESSAGE_LENGTH]
        message += "\n```\n_cropped..._"
    else:
        message += "```"

    return message


def conform_data(data: list):
    if isinstance(data, dict):  # we need a list at the end
        data = data.get("results")

    str_data = str(data)  # convert to str to calculate length

    # remove nulls
    str_data = str_data.replace('null', '"null"')

    # maybe it is useless because done twice
    if len(str_data) > envs.MAX_MESSAGE_LENGTH:
        str_data = str_data[:envs.MAX_MESSAGE_LENGTH]

        while str_data and str_data[-1] != "}" and str_data[-1] != "]":
            str_data = str_data[:-1]

        try:
            return eval(str_data + "]")  # that is why we need a list
        except "Failed to conform":
            return str_data
    else:
        return data


if __name__ == "__main__":
    pass
