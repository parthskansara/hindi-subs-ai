# Import statements
import io
import json
import os
import sys
from moviepy.video.io.VideoFileClip import VideoFileClip
import whisper_timestamped as whisper
from englisttohindi.englisttohindi import EngtoHindi

# Constants
MODEL_NAME = "base"
ENCODING = 'utf-8'

# Utility functions
def parse_json_file(file_path):
    try:
        with open(file_path, 'r', encoding=ENCODING) as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Error occurred at line {e.lineno}, column {e.colno}")
    except IOError as e:
        print(f"I/O Error: {e}")

def parse_timestamp (timestamp):
    sec = int(timestamp)
    ms = int((timestamp - sec) * 1000)

    hrs = sec // 3600
    mins = (sec % 3600) // 60
    sec = sec % 60
    return f"{hrs:02}:{mins:02}:{sec:02},{ms:03}"

# Core functionality classes
class AudioExtractor:
    @staticmethod
    def extract_audio (video_path):
        audio_path = f"{video_path.split('.')[0]}_audio.mp3"

        print(f"Loading video clip at {video_path}")
        # Load the video clip
        video_clip = VideoFileClip(video_path)

        print(f"Extracting audio from the video clip")
        # Extract the audio from the video clip
        audio_clip = video_clip.audio

        print(f"Writing audio to file: {audio_path}")
        # Write the audio to a separate file
        audio_clip.write_audiofile(audio_path)

        # Close the video and audio clips
        audio_clip.close()
        video_clip.close()

        print(f"Audio extraction successful: {audio_path}")
        return audio_path



class Transcriber:
    @staticmethod
    def transcribe_audio_with_timestamps (audio_path):
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"The file {audio_path} does not exist.")

        srt_file_path = f"{audio_path.split("_audio")[0]}_subtitles.srt"
        print(f"Audio file found, loading file")
        
        audio = whisper.load_audio(audio_path)

        print(f"Loading model")
        model = whisper.load_model(MODEL_NAME)

        print(f"Starting transcription...")
        result = whisper.transcribe(model, audio, language="en")

        print(f"Writing transcription to json")

        json_file_path = f"{audio_path.split("_audio")[0]}_json.json"
        with open (json_file_path, 'w') as json_file:
            json.dump(result, json_file, indent=4)

        print(f"Writing json to text file")
        Transcriber.json_to_srt(json_file_path, srt_file_path)
        print(f'Transcribed audio to {srt_file_path}')
        return srt_file_path
    

    @staticmethod
    def json_to_srt(json_file, srt_file_path):
        json_data = parse_json_file(json_file)    
        with open (srt_file_path, "w") as file:
            for i, segment in enumerate(json_data['segments']):
                start_timestamp, end_timestamp = parse_timestamp(segment['start']), parse_timestamp(segment['end'])
                file.write(f"{i+1}\n")
                file.write(f"{start_timestamp} --> {end_timestamp}\n")
                file.write(segment['text'].strip() + '\n\n')


class Translator:
    @staticmethod
    def translate_to_hindi (english_file_path):
        hindi_file_path = f"{english_file_path.split("_subtitle")[0]}_hindi_subtitles.srt"
        print(f"Translating {english_file_path} to Hindi")
        with io.open (hindi_file_path, 'w', encoding=ENCODING) as hindi_file:
            with open (english_file_path, "r") as english_file:  
                for line in english_file:
                    translation = EngtoHindi(line.strip())
                    hindi_file.write(translation.convert + "\n")

        print(f'Translation saved in {hindi_file_path}')
        return hindi_file_path
                
def main(video_file_path):
    audio_path = AudioExtractor.extract_audio(video_file_path)
    subtitle_file = Transcriber.transcribe_audio_with_timestamps(audio_path)
    hindi_subtitle_file = Translator.translate_to_hindi(subtitle_file)
    print(f"Process completed. Hindi subtitles saved in: {hindi_subtitle_file}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        video_file_path = sys.argv[1]
    else:
        raise Exception('No video file path provided')
    main(video_file_path)