#!/usr/bin/env python3
"""Batch upload international gig videos to YouTube as unlisted."""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".claude", "skills", "youtube-uploader", "scripts"))
from youtube_uploader import YouTubeUploader, find_credentials_file

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MP4_DIR = os.path.join(PROJECT_DIR, "media", "mp4")
CREDENTIALS = os.path.join(PROJECT_DIR, "credentials.json")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "youtube_ids.json")

# Video filename -> (artist, venue, city, date_display)
VIDEOS = [
    ("01 Apr 2022 02.mp4", "Record Company", "Radio City Music Hall", "New York, NY, US", "1 Apr 2022"),
    ("01 Apr 2022 04.mp4", "The Revivalists", "Radio City Music Hall", "New York, NY, US", "1 Apr 2022"),
    ("03 Oct 2019 02.mp4", "Gary Clark Jr.", "Stubb's Waller Creek Amphitheater", "Austin, TX, US", "3 Oct 2019"),
    ("04 Nov 2017 01.mp4", "Black Rebel Motorcycle Club", "O2 Academy Brixton", "London, UK", "4 Nov 2017"),
    ("04 Oct 2019 01.mp4", "Austin City Limits Music Festival", "Zilker Park", "Austin, TX, US", "4 Oct 2019"),
    ("05 Nov 2012 01.mp4", "Alabama Shakes", "Astra", "Berlin, Germany", "5 Nov 2012"),
    ("05 Oct 2019 01.mp4", "Austin City Limits Music Festival", "Zilker Park", "Austin, TX, US", "5 Oct 2019"),
    ("06 Apr 2022 01.mp4", "Jack Broadbent", "Rockwood Music Hall", "New York, NY, US", "6 Apr 2022"),
    ("06 Nov 2012 01.mp4", "The Heavy", "Frannz Club", "Berlin, Germany", "6 Nov 2012"),
    ("06 Nov 2022 02.mp4", "Shakey Graves", "Heimathafen Neukölln", "Berlin, Germany", "6 Nov 2022"),
    ("06 Oct 2019 02.mp4", "Austin City Limits Music Festival", "Zilker Park", "Austin, TX, US", "6 Oct 2019"),
    ("07 May 2016 02.mp4", "Iggy Pop", "Tempodrom", "Berlin, Germany", "7 May 2016"),
    ("07 Nov 2022 01.mp4", "Franz Ferdinand", "Verti Music Hall", "Berlin, Germany", "7 Nov 2022"),
    ("07 Nov 2025 01.mp4", "Christone \"Kingfish\" Ingram", "Columbia Theater", "Berlin, Germany", "7 Nov 2025"),
    ("08 Apr 2019 02.mp4", "Tedeschi Trucks Band", "Cirkus", "Stockholm, Sweden", "8 Apr 2019"),
    ("08 Apr 2022 02.mp4", "Buddy Guy", "NYCB Theatre at Westbury", "New York, NY, US", "8 Apr 2022"),
    ("08 Apr 2022 03.mp4", "Buddy Guy", "NYCB Theatre at Westbury", "New York, NY, US", "8 Apr 2022"),
    ("09 Nov 2025 01.mp4", "Wet Leg", "Columbiahalle", "Berlin, Germany", "9 Nov 2025"),
    ("09 Nov 2025 02.mp4", "Wet Leg", "Columbiahalle", "Berlin, Germany", "9 Nov 2025"),
    ("08 Oct 2019 03.mp4", "The Black Keys", "Van Andel Arena", "MI, US", "8 Oct 2019"),
    ("08 Oct 2019 04.mp4", "The Black Keys", "Van Andel Arena", "MI, US", "8 Oct 2019"),
    ("10 Nov 2025 01.mp4", "Mumford & Sons", "Uber Arena", "Berlin, Germany", "10 Nov 2025"),
    ("10 Nov 2025 02.mp4", "Mumford & Sons", "Uber Arena", "Berlin, Germany", "10 Nov 2025"),
    ("11 Feb 2012 01.mp4", "The Black Keys", "Alexandra Palace", "London, UK", "11 Feb 2012"),
    ("11 Feb 2012 02.mp4", "The Black Keys", "Alexandra Palace", "London, UK", "11 Feb 2012"),
    ("12 Nov 2025 02.mp4", "Curtis Harding", "O2 Shepherds Bush Empire", "London, UK", "12 Nov 2025"),
    ("13 Nov 2025 02.mp4", "Bahamas", "Union Chapel", "London, UK", "13 Nov 2025"),
    ("16 Jul 2024 02.mp4", "Fantastic Negrito", "Warsaw", "Poland", "16 Jul 2024"),
    ("16 Jul 2024 03.mp4", "Fantastic Negrito", "Warsaw", "Poland", "16 Jul 2024"),
    ("16 Oct 2018 01.mp4", "The Vintage Caravan", "Lido", "Berlin, Germany", "16 Oct 2018"),
    ("18 Nov 2023 01.mp4", "The Bones of J.R. Jones", "Brotfabrik", "Frankfurt, Germany", "18 Nov 2023"),
    ("18 Nov 2023 02.mp4", "The Bones of J.R. Jones", "Brotfabrik", "Frankfurt, Germany", "18 Nov 2023"),
    ("19 Jun 2022 01.mp4", "Black Pumas", "Berns Salonger", "Stockholm, Sweden", "19 Jun 2022"),
    ("19 Jun 2022 02.mp4", "Black Pumas", "Berns Salonger", "Stockholm, Sweden", "19 Jun 2022"),
    ("20 Jul 2022 02.mp4", "Fantastic Negrito", "Teatro Romano", "Fiesole, Italy", "22 Jul 2022"),
    ("20 Mar 2019 01.mp4", "Tommy Emmanuel", "Royal Festival Hall", "London, UK", "20 Mar 2019"),
    ("23 May 2019 01.mp4", "The Heavy", "La Maroquinerie", "Paris, France", "23 May 2019"),
    ("30 mar 2018 03.mp4", "Nathaniel Rateliff & The Night Sweats", "Berns Salonger", "Stockholm, Sweden", "30 Mar 2018"),
    ("31 May 2023 01.mp4", "The Bones of J.R. Jones", "Paradiso Grote Zaal", "Amsterdam, Netherlands", "31 May 2023"),
    ("31 May 2023 02.mp4", "The Bones of J.R. Jones", "Paradiso Grote Zaal", "Amsterdam, Netherlands", "31 May 2023"),
    ("31 May 2023 03.mp4", "The Devil Makes Three", "Paradiso Grote Zaal", "Amsterdam, Netherlands", "31 May 2023"),
    ("08 Jul 2016 02.mp4", "British Summer Time Festival 2016", "Hyde Park", "London, UK", "8 Jul 2016"),
    ("08 Jul 2016 03.mp4", "British Summer Time Festival 2016", "Hyde Park", "London, UK", "8 Jul 2016"),
    ("08 Jul 2016 04.mp4", "British Summer Time Festival 2016", "Hyde Park", "London, UK", "8 Jul 2016"),
    ("30 Nov 2016 02.mp4", "KALEO", "Paradiso Grote Zaal", "Amsterdam, Netherlands", "30 Nov 2016"),
    ("09 Nov 2024 01.mp4", "Fantastic Negrito", "Nalen Klubb", "Stockholm, Sweden", "9 Nov 2024"),
    ("07 Mar 2025 02.mp4", "Michael Kiwanuka", "Jahrhunderthalle", "Frankfurt, Germany", "7 Mar 2025"),
    ("07 Mar 2025 03.mp4", "Michael Kiwanuka", "Jahrhunderthalle", "Frankfurt, Germany", "7 Mar 2025"),
]


def main():
    # Load any previously uploaded IDs (for resume capability)
    uploaded = {}
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE) as f:
            uploaded = json.load(f)

    credentials_path = find_credentials_file(CREDENTIALS)
    uploader = YouTubeUploader(credentials_path)

    total = len(VIDEOS)
    for i, (filename, artist, venue, city, date_display) in enumerate(VIDEOS, 1):
        if filename in uploaded:
            print(f"[{i}/{total}] SKIP (already uploaded): {filename}")
            continue

        filepath = os.path.join(MP4_DIR, filename)
        if not os.path.exists(filepath):
            print(f"[{i}/{total}] MISSING: {filepath}")
            continue

        title = f"{artist} — {venue}, {city} ({date_display})"
        # Truncate title to 100 chars (YouTube limit)
        if len(title) > 100:
            title = title[:97] + "..."

        description = f"Live at {venue}, {city} on {date_display}.\nTicket Home — concert travels from Helsinki."
        tags = f"live music,concert,{artist},{city}"

        print(f"[{i}/{total}] Uploading: {title}")

        try:
            video_id = uploader.upload(
                file_path=filepath,
                title=title,
                description=description,
                tags=tags.split(","),
                category=10,  # Music
                privacy_status="unlisted",
            )
            uploaded[filename] = {
                "video_id": video_id,
                "title": title,
                "artist": artist,
                "venue": venue,
                "city": city,
                "date": date_display,
            }
            # Save after each upload for resume capability
            with open(OUTPUT_FILE, "w") as f:
                json.dump(uploaded, f, indent=2)
            print(f"  -> Saved: {video_id}")
        except Exception as e:
            print(f"  -> FAILED: {e}")

    print(f"\nDone! {len(uploaded)}/{total} videos uploaded.")
    print(f"Video IDs saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
