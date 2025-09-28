import customtkinter as ctk
import threading
import os
import sys
import webbrowser
import yt_dlp
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import math
import time
def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller's onefile mode. """
    try:
        # PyInstaller creates a temporary folder stored in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".") # Use current directory if not packaged
    return os.path.join(base_path, relative_path)

SPACING_SMALL = 2
SPACING_MED = 5
# Set appearance mode and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class YouTubeAudioDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("YouTube Audio Downloader Pro")
        self.geometry("500x720")
        self.resizable(True, True)
        
        self.download_thread = None
        self.is_downloading = False
        self.selected_format = "mp3"
        self.selected_quality = "192"
        self.search_results = []
        
        # Animation variables
        self.animating = False
        self.animation_duration = 400  # ms
        self.animation_step = 16  # ms (~60fps)
        
        # Store URL and other UI state
        self.current_url = ""
        self.current_folder = os.path.join(os.path.expanduser("~"), "Music")
        
        # Create main container as a canvas for sliding
        self.main_canvas = ctk.CTkFrame(self, corner_radius=0)
        self.main_canvas.pack(fill="both", expand=True)
        
        # Create two frames that will slide
        self.compact_frame = ctk.CTkFrame(self.main_canvas, corner_radius=0)
        self.expanded_frame = ctk.CTkFrame(self.main_canvas, corner_radius=0)
        
        # Initially position frames
        self.compact_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.expanded_frame.place(x=500, y=0, relwidth=1, relheight=1)  # Off-screen to the right
        
        self.setup_compact_ui()
        self.setup_expanded_ui()
    
    def ease_in_out_sine(self, t):
        """Sinus easing functie voor vloeiende animatie."""
        return -(math.cos(math.pi * t) - 1) / 2
    
    def slide_frames(self, show_expanded=True, callback=None):
        """Slide animatie tussen de twee frames"""
        if self.animating:
            return
            
        self.animating = True
        start_time = time.time() * 1000  # Current time in milliseconds
        duration_ms = self.animation_duration
        
        # Get current window width
        window_width = self.winfo_width()
        
        def animate():
            if not self.animating:
                return
                
            current_time = time.time() * 1000
            elapsed = current_time - start_time
            progress = min(elapsed / duration_ms, 1.0)
            
            # Easing berekenen
            easing = self.ease_in_out_sine(progress)
            
            if show_expanded:
                # Slide to expanded view: compact moves left, expanded moves in from right
                compact_x = -window_width * easing
                expanded_x = window_width * (1 - easing)
            else:
                # Slide to compact view: compact moves in from left, expanded moves right
                compact_x = -window_width * (1 - easing)
                expanded_x = window_width * easing
            
            # Update frame positions
            self.compact_frame.place(x=compact_x, y=0, relwidth=1, relheight=1)
            self.expanded_frame.place(x=expanded_x, y=0, relwidth=1, relheight=1)
            
            if progress < 1.0:
                self.after(self.animation_step, animate)
            else:
                self.animating = False
                # Final position
                if show_expanded:
                    self.compact_frame.place(x=-window_width, y=0, relwidth=1, relheight=1)
                    self.expanded_frame.place(x=0, y=0, relwidth=1, relheight=1)
                    self.geometry("900x720")  # Resize window for expanded view
                else:
                    self.compact_frame.place(x=0, y=0, relwidth=1, relheight=1)
                    self.expanded_frame.place(x=window_width, y=0, relwidth=1, relheight=1)
                    self.geometry("500x720")  # Resize window for compact view
                
                if callback:
                    callback()
        
        animate()
    
    def setup_compact_ui(self):
        """Setup the compact downloader interface"""
        # Header Frame
        header_frame = ctk.CTkFrame(self.compact_frame, fg_color="transparent")
        header_frame.pack(pady=5, fill="none", padx=30)
        
        try:
            logo_path = resource_path("logo.png")
            self.logo_image = Image.open("logo.png")
            self.logo_image = self.logo_image.resize((400, 135), Image.Resampling.LANCZOS)
            self.logo_ctk_image = ctk.CTkImage(light_image=self.logo_image,
                                             dark_image=self.logo_image,
                                             size=(400, 135))
            self.logo_label = ctk.CTkLabel(header_frame, image=self.logo_ctk_image, text="")
            self.logo_label.pack(side="left", padx=(0, 15))
        except Exception as e:
            print(f"Logo loading error: {e}")
            self.logo_label = ctk.CTkLabel(header_frame, text="🎵", font=ctk.CTkFont(size=40))
            self.logo_label.pack(side="left", padx=(0, 15))
        
        # URL Entry
        url_label = ctk.CTkLabel(self.compact_frame, text="YouTube URL:")
        url_label.pack(pady=(1, 1), anchor="w", padx=20)
        
        self.url_entry = ctk.CTkEntry(self.compact_frame, height=35,
                                    placeholder_text="Paste YouTube URL here...")
        self.url_entry.pack(pady=5, padx=20, fill="x")
        # self.url_entry.insert(0, self.current_url)
        
        # Search Toggle Button
        search_btn_frame = ctk.CTkFrame(self.compact_frame, fg_color="transparent")
        search_btn_frame.pack(pady=5, fill="x", padx=20)
        
        self.search_toggle_btn = ctk.CTkButton(search_btn_frame, 
                                             text="🔍 Or.....Search songs on YouTube",
                                             height=35,
                                             font=ctk.CTkFont(size=12, weight="bold"),
                                             command=lambda: self.slide_frames(True))
        self.search_toggle_btn.pack(fill="x")
        
        # Format and Quality
        settings_frame = ctk.CTkFrame(self.compact_frame, fg_color="transparent")
        settings_frame.pack(pady=5, fill="x", padx=20)
        
        # Format Selection
        format_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        format_frame.pack(side="left", fill="x", expand=True)
        
        format_label = ctk.CTkLabel(format_frame, text="Audio Format:")
        format_label.pack(anchor="w")
        
        format_buttons_frame = ctk.CTkFrame(format_frame, fg_color="transparent")
        format_buttons_frame.pack(anchor="w", pady=5)
        
        self.format_var = ctk.StringVar(value=self.selected_format)
        
        mp3_radio = ctk.CTkRadioButton(format_buttons_frame, text="MP3 Format", 
                                      variable=self.format_var, value="mp3")
        mp3_radio.pack(side="left", padx=(0, 15))
        
        wav_radio = ctk.CTkRadioButton(format_buttons_frame, text="WAV Format", 
                                      variable=self.format_var, value="wav")
        wav_radio.pack(side="left")
        
        # Quality Selection
        quality_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        quality_frame.pack(side="right", fill="x", expand=True)
        
        quality_label = ctk.CTkLabel(quality_frame, text="Audio Quality:")
        quality_label.pack(anchor="w")
        
        self.quality_var = ctk.StringVar(value=self.selected_quality)
        self.quality_options = ctk.CTkOptionMenu(quality_frame, 
                                               values=["128 kbps", "192 kbps", "256 kbps", "320 kbps"],
                                               variable=self.quality_var)
        self.quality_options.pack(anchor="w", pady=5)
        
        # Download Location
        location_label = ctk.CTkLabel(self.compact_frame, text="Download Folder:")
        location_label.pack(pady=(5,2), anchor="w", padx=20)
        
        location_frame = ctk.CTkFrame(self.compact_frame, fg_color="transparent")
        location_frame.pack(pady=5, fill="x", padx=20)
        
        self.location_var = ctk.StringVar(value=self.current_folder)
        self.location_entry = ctk.CTkEntry(location_frame, textvariable=self.location_var)
        self.location_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = ctk.CTkButton(location_frame, text="Browse", width=80, command=self.browse_folder)
        browse_btn.pack(side="left")
        
        # Progress Bar with Percentage
        progress_header_frame = ctk.CTkFrame(self.compact_frame, fg_color="transparent")
        progress_header_frame.pack(pady=(5, 5), fill="x", padx=20)
        
        self.progress_label = ctk.CTkLabel(progress_header_frame, text="Ready to download")
        self.progress_label.pack(side="left", anchor="w")
        
        self.progress_percentage = ctk.CTkLabel(progress_header_frame, text="0%")
        self.progress_percentage.pack(side="right", anchor="e")
        
        self.progress_bar = ctk.CTkProgressBar(self.compact_frame, height=20)
        self.progress_bar.pack(pady=5, fill="x", padx=20)
        self.progress_bar.set(0)
        
        # Download Info
        self.download_info = ctk.CTkLabel(self.compact_frame, text="", 
                                         font=ctk.CTkFont(size=10), text_color="lightblue")
        self.download_info.pack(pady=(0, 10), anchor="w", padx=20)
        
        # Button Frame
        button_frame = ctk.CTkFrame(self.compact_frame, fg_color="transparent")
        button_frame.pack(pady=5, fill="x", padx=20)
        
        self.download_btn = ctk.CTkButton(button_frame, text="Download Audio", height=40,
                                        font=ctk.CTkFont(size=14, weight="bold"),
                                        command=self.start_download)
        self.download_btn.pack(side="left", padx=(0, 10))
        
        self.cancel_btn = ctk.CTkButton(button_frame, text="Cancel Download", height=40,
                                      fg_color="#D9534F", hover_color="#C9302C",
                                      command=self.cancel_download)
        self.cancel_btn.pack(side="left")
        
        # Success Frame
        self.success_frame = ctk.CTkFrame(self.compact_frame, fg_color="green", corner_radius=10)
        self.success_label = ctk.CTkLabel(self.success_frame, text="Download successfully finished!", 
                                         font=ctk.CTkFont(weight="bold"))
        self.success_label.pack(side="left", padx=10, pady=5)
        
        self.open_folder_btn = ctk.CTkButton(self.success_frame, text="Go to Download Folder", 
                                           width=120, height=30, command=self.open_download_folder)
        self.open_folder_btn.pack(side="left", padx=10, pady=5)
        
        # Status Text
        self.status_text = ctk.CTkTextbox(self.compact_frame, height=80, font=ctk.CTkFont(size=10))
        self.status_text.pack(pady=5, fill="x", padx=20)
        self.status_text.insert("1.0", "Enter a YouTube URL or click the search button to find songs")
        self.status_text.configure(state="disabled")
        
        self.success_frame.pack_forget()
    
    def setup_expanded_ui(self):
        """Setup the expanded UI with search panel taking the full window"""
        # Clear the expanded frame to start fresh
        for widget in self.expanded_frame.winfo_children():
            widget.destroy()

        # Create a main frame for the expanded view that fills the entire window
        main_expanded_frame = ctk.CTkFrame(self.expanded_frame, corner_radius=0)
        main_expanded_frame.pack(fill="both", expand=True)

        # Create a top bar with a button to go back to the compact view
        top_bar_frame = ctk.CTkFrame(main_expanded_frame, fg_color="transparent", height=40)
        top_bar_frame.pack(fill="x", padx=20, pady=5)

        back_button = ctk.CTkButton(top_bar_frame, 
                                    text="← Back to Downloader", 
                                    height=30,
                                    font=ctk.CTkFont(size=12, weight="bold"),
                                    command=lambda: self.slide_frames(False))
        back_button.pack(side="left")

        # Setup search content to fill the remaining space
        self.setup_search_content(main_expanded_frame)
    
    def setup_compact_left_content(self, parent):
        """Setup compact downloader content in left panel of expanded view"""
        # Header
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(pady=5, fill="x", padx=20)
        
        try:
            logo_small = self.logo_image.resize((60, 60), Image.Resampling.LANCZOS)
            self.logo_ctk_image_small = ctk.CTkImage(light_image=logo_small,
                                                   dark_image=logo_small,
                                                   size=(60, 60))
            self.logo_label_small = ctk.CTkLabel(header_frame, image=self.logo_ctk_image_small, text="")
            self.logo_label_small.pack(side="left", padx=(0, 10))
        except:
            self.logo_label_small = ctk.CTkLabel(header_frame, text="🎵", font=ctk.CTkFont(size=30))
            self.logo_label_small.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(header_frame, text="YouTube Downloader", 
                                 font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(side="left", fill="both", expand=True)
        
        # URL Entry
        url_label = ctk.CTkLabel(parent, text="YouTube URL:")
        url_label.pack(pady=(5, 5), anchor="w", padx=20)
        
        self.url_entry_expanded = ctk.CTkEntry(parent, height=35, 
                                             placeholder_text="Paste YouTube URL here...")
        self.url_entry_expanded.pack(pady=5, padx=20, fill="x")
        self.url_entry_expanded.insert(0, self.current_url)
        
        # Close Search Panel Button
        close_btn = ctk.CTkButton(parent, text="✕ Close Search Panel", height=35,
                                font=ctk.CTkFont(size=12, weight="bold"),
                                command=lambda: self.slide_frames(False))
        close_btn.pack(pady=5, fill="x", padx=20)
        
        # Sync the URL entries
        self.url_entry_expanded.bind("<KeyRelease>", self.sync_url_entries)
        self.url_entry.bind("<KeyRelease>", self.sync_url_entries)
        
        # Rest of the compact UI elements would go here...
        # (Format, Quality, Location, Progress, etc.)
        
    def sync_url_entries(self, event=None):
        """Keep both URL entries in sync"""
        if event.widget == self.url_entry:
            self.current_url = self.url_entry.get()
            self.url_entry_expanded.delete(0, "end")
            self.url_entry_expanded.insert(0, self.current_url)
        elif event.widget == self.url_entry_expanded:
            self.current_url = self.url_entry_expanded.get()
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, self.current_url)
    
    def setup_search_content(self, parent):
        """Setup search content to fill the given parent frame"""
        # Search Title
        search_title = ctk.CTkLabel(parent, text="YouTube Search", 
                                  font=ctk.CTkFont(size=22, weight="bold"))
        search_title.pack(pady=5)

        # Search Entry Frame
        search_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_frame.pack(pady=5, fill="x", padx=50)  # Add horizontal padding

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search for songs...", height=40)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_youtube())

        self.search_btn = ctk.CTkButton(search_frame, text="Search", width=100, height=40, command=self.search_youtube)
        self.search_btn.pack(side="left")

        # Results Label
        self.results_label = ctk.CTkLabel(parent, text="Enter a search term above", 
                                         font=ctk.CTkFont(size=12))
        self.results_label.pack(pady=5)

        # Results Frame - This will now expand to fill the available space
        self.results_frame = ctk.CTkScrollableFrame(parent)
        self.results_frame.pack(pady=5, fill="both", expand=True, padx=20)  # Fill and expand

        # Initial message in the results frame
        no_results = ctk.CTkLabel(self.results_frame, text="Search results will appear here",
                                 text_color="gray")
        no_results.pack(pady=30)
    
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.current_folder)
        if folder:
            self.current_folder = folder
            self.location_var.set(folder)
    
    def search_youtube(self):
        """Search for YouTube videos"""
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        self.search_btn.configure(state="disabled", text="Searching...")
        thread = threading.Thread(target=self.perform_search, args=(query,))
        thread.daemon = True
        thread.start()
    
    def perform_search(self, query):
        """Perform YouTube search in background thread"""
        try:
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'force_json': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_results = ydl.extract_info(f"ytsearch10:{query}", download=False)
                self.after(0, self.display_search_results, search_results['entries'])
                
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Search Error", f"Search failed: {str(e)}"))
        finally:
            self.after(0, lambda: self.search_btn.configure(state="normal", text="Search"))
    
    def display_search_results(self, results):
        """Display search results in the UI"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        if not results:
            no_results = ctk.CTkLabel(self.results_frame, text="No results found", text_color="gray")
            no_results.pack(pady=30)
            return
        
        self.results_label.configure(text=f"Found {len(results)} results")
        
        for i, result in enumerate(results):
            result_frame = ctk.CTkFrame(self.results_frame, corner_radius=5)
            result_frame.pack(fill="x", pady=5, padx=5)
            
            title = result.get('title', 'Unknown Title')
            if len(title) > 50:
                title = title[:47] + "..."
            
            title_label = ctk.CTkLabel(result_frame, text=title, font=ctk.CTkFont(weight="bold"))
            title_label.pack(anchor="w", padx=10, pady=(5, 0))
            
            url_frame = ctk.CTkFrame(result_frame, fg_color="transparent")
            url_frame.pack(fill="x", padx=10, pady=5)
            
            url = f"https://youtube.com/watch?v={result['id']}"
            url_label = ctk.CTkLabel(url_frame, text="📎 Copy URL", text_color="lightblue", 
                                   font=ctk.CTkFont(size=10), cursor="hand2")
            url_label.pack(side="left")
            url_label.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
            
            copy_btn = ctk.CTkButton(url_frame, text="Copy", width=50, height=20,
                                   font=ctk.CTkFont(size=9),
                                   command=lambda u=url: self.copy_to_url_entry(u))
            copy_btn.pack(side="right", padx=(10, 0))
    
    def copy_to_url_entry(self, url):
        """Copy URL to the entry field and auto-close search panel"""
        try:
            self.current_url = url
            if hasattr(self, 'url_entry') and self.url_entry.winfo_exists():
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, url)
            if hasattr(self, 'url_entry_expanded') and self.url_entry_expanded.winfo_exists():
                self.url_entry_expanded.delete(0, "end")
                self.url_entry_expanded.insert(0, url)
            
            self.status_text.configure(state="normal")
            self.status_text.delete("1.0", "end")
            self.status_text.insert("1.0", f"URL copied: {url}")
            self.status_text.configure(state="disabled")
            
            # Auto-close search panel with slide animation
            self.slide_frames(False)
                
        except Exception as e:
            print(f"Error in copy_to_url_entry: {e}")
        
    def open_download_folder(self):
        """Open the download folder in file explorer"""
        download_folder = self.location_var.get()
        if os.path.exists(download_folder):
            os.startfile(download_folder)
        else:
            messagebox.showerror("Error", "Download folder doesn't exist")
    
    def show_success_message(self):
        """Show success message after download"""
        self.success_frame.pack(pady=5, fill="x", padx=20)
    
    def hide_success_message(self):
        """Hide success message"""
        self.success_frame.pack_forget()
    
    def update_status(self, message):
        """Update status text"""
        self.after(0, self._update_status_gui, message)
    
    def _update_status_gui(self, message):
        """Update status text in GUI thread"""
        self.status_text.configure(state="normal")
        self.status_text.delete("1.0", "end")
        self.status_text.insert("1.0", message)
        self.status_text.configure(state="disabled")
        self.hide_success_message()
    
    def update_progress(self, value, percentage_text="", info_text=""):
        """Update progress bar with percentage and info"""
        self.after(0, lambda: self._update_progress_gui(value, percentage_text, info_text))
    
    def _update_progress_gui(self, value, percentage_text, info_text):
        """Update progress bar in GUI thread"""
        self.progress_bar.set(min(max(value, 0.0), 1.0))
        if percentage_text:
            self.progress_percentage.configure(text=percentage_text)
        if info_text:
            self.download_info.configure(text=info_text)
    
    def start_download(self):
        """Start download process"""
        if self.is_downloading:
            return
            
        url = self.current_url.strip()
        if not url:
            self.update_status("Error: Please enter a YouTube URL")
            return
        
        format_type = self.format_var.get()
        quality = self.quality_var.get().split(" ")[0]
        
        self.is_downloading = True
        self.download_btn.configure(state="disabled")
        self.hide_success_message()
        self.update_status(f"Starting {format_type.upper()} download at {quality}kbps...")
        self.update_progress(0.1, "10%", "Initializing download...")
        
        self.download_thread = threading.Thread(target=self.download_audio, args=(url, format_type, quality))
        self.download_thread.daemon = True
        self.download_thread.start()
    
    def cancel_download(self):
        """Cancel current download"""
        self.is_downloading = False
        self.update_status("Download cancelled by user.")
        self.update_progress(0, "0%", "Download cancelled")
        self.reset_ui()
    
    def reset_ui(self):
        """Reset UI after download"""
        self.is_downloading = False
        self.download_btn.configure(state="normal")
        self.update_progress(0, "0%", "")
    
    def download_audio(self, url, format_type, quality):
        """Download audio with real-time progress"""

        try:
            download_folder = self.location_var.get()
            os.makedirs(download_folder, exist_ok=True)
            ffmpeg_path = resource_path("ffmpeg.exe")
            if format_type == "wav":
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'wav',
                    }],
                    'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
                    'quiet': True,
                    'progress_hooks': [self.progress_hook],
                }
            else:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality,
                    }],
                    'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
                    'quiet': True,
                    'progress_hooks': [self.progress_hook],
                    'ffmpeg_location': ffmpeg_path # Point yt-dlp to the bundled binary:cite[8]
                }

            self.update_status("Getting video information...")
            self.update_progress(0.05, "5%", "Fetching video info...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown Title')

                self.update_status(f"Downloading: {title}")
                self.update_progress(0.1, "10%", "Starting download...")

                ydl.download([url])

            if not self.is_downloading:
                return

            self.update_progress(1.0, "100%", "Download complete!")
            success_msg = f"Download completed!\nFile saved in: {download_folder}"
            self.update_status(success_msg)

            self.after(0, self.show_success_message)

        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            self.update_progress(0, "0%", f"Error: {str(e)}")
        finally:
            if self.is_downloading:
                self.after(0, self.reset_ui)
    
    def progress_hook(self, d):
        """Progress hook for real-time updates"""
        if d['status'] == 'downloading':
            if d.get('total_bytes_estimate'):
                progress = d['downloaded_bytes'] / d['total_bytes_estimate']
            elif d.get('total_bytes'):
                progress = d['downloaded_bytes'] / d['total_bytes']
            else:
                progress = 0.5

            percentage = progress * 100
            percentage_text = f"{percentage:.1f}%"
            
            eta = d.get('eta')
            speed = d.get('speed')
            
            eta_str = f"ETA: {self.format_eta(eta)}" if eta else ""
            speed_str = f"Speed: {self.format_speed(speed)}" if speed else ""
            
            info_text = f"{eta_str} {speed_str}".strip()
            
            self.update_progress(progress, percentage_text, info_text)
            
            filename = d.get('filename', 'Unknown file')
            if len(filename) > 50:
                filename = os.path.basename(filename)[:47] + "..."
            self.update_status(f"Downloading: {filename}")

        elif d['status'] == 'finished':
            self.update_progress(1.0, "100%", "Processing file...")
            self.update_status("Download complete, processing file...")
    
    def format_eta(self, seconds):
        """Format ETA to readable string"""
        if not seconds:
            return ""
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h}h {m}m {s}s"
        elif m > 0:
            return f"{m}m {s}s"
        return f"{s}s"

    def format_speed(self, speed):
        """Format speed to readable string"""
        if not speed:
            return ""
        for unit in ['B/s', 'KB/s', 'MB/s', 'GB/s']:
            if speed < 1024:
                return f"{speed:.2f} {unit}"
            speed /= 1024
        return f"{speed:.2f} TB/s"
    
    def on_closing(self):
        """Handle application shutdown"""
        self.is_downloading = False
        self.animating = False
        if self.download_thread and self.download_thread.is_alive():
            self.download_thread.join(timeout=2)
        self.destroy()

if __name__ == "__main__":
    try:
        app = YouTubeAudioDownloader()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except KeyboardInterrupt:
        print("Application interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")