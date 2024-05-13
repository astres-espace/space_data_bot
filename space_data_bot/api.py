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
        self._tokens = {}

    def _get(self, url: str, headers: dict = None,
             filters: dict = None) -> requests.Response:
        """Makes a customized GET request

        Args:
            url (str): the request url
            headers (dict, optional): token and additionals. Defaults to None.
            filters (dict, optional): search filters. Defaults to None.

        Returns:
            requests.Response
        """
        if filters:
            query = "&".join([f"{k}={v}" for k, v in filters.items()])
            url += f"/?{query}"

        if headers:
            return requests.get(url, headers=headers)

        return requests.get(url)

    def _post(self, url: str, data: dict) -> requests.Response:
        url += "/#post-object-form"

        return requests.post(url, json=data)
    
    def _pack_get(self, token: str, endpoint: str) -> str:
        """Allows a user to get information about domains owned by a space
        organization.

        Returns:
            str: Results with MD syntax
        """
        url = f"{self._url}/{endpoint}"
        headers = {"Authorization": f"JWT {token}"}

        resp = self._get(url, headers=headers)
        if resp.status_code == 200:
            return content.data_message(resp.json())
        else:
            return content.LOG_ERROR

    def get_token(self, id: str = 0, type: str = "access") -> str:
        if self._tokens.get(id, None):
            return self._tokens[id].get(type, "")

    def set_token(self, id: str, data: dict) -> None:
        self._tokens[id] = data

    def update_token(self, id: str) -> str:
        data = {"refresh": self.get_token(id, type="refresh")}
        resp = self._post(f"{self._url}/{envs.TOKEN_REFRESH}", data)

        if resp.status_code == 200:
            new_data = resp.json()
            self.set_token(id, new_data)

            return new_data["access"]

    def connect(self, email: str, password: str, id: str = 0) -> dict:
        url = f"{self._url}/{envs.TOKEN}"
        data = {
            "email": email,
            "password": password
        }

        resp = self._post(url, data)

        if resp.status_code != 200:
            return content.LOG_ERROR

        data = resp.json()

        if id:
            self.set_token(id, data)

        return content.LOG_SUCCESS

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

        filters = {}
        if orgname:
            filters["orgname"] = orgname

        if tags:
            filters["tags"] = tags

        if not filters:
            return content.ORGNAME_DEFAULT

        resp = self._get(url, filters=filters)
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

        filters = {}
        if orgname:
            filters["orgname"] = orgname

        if tags:
            filters["tags"] = tags

        if not filters:
            return content.ORGNAME_DEFAULT

        resp = self._get(url, filters=filters)
        data = resp.json()["results"]

        if not data:  # no result
            return content.EMPTY

        elif len(data) > envs.MAX_ITER_NUMBER:  # too much results
            return content.too_much_data(data, "organisationname")

        else:  # sends requested info
            return content.data_message(data)

    def weaponspublic(self) -> str:
        """Allows a user to get information about space-related weapons
        (not all details). (GET)

        Returns:
            str: Results with MD syntax
        """
        url = f"{self._url}/{envs.WEAPONSPUBLIC}"
        data = self._get(url).json()

        if not data:  # no result
            return content.EMPTY

        return content.data_message(data)

    def records(self) -> str:
        """Allows a user to get an insight into the database content.

        Returns:
            str: Results with MD syntax
        """
        url = f"{self._url}/{envs.RECORDS}"
        data = self._get(url).json()

        if not data:  # no result
            return content.EMPTY

        return content.data_message(data)

    def tag(self) -> str:
        """Allows a user to get all tags available for filtering purposes.

        Returns:
            str: Results with MD syntax
        """
        url = f"{self._url}/{envs.TAG}"
        data = self._get(url).json()

        if not data:  # no result
            return content.EMPTY

        return content.data_message(data)

    def myaccount(self, token: str) -> str:
        """Once logged in, you can check your account details.

        Returns:
            str: Results with MD syntax
        """
        url = f"{self._url}/{envs.ACCOUNT}"
        headers = {"Authorization": f"JWT {token}"}

        resp = self._get(url, headers=headers)
        if resp.status_code == 200:
            return content.data_message(resp.json())
        else:
            return content.LOG_ERROR

    def orgname(self,id : int, token: str, orgname: str = "",
                tags: str = "", has_satellite_named: str = "",
                has_satellite_operated_by_country: str = "") -> str:
        """Allows a user to get information about space organizations.

        Returns:
            str: Results with MD syntax
        """
        if id:
            url = f"{self._url}/{envs.ORGNAME}/"+str(id)
            headers = {"Authorization": f"JWT {token}"}
            resp = self._get(url, headers=headers)
        else:

            url = f"{self._url}/{envs.ORGNAME}"
            headers = {"Authorization": f"JWT {token}"}

            filters = {}
            if orgname:
                filters["orgname"] = orgname

            if tags:
                filters["tags"] = tags

            if has_satellite_named:
                filters["hassatellitenamed"] = has_satellite_named

            if has_satellite_operated_by_country:
                filters[
                    "hassatelliteoperatedbycountry"
                ] = has_satellite_operated_by_country

            resp = self._get(url, headers=headers, filters=filters)
        if resp.status_code == 200:
            return content.data_message(resp.json())
        else:
            return content.LOG_ERROR

    def orgnamegps(self, token: str, orgname: str = "",
                   tags: str = "") -> str:
        """Allows a user to get information about space organizations.

        Returns:
            str: Results with MD syntax
        """
        url = f"{self._url}/{envs.ORGNAMEGPS}"
        headers = {"Authorization": f"JWT {token}"}

        filters = {}
        if orgname:
            filters["orgname"] = orgname

        if tags:
            filters["tags"] = tags

        resp = self._get(url, headers=headers, filters=filters)
        if resp.status_code == 200:
            return content.data_message(resp.json())
        else:
            return content.LOG_ERROR

    def satellite(self, token: str, name: str = "",
                  country_operator: str = "", orbit: str = "",
                  launch_vehicle: str = "") -> str:
        """Allows a user to get information about satellites of a space
        organization.

        Returns:
            str: Results with MD syntax
        """
        url = f"{self._url}/{envs.SATELLITE}"
        headers = {"Authorization": f"JWT {token}"}

        filters = {}
        if name:
            filters["satellitename"] = name

        if country_operator:
            filters["satellitecountryoperator"] = country_operator

        if orbit:
            filters["satelliteorbit"] = orbit

        if launch_vehicle:
            filters["satellitelaunchvehicle"] = launch_vehicle

        resp = self._get(url, headers=headers, filters=filters)
        if resp.status_code == 200:
            return content.data_message(resp.json())
        else:
            return content.LOG_ERROR

    def domain(self, token: str, id:int) -> str:
        url = f"{self._url}/{envs.DOMAIN}/"+str(id)
        headers = {"Authorization": f"JWT {token}"}
        resp = self._get(url, headers=headers)

        if resp.status_code == 200:
            return content.data_message(resp.json())
        else:
            return content.LOG_ERROR

    def subdomain(self, token: str, id:int) -> str:
        url = f"{self._url}/{envs.DOMAIN}/"+str(id)
        headers = {"Authorization": f"JWT {token}"}
        resp = self._get(url, headers=headers)

        if resp.status_code == 200:
            return content.data_message(resp.json())
        else:
            return content.LOG_ERROR

    def ip(self, token: str, id:int) -> str:
        url = f"{self._url}/{envs.DOMAIN}/"+str(id)
        headers = {"Authorization": f"JWT {token}"}
        resp = self._get(url, headers=headers)

        if resp.status_code == 200:
            return content.data_message(resp.json())
        else:
            return content.LOG_ERROR

    def taglaws(self, token: str) -> str:
        url = f"{self._url}/{envs.TAGLAWS}"
        headers = {"Authorization": f"JWT {token}"}
        resp = self._get(url, headers=headers)

        if resp.status_code == 200:
            return content.data_message(resp.json())
        else:
            return content.LOG_ERROR


    def weapons(self, token: str) -> str:
        url = f"{self._url}/{envs.WEAPONS}"
        headers = {"Authorization": f"JWT {token}"}
        resp = self._get(url, headers=headers)

        if resp.status_code == 200:
            return content.data_message(resp.json())
        else:
            return content.LOG_ERROR

    def financial(self, token: str, id: int) -> str:
        url = f"{self._url}/{envs.FINANCIAL}/"+str(id)
        headers = {"Authorization": f"JWT {token}"}
        resp = self._get(url, headers=headers)

        if resp.status_code == 200:
            return content.data_message(resp.json())
        else:
            return content.LOG_ERROR

api_instance = SpaceDataApi()
api_instance.domain('your_token_here', 15)