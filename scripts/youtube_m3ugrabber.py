#! /usr/bin/python3

import requests
import os
import sys
import subprocess

banner = r'''
#########################################################################
#      ____            _           _   __  __                           #
#     |  _ \ _ __ ___ (_) ___  ___| |_|  \/  | ___   ___  ___  ___      #
#     | |_) | '__/ _ \| |/ _ \/ __| __| |\/| |/ _ \ / _ \/ __|/ _ \     #
#     |  __/| | | (_) | |  __/ (__| |_| |  | | (_) | (_) \__ \  __/     #
#     |_|   |_|  \___// |\___|\___|\__|_|  |_|\___/ \___/|___/\___|     #
#                   |__/                                                #
#                                                                       #
#########################################################################
'''

windows = False
if 'win' in sys.platform:
    windows = True

def download_youtube_video(url, resolution='2160'):
    # 尝试首先获取2K视频，如果没有则获取最高分辨率
    format_string = f'(bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}])/best'
    command = [
        'yt-dlp',
        '-f', format_string,
        '--get-url',
        url
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def grab(url):
    try:
        video_url = download_youtube_video(url)
        if video_url:
            print(video_url)
        else:
            print('https://raw.githubusercontent.com/gyssi007/YouTube_to_m3u/main/assets/moose_na.m3u')
    except Exception as e:
        print('https://raw.githubusercontent.com/gyssi007/YouTube_to_m3u/main/assets/moose_na.m3u')

print('#EXTM3U x-tvg-url="https://github.com/botallen/epg/releases/download/latest/epg.xml"')
print(banner)

with open('../youtube_channel_info.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            ch_name = line[0].strip()
            grp_title = line[1].strip().title()
            tvg_logo = line[2].strip()
            tvg_id = line[3].strip()
            print(f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}')
        else:
            grab(line)  # 这里指定分辨率为2K
            
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
