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

from space_data_bot import envs


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

# LOGIN

LOG_SUCCESS = "You are successfully logged in!"
LOG_ERROR = """
Error!
Create an account first or check that you haven't made a mistake entering your login details.
"""

# ORGNAMEPUBLIC

ORGNAMEPUBLIC_SAMPLE = f"""
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
"""
