import argparse
import os
from os.path import sep
import shutil
import time

_TEMP_DIR = f'{os.getcwd()}{sep}temp'
_FINAL_DIR = f'{os.getcwd()}{sep}final'

def _create_instrumental_video(yt_url: str) -> None:
    os.system(f'yt-dlp -f bestaudio --extract-audio --audio-format wav --audio-quality 0 -o "{_TEMP_DIR}{sep}yt_audio.wav" {yt_url}')
    os.system(f'yt-dlp -f bestvideo -o "{_TEMP_DIR}{sep}yt_video.webm" {yt_url}')
    
    os.system(f'demucs "{_TEMP_DIR}{sep}yt_audio.wav" -o "{_TEMP_DIR}{sep}"')

    os.system(f'ffmpeg -i "{_TEMP_DIR}{sep}htdemucs{sep}yt_audio{sep}bass.wav" -i "{_TEMP_DIR}{sep}htdemucs{sep}yt_audio{sep}drums.wav" -i "{_TEMP_DIR}{sep}htdemucs{sep}yt_audio{sep}other.wav" -filter_complex [0:a:0][1:a:0]amix=inputs=3:duration=longest[aout] -map [aout] "{_TEMP_DIR}{sep}instrumental.wav"')

    os.system(f'ffmpeg -i "{_TEMP_DIR}{sep}yt_video.webm" -i "{_TEMP_DIR}{sep}instrumental.wav" -c:v copy -c:a aac "{_FINAL_DIR}{sep}{str(int(time.time()))}.mp4"')

def _main(yt_url: str) -> None:
    os.makedirs(_TEMP_DIR, exist_ok=True)
    os.makedirs(_FINAL_DIR, exist_ok=True)

    try:
        _create_instrumental_video(yt_url)
    except Exception as _:
        pass
    finally:
        shutil.rmtree(_TEMP_DIR)

if __name__ == '__main__':
    _parser = argparse.ArgumentParser()
    _parser.add_argument('--yt-url', required=True)
    _args = _parser.parse_args()
    
    _main(_args.yt_url)
