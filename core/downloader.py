# core/downloader.py
import os
import webbrowser
import yaml

class Downloader:
    """Opens the official download page of the promoted game."""
    
    def __init__(self):
        with open("config.yaml", "r") as f:
            self.config = yaml.safe_load(f)
        self.download_dir = self.config['download_dir']
        os.makedirs(self.download_dir, exist_ok=True)
    
    def download_game(self, url=None):
        """Open the official download page in browser."""
        if url is None:
            url = self.config['target_game']['download_page']
        print("正在打开暗区突围官网，请自行下载客户端...")
        webbrowser.open(url)
