# YouTube Audio Downloader Pro 🎵

A modern, feature-rich desktop application for downloading high-quality audio from YouTube videos.  
Built with **Python** and **CustomTkinter** for a sleek, dark-themed interface.

![Version](https://img.shields.io/badge/Version-1.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🎵 **High-Quality Audio Downloads** – Download audio in MP3 or WAV format  
- 📊 **Multiple Quality Options** – Choose from 128kbps to 320kbps  
- 🔍 **Built-in YouTube Search** – Search and download directly from the app  
- 🎨 **Modern Dark UI** – Clean, intuitive interface with smooth animations  
- 📁 **Custom Download Location** – Choose where to save your files  
- 📊 **Real-time Progress** – Live download progress with ETA and speed  
- 🚀 **Fast & Efficient** – Multi-threaded downloading with `yt-dlp`  
- 💾 **Portable** – Standalone executable available  

---

## 🚀 Quick Start

### Download Pre-built Executable
1. Go to the [Releases page](https://github.com/1972nollus/fy-tube-downloader/releases/tag/v1.0.0)
2. Download the latest `YouTubeAudioDownloaderPro.exe`  
3. Run the executable – no installation required!  

### Build from Source

**Prerequisites**
- Python 3.8 or higher  
- pip (Python package manager)  

**Installation Steps**
```bash
git clone https://github.com/1972nollus/fy-tube-downloader.git
cd fy-tube-downloader
pip install -r requirements.txt
python fy-tube-downloader.py
```
📦 Requirements
The application requires the following Python packages:
- customtkinter>=5.2.0
- yt-dlp>=2023.11.16
- pillow>=10.0.0
And manual install :
- ffmpeg ( for windows download and set path to /fy-tube-downloader : https://ffmpeg.org/download.html )
- put ffmeg.exe in /fy-tube-downloader folder 
📦Install all dependencies automatically:
```bash
pip install -r requirements.txt
``` 
🛠️ Building from Source

Make sure you have FFmpeg installed on your system !

Run:
```bash
python fy-tube-downloader.py
``` 
Creating Standalone Executable
Install PyInstaller:

````bash
pip install pyinstaller
````
Build the executable:
```bash
pyinstaller --onefile --windowed --add-data "ffmpeg.exe;." --icon=logo.ico fy-tube-downloader.py
```

Find the executable in the dist/ folder

🎯 How to Use
      Basic Download :
      - Paste YouTube URL in the main input field
      And
      - Select Format – MP3 (compressed) or WAV (lossless)
      - Choose Quality – 128kbps to 320kbps
      - Set Download Folder – default is your Music folder
      - Click "Download Audio"
    
🎯 Search & Download
      - Click "Search songs on YouTube"
      - Enter search term in the search panel
      - Browse results and click "Copy" on any video. Search window closes automaticly 
      - The URL is auto-filled in the downloader
      - CLick "Download Audio"

📁 File Structure
````bash
fy-tube-downloader/
├── fy-tube-downloader.py   # Main application script
├── requirements.txt        # Python dependencies
├── ffmpeg.exe              # FFmpeg binary (for audio conversion) - put the exe manually in the folder.
├── logo.png                # Application logo
├── README.md               # This file
└── build/                  # Build directory (if building)
````
🔧 Technical Details
  - GUI Framework: CustomTkinter
  - YouTube Integration: yt-dlp
  - Audio Processing: FFmpeg
  - Threading: Background downloads with real-time UI updates
  - Packaging: PyInstaller

⚠️ Legal Notice
  - This software is intended for:
  - Downloading content you have the rights to
  - Personal use and archival purposes
  - Educational and development purposes

👉 Please respect copyright laws and YouTube's Terms of Service.
  -Users are responsible for ensuring they have permission to download any content.

🐛 Troubleshooting
  "FFmpeg not found" error :
  - Ensure ffmpeg.exe is in the same directory as the executable.
  - For source version, install FFmpeg system-wide.

  Download fails :
  - Check your internet connection
  - Verify the YouTube URL is valid
  - Try a different video (some may have restrictions)

  Application crashes
  - Check Windows Event Viewer for error logs
  - 
🤝 Contributing
  - Contributions are welcome!

Fork the repository

Create your feature branch
```bash
git checkout -b feature/AmazingFeature
```
Commit your changes
```bash
git commit -m "Add some AmazingFeature"
```
Push to the branch
```bash
git push origin feature/AmazingFeature
```
Open a Pull Request

📄 License
- This project is licensed under the MIT License – see the LICENSE file for details.

🙏 Acknowledgments
  - yt-dlp – YouTube video downloader
  - CustomTkinter – Modern UI components
  - FFmpeg – Audio/video processing
