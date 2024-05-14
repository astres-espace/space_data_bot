**Copyright (c) 2024 Alliance Stratégique des Étudiants du Spatial (ASTRES)**

*Permission is hereby granted, free of charge, to any person obtaining a copy*
*of this software and associated documentation files (the "Software"), to deal*
*in the Software without restriction, including without limitation the rights*
*to use, copy, modify, merge, publish, distribute, sublicense, and/or sell*
*copies of the Software, and to permit persons to whom the Software is*
*furnished to do so, subject to the following conditions:*

*The above copyright notice and this permission notice shall be included in all*
*copies or substantial portions of the Software.*

*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR*
*IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,*
*FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE*
*AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER*
*LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,*
*OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE*
*SOFTWARE.*

<h3 align="center">
    A Bot for accessing a huge space database
</h3>


# ABOUT

This Discord bot lets you communicate easily and efficiently with **Recon[.]Space** data.

##
This tool is written in **Python 3**.

Python3 requirements : Discord
Discord requirements: Create a discord bot using the discord dev portal, assign permission and a channel to the bot. Get the bot token, server id and channel id. (info : https://discordpy.readthedocs.io/en/stable/discord.html)

# INSTALL
1. Install discord.py by executing the command :
```
pip3 install discord
````

2. Create these environment variables:
```
BOT_TOKEN : <your bot's token>.
ASTRES_ID: <the ID of your Discord server>
SPACEDATA_CHANNEL_ID: <the ID of the channel in which you want to use the bot>
```
You will find help to create them in : create_local_env_variables file.

3. Download the repository and execute the `main.py` file


# Usage - bot commands
_Use the bot through your discord channel, here are the commands that you can use to fetch Recon[.]Space data:_
|*Command* |Status|Info|
|-|:-:|-|
|**help**|public|Get the help about discord usage|
|**orgnamepublic**|public|Company information|
|**orgnamegpspublic**|public|Company gps information|
|**weaponspublic**|public|Space weapons information|
|**connect**|public|Connect to you recon.space account|
|**records**|public|Get an insigh of recon.space db|
|**connect**|public|Tags that can be used for filtering|
|**orgname**|private|Company information|
|**orgnamegps**|private|Company gps information|
|**financial**|private|Company financial information|
|**satellite**|private|Satellite information|
|**weapons**|private|Weapons information|
|**myaccount**|private|Your account information|
|**domain**|private|Company domain information|
|**ip**|private|Company ip addresses information|
|**subdomain**|private|Company subdomain information|
|**taglaws**|private|Company laws information|

