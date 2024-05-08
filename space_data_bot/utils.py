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
import json
import requests
from space_data_bot import envs


def update_token(user_id: str):
    """Sends a request to refresh the token
    """
    token = get_token(user_id, refresh=True)

    url = f"{envs.API_ROOT}/{envs.TOKEN_REFRESH}/#post-object-form"
    data = {"refresh": token}

    resp = requests.post(url, json=data)
    if resp.status_code == 200:
        resp_json = resp.json()
        set_token(user_id, resp_json)
        return resp_json["access"]


def get_token(user_id: str, refresh: bool = False) -> str:
    """Get access token from temporary files, refresh if necessary.

    Returns:
        str: the access token
    """

    if not envs.TOKEN_FILE.is_file():
        return envs.TOKEN_INIT_ERROR_ID

    with open(envs.TOKEN_FILE, 'r') as file:
        content = json.load(file)

        if content.get(str(user_id)):
            if refresh:
                key = "refresh"
            else:
                key = "access"
            token = content[str(user_id)][key]
            return token
        else:
            return envs.TOKEN_USER_ERROR_ID


def set_token(user_id: str, credentials: dict) -> dict:
    """Saves tokens to a temporary file on the server. To access tokens,
    use the ID of the user requesting them

    Args:
        user_id (str): The user's Discord ID
        credentials (dict): the tokens as resp.json()

    Returns:
        dict: the file content
    """
    if not os.path.exists(envs.TOKEN_FILE):
        with open(envs.TOKEN_FILE, "w") as file:
            json.dump({}, file)

    with open(envs.TOKEN_FILE, "r+") as file:
        content = json.load(file)
        content[user_id] = credentials
        file.seek(0)
        json.dump(content, file, indent=4)
        return content


def crop(message: str) -> str:
    """Crops a Discord message if its length is higher than 2000

    Args:
        message (str): the message to crop

    Returns:
        str: the cropped message
    """
    if len(message) > 1990:
        message = f"{message[:1990]}\n..."

    return message
