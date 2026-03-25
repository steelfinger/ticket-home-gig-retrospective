---
name: youtube-uploader
description: Uploads videos to YouTube using the YouTube Data API v3. This skill is used for (1) uploading videos created with Manim to YouTube, (2) setting video metadata (title, description, tags), (3) privacy settings (public, unlisted, private), (4) scheduled posts, and (5) adding to playlists.
---

# YouTube Video Uploader

Programmatically upload created videos to YouTube using the YouTube Data API v3.

---

## Prerequisites

### Initial Setup (User Action Required)

The following setup must be performed by the user. If the setup is not complete, guide the user to the "Initial Setup Guide" section of this skill.

1. Create a project in the Google Cloud Console.
2. Enable the YouTube Data API v3.
3. Create OAuth 2.0 credentials.
4. Download `credentials.json`.

### Dependencies

```bash
pip3 install google-auth-oauthlib google-api-python-client

```

---

## credentials.json Location

**Important**: The script automatically searches for `credentials.json` in the following order of priority. If placed in these locations, it will be used automatically even without the explicit `--credentials` option.

### Search Priority

| Priority | Location | Path |
| --- | --- | --- |
| 1 | Explicit Specification | `--credentials /path/to/credentials.json` |
| 2 | Project Directory | `./credentials.json` |
| 3 | Home Directory | `~/credentials.json` |
| 4 | Config Directory | `~/.config/youtube/credentials.json` |
| 5 | Plugin Directory | `${CLAUDE_PLUGIN_ROOT}/credentials.json` |

### Recommended Locations

```bash
# Personal use (common across projects) - Recommended
~/.config/youtube/credentials.json

# Or
~/credentials.json

# Project-specific credentials
./credentials.json

```

### Notes

* `token.json` (authentication token) is automatically generated in the same directory as `credentials.json`.
* Add `credentials.json` and `token.json` to your `.gitignore`.
* If `credentials.json` exists in multiple locations, the one with the highest priority will be used.

---

## Pre-upload Checklist

Before uploading a video, please verify the following:

```
1. Video File Verification
   - Is the file path correct?
   - Is it in MP4 format?
   - Does the file exist?

2. Credential Verification
   - Does credentials.json exist?
   - Browser authentication is required on the first run.

3. Metadata Preparation
   - Title (Required)
   - Description (Recommended)
   - Tags (Recommended)
   - Category (Default: 22 = People & Blogs)
   - Privacy Settings (Default: private)

```

---

## Usage

### Script Location

The upload script is located at:
`${CLAUDE_PLUGIN_ROOT}/skills/youtube-uploader/scripts/youtube_uploader.py`

### Basic Upload

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-uploader/scripts/youtube_uploader.py \
  /path/to/video.mp4 \
  --title "Video Title" \
  --credentials /path/to/credentials.json

```

### Upload with Full Options

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-uploader/scripts/youtube_uploader.py \
  /path/to/video.mp4 \
  --title "Video Title" \
  --description "Detailed description of the video" \
  --tags "manim,animation,explanation" \
  --privacy private \
  --category 27 \
  --credentials /path/to/credentials.json

```

### Example: Uploading a Manim Video

```bash
# Upload a video output from Manim
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-uploader/scripts/youtube_uploader.py \
  ./media/videos/scene/1080p60/MyScene.mp4 \
  --title "Explainer Video created with Manim" \
  --description "Animation created with the Manim Community library" \
  --tags "manim,animation,python,math" \
  --privacy unlisted \
  --category 27 \
  --credentials ~/credentials.json

```

---

## Command Line Options

| Option | Required | Description | Default |
| --- | --- | --- | --- |
| `file` | Yes | Path to the MP4 video to upload | - |
| `--title` | Yes | Video title | - |
| `--description` | No | Video description | Empty |
| `--tags` | No | Comma-separated tags | Empty |
| `--privacy` | No | `private`, `unlisted`, `public` | `private` |
| `--category` | No | YouTube Category ID | `22` |
| `--credentials` | No | Path to credentials.json | `credentials.json` |
| `--playlist` | No | Target Playlist ID | - |
| `--publish-at` | No | Scheduled post date/time (ISO 8601 format) | - |

---

## YouTube Category IDs

| Category | ID |
| --- | --- |
| Film & Animation | 1 |
| Autos & Vehicles | 2 |
| Music | 10 |
| Pets & Animals | 15 |
| Sports | 17 |
| Travel & Events | 19 |
| Gaming | 20 |
| People & Blogs | 22 |
| Comedy | 23 |
| Entertainment | 24 |
| News & Politics | 25 |
| Howto & Style | 26 |
| Education | 27 |
| Science & Technology | 28 |

**Recommended categories for Manim videos:**

* Explainer/Educational: `27` (Education)
* Technical Demos: `28` (Science & Technology)
* Entertainment: `24` (Entertainment)

---

## Initial Setup Guide

If the user has not completed the setup, please provide the following steps.

### Step 1: Create a Project in Google Cloud Console

1. Go to the [Google Cloud Console](https://console.cloud.google.com).
2. Click "Select a project" at the top -> "New Project".
3. Enter a project name (e.g., `YouTube-Uploader`).
4. Click "Create".

### Step 2: Enable YouTube Data API v3

1. Left Menu -> "APIs & Services" -> "Library".
2. Search for "YouTube Data API v3".
3. Click "Enable".

### Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" -> "Credentials".
2. Click "+ Create Credentials" -> "OAuth client ID".

**Configure Consent Screen (First time only):**

1. User Type: Select "External".
2. App name: `YouTube Uploader`.
3. Support email: Your email address.
4. Continue through "Save and Continue" prompts.
5. Add your Google account to "Test users".

**Create OAuth Client ID:**

1. Application type: "Desktop app".
2. Click "Create" -> "Download JSON".
3. Rename the downloaded file to `credentials.json`.

### Step 4: Install Dependencies

```bash
pip3 install google-auth-oauthlib google-api-python-client

```

### Step 5: Initial Authentication

```bash
python3 youtube_uploader.py test_video.mp4 \
  --title "Test Upload" \
  --credentials credentials.json

```

On first run:

1. The browser opens automatically.
2. Log in with your Google account.
3. Click "Allow".
4. `token.json` is generated automatically (used for subsequent logins).

---

## Scheduled Posting

You can schedule a video to be published at a specific time:

```bash
python3 youtube_uploader.py video.mp4 \
  --title "Scheduled Video" \
  --privacy private \
  --publish-at "2025-02-01T18:00:00Z"

```

**Note:** Scheduled posts only work for videos set to `private` or `unlisted`.

---

## Adding to Playlists

Add to a playlist simultaneously with the upload:

```bash
python3 youtube_uploader.py video.mp4 \
  --title "Playlist Video" \
  --playlist "PLxxxxxxxxxxxx"

```

How to get a Playlist ID:

1. Open the playlist on YouTube.
2. Extract from URL: `https://www.youtube.com/playlist?list=PLxxxxxxxxxxxx`
3. The part after `list=` is the Playlist ID.

---

## Troubleshooting

### `credentials.json` not found

```bash
# Specify the correct path
python3 youtube_uploader.py video.mp4 \
  --title "Test" \
  --credentials ~/path/to/credentials.json

```

### Permission Error (403)

1. Delete `token.json`.
2. Re-run the script to re-authenticate.
3. Ensure you click "Allow All".

### Invalid Value Error (400)

* Verify if `--category` is within the 1-28 range.
* Verify if `--publish-at` is in ISO 8601 format: `2025-01-15T15:30:00Z`.

### Upload Stalls

* Can be interrupted with `Ctrl+C`.
* May resume upon re-execution.
* Check your network connection.

---

## Security

### Managing Credential Files

```bash
# Add to .gitignore
echo "credentials.json" >> .gitignore
echo "token.json" >> .gitignore

```

### Management via Environment Variables

```bash
export YOUTUBE_CREDENTIALS_FILE="/path/to/credentials.json"

python3 youtube_uploader.py video.mp4 \
  --title "My Video" \
  --credentials $YOUTUBE_CREDENTIALS_FILE

```

---

## Example Workflow: Manim Creation -> YouTube Upload

```bash
# 1. Render video with Manim
uv run manim -qh scene.py MyScene

# 2. Combine Audio (if using a full version script)
python3 combine_final.py

# 3. Upload to YouTube
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-uploader/scripts/youtube_uploader.py \
  ./final_output.mp4 \
  --title "Manim Explainer Video" \
  --description "Created with the Manim Community library" \
  --tags "manim,animation,python" \
  --privacy unlisted \
  --category 27 \
  --credentials ~/credentials.json

```

---

## References

* [YouTube Data API v3 Official Documentation](https://developers.google.com/youtube/v3)
* [Video Upload API Guide](https://developers.google.com/youtube/v3/guides/uploading_a_video)
* [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
