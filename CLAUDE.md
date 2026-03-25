# My Gigs in Retrospective

A personal retrospective of music gigs and festivals attended, presented as a static website ("Ticket Home").

## Project Structure

- `index.html` — single-page static website with map, timeline, media, and stories
- `gigs.md` — master list of all attended events (source of truth for dates/artists/venues)
- `public-data-of-gigs.md` — researched public data for each event (setlists, tour names, venue details)
- `media/` — original photos and videos from events
- `images/` — optimized images (max height 1200px, JPEG ~60% quality) served by the website
- `media/posters/` — video poster thumbnails for YouTube-pending videos
- `media/mp4/` — converted MP4 videos for YouTube upload
- `upload_videos.py` — YouTube upload script using Google API
- `generate_posters.py` — generates video poster thumbnails
- `youtube_ids.json` — maps media filenames to YouTube video IDs
- `credentials.json` — Google API credentials (for YouTube uploads)
- `token.json` — Google OAuth token (auto-generated)
- `favicon.svg`, `og-image.jpg`, `og-image.svg` — site assets
- `.venv/` — Python virtual environment (google-auth-oauthlib, google-api-python-client)

## gigs.md Format

Markdown table with 5 columns:

| Column | Description |
|--------|-------------|
| Date | Start date of the event (e.g. `13 Nov 2025`). May or may not have leading zero. |
| End Date | End date for multi-day festivals; empty for single-day events |
| Headline Artist or Festival | The headlining artist or festival name |
| Bands or Supporting Band | Supporting acts, festival lineup highlights; may be empty |
| Venue or Location | Full venue name and city/country |

## index.html Structure

The website is a single HTML file containing:
- Inline CSS and JavaScript (no build step)
- A Leaflet.js map showing gig locations with arcs from Helsinki
- A `GIGS` array in JS containing all event data (date, artist, venue, coords, images, videos, stories)
- A `YOUTUBE_IDS` map linking media filenames to YouTube video IDs
- Images are referenced by name (without extension) from `images/` as `.jpg`
- Videos are either YouTube embeds (via ID) or show poster thumbnails from `media/posters/`

When adding new media to the website:
1. Optimize images and place in `images/` (JPEG, max 1920px)
2. Add the image name (without `.jpg` extension) to the `images` array of the corresponding gig in the `GIGS` JS array
3. For videos: upload to YouTube, add ID to `YOUTUBE_IDS` map or `youtube_ids.json`

## Media Files

All original media (photos and videos) live in the `media/` folder.

### Naming Convention

```
DD Mon YYYY ##.ext
```

Examples:
- `13 Nov 2025 01.jpg`
- `13 Nov 2025 02.mov`
- `06 Mar 2013.JPG` (no sequence number if only one file)

The date in the filename is the **only link** between a media file and its corresponding event in `gigs.md`. The date format must match the Date column in `gigs.md` to associate correctly.

### Supported File Types

Images: `.jpg`, `.JPG`, `.jpeg`
Videos: `.mov`, `.MOV`, `.mp4`

### Adding New Media

New images should be placed in `add-media/` for processing, then:
1. Optimize with `sips -z 1200 <width> -s format jpeg -s formatOptions 60` (max height 1200px, ~60% quality; do NOT scale up smaller images)
2. Copy originals to `media/` and optimized versions to `images/`
3. Normalize extensions to lowercase `.jpg`
4. Fix any filename typos (e.g. letter O vs zero 0)
5. Verify dates match events in `gigs.md`
6. Update `images` arrays in `index.html` GIGS data

## Key Relationships

- Match media to events by date: the filename date corresponds to the `Date` column in `gigs.md`
- For festivals, all media files use the festival start date
- A sequence number (`01`, `02`, ...) differentiates multiple files from the same event
- The `GIGS` array in `index.html` is the rendering data; `gigs.md` is the canonical event list
- `images/` serves the website; `media/` holds originals
