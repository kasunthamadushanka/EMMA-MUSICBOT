# Ā© TamilBots 2021-22

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
from config import Config

bot = Client(
    'SongPlayRoBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------
@bot.on_message(filters.command(['start']))
def start(client, message):
    TamilBots = f'š Hay @{message.from_user.username}\n\nI am šµ šššš ššššš ššš [š¶](https://telegra.ph/file/deb4201942e6cf5ee88ae.mp4)\n\nSend The Name of the Song You Want..\n\nš§šš½š² /s š¦š¼š»š“ š”š®šŗš²\n\nšš . `/s bad habits`'
    message.reply_text(
        text=TamilBots, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('š£ BOT UPDATES š£', url='https://t.me/epusthakalaya_bots'),
                    InlineKeyboardButton('āļø ADD ME āļø', url='https://t.me/EmmaMusicBot?startgroup=true')
                ]
            ]
        )
    )

@bot.on_message(filters.command(['s']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('š Searching Your Song...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('Found Nothing. Please Try Again')
            return
    except Exception as e:
        m.edit(
            "āļø Sorry. I couldn't found nothing..\n\nTry Another Keyword or Check Your Spell.\n\nEg.`/s Bad habits`"
        )
        print(str(e))
        return
    m.edit("š šš¢š§šš¢š§š  š ššØš§š  šš„ššš¬š ššš¢š­ ššØš« ššš° ššššØš§šš¬ [ā³ļø](https://telegra.ph/file/aa86463e01037948867c4.mp4)")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'š§ šš¢š­š„š : [{title[:35]}]({link})\nš šš®š«šš­š¢šØš§ : `{duration}`\nš¬ ššØš®š«šš : [Youtube](https://youtu.be/3pN0W4KzzNY)\nšāšØ šš¢šš°š¬ : `{views}`\n\nšµ Uploaded by : @EmmaMusicBot'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('ā šš«š«šØš«\n\n Report This Erorr To Fix @epusthakalaya_bots')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
