#!/usr/bin/env python3
"""Scrape GitHub contribution data from the public contributions page."""

import json
import pathlib
import requests
from bs4 import BeautifulSoup

USERNAME = "myriamlmiii"
URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch():
    resp = requests.get(URL, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = []
    # GitHub renders contributions as <td> elements with data-date and data-level
    for td in soup.select("td.ContributionCalendar-day"):
        date = td.get("data-date", "")
        level = int(td.get("data-level", 0))
        # Try to get count from tooltip or aria-label
        count = 0
        tool_tip = td.find("tool-tip") or td.find("span", class_="sr-only")
        if tool_tip:
            text = tool_tip.get_text(strip=True)
            parts = text.split()
            if parts and parts[0].isdigit():
                count = int(parts[0])
        elif level > 0:
            count = level  # fallback

        if date:
            days.append({"date": date, "count": count, "level": level})

    return days


if __name__ == "__main__":
    data = fetch()
    out = pathlib.Path(__file__).resolve().parent.parent / "data" / "contributions.json"
    out.write_text(json.dumps(data, indent=2))
    print(f"✓ Fetched {len(data)} days → {out}")
