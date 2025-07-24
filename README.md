# Video English Recognition System

A comprehensive video speech recognition system that uses OpenAI Whisper to extract and transcribe English speech from video files. Features both single file processing and batch processing capabilities with automatic SRT subtitle generation.

## Features

- **High-accuracy Speech Recognition**: Uses OpenAI Whisper model for precise English speech recognition
- **Batch Processing**: Process multiple videos in a folder automatically
- **Multiple Output Formats**: Generates text, JSON, and SRT subtitle files
- **Automatic Audio Extraction**: Extracts audio from video files using MoviePy
- **SRT Subtitle Generation**: Creates standard SRT subtitle files for video players
- **Smart File Management**: Skips already processed files and cleans up temporary files
- **Progress Tracking**: Shows detailed progress and processing status
- **Comprehensive Error Handling**: Robust error handling with detailed reporting

## Project Structure

```
video-english-recognition/
├── src/
│   └── video_english_recognition.py    # Core recognition system
├── batch_process.py                    # Batch processing script
├── ffmpeg.exe                          # Local FFmpeg executable
├── requirements.txt                    # Python dependencies
├── environment.yml                     # Conda environment
├── setup.py                           # Package setup
└── README.md                          # This file
```

## Quick Start

### 1. Installation

**Option A: Using Conda (Recommended)**
```bash
conda env create -f environment.yml
conda activate video-english-recognition
```

**Option B: Using pip**
```bash
python -m venv video-english-recognition
# Windows:
video-english-recognition\Scripts\activate
# Linux/Mac:
source video-english-recognition/bin/activate

pip install -r requirements.txt
```

### 2. Batch Processing (Recommended)

```bash
python batch_process.py
```

This will:
- Create `input_videos/` and `output_transcriptions/` folders
- Process all videos in `input_videos/`
- Generate transcriptions and subtitles in `output_transcriptions/`

### 3. Single File Processing

```python
from src.video_english_recognition import VideoEnglishRecognizer

recognizer = VideoEnglishRecognizer(model_size="base")
result = recognizer.process_video("your_video.mp4")
```

## Usage Guide

### Batch Processing Workflow

1. **Add Videos**: Place your video files in the `input_videos/` folder
2. **Run Processing**: Execute `python batch_process.py`
3. **Check Results**: Find outputs in the `output_transcriptions/` folder

### Supported Video Formats
- .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm, .m4v

### Output Files

Each processed video generates three files:
- `[video_name]_transcription.txt` - Human-readable text with timestamps
- `[video_name]_transcription.json` - Machine-readable format with metadata
- `[video_name].srt` - Standard SRT subtitle file for video players

### Model Selection

Choose different Whisper models based on your needs:
- `tiny`: Fastest, least accurate (~39x realtime)
- `base`: Good balance (default, ~16x realtime)
- `small`: Better accuracy (~6x realtime)
- `medium`: High accuracy (~2x realtime)
- `large`: Best accuracy (~1x realtime)

```python
recognizer = VideoEnglishRecognizer(model_size="base")
```

## Advanced Usage

### Programmatic API

```python
from src.video_english_recognition import VideoEnglishRecognizer

# Initialize with specific model
recognizer = VideoEnglishRecognizer(model_size="small")

# Process single video
result = recognizer.process_video(
    video_path="meeting.mp4",
    output_dir="./results",
    clean_audio=True  # Delete temporary audio files
)

if result["success"]:
    print(f"Transcription saved to: {result['output_path']}")
    # Access transcription data
    transcription = result["transcription"]
    full_text = transcription["text"]
    segments = transcription["segments"]
```

### Batch Processing Features

- **Smart Resume**: Automatically skips already processed files
- **Progress Tracking**: Shows real-time progress with progress bars
- **Error Recovery**: Continues processing other files if one fails
- **Summary Report**: Displays detailed results after completion

## Configuration

### Environment Variables
- Set `CUDA_VISIBLE_DEVICES` for GPU selection
- Adjust `OMP_NUM_THREADS` for CPU optimization

### Performance Optimization
- **GPU Acceleration**: Install PyTorch with CUDA support for faster processing
- **Memory Management**: Use smaller models for systems with limited RAM
- **Disk Space**: Ensure sufficient space for temporary audio files

## Dependencies

Core dependencies automatically installed:
- **openai-whisper**: Speech recognition model
- **moviepy**: Video/audio processing
- **torch**: PyTorch for model inference
- **tqdm**: Progress bars
- **pathlib**: File path handling

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Solution: The project includes `ffmpeg.exe` for Windows
   - For other platforms: Install FFmpeg system-wide

2. **Out of memory errors**
   - Solution: Use smaller model (`tiny` or `base`)
   - Close other applications to free memory

3. **Slow processing**
   - Solution: Install CUDA-enabled PyTorch for GPU acceleration
   - Use smaller model for faster processing

4. **Video format not supported**
   - Solution: Convert video to MP4 format
   - Ensure video has audio track

### Performance Tips

- **First run**: Models are downloaded automatically (may take time)
- **GPU usage**: Install `torch` with CUDA for 5-10x speedup
- **Batch size**: Process multiple small videos together for efficiency
- **Storage**: Use SSD for faster temporary file operations

## Technical Details

### Processing Pipeline

1. **Video Input**: Accepts common video formats
2. **Audio Extraction**: Converts to 16kHz mono WAV using MoviePy
3. **Speech Recognition**: Processes through Whisper model
4. **Output Generation**: Creates TXT, JSON, and SRT files simultaneously
5. **Cleanup**: Removes temporary audio files

### SRT Format

Generated SRT files follow standard format:
```
1
00:00:00,000 --> 00:00:05,000
First subtitle text

2
00:00:05,000 --> 00:00:10,000
Second subtitle text
```

### Model Performance

| Model  | Size | Speed | VRAM | Quality |
|--------|------|-------|------|---------|
| tiny   | 39MB | ~39x  | ~1GB | Good    |
| base   | 74MB | ~16x  | ~1GB | Better  |
| small  | 244MB| ~6x   | ~2GB | High    |
| medium | 769MB| ~2x   | ~5GB | Higher  |
| large  | 1550MB| ~1x  | ~10GB| Best    |

## Examples

### Basic Batch Processing
```bash
# Create input folder and add videos
mkdir input_videos
# Copy your video files to input_videos/

# Run batch processing
python batch_process.py

# Check results
ls output_transcriptions/
```

### Single Video with Custom Settings
```python
recognizer = VideoEnglishRecognizer(model_size="large")
result = recognizer.process_video(
    "important_meeting.mp4",
    output_dir="./meeting_transcripts"
)
```

## License

This project is open source. Key dependencies:
- OpenAI Whisper: MIT License
- MoviePy: MIT License
- PyTorch: BSD License

## Acknowledgments

- OpenAI for the Whisper speech recognition model
- MoviePy team for video processing capabilities
- Hugging Face for model distribution infrastructure

---

**Hardware Requirements**: 
- Minimum: 4GB RAM, 2GB storage
- Recommended: 8GB+ RAM, GPU with 4GB+ VRAM, SSD storage
- Large model: 16GB+ RAM, GPU with 10GB+ VRAM