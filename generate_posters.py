#!/usr/bin/env python3
"""Generate best poster image for each video by comparing frames at 3 timestamps.
Picks the sharpest frame using Laplacian variance."""

import subprocess
import os
import json
import struct

MP4_DIR = "/Users/teroaarnio/projects/my-gigs-in-retrospective/media/mp4"
POSTER_DIR = "/Users/teroaarnio/projects/my-gigs-in-retrospective/media/posters"
os.makedirs(POSTER_DIR, exist_ok=True)


def get_duration(filepath):
    """Get video duration in seconds using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", filepath],
        capture_output=True, text=True
    )
    info = json.loads(result.stdout)
    return float(info["format"].get("duration", 0))


def extract_frame(filepath, timestamp, output):
    """Extract a single frame at given timestamp."""
    subprocess.run(
        ["ffmpeg", "-y", "-ss", str(timestamp), "-i", filepath,
         "-frames:v", "1", "-q:v", "2", output],
        capture_output=True
    )


def calculate_sharpness_pgm(filepath):
    """Calculate image sharpness using a simple Laplacian-like approach.
    Convert to grayscale PGM via sips/ffmpeg, then compute variance of
    differences between adjacent pixels."""
    # Convert to raw grayscale using ffmpeg
    raw_path = filepath + ".pgm"
    subprocess.run(
        ["ffmpeg", "-y", "-i", filepath, "-vf", "format=gray", "-f", "image2", raw_path],
        capture_output=True
    )

    if not os.path.exists(raw_path):
        return 0

    try:
        with open(raw_path, "rb") as f:
            # Parse PGM header
            magic = f.readline().strip()
            # Skip comments
            line = f.readline()
            while line.startswith(b"#"):
                line = f.readline()
            width, height = map(int, line.split())
            maxval = int(f.readline().strip())
            pixels = f.read()

        if len(pixels) < width * 2:
            return 0

        # Compute variance of horizontal differences (approximates sharpness)
        diffs = []
        for y in range(0, min(height, 500)):  # Sample up to 500 rows for speed
            row_start = y * width
            for x in range(1, width):
                if row_start + x < len(pixels):
                    diff = pixels[row_start + x] - pixels[row_start + x - 1]
                    diffs.append(diff * diff)

        sharpness = sum(diffs) / len(diffs) if diffs else 0
        return sharpness
    finally:
        os.remove(raw_path)


def main():
    videos = sorted(f for f in os.listdir(MP4_DIR) if f.endswith(".mp4"))
    total = len(videos)

    for i, filename in enumerate(videos, 1):
        base = os.path.splitext(filename)[0]
        poster_path = os.path.join(POSTER_DIR, f"{base}.jpg")

        if os.path.exists(poster_path):
            print(f"[{i}/{total}] SKIP (exists): {base}.jpg")
            continue

        filepath = os.path.join(MP4_DIR, filename)
        duration = get_duration(filepath)

        if duration < 1:
            print(f"[{i}/{total}] SKIP (too short): {filename}")
            continue

        # Sample at 10%, 33%, 50% of duration (avoid very start/end)
        timestamps = [
            max(1, duration * 0.10),
            duration * 0.33,
            duration * 0.50,
        ]

        best_sharpness = -1
        best_tmp = None
        tmp_files = []

        for j, ts in enumerate(timestamps):
            tmp_path = os.path.join(POSTER_DIR, f"_tmp_{base}_{j}.jpg")
            tmp_files.append(tmp_path)
            extract_frame(filepath, ts, tmp_path)

            if not os.path.exists(tmp_path):
                continue

            sharpness = calculate_sharpness_pgm(tmp_path)
            if sharpness > best_sharpness:
                best_sharpness = sharpness
                best_tmp = tmp_path

        # Keep the best, remove the rest
        if best_tmp:
            os.rename(best_tmp, poster_path)
            size = os.path.getsize(poster_path) // 1024
            print(f"[{i}/{total}] OK: {base}.jpg ({size}K, sharpness={best_sharpness:.0f})")
        else:
            print(f"[{i}/{total}] FAILED: {filename}")

        for tmp in tmp_files:
            if os.path.exists(tmp):
                os.remove(tmp)

    print("Done!")


if __name__ == "__main__":
    main()
