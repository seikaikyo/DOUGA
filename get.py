import subprocess
import os
import json
from pytube import Playlist

def download_video(video_url, output_directory, playlist_title):
    """使用 yt-dlp 下載單個YouTube影片到指定播放列表的資料夾，並返回檔案路徑"""
    playlist_directory = os.path.join(output_directory, playlist_title)
    if not os.path.exists(playlist_directory):
        os.makedirs(playlist_directory)

    file_path = os.path.join(playlist_directory, '%(title)s.%(ext)s')
    command = [
        'yt-dlp',
        '-o', file_path,
        video_url
    ]

    subprocess.run(command)
    return file_path

def get_new_videos(playlist_url, history_path):
    """獲取新影片列表"""
    playlist = Playlist(playlist_url)
    
    if not os.path.exists(history_path) or os.stat(history_path).st_size == 0:
        downloaded_videos = []
    else:
        with open(history_path, 'r') as file:
            try:
                downloaded_videos = json.load(file).get(playlist_url, [])
            except json.JSONDecodeError:
                downloaded_videos = []

    new_videos = [video for video in playlist.video_urls if video not in downloaded_videos]
    return new_videos

def update_download_history(playlist_url, video_url, file_path, history_path):
    """更新下載歷史記錄，包括檔案路徑"""
    if not os.path.exists(history_path) or os.stat(history_path).st_size == 0:
        downloaded_videos = {}
    else:
        with open(history_path, 'r') as file:
            try:
                downloaded_videos = json.load(file)
            except json.JSONDecodeError:
                downloaded_videos = {}

    if playlist_url not in downloaded_videos:
        downloaded_videos[playlist_url] = []

    downloaded_videos[playlist_url].append({'url': video_url, 'file_path': file_path})

    with open(history_path, 'w') as file:
        json.dump(downloaded_videos, file)

def filter_videos_by_keyword(playlist, keywords):
    """過濾掉含有特定關鍵字的影片"""
    filtered_videos = []
    for video in playlist.videos:
        if not any(keyword.lower() in video.title.lower() for keyword in keywords):
            filtered_videos.append(video.watch_url)
    return filtered_videos

def download_new_videos(playlist_url, output_directory, history_path, exclude_keywords):
    """自動下載新影片並更新歷史記錄，排除包含特定關鍵字的影片"""
    playlist = Playlist(playlist_url)
    new_videos = get_new_videos(playlist_url, history_path)
    filtered_videos = filter_videos_by_keyword(playlist, exclude_keywords)
    print(f"正在處理播放列表：{playlist.title}")
    print(f"即將下載的新影片：{[video for video in filtered_videos]}")
    
    for video_url in filtered_videos:
        file_path = download_video(video_url, output_directory, playlist.title)
        update_download_history(playlist_url, video_url, file_path, history_path)

# 播放列表 URL
playlist_urls = [
    "https://www.youtube.com/watch?v=1H2cyhWYXrE&list=PL12UaAf_xzfpHlIkQd-mHKo6pBQYEPDV-",
    "https://www.youtube.com/watch?v=Y3roUIXa2Fg&list=PL12UaAf_xzfpv_EIuCk3K-WwFSDdYvJiE",
    "https://www.youtube.com/watch?v=fxOE6_bJYrs&list=PL12UaAf_xzfoLF2J08Cpz5Ag2S4mK1J9A",
    "https://www.youtube.com/watch?v=6Lb6NVoF4Jc&list=PL12UaAf_xzfp_uOtg2M8yHR8P6sTzN0ot",
    "https://www.youtube.com/watch?v=Atp1KzTs4vQ&list=PL12UaAf_xzfqaNNTfkEsrOmfkYtHVZzYl",
    "https://www.youtube.com/watch?v=BKtsKzr4S24&list=PL12UaAf_xzfrBTYxrhXL6TVvROBkpfQ7K",
    "https://www.youtube.com/watch?v=PMTx3gfcd4E&list=PLC18xlbCdwtQGlyMs9SVOYp2lP-myamDL",
    "https://www.youtube.com/watch?v=q83aziWwXak&list=PLC18xlbCdwtQkrUFepeQOELa13PBFFOPE",
    "https://www.youtube.com/watch?v=2bM7cx1zV-Q&list=PLC18xlbCdwtT-lLfBkMTj8sAdhKrTT14s",
    "https://www.youtube.com/watch?v=sP55jv-Hrms&list=PLC18xlbCdwtSoMtcbwQJQijWBKQTKhuaB",
    "https://www.youtube.com/watch?v=gLkCOrQzZjg&list=PLC18xlbCdwtT8MiM0FpwyVmE6i5gdD2Bj",
    "https://www.youtube.com/watch?v=GizKkKmI_hA&list=PLC18xlbCdwtSoOqDJHzgkYqIc9aJ0Jd7F",
    "https://www.youtube.com/watch?v=bAABHgjmbLg&list=PLC18xlbCdwtSow1ByrUAkL12nhNTDDmvx"
]

output_directory = "playlist_downloads"
history_path = "download_history.json"

exclude_keywords = ['預告','新番']

for playlist_url in playlist_urls:
    download_new_videos(playlist_url, output_directory, history_path, exclude_keywords)
