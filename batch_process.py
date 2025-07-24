#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Video Processing Script
Process all videos in input folder and save transcriptions to output folder
"""

import os
import sys
import glob
import subprocess
from pathlib import Path
from tqdm import tqdm

def setup_environment():
    """Setup environment with local FFmpeg"""
    current_dir = os.getcwd()
    current_path = os.environ.get('PATH', '')
    if current_dir not in current_path:
        os.environ['PATH'] = current_dir + os.pathsep + current_path
    
    try:
        result = subprocess.run(['ffmpeg.exe', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("FFmpeg is working")
            return True
        else:
            print("FFmpeg test failed")
            return False
    except Exception as e:
        print(f"FFmpeg error: {e}")
        return False

def get_video_files(input_folder):
    """Get all video files from input folder"""
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']
    video_files = []
    
    for ext in video_extensions:
        pattern = os.path.join(input_folder, f"*{ext}")
        video_files.extend(glob.glob(pattern, recursive=False))
        pattern = os.path.join(input_folder, f"*{ext.upper()}")
        video_files.extend(glob.glob(pattern, recursive=False))
    
    return sorted(list(set(video_files)))

def format_time_srt(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def generate_srt_file(transcription_result, output_path):
    """Generate SRT subtitle file from transcription result"""
    try:
        srt_content = []
        
        for i, segment in enumerate(transcription_result["segments"], 1):
            start_time = format_time_srt(segment["start"])
            end_time = format_time_srt(segment["end"])
            text = segment["text"].strip()
            
            if text:  # Only add non-empty text
                srt_entry = f"{i}\n{start_time} --> {end_time}\n{text}\n"
                srt_content.append(srt_entry)
        
        # Write SRT file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_content))
        
        return True
    except Exception as e:
        print(f"Failed to generate SRT file: {e}")
        return False

def process_single_video(video_path, output_folder, model):
    """Process a single video file"""
    try:
        from src.video_english_recognition import VideoEnglishRecognizer
        
        recognizer = VideoEnglishRecognizer(model_size="base")
        recognizer.model = model  # Reuse loaded model
        
        # Generate output filename
        video_name = Path(video_path).stem
        output_file = os.path.join(output_folder, f"{video_name}_transcription.txt")
        json_file = os.path.join(output_folder, f"{video_name}_transcription.json")
        srt_file = os.path.join(output_folder, f"{video_name}.srt")
        
        # Check if already processed
        if os.path.exists(output_file) and os.path.exists(json_file) and os.path.exists(srt_file):
            print(f"Skipping {video_name} (already processed)")
            return True, f"Already processed: {video_name}"
        
        # Process video
        result = recognizer.process_video(video_path, output_dir=output_folder, clean_audio=True)
        
        if result["success"]:
            # Generate SRT file
            if generate_srt_file(result["transcription"], srt_file):
                return True, f"Successfully processed: {video_name} (TXT, JSON, SRT created)"
            else:
                return True, f"Successfully processed: {video_name} (TXT, JSON created, SRT failed)"
        else:
            return False, f"Failed to process: {video_name} - {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return False, f"Error processing {Path(video_path).name}: {str(e)}"

def main():
    """Main batch processing function"""
    print("=== Batch Video English Recognition ===")
    
    # Setup environment
    if not setup_environment():
        print("FFmpeg setup failed!")
        return
    
    # Create default folders
    input_folder = "input_videos"
    output_folder = "output_transcriptions"
    
    # Create folders if they don't exist
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"Input folder: {os.path.abspath(input_folder)}")
    print(f"Output folder: {os.path.abspath(output_folder)}")
    
    # Get video files
    video_files = get_video_files(input_folder)
    
    if not video_files:
        print(f"\nNo video files found in '{input_folder}' folder!")
        print("Supported formats: .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm, .m4v")
        print(f"Please add video files to: {os.path.abspath(input_folder)}")
        return
    
    print(f"\nFound {len(video_files)} video files:")
    for i, video_file in enumerate(video_files, 1):
        print(f"  {i}. {Path(video_file).name}")
    
    # Load Whisper model once
    print("\nLoading Whisper model...")
    try:
        import whisper
        model = whisper.load_model("base")
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Failed to load Whisper model: {e}")
        return
    
    # Process each video
    print(f"\nProcessing {len(video_files)} videos...")
    results = []
    
    for video_file in tqdm(video_files, desc="Processing videos"):
        video_name = Path(video_file).name
        print(f"\nProcessing: {video_name}")
        
        success, message = process_single_video(video_file, output_folder, model)
        results.append((video_name, success, message))
        
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
    
    # Summary
    print(f"\n{'='*60}")
    print("BATCH PROCESSING SUMMARY")
    print(f"{'='*60}")
    
    successful = sum(1 for _, success, _ in results if success)
    failed = len(results) - successful
    
    print(f"Total videos: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print(f"\nFailed videos:")
        for video_name, success, message in results:
            if not success:
                print(f"  ✗ {video_name}: {message}")
    
    print(f"\nOutput files saved to: {os.path.abspath(output_folder)}")
    print("Each video generates:")
    print("  - [video_name]_transcription.txt (human-readable)")
    print("  - [video_name]_transcription.json (machine-readable)")
    print("  - [video_name].srt (subtitle file)")

if __name__ == "__main__":
    main()