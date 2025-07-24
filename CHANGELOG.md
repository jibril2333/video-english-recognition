# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Video English Recognition System
- Core video speech recognition using OpenAI Whisper
- Batch processing capabilities for multiple videos
- Automatic SRT subtitle generation
- Support for multiple video formats (MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V)
- Multiple output formats (TXT, JSON, SRT)
- Smart file management with automatic cleanup
- Progress tracking and error reporting
- Cross-platform support (Windows, macOS, Linux)

### Features
- **VideoEnglishRecognizer Class**: Core recognition engine
- **Batch Processing Script**: Process multiple videos automatically
- **SRT Generation**: Create standard subtitle files
- **Model Selection**: Support for all Whisper model sizes (tiny to large)
- **Audio Extraction**: Automatic audio extraction from video files
- **Error Handling**: Comprehensive error handling and recovery
- **Resume Capability**: Skip already processed files

### Dependencies
- openai-whisper: Speech recognition model
- moviepy: Video/audio processing
- torch: PyTorch for model inference
- tqdm: Progress bars
- pathlib: File path handling

### Documentation
- Comprehensive README with installation and usage guides
- API documentation and examples
- Troubleshooting guide
- Performance optimization tips

## [1.0.0] - 2024-07-24

### Added
- Initial project structure
- Core functionality implementation
- Documentation and examples

### Technical Details
- Python 3.8+ support
- Multi-platform compatibility
- Integrated FFmpeg for Windows
- Conda and pip installation support

---

## Template for Future Releases

## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements