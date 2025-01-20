import hashlib
import subprocess
import re
import os

def file_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def extract_subtitles(input_file, subtitles_dir):
    # Check file extension to ensure it supports subtitles
    supported_extensions = [".mkv", ".mp4"]
    if not any(input_file.endswith(ext) for ext in supported_extensions):
        print(f"Unsupported file format: {input_file}. Only MKV and MP4 are supported.")
        return
    
    # Get the list of streams (tracks) in the input file using ffmpeg
    ffmpeg_command = ["ffmpeg", "-i", input_file]
    
    try:
        # Run the ffmpeg command and capture the output
        result = subprocess.run(ffmpeg_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        ffmpeg_output = result.stderr
        
        # Print the FFmpeg output for debugging
        print("FFmpeg Output:\n", ffmpeg_output)
        
        # Regex pattern to find subtitle streams in the ffmpeg output
        subtitle_pattern = re.compile(r"Stream #(\d+:\d+)\((\w*)\): Subtitle: (\w+)")
        subtitle_tracks = subtitle_pattern.findall(ffmpeg_output)
        
        if not subtitle_tracks:
            return "No subtitles found."
        
        os.makedirs(subtitles_dir, exist_ok=True)
        
        # Map subtitle formats to valid file extensions
        subtitle_format_map = {
            "subrip": "srt",    # Common in MKV
            "ass": "ass",       # Advanced SubStation Alpha
            "webvtt": "vtt",    # Common for web subtitles
            "mov_text": "srt",  # Common for MP4 subtitles
        }
        
        # Extract each subtitle track
        for i, (stream_id, language, subtitle_type) in enumerate(subtitle_tracks):
            # Default to "unknown" if language is missing
            language = language if language else "unknown"
            file_extension = subtitle_format_map.get(subtitle_type.lower(), "sub")  # Default to ".sub" if unknown
            output_file = os.path.join(subtitles_dir, f"subtitle_{i + 1}_{language}.{file_extension}")
            
            if os.path.exists(output_file):
                # Generate a temporary file to compare content
                temp_output_file = f"{output_file}.temp"
                extract_command = [
                    "ffmpeg",
                    "-i", input_file,
                    "-map", stream_id,
                    "-c:s", "srt" if subtitle_type.lower() == "mov_text" else "copy",
                    temp_output_file
                ]

                # Run FFmpeg command for the temporary file
                subprocess.run(extract_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

                # Compare hashes of the existing file and the new temporary file
                if os.path.exists(temp_output_file) and file_hash(output_file) == file_hash(temp_output_file):
                    print(f"File {output_file} already exists with the same content. Skipping extraction.")
                    os.remove(temp_output_file)  # Clean up temporary file
                else:
                    # Replace the existing file with the new content
                    os.rename(temp_output_file, output_file)
                    print(f"Updated {output_file} with new content.")
            else:
                # File does not exist; proceed with normal extraction
                extract_command = [
                    "ffmpeg",
                    "-i", input_file,
                    "-map", stream_id,
                    "-c:s", "srt" if subtitle_type.lower() == "mov_text" else "copy",
                    output_file
                ]
                print(f"Extracting subtitle {i + 1}: {stream_id} ({language}) -> {output_file}")
                subprocess.Popen(extract_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        else:
            return "Subtitles found. Extracting...Play the first 30 seconds then refresh to load extracted subtitles."
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return "Subtitles available."
