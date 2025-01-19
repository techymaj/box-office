import subprocess
import re
import os

def extract_subtitles(input_file, parent_directory):
    # Get the list of streams (tracks) in the MKV file using ffmpeg
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
            print("No subtitles found.")
            return
        
        # Create output directory for subtitles if it doesn't exist
        output_dir = f"{parent_directory}/subtitles"
        os.makedirs(output_dir, exist_ok=True)
        
        # Map subtitle formats to valid file extensions
        subtitle_format_map = {
            "subrip": "srt",
            "ass": "ass",
            "webvtt": "vtt",
        }
        
        # Extract each subtitle track
        for i, (stream_id, language, subtitle_type) in enumerate(subtitle_tracks):
            # Default to "unknown" if language is missing
            language = language if language else "unknown"
            file_extension = subtitle_format_map.get(subtitle_type.lower(), "sub")  # Default to ".sub" if unknown
            output_file = os.path.join(output_dir, f"subtitle_{i + 1}_{language}.{file_extension}")
            
            # FFmpeg command to extract the subtitle
            extract_command = [
                "ffmpeg",
                "-i", input_file,
                "-map", stream_id,
                output_file
            ]
            print(f"Extracting subtitle {i + 1}: {stream_id} ({language}) -> {output_file}")
            subprocess.run(extract_command)
        
        print("Subtitle extraction complete.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
