#     Batch-AudioNormalizer
Normalize audio files (WAV/MP3) in a folder to a target dBFS level with optional backup and logging.

## Features
- Normalize audio files to target dBFS
- Optional backup of original files
- Track processed files using a log
- Preserve file metadata
- Handles WAV and MP3 formats
- Recursive processing of subdirectories

## Installation
### Prerequisites
- Python 3.7+ (Download from [python.org](https://www.python.org/downloads/))
- FFmpeg (Download from [ffmpeg.org](https://ffmpeg.org/download.html))
  - Add FFmpeg to your system's PATH environment variable
- Pydub library

### Install Dependencies
```bash
pip install pydub
```

## Usage
```bash
python AudioNormalizer.py --input "path/to/folder" --target "-3dB" [--backup | --no-backup] [--log-file "log_file.log"] [--reset-log]
```

## Arguments
| Argument       | Description                          | Default Value |
|----------------|--------------------------------------|---------------|
| `--input`      | Input folder containing audio files  |               |
| `--target`     | Target dBFS value (e.g., `-3dB`)     |               |
| `--backup`     | Create backup of original files      |               |
| `--no-backup`  | Skip backup and overwrite files      |               |
| `--log-file`   | Specify log file for processed files | `processed_files.log` |
| `--reset-log`  | Reset log file and reprocess all files |               |

## Example Usage
### Normalize with Backup
```bash
python AudioNormalizer.py --input "E:\Audio Files" --target "-3dB" --backup
```

### Normalize without Backup
```bash
python AudioNormalizer.py --input "E:\Audio Files" --target "-3dB" --no-backup
```

### Reset Log and Reprocess All Files
```bash
python AudioNormalizer.py --input "E:\Audio Files" --target "-3dB" --reset-log
```

## Backup System
- Backup files are stored in a `Backup` folder inside the input directory
- Example backup location:

E:\Audio Files
├── Backup
│   ├── audio_file1.wav
│   ├── audio_file2.mp3
├── Audio Files
│   ├── audio_file1.wav
│   ├── audio_file2.mp3


## Logging System
- Processed files are logged in `processed_files.log` (or specified log file)
- Log file contains relative paths of processed files
- Use `--reset-log` to clear the log and reprocess all files

## Troubleshooting
### Silent Files
- Files with `audio.max == 0` are considered silent and skipped
- Verify audio files using a media player or FFmpeg

### Permission Issues
- Run the script as Administrator if you encounter permission errors

### FFmpeg Errors
- Ensure FFmpeg is installed and accessible in your system's PATH
- Verify FFmpeg installation:
"""bash
ffmpeg -version
"""

## Contributing
### Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add some feature"`)
4. Push to your branch (`git push origin feature/your-feature`)
5. Open a pull request

### Code Style
- Follow PEP 8 coding standards
- Use descriptive variable and function names
- Add comments and docstrings

## License
[MIT License](LICENSE)

## Contact
For any questions or issues, please open an issue on the GitHub repository.
