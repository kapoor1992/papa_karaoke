import argparse
import os
import shutil
import time

_TEMP_DIR = f'{os.getcwd()}/temp'
_FINAL_DIR = f'{os.getcwd()}/final'

def _create_instrumental_video(yt_url: str) -> None:
    os.system(f'yt-dlp -f bestaudio --extract-audio --audio-format wav --audio-quality 0 -o "{_TEMP_DIR}/yt_audio.wav" {yt_url}')
    os.system(f'yt-dlp -f bestvideo -o "{_TEMP_DIR}/yt_video.webm" {yt_url}')

    os.system(f'demucs "{_TEMP_DIR}/yt_audio.wav" -o "{_TEMP_DIR}/"')

    os.system(f'ffmpeg -i "{_TEMP_DIR}/htdemucs/yt_audio/bass.wav" -i "{_TEMP_DIR}/htdemucs/yt_audio/drums.wav" -i "{_TEMP_DIR}/htdemucs/yt_audio/other.wav" -filter_complex [0:a:0][1:a:0]amix=inputs=3:duration=longest[aout] -map [aout] "{_TEMP_DIR}/instrumental.wav"')

    os.system(f'ffmpeg -i "{_TEMP_DIR}/yt_video.webm" -i "{_TEMP_DIR}/instrumental.wav" -c:v copy -c:a aac "{_FINAL_DIR}/{str(int(time.time()))}.mp4"')

def _main(yt_url: str) -> None:
    os.makedirs(_TEMP_DIR, exist_ok=True)
    os.makedirs(_FINAL_DIR, exist_ok=True)

    _create_instrumental_video(yt_url)
    
    shutil.rmtree(_TEMP_DIR)

if __name__ == '__main__':
    _parser = argparse.ArgumentParser()
    _parser.add_argument('--yt-url', required=True)
    _args = _parser.parse_args()
    
    _main(_args.yt_url)
