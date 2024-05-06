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

from pathlib import Path
import tempfile
import json

from space_data_bot import envs


def refresh_token(token: str):  # WIP
    """Sends a request to refresh the token

    Args:
        token (str): the refresh token

    Returns:
        str: a new access token
    """
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
    """Crops a Discord message if its length is higher than 2000

    Args:
        message (str): the message to crop

    Returns:
        str: the cropped message
    """
    if len(message) > 1990:
        message = f"{message[:1990]}\n..."

    return message
