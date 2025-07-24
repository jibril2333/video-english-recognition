# Contributing to Video English Recognition System

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

Before creating an issue, please:
1. Check if the issue already exists in our [issue tracker](../../issues)
2. Use our issue template to provide detailed information
3. Include relevant system information and error messages

### Submitting Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/video-english-recognition.git
   cd video-english-recognition
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   conda env create -f environment.yml
   conda activate video-english-recognition
   ```

4. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

5. **Test your changes**
   ```bash
   python -c "from src.video_english_recognition import VideoEnglishRecognizer; print('Import test passed')"
   # Test with a sample video file
   python batch_process.py
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```

7. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style Guidelines

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example:
```python
def process_video(self, video_path: str, output_dir: str = ".") -> dict:
    """
    Process video file and generate transcriptions.
    
    Args:
        video_path: Path to input video file
        output_dir: Directory for output files
        
    Returns:
        dict: Processing results with success status
    """
    # Implementation here
```

### Documentation
- Update README.md for user-facing changes
- Add inline comments for complex logic
- Update CHANGELOG.md with your changes

## Development Setup

### Prerequisites
- Python 3.8+
- FFmpeg
- Git

### Environment Setup
```bash
# Clone repository
git clone https://github.com/username/video-english-recognition.git
cd video-english-recognition

# Create environment
conda env create -f environment.yml
conda activate video-english-recognition

# Install in development mode
pip install -e .
```

### Testing
Currently, testing is done through:
1. Import tests
2. Basic functionality tests
3. Manual testing with sample videos

We welcome contributions to improve our testing framework!

## Types of Contributions

### Bug Fixes
- Fix existing issues
- Improve error handling
- Performance improvements

### New Features
- Additional video format support
- New output formats
- Performance optimizations
- UI improvements

### Documentation
- Improve existing documentation
- Add examples and tutorials
- Fix typos and formatting

### Testing
- Add unit tests
- Add integration tests
- Improve test coverage

## Review Process

1. All pull requests will be reviewed by maintainers
2. We may ask for changes or improvements
3. Once approved, your changes will be merged
4. Your contribution will be acknowledged in the changelog

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow our code of conduct

## Getting Help

- Create an issue for questions
- Check existing documentation
- Look at similar projects for inspiration

## Recognition

Contributors will be acknowledged in:
- CHANGELOG.md
- Repository contributors list
- Release notes (for significant contributions)

Thank you for contributing to make this project better!