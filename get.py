import subprocess
import os
import json
from pytube import Playlist, YouTube

def download_video(video_url, output_directory, playlist_title):
    try:
        yt = YouTube(video_url)
        video_title = yt.title
    except Exception as e:
        if "members-only" in str(e).lower():
            mark_members_only(output_directory, playlist_title)
            return None, None
        else:
            raise e

    playlist_directory = os.path.join(output_directory, playlist_title)
    if not os.path.exists(playlist_directory):
        os.makedirs(playlist_directory)

    file_path = os.path.join(playlist_directory, f'{video_title}.%(ext)s')
    command = ['yt-dlp', '-o', file_path, video_url]

    subprocess.run(command)
    return video_title, file_path
def download_single_video(video_url, output_directory):
    """下載單一YouTube影片到指定資料夾"""
    try:
        yt = YouTube(video_url)
        video_title = yt.title
        file_path = os.path.join(output_directory, f'{video_title}.%(ext)s')
        command = ['yt-dlp', '-o', file_path, video_url]
        subprocess.run(command)
        return video_title, file_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None, None

def process_url(url, output_directory, history_path, exclude_keywords=[]):
    """處理單一影片或播放列表URL"""
    if "list=" in url:
        download_new_videos(url, output_directory, history_path, exclude_keywords)
    else:
        video_title, file_path = download_single_video(url, output_directory)
        if video_title and file_path:
            update_download_history_single(url, video_title, file_path, history_path)
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

def update_download_history(playlist_url, video_title, video_url, file_path, history_path):
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

    if video_title and file_path:
        downloaded_videos[playlist_url].append({'title': video_title, 'url': video_url, 'file_path': file_path})

    with open(history_path, 'w', encoding='utf-8') as file:
        json.dump(downloaded_videos, file, indent=4, ensure_ascii=False)


def mark_members_only(output_directory, playlist_title):
    playlist_directory = os.path.join(output_directory, playlist_title)
    if not os.path.exists(playlist_directory):
        os.makedirs(playlist_directory)

    marker_path = os.path.join(playlist_directory, "members-only.txt")
    with open(marker_path, 'w') as file:
        file.write("This playlist contains members-only content.\n")

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
        video_title, file_path = download_video(video_url, output_directory, playlist.title)
        if video_title is not None and file_path is not None:
            update_download_history(playlist_url, video_title, video_url, file_path, history_path)


# 播放列表 URL
playlist_urls = [
    "https://www.youtube.com/watch?v=gLH-lZ80AOw",
    "https://www.youtube.com/watch?v=RhubhOrB0hE",
    "https://www.youtube.com/watch?v=gNXwUwPkkUo",
    "https://www.youtube.com/watch?v=ltEWFiLzNvQ&list=PL12UaAf_xzfoy0YU-yiND4M-7Mf1-AgW6",
    "https://www.youtube.com/watch?v=vXD89zNSI8I"
]

output_directory = "playlist_downloads"
history_path = "download_history.json"
exclude_keywords = ['預告', '新番']

for url in playlist_urls:
    process_url(url, output_directory, history_path, exclude_keywords)

