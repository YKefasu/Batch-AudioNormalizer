import os
import math
import shutil
from pydub import AudioSegment
import argparse

def get_peak_dBFS(audio_segment):
    max_amplitude = audio_segment.max
    max_possible = audio_segment.max_possible_amplitude
    return 20 * math.log10(abs(max_amplitude)/max_possible) if max_amplitude else -float('inf')

def main():
    parser = argparse.ArgumentParser(description='Normalize audio files with backup and logging.')
    parser.add_argument('--input', '-i', required=True, help='Input folder')
    parser.add_argument('--target', '-t', required=True, help='Target dBFS (e.g., -3dB)')
    parser.add_argument('--backup', action='store_true', help='Create backup')
    parser.add_argument('--no-backup', action='store_true', help='Skip backup')
    parser.add_argument('--log-file', default='processed_files.log', help='Log file for tracking processed files')
    parser.add_argument('--reset-log', action='store_true', help='Reset the log file and reprocess all files')
    args = parser.parse_args()

    if args.backup and args.no_backup:
        print("Error: Conflicting backup options")
        return

    input_folder = args.input
    log_file = args.log_file
    if not os.path.isdir(input_folder):
        print(f"Error: '{input_folder}' not found")
        return

    do_backup = False
    if args.backup:
        do_backup = True
    elif args.no_backup:
        do_backup = False
    else:
        response = input("Create backup? (y/n): ").lower()
        while response not in ['y', 'n']:
            response = input("Enter 'y' or 'n': ").lower()
        do_backup = response == 'y'

    # Initialize log
    processed_files = set()
    if not args.reset_log and os.path.exists(log_file):
        with open(log_file, 'r') as f:
            processed_files = set(line.strip() for line in f)
    else:
        # Reset log
        if os.path.exists(log_file):
            os.remove(log_file)

    # Backup files
    if do_backup:
        backup_dir = os.path.join(input_folder, 'Backup')  # Placed inside the input folder
        os.makedirs(backup_dir, exist_ok=True)
        print(f"Backup folder created at: {backup_dir}")
        except Exception as e:
            print(f"Error creating backup folder: {e}")
            return

        backup_count = 0
        for root, _, files in os.walk(input_folder):
            for file in files:
                if file.lower().endswith(('.wav', '.mp3')):
                    src = os.path.join(root, file)
                    dst = os.path.join(backup_dir, file)
                    try:
                        shutil.copy2(src, dst)
                        backup_count += 1
                    except Exception as e:
                        print(f"Failed to copy {file}: {e}")
        if backup_count > 0:
            print(f"Backup complete: {backup_count} files backed up")
        else:
            print("No audio files found for backup")

    # Normalize files
    try:
        target_dB = float(args.target.strip('dB'))
    except:
        print("Error: Invalid target dBFS")
        return

    new_entries = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if not file.lower().endswith(('.wav', '.mp3')):
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, input_folder)

            # Skip already processed files
            if relative_path in processed_files:
                print(f"Skipping already processed file: {file}")
                continue

            try:
                audio = AudioSegment.from_file(file_path)
                if audio.max == 0:
                    print(f"Skipping silent file: {file}")
                    continue
            except Exception as e:
                print(f"Error loading {file}: {e}")
                continue

            peak_dB = get_peak_dBFS(audio)
            required_gain = target_dB - peak_dB

            try:
                normalized_audio = audio.apply_gain(required_gain)
                normalized_audio.export(file_path, format=file.split('.')[-1])
                print(f"Normalized {file} ({required_gain:+.1f} dB)")

                # Add to new entries
                new_entries.append(relative_path)
            except Exception as e:
                print(f"Error normalizing {file}: {e}")

    # Update log
    if new_entries:
        with open(log_file, 'a') as f:
            for entry in new_entries:
                f.write(entry + '\n')
        print(f"Log updated with {len(new_entries)} new entries")
    else:
        print("No new files processed")

if __name__ == "__main__":
    main()