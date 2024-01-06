import subprocess
import os
import json
from pytube import Playlist, YouTube
import time
import logging

# 日誌配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='download_log.txt',
                    filemode='a')

def download_with_retry(video_url, output_directory, playlist_title, max_retries=3):
    retry_count = 0
    while retry_count < max_retries:
        try:
            video_title, file_path = download_video(video_url, output_directory, playlist_title)
            if video_title is not None and file_path is not None:
                logging.info(f"成功下載視頻: {video_url}")
                return video_title, file_path
        except Exception as e:
            if "premieres in" in str(e).lower():  # 檢查是否是未來首播錯誤
                logging.warning(f"視頻 {video_url} 尚未開始，將在一小時後重試")
                retry_count += 1
                time.sleep(60 * 60)  # 等待一小時後重試
            else:
                logging.error(f"下載視頻時發生錯誤: {str(e)}")
                raise e
    logging.error(f"無法下載視頻 {video_url}，已達最大重試次數")
    return None, None

def download_video(video_url, output_directory, playlist_title):
    try:
        yt = YouTube(video_url)
        video_title = yt.title
        logging.info(f"正在下載視頻: {video_url}")
        # ... 程式碼邏輯 ...
    except Exception as e:
        logging.error(f"下載視頻時發生錯誤: {str(e)}")
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
        logging.error(f"Error downloading single video: {e}")
        return None, None

def process_url(url, output_directory, history_path, exclude_keywords=[]):
    if "list=" in url:
        download_new_videos(url, output_directory, history_path, exclude_keywords)
    else:
        video_title, file_path = download_with_retry(url, output_directory, "Single Video", max_retries=3)
        if video_title and file_path:
            update_download_history_single(url, video_title, file_path, history_path)

def update_download_history_single(video_url, video_title, file_path, history_path):
    if not os.path.exists(history_path) or os.stat(history_path).st_size == 0:
        downloaded_videos = {}
    else:
        with open(history_path, 'r', encoding='utf-8') as file:
            try:
                downloaded_videos = json.load(file)
            except json.JSONDecodeError:
                logging.error(f"JSON decode error when updating download history for single video")
                downloaded_videos = {}

    downloaded_videos[video_url] = {'title': video_title, 'file_path': file_path}

    with open(history_path, 'w', encoding='utf-8') as file:
        json.dump(downloaded_videos, file, indent=4, ensure_ascii=False)

def get_new_videos(playlist_url, history_path):
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
    filtered_videos = []
    for video in playlist.videos:
        if not any(keyword.lower() in video.title.lower() for keyword in keywords):
            filtered_videos.append(video.watch_url)
    return filtered_videos

def download_new_videos(playlist_url, output_directory, history_path, exclude_keywords):
    playlist = Playlist(playlist_url)
    new_videos = get_new_videos(playlist_url, history_path)
    filtered_videos = filter_videos_by_keyword(playlist, exclude_keywords)
    logging.info(f"正在處理播放列表：{playlist.title}")
    logging.info(f"即將下載的新影片：{[video for video in filtered_videos]}")

    for video_url in filtered_videos:
        video_title, file_path = download_video(video_url, output_directory, playlist.title)
        if video_title is not None and file_path is not None:
            update_download_history(playlist_url, video_title, video_url, file_path, history_path)

def read_playlist_urls(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

if __name__ == "__main__":
    output_directory = "playlist_downloads"
    history_path = "download_history.json"
    exclude_keywords = ['預告', '新番']
    playlist_file = "playlists.txt"

    playlist_urls = read_playlist_urls(playlist_file)
    for url in playlist_urls:
        process_url(url, output_directory, history_path, exclude_keywords)
