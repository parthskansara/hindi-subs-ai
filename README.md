# HindiSubs.ai

This project generates subtitle files in Hindi from English videos. It extracts audio from the video file, transcribes it to English with timestamps, and then translates this to Hindi transcripts.
## Features

- Audio extraction from video files
- English transcription with timestamps
- Hindi translation of transcripts
- Generation of SRT subtitle files in both English and Hindi

## Installation

 1. Clone this repository:

```bash
git clone https://github.com/yourusername/hindi-transcript-generator.git
cd hindi-transcript-generator
```
 2. Install the required dependencies:

```bash
pip install -r requirements.txt
```
## Usage
Run the main script with the path to your video file:

```bash
python main.py <video_file_path>
```
For example:

```bash
python main.py videos/test.mp4
```
## Output Files
The script generates the following files:

- `<video_name>_audio.mp3`: Extracted audio from the video
- `<video_name>_json.json`: JSON file containing transcription data
- `<video_name>_subtitles.srt`: English subtitles in SRT format
- `<video_name>_hindi_subtitles.srt`: Hindi subtitles in SRT format

## Test Video
A test video file (test.mp4) is provided in the `/videos` folder. You can use this to test the program:

```bash
python main.py videos/test.mp4
```
## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the GPL License - see the LICENSE file for details.
