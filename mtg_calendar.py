# =========================
# 📅 MTG Calendar Module
# =========================
import requests
from datetime import datetime, timedelta
import json
import os
import re
from bs4 import BeautifulSoup

CACHE_FILE = "calendar_cache.json"
CACHE_EXPIRY_HOURS = 24

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_cache(data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def parse_date(date_str):
    """Convert a date string to dd-mm-yyyy, Qx YYYY or TBA"""
    if not date_str:
        return "TBA"
    date_str = date_str.strip()
    # Qx format
    if re.match(r"Q[1-4]\s\d{4}", date_str):
        return date_str
    # Normal date
    try:
        dt = datetime.strptime(date_str, "%B %d, %Y")
        return dt.strftime("%d-%m-%Y")
    except:
        if "TBA" in date_str or "To Be Announced" in date_str:
            return "TBA"
        return date_str

# --- Scryfall releases ---
def fetch_scryfall_releases():
    url = "https://api.scryfall.com/sets"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json().get("data", [])
        events = []
        for s in data:
            if s.get("released_at") and not s.get("digital", False):
                events.append({
                    "Datum": parse_date(s["released_at"]),
                    "Evenement": s["name"],
                    "Type": "Release"
                })
        return events
    except:
        return []

# --- Draftsim upcoming sets ---
def fetch_draftsim_upcoming_events():
    BASE_URL = "https://draftsim.com/mtg-release-schedule/"
    events = []
    try:
        r = requests.get(BASE_URL, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        table = soup.find("table")
        if not table:
            return []

        rows = table.find_all("tr")[1:]  # skip header
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 4:
                continue
            set_name_cell = cells[0]
            release_date_cell = cells[2]
            set_name = set_name_cell.get_text(strip=True)
            release_date = parse_date(release_date_cell.get_text(strip=True))

            events.append({
                "Datum": release_date,
                "Evenement": set_name,
                "Type": "Release"
            })
        return events
    except:
        return []

def get_upcoming_events():
    """Return future events from Scryfall + Draftsim"""
    cached = load_cache()
    if cached:
        last_cached = datetime.strptime(cached[0].get("_cached_at", datetime.now().strftime("%Y-%m-%d %H:%M")), "%Y-%m-%d %H:%M")
        if datetime.now() - last_cached < timedelta(hours=CACHE_EXPIRY_HOURS):
            today = datetime.now().date()
            return [e for e in cached if e["Datum"] == "TBA" or "Q" in e["Datum"] or datetime.strptime(e["Datum"].split()[0], "%d-%m-%Y").date() >= today]

    events = []
    events.extend(fetch_scryfall_releases())
    events.extend(fetch_draftsim_upcoming_events())

    # Voeg cache timestamp toe
    for e in events:
        e["_cached_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Filter alleen toekomstige events
    today = datetime.now().date()
    future_events = []
    for e in events:
        if e["Datum"] == "TBA" or "Q" in e["Datum"]:
            future_events.append(e)
        else:
            try:
                dt = datetime.strptime(e["Datum"].split()[0], "%d-%m-%Y").date()
                if dt >= today:
                    future_events.append(e)
            except:
                continue

    # Sorteer op datum
    def sort_key(e):
        if e["Datum"] in ["TBA"] or "Q" in e["Datum"]:
            return datetime.max
        try:
            return datetime.strptime(e["Datum"].split()[0], "%d-%m-%Y")
        except:
            return datetime.max

    future_events = sorted(future_events, key=sort_key)
    save_cache(future_events)
    return future_events
