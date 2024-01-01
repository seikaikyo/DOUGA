# YouTube Playlist Downloader

This Python script downloads videos from specified YouTube playlists, ensuring that only new videos since the last download are fetched. It now supports reading playlist URLs from an external file, enhancing flexibility and ease of management.

## Features

- Automatically downloads new videos from YouTube playlists.
- Organizes videos into separate folders for each playlist.
- Maintains a download history to prevent redundancy, including the file path. History now correctly displays non-ASCII characters.
- Reads playlist URLs from an external file, making it easier to update and manage.

## Recent Changes

- Enhanced JSON output to support Unicode characters, allowing correct display of non-ASCII characters like Chinese.
- Fixed a JSON parsing error and enhanced error handling for more reliable operations.
- Improved compatibility with various playlist formats.
- Added functionality to read playlist URLs from an external file.

## Usage

1. Install `pytube` and `yt-dlp` in your environment.
2. Add the URLs of the YouTube playlists you wish to download to an external file.
3. Run the script to download new videos from these playlists.

## Dependencies

- Python 3
- pytube
- yt-dlp

## Contributing

Contributions are welcome. Please open an Issue for discussion before making any significant changes.

## License

[MIT](https://choosealicense.com/licenses/mit/)

# YouTube プレイリストダウンローダー

この Python スクリプトは、指定された YouTube プレイリストから動画をダウンロードし、最後のダウンロード以降の新しい動画のみを取得します。外部ファイルからプレイリスト URL を読み込むようになり、柔軟性と管理のしやすさが向上しました。

## 特徴

- YouTube プレイリストから新しい動画を自動的にダウンロードします。
- 各プレイリストの動画を別々のフォルダに整理します。
- 重複を避けるためのダウンロード履歴を維持します。履歴は非 ASCII 文字を正しく表示します。
- 外部ファイルからプレイリスト URL を読み込み、更新や管理を容易にします。

## 最近の変更

- Unicode 文字をサポートするように JSON 出力を強化し、中国語などの非 ASCII 文字を正しく表示できるようにしました。
- JSON 解析エラーを修正し、エラー処理を強化してより信頼性の高い操作が可能になりました。
- さまざまなプレイリスト形式との互換性を改善しました。
- 外部ファイルからプレイリスト URL を読み込む機能を追加しました。

## 使い方

1. 環境に `pytube` と `yt-dlp` をインストールします。
2. ダウンロードしたい YouTube プレイリストの URL を外部ファイルに追加します。
3. このスクリプトを実行して、これらのプレイリストから新しい動画をダウンロードします。

## 依存関係

- Python 3
- pytube
- yt-dlp

## 貢献

貢献を歓迎します。重要な変更を加える前に、議論のために Issue を開いてください。

## ライセンス

[MIT](https://choosealicense.com/licenses/mit/)

# YouTube 播放列表下載器

這個 Python 腳本用於從指定的 YouTube 播放列表中下載影片，確保自上次下載以來只獲取新影片。現在支持從外部檔案讀取播放列表 URL，增強了靈活性和易於管理。

## 功能

- 自動從 YouTube 播放列表中下載新影片。
- 為每個播放列表中的影片在不同資料夾進行整理。
- 維護下載歷史以避免重複，包括檔案路徑。歷史記錄現在可以正確顯示非 ASCII 字符。
- 從外部檔案讀取播放列表 URL，使更新和管理更加方便。

## 最近變更

- 增強了 JSON 輸出以支持 Unicode 字符，允許正確顯示中文等非 ASCII 字符。
- 修正了 JSON 解析錯誤並增強了錯誤處理，確保更可靠的操作。
- 改進了對不同播放列表格式的兼容性。
- 新增從外部檔案讀取播放列表 URL 的功能。

## 使用方法

1. 在您的環境中安裝 `pytube` 和 `yt-dlp`。
2. 在外部檔案中列出您想要下載的 YouTube 播放列表 URL。
3. 執行腳本以從這些播放列表中下載新影片。

## 依賴

- Python 3
- pytube
- yt-dlp

## 貢獻

歡迎您的貢獻！如需變更，請先開啟一個 Issue 進行討論。

## 授權

[MIT](https://choosealicense.com/licenses/mit/)
