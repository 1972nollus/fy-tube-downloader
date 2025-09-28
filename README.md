YouTube Audio Downloader Pro 🎵
A modern, feature-rich desktop application for downloading high-quality audio from YouTube videos. Built with Python and CustomTkinter for a sleek, dark-themed interface.

https://img.shields.io/badge/Version-1.0-blue https://img.shields.io/badge/Python-3.8%252B-green https://img.shields.io/badge/License-MIT-yellow

✨ Features
🎵 High-Quality Audio Downloads - Download audio in MP3 or WAV format

📊 Multiple Quality Options - Choose from 128kbps to 320kbps

🔍 Built-in YouTube Search - Search and download directly from the app

🎨 Modern Dark UI - Clean, intuitive interface with smooth animations

📁 Custom Download Location - Choose where to save your files

📊 Real-time Progress - Live download progress with ETA and speed

🚀 Fast & Efficient - Multi-threaded downloading with yt-dlp

💾 Portable - Standalone executable available

🚀 Quick Start
Download Pre-built Executable
Go to the Releases page

Download the latest YouTubeAudioDownloaderPro.exe

Run the executable - no installation required!

Or Build from Source
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Installation Steps
Clone the repository

bash
git clone https://github.com/yourusername/youtube-audio-downloader.git
cd youtube-audio-downloader
Install required dependencies

bash
pip install -r requirements.txt
Run the application

bash
python youtube_downloader.py
📦 Requirements
The application requires the following Python packages:

text
customtkinter>=5.2.0
yt-dlp>=2023.11.16
pillow>=10.0.0
Install all dependencies automatically:

bash
pip install -r requirements.txt
🛠️ Building from Source
For Development
Follow the "Build from Source" steps above

Make sure you have FFmpeg installed on your system

Run python youtube_downloader.py to start development

Creating Standalone Executable
To build your own executable:

Install PyInstaller

bash
pip install pyinstaller
Build the executable

bash
pyinstaller --onefile --windowed --add-data "ffmpeg.exe;." --icon=logo.ico youtube_downloader.py
Find the executable in the dist folder

🎯 How to Use
Basic Download
Paste YouTube URL in the main input field

Select Format - MP3 (compressed) or WAV (lossless)

Choose Quality - 128kbps to 320kbps

Set Download Folder - Default is your Music folder

Click "Download Audio"

Search & Download
Click "Search songs on YouTube"

Enter search term in the search panel

Browse results and click "Copy" on any video

Automatically returns to download view with URL filled

Proceed with download

📁 File Structure
text
youtube-audio-downloader/
├── youtube_downloader.py    # Main application script
├── requirements.txt         # Python dependencies
├── ffmpeg.exe              # FFmpeg binary (for audio conversion)
├── logo.png                # Application logo
├── README.md               # This file
└── build/                  # Build directory (if building)
🔧 Technical Details
GUI Framework: CustomTkinter for modern UI

YouTube Integration: yt-dlp for reliable video extraction

Audio Processing: FFmpeg for format conversion

Threading: Background downloads with real-time UI updates

Packaging: PyInstaller for standalone executables

⚠️ Legal Notice
This software is intended for:

Downloading content you have the rights to

Personal use and archival purposes

Educational and development purposes

Please respect copyright laws and YouTube's Terms of Service. Users are responsible for ensuring they have permission to download any content.

🐛 Troubleshooting
Common Issues
"FFmpeg not found" error

Ensure ffmpeg.exe is in the same directory as the executable

For source version, install FFmpeg system-wide

Download fails

Check your internet connection

Verify the YouTube URL is valid

Try a different video (some may have restrictions)

Application crashes

Ensure you have the latest version

Check Windows Event Viewer for detailed error logs

🤝 Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
yt-dlp - YouTube video downloader

CustomTkinter - Modern UI components

FFmpeg - Audio/video processing
