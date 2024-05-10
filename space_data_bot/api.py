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

import requests
from space_data_bot import envs, content


class SpaceDataApi:
    def __init__(self) -> None:
        self._url = envs.API_ROOT

    def _filter_request(self, url: str, filters: dict, ) -> requests.Response:
        query = "&".join([f"{k}={v}" for k, v in filters.items()])
        url += f"/?{query}"
        return requests.get(url)

    def orgnamepublic(self, orgname: str = "", tags: str = "") -> str:
        """Allows a user to get information about space organizations
        (50% of DB content). (GET)

        Args:
            orgname (str, optional): The name of the organization.
            tags (str, optional): some tags.

        Returns:
            str: Results with MD syntax
        """
        url = f"{self._url}/{envs.ORGNAMEPUBLIC}"

        if orgname:
            resp = self._filter_request(url, {"orgname": orgname})

        elif tags:
            resp = self._filter_request(url, {"tags": tags})

        elif orgname and tags:
            resp = self._filter_request(url,
                                        {"orgname": orgname, "tags": tags})

        else:
            return content.ORGNAME_DEFAULT

        data = resp.json()["results"]

        if not data:  # no result
            return content.EMPTY

        elif len(data) > envs.MAX_ITER_NUMBER:  # too much results
            return content.too_much_data(data, "organisationname")

        else:  # sends requested info
            return content.data_message(data)

    def orgnamegpspublic(self, orgname: str = "", tags: str = "") -> str:
        """Allows a user to get information about the localization of space
        organizations (33% of DB content). (GET)

        Args:
            orgname (str, optional): The name of the organization.
            tags (str, optional): some tags.

        Returns:
            str: Results with MD syntax
        """
        url = f"{self._url}/{envs.ORGNAMEGPSPUBLIC}"

        if orgname:
            resp = self._filter_request(url, {"orgname": orgname})

        elif tags:
            resp = self._filter_request(url, {"tags": tags})

        elif orgname and tags:
            resp = self._filter_request(url,
                                        {"orgname": orgname, "tags": tags})

        else:
            return content.ORGNAMEGPS_DEFAULT

        data = resp.json()

        if not data:  # no result
            return content.EMPTY

        elif len(data) > envs.MAX_ITER_NUMBER:  # too much results
            return content.too_much_data(data, "organisationname")

        else:  # sends requested info
            return content.data_message(data)
