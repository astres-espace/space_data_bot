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

import os
import tempfile
from pathlib import Path


# DISCORD ENV
# Replace BOT_TOKEN, GUILD_ID and CHANNEL_ID with your own information
BOT_TOKEN = os.getenv("DISCORD_BOT")
GUILD_ID = os.getenv("ASTRES_ID")
CHANNEL_ID = os.getenv("SPACEDATA_CHANNEL_ID")

# DESTINATION ENV
# Do not edit these constants
HOME_URL = "https://recon.space"
API_ROOT = "https://api.recon.space/myapi"
TOKEN_FILE = Path(tempfile.gettempdir()) / "space_data_tokens.json"

# PUBLIC ENDPOINTS
ORGNAMEPUBLIC = "orgnamepublic"
ORGNAMEGPSPUBLIC = "orgnamegpspublic"  # filter
WEAPONSPUBLIC = "weaponspublic"
TOKEN = "token"
TOKEN_REFRESH = "token/refresh"
RECORDS = "records"
TAG = "tag"

# CONNECTED ENDPOINTS
ACCOUNT = "myaccount"
ORGNAME = "orgname"  # filter by name, city, tag
ORGNAMEGPS = "orgnamegps"  # filter
DOMAIN = "domain"
SUBDOMAIN = "subdomain"
IP = "ip"
SATELLITE = "satellite"  # filter
TAGLAWS = "taglaws"
WEAPONS = "weapons"
FINANCIAL = "financial"

MAX_ITER_NUMBER = 5
MAX_MESSAGE_LENGTH = 1980

TOKEN_INIT_ERROR_ID = 0
TOKEN_USER_ERROR_ID = 1
