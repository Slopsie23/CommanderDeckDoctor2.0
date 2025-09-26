import streamlit as st
import requests
import time
from PIL import Image
import datetime
from urllib.parse import quote_plus, unquote
import diskcache
import re
import json
import os

# ---------------- Page config ----------------
st.set_page_config(
    page_title="CommanderDeckDoctor",
    page_icon="🐻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- Session state ----------------
if "app_started" not in st.session_state:
    st.session_state.app_started = False
if "deck_box" not in st.session_state:
    st.session_state["deck_box"] = []

# ---------------- Landingpagina ----------------
if not st.session_state.app_started:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        .landing-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }
        .start-button {
            border-radius: 50px !important;
            background: linear-gradient(to right, #e7684f, #584d99) !important;
            color: white !important;
            font-size: 24px !important;
            font-weight: bold !important;
            padding: 16px 40px !important;
            border: none !important;
            cursor: pointer !important;
            margin-top: 24px !important;
            transition: all 0.2s ease-in-out !important;
        }
        .start-button:hover {
            background: linear-gradient(to right, #584d99, #e7684f) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    landing_container = st.container()
    with landing_container:
        if os.path.exists("12.png"):
            img = Image.open("12.png")
            st.image(img, use_container_width=False)
        else:
            st.error("Afbeelding '12.png' niet gevonden.")

        if st.button("Start Doctoring", key="start_button"):
            st.session_state.app_started = True
            landing_container.empty()

# ---------------- Hoofdapp ----------------
else:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: block;}
        </style>
    """, unsafe_allow_html=True)

# ------------------ Styling ------------------
st.markdown("""
<style>
.stApp { 
    background: linear-gradient(135deg, #150f30, #001900); 
    color: white; 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
}

/* ---------------- Card Grid ---------------- */
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-top: 16px;
    justify-content: center;
}

.card-grid-item {
    background-color: #1a1a1a;
    border-radius: 8px;
    padding: 4px;
    box-shadow: 0 0 8px rgba(0,0,0,0.7);
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
}

.card-grid-item:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(59,124,59,0.8);
}

.card-grid-item img {
    width: 200px;
    height: 280px;
    object-fit: contain;
    border-radius: 8px 8px 0 0;
    user-select: none;
}

.card-name {
    text-align: center;
    color: white;
    font-size: 14px;
    margin: 4px 0 0 0;
    padding: 0 4px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    width: 100%;
    flex-shrink: 0;
}

/* ---------------- Buttons ---------------- */
div.stButton > button { 
    background: linear-gradient(to right, #e7684f, #584d99); 
    border: 1px solid #2e4730; 
    color: white; 
    font-weight: bold; 
    padding: 10px 24px; 
    border-radius: 6px; 
    transition: all 0.2s ease-in-out; 
    cursor: pointer; 
}
div.stButton > button:hover { 
    background: linear-gradient(to right, #584d99, #e7684f); 
    border-color: #3b7c3b; 
    color: white; 
}

/* ---------------- Deck-box ---------------- */
.deck-box-container {
    max-height: 400px;
    overflow-y: auto;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    border: 2px dashed #aaa;
    padding: 8px;
    border-radius: 8px;
    background-color: #1a1a1a;
}
.deck-box-card {
    width: 70px;
    text-align: center;
    transition: transform 0.2s ease-in-out;
}
.deck-box-card img {
    width: 70px;
    border-radius: 4px;
    border: 1px solid #555;
}
.deck-box-card:hover {
    transform: scale(1.1);
    border-color: #3b7c3b;
}
.deck-box-card button {
    width: 70px;
    margin-top: 2px;
    background-color: #e7684f;
    border: none;
    color: white;
    border-radius: 4px;
    cursor: pointer;
}
.deck-box-card button:hover {
    background-color: #584d99;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Cache Setup ------------------
cache = diskcache.Cache("./cache_dir")
def safe_api_call(url):
    if url in cache:
        return cache[url]
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            cache[url] = data
            return data
    except:
        pass
    return None

def scryfall_search_all_limited(query, max_cards=1000):
    cards = []
    url = f"https://api.scryfall.com/cards/search?q={query}&order=released&dir=desc"
    while url and len(cards) < max_cards:
        try:
            r = requests.get(url)
            if r.status_code != 200:
                break
            data = r.json()
            cards.extend(data.get("data", []))
            if not data.get("has_more"):
                break
            url = data.get("next_page")
            time.sleep(0.1)
        except:
            break
    return cards[:max_cards]

# ------------------ Render Cards With Add ------------------
def render_cards_with_add(cards):
    deck_box = st.session_state.get("deck_box", [])
    card_html = "<div class='card-grid'>"
    for card in cards:
        img_url = card.get("image_uris", {}).get("normal", "https://via.placeholder.com/223x310?text=Geen+afbeelding")
        name = card.get("name", "Onbekend")
        card_html += f"""
        <div class='card-grid-item'>
            <img src="{img_url}" title="{name}">
            <div class="card-name" title="{name}">{name}</div>
            <form>
                <button onclick="window.location.href=window.location.href+'?add={quote_plus(name)}'">➕</button>
            </form>
        </div>
        """
    card_html += "</div>"
    st.markdown(card_html, unsafe_allow_html=True)

# ------------------ Query Params toevoegen ------------------
query_params = st.query_params
deck_box = st.session_state.get("deck_box", [])

# Voeg kaart toe via ?add=
if "add" in query_params:
    card_name_to_add = unquote(query_params["add"][0])
    if card_name_to_add not in [c["name"] for c in deck_box]:
        deck_box.append({"name": card_name_to_add, "image_uris":{"normal":"https://via.placeholder.com/223x310?text=Geen+afbeelding"}})
        st.session_state["deck_box"] = deck_box
        st.experimental_set_query_params()
        st.experimental_rerun()

# Verwijder kaart via ?remove=
if "remove" in query_params:
    card_name_to_remove = unquote(query_params["remove"][0])
    deck_box = [c for c in deck_box if c["name"] != card_name_to_remove]
    st.session_state["deck_box"] = deck_box
    st.experimental_set_query_params()
    st.experimental_rerun()

st.session_state["deck_box"] = deck_box

# ------------------ Voorbeeld: Kaarten tonen ------------------
# Hier zou je de resultaten van Search & Find of analyse plaatsen
# Voor demo, een paar dummy kaarten:
dummy_cards = [
    {"name":"Island","image_uris":{"normal":"https://cards.scryfall.io/normal/front/a/2/a2e22347-f0cb-4cfd-88a3-4f46a16e4946.jpg?1755290097"}},
    {"name":"Forest","image_uris":{"normal":"https://cards.scryfall.io/normal/front/a/3/a305e44f-4253-4754-b83f-1e34103d77b0.jpg?1755290142"}},
    {"name":"Mountain","image_uris":{"normal":"https://cards.scryfall.io/normal/front/1/1/11111111-1111-1111-1111-111111111111.jpg?1755290000"}}
]
render_cards_with_add(dummy_cards)

# ------------------ Deck-box render ------------------
st.markdown('<div class="deck-box-container">', unsafe_allow_html=True)
for i, card in enumerate(deck_box):
    img_url = card.get("image_uris", {}).get("normal", "https://via.placeholder.com/80x110?text=Geen+afbeelding")
    name = card["name"]
    st.markdown(f"""
        <div class="deck-box-card">
            <img src="{img_url}" title="{name}">
            <div>{name}</div>
            <form>
                <button onclick="window.location.href=window.location.href+'?remove={quote_plus(name)}'">❌</button>
            </form>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
