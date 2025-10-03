import streamlit as st
from supabase import create_client, Client
import pandas as pd
import requests

# ------------------ Supabase setup ------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------ Streamlit UI ------------------
st.title("Gebruikers Deck Data Overzicht")

# Optioneel: filter op specifieke gebruikersnaam
filter_username = st.text_input(
    "Bekijk specifieke gebruiker (optioneel)", 
    value=""
).strip()

# ------------------ Data ophalen ------------------
try:
    response = supabase.table("user_decks").select("*").execute()
    all_users = response.data  # lijst van dicts
except Exception as e:
    st.error(f"Fout bij ophalen van data: {e}")
    all_users = []

if not all_users:
    st.info("Geen gebruikersdata gevonden.")
else:
    # DataFrame maken voor overzicht
    df = pd.DataFrame(all_users)

    # Kolom met door gebruiker ingevoerde naam weergeven met hoofdletter
    if "user_name" in df.columns:
        df["Gebruikersnaam"] = df["user_name"].apply(lambda x: x.capitalize())

    # Kolom met aantal decks
    if "deck_data" in df.columns:
        df["Aantal Decks"] = df["deck_data"].apply(lambda x: len(x) if x else 0)

    # Decknamen ophalen via Archidekt API
    def get_deck_names(deck_list):
        if not deck_list:
            return ""
        names = []
        for deck_id in deck_list:
            try:
                url = f"https://archidekt.com/api/decks/{deck_id}/"
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    names.append(data.get("name", deck_id))
                else:
                    names.append(deck_id)  # fallback
            except:
                names.append(deck_id)
        return "\n".join(names)

    if "deck_data" in df.columns:
        df["Deck Namen"] = df["deck_data"].apply(get_deck_names)

    # Filter toepassen als tekst is ingevuld
    if filter_username:
        df = df[df["Gebruikersnaam"].str.lower() == filter_username.lower()]

    # Kolommen tonen in gewenste volgorde
    columns_to_show = ["Gebruikersnaam", "Aantal Decks", "Deck Namen"]

    # Standaard st.dataframe laat verticale scroll toe voor lange cellen
    st.dataframe(df[columns_to_show], use_container_width=True, height=500)

    st.success(f"Totaal {len(df)} gebruikers getoond.")
