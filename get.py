import subprocess
import os
import json
from pytube import Playlist

def download_video(video_url, output_directory, playlist_title):
    """使用 yt-dlp 下載單個YouTube影片到指定播放列表的資料夾"""
    playlist_directory = os.path.join(output_directory, playlist_title)
    if not os.path.exists(playlist_directory):
        os.makedirs(playlist_directory)

    command = [
        'yt-dlp',
        '-o', os.path.join(playlist_directory, '%(title)s.%(ext)s'),
        video_url
    ]

    subprocess.run(command)

def get_new_videos(playlist_url, history_path):
    """獲取新影片列表"""
    playlist = Playlist(playlist_url)
    if not os.path.exists(history_path):
        return playlist.video_urls  # 如果沒有歷史記錄，返回所有影片

    with open(history_path, 'r') as file:
        downloaded_videos = json.load(file).get(playlist_url, [])

    new_videos = [video for video in playlist.video_urls if video not in downloaded_videos]
    return new_videos

def update_download_history(playlist_url, video_url, history_path):
    """更新下載歷史記錄"""
    if not os.path.exists(history_path):
        downloaded_videos = {}
    else:
        with open(history_path, 'r') as file:
            downloaded_videos = json.load(file)

    if playlist_url not in downloaded_videos:
        downloaded_videos[playlist_url] = []

    downloaded_videos[playlist_url].append(video_url)

    with open(history_path, 'w') as file:
        json.dump(downloaded_videos, file)

def download_new_videos(playlist_url, output_directory, history_path):
    """自動下載新影片並更新歷史記錄"""
    new_videos = get_new_videos(playlist_url, history_path)
    playlist = Playlist(playlist_url)
    print(f"正在處理播放列表：{playlist.title}")
    print(f"即將下載的新影片：{new_videos}")
    for video_url in new_videos:
        download_video(video_url, output_directory, playlist.title)
        update_download_history(playlist_url, video_url, history_path)


# 播放列表 URL
playlist_urls = [
    "https://www.youtube.com/watch?v=1H2cyhWYXrE&list=PL12UaAf_xzfpHlIkQd-mHKo6pBQYEPDV-",
    "https://www.youtube.com/watch?v=Y3roUIXa2Fg&list=PL12UaAf_xzfpv_EIuCk3K-WwFSDdYvJiE",
    "https://www.youtube.com/watch?v=fxOE6_bJYrs&list=PL12UaAf_xzfoLF2J08Cpz5Ag2S4mK1J9A",
    "https://www.youtube.com/watch?v=6Lb6NVoF4Jc&list=PL12UaAf_xzfp_uOtg2M8yHR8P6sTzN0ot",
    "https://www.youtube.com/watch?v=Atp1KzTs4vQ&list=PL12UaAf_xzfqaNNTfkEsrOmfkYtHVZzYl",
    "https://www.youtube.com/watch?v=BKtsKzr4S24&list=PL12UaAf_xzfrBTYxrhXL6TVvROBkpfQ7K"
]

output_directory = "playlist_downloads"
history_path = "download_history.json"

for playlist_url in playlist_urls:
    download_new_videos(playlist_url, output_directory, history_path)
