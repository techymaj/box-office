import os
import subprocess

def generate_hls(input_video, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # FFmpeg command to create HLS stream
    ffmpeg_command = [
        "ffmpeg",
        "-i", input_video,  # Input video file
        "-c:v", "copy",  # Copy video codec
        "-start_number", "0",  # Start segment numbering
        "-hls_time", "10",  # Duration of each segment (in seconds)
        "-hls_list_size", "0",  # Include all segments in the playlist
        "-f", "hls",  # Output format
        os.path.join(output_dir, "playlist.m3u8")  # Output M3U8 playlist
    ]

    # Run the FFmpeg command
    process = subprocess.Popen(
        ffmpeg_command,
        stdout=subprocess.PIPE,  # Redirect stdout if needed
        stderr=subprocess.PIPE,  # Redirect stderr if needed
        text=True                # Capture output as strings instead of bytes
    )
    print(f"Started HLS generation process with PID {process.pid}")
    return process
