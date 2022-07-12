<p align="center">
    <a href="https://github.com/Skammato/Base-for-bot_api">
        <img src="https://www.vhv.rs/dpng/d/492-4925781_telegram-free-download-and-circle-twitter-logo-png.png" alt="Telegram Apis" width="50%">
    </a>
    <br>
    <b>Telegram bot api client in python</b>
    <br>
</p>

``` python
from tg_api import tg_api

bot = TelegramClient("PorcoCazzo", TELEGRAM_API_TOKEN)


@bot.on_message(filters.command("start"))
async def handler(client, message):
    print(message)
    await message.bounds.reply_text(f"Hello {message.from_user.first_name}")


bot.start()
```

# Base for bot api
This repo is a small-library, or rather a base used **to build a telegram client**. It is developed in **python3** and comes with filters and is **super simple to use**.

# Installation
 - Execute **these** steps
 - After, you can **erase** 'Base-for-bot_api' folder
 ```bash
 git clone https://github.com/Skammato/Base-for-bot_api.git  
 cd Base-for-bot_api
 python3 setup.py
 
  ```
# Things to know
 - The **updates** received by telegram **and** the **responses** to the methods **are objects** of type "Object" (see types). 
 - Using **str(Object)** it is possible to get a **json** encoded **string**.
 - Often telegram returns the dict **"from" within an update**, containing the information of the user who called the update; but **you can find this object as 'from_user'** because only 'from' gave a syntax error.

# Contact Me
If you have problems with the use of this base or have any ideas to improve it, write me on telegram.
<p color="blue"><a href="https://telegram.me/invecchiato">My Profile</a></p>
