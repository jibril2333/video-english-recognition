#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video English Recognition System
Using OpenAI Whisper model to recognize English content in videos
"""

import os
import sys

import whisper

try:
    import moviepy.editor as mp

    # Set FFmpeg path for moviepy
    try:
        import imageio_ffmpeg

        os.environ["IMAGEIO_FFMPEG_EXE"] = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass
except ImportError:
    print("MoviePy not found, trying alternative import...")
    try:
        from moviepy import VideoFileClip

        mp = type("MockMP", (), {"VideoFileClip": VideoFileClip})
    except ImportError:
        print(
            "Error: MoviePy is not properly installed. Please install it with: pip install moviepy"
        )
        sys.exit(1)

import json
import time
from pathlib import Path


class VideoEnglishRecognizer:
    def __init__(self, model_size="base"):
        """
        Initialize video English recognizer

        Args:
            model_size (str): Whisper model size ("tiny", "base", "small", "medium", "large")
        """
        print(f"Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size)
        print("Model loaded successfully!")

    def extract_audio_from_video(self, video_path, audio_path=None):
        """
        Extract audio from video file

        Args:
            video_path (str): Video file path
            audio_path (str): Output audio file path, auto-generated if None

        Returns:
            str: Audio file path
        """
        print(f"Extracting audio from video: {video_path}")

        if audio_path is None:
            video_name = Path(video_path).stem.replace(" ", "_")
            audio_path = f"{video_name}_audio.wav"

        try:
            # Use moviepy to extract audio
            video = mp.VideoFileClip(video_path)
            audio = video.audio
            audio.write_audiofile(audio_path, logger=None)
            audio.close()
            video.close()

            print(f"Audio extraction completed: {audio_path}")
            return audio_path

        except Exception as e:
            print(f"Audio extraction failed: {e}")
            return None

    def transcribe_audio(self, audio_path, language="en"):
        """
        Transcribe audio using Whisper model

        Args:
            audio_path (str): Audio file path
            language (str): Language code, default is English

        Returns:
            dict: Transcription result
        """
        print(f"Transcribing audio: {audio_path}")

        # Verify audio file exists
        if not os.path.exists(audio_path):
            print(f"Audio file not found: {audio_path}")
            return None

        try:
            # Use Whisper for transcription
            result = self.model.transcribe(
                os.path.abspath(audio_path), language=language, verbose=False
            )

            print("Transcription completed!")
            return result

        except Exception as e:
            print(f"Transcription failed: {e}")
            return None

    def format_time_srt(self, seconds):
        """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

    def generate_srt_file(self, result, srt_path):
        """Generate SRT subtitle file from transcription result"""
        try:
            srt_content = []

            for i, segment in enumerate(result["segments"], 1):
                start_time = self.format_time_srt(segment["start"])
                end_time = self.format_time_srt(segment["end"])
                text = segment["text"].strip()

                if text:  # Only add non-empty text
                    srt_entry = f"{i}\n{start_time} --> {end_time}\n{text}\n"
                    srt_content.append(srt_entry)

            # Write SRT file
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write("\n".join(srt_content))

            return True
        except Exception as e:
            print(f"Failed to generate SRT file: {e}")
            return False

    def save_transcription(self, result, output_path):
        """
        Save transcription results to file

        Args:
            result (dict): Whisper transcription result
            output_path (str): Output file path
        """
        try:
            # Save complete JSON result
            json_path = output_path.replace(".txt", ".json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            # Generate SRT file
            srt_path = output_path.replace("_transcription.txt", ".srt")
            srt_success = self.generate_srt_file(result, srt_path)

            # Save plain text result
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("=" * 50 + "\n")
                f.write("Video English Speech Recognition Results\n")
                f.write("=" * 50 + "\n\n")

                # Write complete text
                f.write("Complete Transcription Text:\n")
                f.write("-" * 30 + "\n")
                f.write(result["text"] + "\n\n")

                # Write segmented text (with timestamps)
                f.write("Segmented Transcription (with timestamps):\n")
                f.write("-" * 30 + "\n")

                for segment in result["segments"]:
                    start_time = segment["start"]
                    end_time = segment["end"]
                    text = segment["text"].strip()

                    # Format time
                    start_min, start_sec = divmod(start_time, 60)
                    end_min, end_sec = divmod(end_time, 60)

                    f.write(
                        f"[{int(start_min):02d}:{start_sec:05.2f} - {int(end_min):02d}:{end_sec:05.2f}] {text}\n"
                    )

            print(f"Transcription results saved to:")
            print(f"  Text file: {output_path}")
            print(f"  JSON file: {json_path}")
            if srt_success:
                print(f"  SRT file: {srt_path}")
            else:
                print(f"  SRT file: Failed to create {srt_path}")

        except Exception as e:
            print(f"Failed to save transcription results: {e}")

    def process_video(self, video_path, output_dir=".", clean_audio=True):
        """
        Process video file, complete audio extraction and speech recognition

        Args:
            video_path (str): Video file path
            output_dir (str): Output directory
            clean_audio (bool): Whether to delete intermediate audio files

        Returns:
            dict: Processing results
        """
        start_time = time.time()

        print(f"\n{'='*60}")
        print(f"Processing video: {video_path}")
        print(f"{'='*60}")

        # Check if video file exists
        if not os.path.exists(video_path):
            print(f"Error: Video file not found - {video_path}")
            return None

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Generate output file paths
        video_name = Path(video_path).stem.replace(" ", "_")
        audio_path = os.path.join(output_dir, f"{video_name}_audio.wav")
        output_path = os.path.join(output_dir, f"{video_name}_transcription.txt")

        try:
            # Step 1: Extract audio
            audio_file = self.extract_audio_from_video(video_path, audio_path)
            if not audio_file:
                return None

            # Step 2: Speech recognition
            transcription_result = self.transcribe_audio(audio_file, language="en")
            if not transcription_result:
                return None

            # Step 3: Save results
            self.save_transcription(transcription_result, output_path)

            # Step 4: Clean temporary files
            if clean_audio and os.path.exists(audio_file):
                os.remove(audio_file)
                print(f"Temporary audio file deleted: {audio_file}")

            # Calculate processing time
            processing_time = time.time() - start_time

            print(f"\n{'='*60}")
            print(f"Processing completed! Total time: {processing_time:.2f} seconds")
            print(f"{'='*60}")

            return {
                "success": True,
                "video_path": video_path,
                "output_path": output_path,
                "processing_time": processing_time,
                "transcription": transcription_result,
            }

        except Exception as e:
            print(f"Error occurred while processing video: {e}")
            return {"success": False, "error": str(e), "video_path": video_path}


def main():
    """Main function"""
    print("Video English Recognition System")
    print("=" * 40)

    # Default video path
    default_video = "SRE Basic Overview.mp4"

    # Check if default video exists
    if os.path.exists(default_video):
        video_path = default_video
        print(f"Found target video: {video_path}")
    else:
        print(f"Default video file not found: {default_video}")
        return

    # Create recognizer instance (using base model for balanced speed and accuracy)
    recognizer = VideoEnglishRecognizer(model_size="base")

    # Process video
    result = recognizer.process_video(
        video_path=video_path, output_dir="output", clean_audio=True
    )

    if result and result["success"]:
        print(f"\nRecognition successful!")
        print(f"Transcription result file: {result['output_path']}")

        # Show partial transcription content preview
        try:
            with open(result["output_path"], "r", encoding="utf-8") as f:
                content = f.read()
                preview = content[:500] + "..." if len(content) > 500 else content
                print(f"\nTranscription content preview:")
                print("-" * 30)
                print(preview)
        except:
            pass

    else:
        print("\nRecognition failed!")
        if result:
            print(f"Error message: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
