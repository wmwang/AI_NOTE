#!/usr/bin/env python3
"""
YouTube 字幕產生器 - 使用 OpenAI Whisper
=========================================
從 YouTube 影片自動下載音訊並透過 Whisper 產生字幕檔 (.srt / .vtt / .txt)。

使用方式:
  python3 yt-whisper-sub.py <YouTube_URL> [options]

範例:
  python3 yt-whisper-sub.py https://www.youtube.com/watch?v=xxxxxxxxx
  python3 yt-whisper-sub.py https://youtu.be/xxxxxxxxx --model medium --lang zh --format srt
  python3 yt-whisper-sub.py https://www.youtube.com/watch?v=xxxxxxxxx --output ./my_subs

依賴安裝:
  pip3 install openai-whisper yt-dlp
  (也需要 ffmpeg: brew install ffmpeg)
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path


# ── 顏色輸出 ──────────────────────────────────────────────
class Color:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_step(msg: str):
    print(f"\n{Color.CYAN}{Color.BOLD}▶ {msg}{Color.RESET}")


def print_success(msg: str):
    print(f"{Color.GREEN}✔ {msg}{Color.RESET}")


def print_warn(msg: str):
    print(f"{Color.YELLOW}⚠ {msg}{Color.RESET}")


def print_error(msg: str):
    print(f"{Color.RED}✘ {msg}{Color.RESET}")


# ── 檢查依賴 ──────────────────────────────────────────────
def check_dependencies():
    """檢查必要的工具是否已安裝。"""
    missing = []

    # 檢查 ffmpeg
    if not shutil.which("ffmpeg"):
        missing.append("ffmpeg (安裝: brew install ffmpeg)")

    # 檢查 Python 套件
    try:
        import whisper
    except ImportError:
        missing.append("openai-whisper (安裝: pip3 install openai-whisper)")

    try:
        import yt_dlp
    except ImportError:
        missing.append("yt-dlp (安裝: pip3 install yt-dlp)")

    if missing:
        print_error("缺少以下依賴：")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)


# ── 下載音訊 ──────────────────────────────────────────────
def download_audio(url: str, output_dir: str) -> str:
    """
    使用 yt-dlp 下載 YouTube 影片的音訊（最佳品質）。
    回傳下載的音訊檔案路徑。
    """
    import yt_dlp

    print_step(f"正在下載音訊：{url}")

    # 輸出模板：使用影片標題作為檔名
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
        "quiet": False,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "unknown")
            # 找到下載的檔案
            downloaded_files = list(Path(output_dir).glob("*.wav"))
            if not downloaded_files:
                # 可能是其他格式
                downloaded_files = list(Path(output_dir).iterdir())
                downloaded_files = [f for f in downloaded_files if f.is_file() and not f.name.startswith(".")]

            if downloaded_files:
                audio_path = str(downloaded_files[-1])
                print_success(f"已下載音訊：{audio_path}")
                print_success(f"影片標題：{title}")
                return audio_path
            else:
                print_error("找不到下載的音訊檔案")
                sys.exit(1)
    except Exception as e:
        print_error(f"下載失敗：{e}")
        sys.exit(1)


# ── Whisper 轉錄 ──────────────────────────────────────────
def transcribe_audio(audio_path: str, model_name: str, language: str = None) -> dict:
    """
    使用 OpenAI Whisper 模型進行語音轉錄。
    回傳 Whisper 的結果字典。
    """
    import whisper

    print_step(f"正在載入 Whisper 模型：{model_name}")
    model = whisper.load_model(model_name)
    print_success("模型載入完成")

    lang_msg = f"，語言：{language}" if language else "（自動偵測語言）"
    print_step(f"開始轉錄{lang_msg}")
    print_warn("這可能需要幾分鐘到幾十分鐘，取決於影片長度和模型大小...")

    options = {}
    if language:
        options["language"] = language

    result = model.transcribe(audio_path, **options)

    detected_lang = result.get("language", "unknown")
    print_success(f"轉錄完成！偵測到的語言：{detected_lang}")

    return result


# ── 時間格式化 ────────────────────────────────────────────
def format_timestamp_srt(seconds: float) -> str:
    """將秒數格式化為 SRT 時間戳格式：HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_timestamp_vtt(seconds: float) -> str:
    """將秒數格式化為 WebVTT 時間戳格式：HH:MM:SS.mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


# ── 儲存字幕檔 ────────────────────────────────────────────
def save_srt(segments: list, filepath: str):
    """儲存為 SRT 格式。"""
    with open(filepath, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            start = format_timestamp_srt(seg["start"])
            end = format_timestamp_srt(seg["end"])
            text = seg["text"].strip()
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")


def save_vtt(segments: list, filepath: str):
    """儲存為 WebVTT 格式。"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for i, seg in enumerate(segments, 1):
            start = format_timestamp_vtt(seg["start"])
            end = format_timestamp_vtt(seg["end"])
            text = seg["text"].strip()
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")


def save_txt(segments: list, filepath: str):
    """儲存為純文字格式。"""
    with open(filepath, "w", encoding="utf-8") as f:
        for seg in segments:
            text = seg["text"].strip()
            if text:
                f.write(f"{text}\n")


def save_subtitles(result: dict, base_name: str, output_dir: str, formats: list):
    """根據指定格式儲存字幕檔。"""
    segments = result["segments"]
    saved_files = []

    for fmt in formats:
        filepath = os.path.join(output_dir, f"{base_name}.{fmt}")
        if fmt == "srt":
            save_srt(segments, filepath)
        elif fmt == "vtt":
            save_vtt(segments, filepath)
        elif fmt == "txt":
            save_txt(segments, filepath)
        else:
            print_warn(f"不支援的格式：{fmt}，已跳過")
            continue
        saved_files.append(filepath)
        print_success(f"已儲存：{filepath}")

    return saved_files


# ── 主程式 ────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="YouTube 字幕產生器 - 使用 OpenAI Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  %(prog)s https://www.youtube.com/watch?v=xxxxxxxxx
  %(prog)s https://youtu.be/xxxxxxxxx --model medium --lang zh
  %(prog)s https://www.youtube.com/watch?v=xxxxxxxxx --format srt vtt txt
  %(prog)s https://www.youtube.com/watch?v=xxxxxxxxx --output ./subtitles

可用模型（由小到大）：
  tiny, base, small, medium, large, turbo
  建議：中文用 medium 以上，英文用 small 即可
        """,
    )

    parser.add_argument("url", help="YouTube 影片網址")
    parser.add_argument(
        "-m", "--model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large", "turbo"],
        help="Whisper 模型名稱（預設：medium）",
    )
    parser.add_argument(
        "-l", "--lang",
        default=None,
        help="語言代碼，如 zh、en、ja（預設：自動偵測）",
    )
    parser.add_argument(
        "-f", "--format",
        nargs="+",
        default=["srt"],
        choices=["srt", "vtt", "txt"],
        help="輸出字幕格式（預設：srt），可同時輸出多種格式",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="輸出目錄（預設：與影片同目錄）",
    )
    parser.add_argument(
        "--keep-audio",
        action="store_true",
        help="保留下載的音訊檔案（預設會刪除）",
    )

    args = parser.parse_args()

    # 歡迎訊息
    print(f"\n{Color.BOLD}{'='*50}{Color.RESET}")
    print(f"{Color.BOLD}  YouTube 字幕產生器 (Whisper){Color.RESET}")
    print(f"{Color.BOLD}{'='*50}{Color.RESET}")

    # 檢查依賴
    check_dependencies()

    # 設定輸出目錄
    output_dir = args.output or os.getcwd()
    os.makedirs(output_dir, exist_ok=True)

    # 使用暫存目錄下載音訊
    temp_dir = tempfile.mkdtemp(prefix="yt-whisper-")
    try:
        # 下載音訊
        audio_path = download_audio(args.url, temp_dir)

        # 取得影片標題作為檔名
        audio_name = Path(audio_path).stem
        # 清理檔名中的特殊字元
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', audio_name)

        # 轉錄
        result = transcribe_audio(audio_path, args.model, args.lang)

        # 儲存字幕
        saved = save_subtitles(result, safe_name, output_dir, args.format)

        # 顯示轉錄文字預覽
        full_text = result.get("text", "").strip()
        preview = full_text[:200] + "..." if len(full_text) > 200 else full_text
        print_step("轉錄文字預覽：")
        print(f"  {preview}")

    finally:
        # 清理暫存音訊
        if not args.keep_audio:
            shutil.rmtree(temp_dir, ignore_errors=True)
            print_success("已清理暫存音訊檔案")
        else:
            print_warn(f"音訊檔案保留在：{temp_dir}")

    # 最終摘要
    print(f"\n{Color.GREEN}{Color.BOLD}{'='*50}{Color.RESET}")
    print(f"{Color.GREEN}{Color.BOLD}  完成！{Color.RESET}")
    print(f"{Color.GREEN}{Color.BOLD}{'='*50}{Color.RESET}")
    print(f"  模型：{args.model}")
    print(f"  格式：{', '.join(args.format)}")
    print(f"  輸出目錄：{output_dir}")


if __name__ == "__main__":
    main()