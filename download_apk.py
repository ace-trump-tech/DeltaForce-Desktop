#!/usr/bin/env python3
"""
Enhanced Hugging Face File Downloader
Features:
1. Download any file from Hugging Face repo (resume, retry, progress)
2. Support CLI arguments, config file, environment variables (Token)
3. Support file integrity check (MD5)
4. Built-in Base64 decoder, decode and highlight preset message at startup
5. Support multi-threaded chunk download (acceleration)
6. Detailed logging
"""

import os
import sys
import time
import json
import hashlib
import logging
import argparse
import base64
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict

import requests
from tqdm import tqdm

# ==================== Constants ====================
DEFAULT_CONFIG_PATH = "hf_downloader.json"
DEFAULT_CHUNK_SIZE = 8192
DEFAULT_NUM_THREADS = 4
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 2
DEFAULT_TIMEOUT = 30

BASE64_SECRET = "5L2g6ICD5b6X5LiK5aSn5a2m5ZCX77yM5L2g5bCx57uZ5LiJ6KeS5rSy5byA5oyC"

# ==================== Logging Setup ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ==================== Data Model ====================
@dataclass
class DownloadConfig:
    repo_id: str
    filename: str
    local_path: Optional[str] = None
    token: Optional[str] = None
    overwrite: bool = False
    resume: bool = False
    num_threads: int = DEFAULT_NUM_THREADS
    max_retries: int = DEFAULT_MAX_RETRIES
    verify_md5: Optional[str] = None
    timeout: int = DEFAULT_TIMEOUT

# ==================== Base64 Decode and Annotation ====================
def decode_and_annotate(b64_string: str) -> str:
    try:
        decoded_bytes = base64.b64decode(b64_string)
        decoded_text = decoded_bytes.decode('utf-8')
    except Exception as e:
        logger.error(f"Base64 decode failed: {e}")
        decoded_text = "[Decode failed]"
    
    border = "=" * 60
    annotation = f"""
{border}
  🔓 Decoded Message 🔓  
{border}
{decoded_text}
{border}
    """
    print(annotation)
    return decoded_text

# ==================== Helper Functions ====================
def get_file_size(url: str, headers: Dict) -> Optional[int]:
    try:
        resp = requests.head(url, headers=headers, timeout=DEFAULT_TIMEOUT)
        if resp.status_code == 200:
            size = int(resp.headers.get('content-length', 0))
            return size if size > 0 else None
    except Exception as e:
        logger.warning(f"Failed to get file size: {e}")
    return None

def get_local_file_size(local_path: str) -> int:
    if os.path.exists(local_path):
        return os.path.getsize(local_path)
    return 0

def calculate_md5(file_path: str, chunk_size: int = 8192) -> str:
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

def validate_md5(file_path: str, expected_md5: str) -> bool:
    actual = calculate_md5(file_path)
    if actual.lower() != expected_md5.lower():
        logger.error(f"MD5 mismatch: expected {expected_md5}, got {actual}")
        return False
    logger.info("MD5 checksum passed")
    return True

# ==================== Single-thread download (with resume) ====================
def download_single_thread(url: str, local_path: str, headers: Dict,
                           total_size: int, resume: bool = False) -> bool:
    existing_size = get_local_file_size(local_path) if resume else 0
    if existing_size > 0 and resume:
        headers['Range'] = f'bytes={existing_size}-'
        mode = 'ab'
        initial_pos = existing_size
        logger.info(f"Resume download, existing {existing_size} / {total_size} bytes")
    else:
        mode = 'wb'
        initial_pos = 0
        if existing_size > 0 and not resume:
            logger.info("Resume disabled, will overwrite existing file")

    try:
        with requests.get(url, headers=headers, stream=True, timeout=DEFAULT_TIMEOUT) as response:
            if response.status_code not in (200, 206):
                logger.error(f"Download failed, HTTP {response.status_code}")
                return False

            if total_size is None:
                total_size = int(response.headers.get('content-length', 0)) + initial_pos

            with open(local_path, mode) as f:
                with tqdm(total=total_size, initial=initial_pos, unit='B',
                          unit_scale=True, desc=os.path.basename(local_path)) as pbar:
                    for chunk in response.iter_content(chunk_size=DEFAULT_CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
        return True
    except Exception as e:
        logger.error(f"Download exception: {e}")
        return False

# ==================== Multi-thread chunk download ====================
def download_chunk(url: str, start: int, end: int, chunk_index: int,
                   temp_dir: str, headers: Dict, timeout: int) -> Tuple[int, bool]:
    chunk_headers = headers.copy()
    chunk_headers['Range'] = f'bytes={start}-{end}'
    chunk_file = os.path.join(temp_dir, f"chunk_{chunk_index}")
    try:
        resp = requests.get(url, headers=chunk_headers, stream=True, timeout=timeout)
        if resp.status_code not in (200, 206):
            return chunk_index, False
        with open(chunk_file, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=DEFAULT_CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        return chunk_index, True
    except Exception as e:
        logger.error(f"Chunk {chunk_index} download failed: {e}")
        return chunk_index, False

def download_multithread(config: DownloadConfig, url: str, headers: Dict,
                         total_size: int) -> bool:
    if total_size is None:
        logger.error("Cannot get file size, multi-thread download not possible")
        return False

    num_threads = min(config.num_threads, max(1, total_size // (10 * 1024 * 1024)))
    chunk_size = total_size // num_threads
    temp_dir = f"{config.local_path}.parts"
    os.makedirs(temp_dir, exist_ok=True)

    tasks = []
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size - 1 if i < num_threads - 1 else total_size - 1
        tasks.append((start, end, i))

    logger.info(f"Starting {len(tasks)} threads to download chunks...")
    success = True
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(download_chunk, url, start, end, idx,
                                   temp_dir, headers, config.timeout): idx
                   for (start, end, idx) in tasks}
        with tqdm(total=total_size, unit='B', unit_scale=True,
                  desc=f"Multi-thread download {os.path.basename(config.local_path)}") as pbar:
            for future in as_completed(futures):
                idx, ok = future.result()
                if not ok:
                    logger.error(f"Chunk {idx} download failed")
                    success = False

    if success:
        logger.info("Merging chunks...")
        with open(config.local_path, 'wb') as outfile:
            for i in range(num_threads):
                chunk_file = os.path.join(temp_dir, f"chunk_{i}")
                with open(chunk_file, 'rb') as infile:
                    outfile.write(infile.read())
                os.remove(chunk_file)
        os.rmdir(temp_dir)
        logger.info("Multi-thread download completed")
    else:
        logger.error("Multi-thread download failed, cleaning temporary files")
        for i in range(num_threads):
            chunk_file = os.path.join(temp_dir, f"chunk_{i}")
            if os.path.exists(chunk_file):
                os.remove(chunk_file)
        os.rmdir(temp_dir)

    return success

# ==================== Main download function with retry ====================
def download_from_hf(config: DownloadConfig) -> bool:
    url = f"https://huggingface.co/{config.repo_id}/resolve/main/{config.filename}"
    
    headers = {}
    if config.token:
        headers['Authorization'] = f'Bearer {config.token}'
    
    total_size = get_file_size(url, headers)
    if total_size is None:
        logger.warning("Cannot get remote file size, will use streaming (no resume/multi-thread)")
    
    if os.path.exists(config.local_path) and not config.overwrite and not config.resume:
        logger.error(f"Local file {config.local_path} exists. Use --overwrite to replace or --resume to continue")
        return False
    
    if config.resume and total_size:
        local_size = get_local_file_size(config.local_path)
        if local_size >= total_size:
            logger.info("Local file already complete, no need to download")
            return True
        elif local_size > 0:
            logger.info(f"Resuming, downloaded {local_size} / {total_size}")
    
    use_multithread = (config.num_threads > 1 and total_size is not None and total_size > 10*1024*1024)
    
    for attempt in range(1, config.max_retries + 1):
        logger.info(f"Download attempt {attempt} ...")
        if use_multithread:
            success = download_multithread(config, url, headers, total_size)
        else:
            success = download_single_thread(url, config.local_path, headers,
                                             total_size, config.resume)
        if success:
            if config.verify_md5:
                if not validate_md5(config.local_path, config.verify_md5):
                    os.remove(config.local_path)
                    logger.warning("MD5 mismatch, deleted file and will retry")
                    continue
            logger.info(f"Download successful: {config.local_path}")
            return True
        else:
            if attempt < config.max_retries:
                logger.info(f"Download failed, retrying in {DEFAULT_RETRY_DELAY} seconds...")
                time.sleep(DEFAULT_RETRY_DELAY)
            else:
                logger.error("Max retries reached, download failed")
    return False

# ==================== Load config from file ====================
def load_config_from_file(file_path: str) -> Dict:
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read config file: {e}")
    return {}

# ==================== Command line argument parsing ====================
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Enhanced Hugging Face file downloader (supports APK and any files)",
        epilog="Example: python download_apk.py --repo-id user/repo --filename file.apk --resume"
    )
    parser.add_argument("--repo-id", "-r", required=True,
                        help="Hugging Face repository ID, format: username/repo_name")
    parser.add_argument("--filename", "-f", required=True,
                        help="File path in repository, e.g., 'apk/app.apk'")
    parser.add_argument("--local-path", "-o", default=None,
                        help="Local save path (default: basename of filename)")
    parser.add_argument("--token", "-t", default=None,
                        help="Hugging Face access token (for private repos)")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing local file")
    parser.add_argument("--resume", action="store_true",
                        help="Resume interrupted download (single-thread only)")
    parser.add_argument("--threads", "-n", type=int, default=DEFAULT_NUM_THREADS,
                        help=f"Number of threads for multi-thread download (default {DEFAULT_NUM_THREADS})")
    parser.add_argument("--max-retries", type=int, default=DEFAULT_MAX_RETRIES,
                        help=f"Maximum retry attempts (default {DEFAULT_MAX_RETRIES})")
    parser.add_argument("--md5", default=None,
                        help="Expected MD5 hash of the file for integrity check")
    parser.add_argument("--config", default=DEFAULT_CONFIG_PATH,
                        help=f"Config file path (JSON format, default {DEFAULT_CONFIG_PATH})")
    parser.add_argument("--no-base64", action="store_true",
                        help="Do not display Base64 decoded message")
    return parser.parse_args()

# ==================== Main ====================
def main():
    args = parse_arguments()

    if not args.no_base64:
        decode_and_annotate(BASE64_SECRET)

    config_defaults = load_config_from_file(args.config)

    local_path = args.local_path
    if local_path is None:
        local_path = os.path.basename(args.filename)

    token = args.token or os.environ.get("HF_TOKEN") or config_defaults.get("token")

    download_config = DownloadConfig(
        repo_id=args.repo_id,
        filename=args.filename,
        local_path=local_path,
        token=token,
        overwrite=args.overwrite,
        resume=args.resume,
        num_threads=args.threads,
        max_retries=args.max_retries,
        verify_md5=args.md5,
        timeout=DEFAULT_TIMEOUT
    )

    success = download_from_hf(download_config)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
