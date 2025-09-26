import streamlit as st
import requests
import time
from PIL import Image
import datetime
from urllib.parse import quote_plus
import diskcache
import re
import json
import os
import pandas as pd
import io

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
    # Sidebar verbergen
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

    # Container voor landing
    landing_container = st.container()
    with landing_container:
        if os.path.exists("12.png"):
            img = Image.open("12.png")
            st.image(img, use_container_width=False)  # behoud origineel formaat
        else:
            st.error("Afbeelding '12.png' niet gevonden.")

        # Knop om app te starten
        if st.button("Start Doctoring", key="start_button"):
            st.session_state.app_started = True
            landing_container.empty()  # verwijder landing

# ---------------- Hoofdapp ----------------
else:
    # Sidebar zichtbaar
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: block;}
        </style>
    """, unsafe_allow_html=True)

# ------------------ Styling ------------------
st.markdown("""
<style>
/* ---------------- App achtergrond ---------------- */
.stApp { 
    background: linear-gradient(135deg, #150f30, #001900); 
    color: white; 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
}

/* ---------------- Card Grid ---------------- */
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 16px;
    margin-top: 16px;
    justify-content: center; /* centreren bij weinig kaarten */
}

/* ---------------- Individuele kaart-container ---------------- */
.card-hover-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 16px;
    overflow: visible;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    position: relative;
    z-index: 1;
    padding-bottom: -2px;   /* verwijder extra ruimte onderin */
}

.card-hover-container:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(59,124,59,0.8);
    z-index: 10;
}

/* Kaart afbeelding */
.card-hover-container img {
    width: 220px;
    height: 300px;
    object-fit: contain;
    border-radius: 16px 16px 0 0;
    user-select: none;
}

/* Kaart naam */
.card-name {
    text-align: center;
    color: white;
    font-size: 14px;
    margin: 4px  0 0px;      /* boven 4px, onder 6px */
    padding: 0 4px;         /* horizontale padding blijft */
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    width: 100%;
}

/* ---------------- Add-to-Deck knop ---------------- */
.card-hover-button {
    all: unset;                 /* reset alle default styling van Streamlit */
    display: block;             /* blok zodat margin auto werkt */
    margin: 6px auto 0 auto;    /* boven:6px, horizontaal gecentreerd */
    color: transparent;
    font-size: 22px;
    cursor: pointer;
    transition: color 0.2s ease, transform 0.2s ease, text-shadow 0.2s ease;
    text-align: center;
}

.card-hover-button:hover {
    color: #00d42d;
    transform: scale(1.3);
    text-shadow: 0 0 8px rgba(59,124,59,0.8);
}
.deckbox-remove {
    display: block;
    margin: 6px auto 0 auto;
    color: rgba(220,50,50,0.8);
    background-color: transparent;
    border: none;
    font-size: 22px;
    cursor: pointer;
    transition: color 0.2s ease, transform 0.2s ease, text-shadow 0.2s ease;
}

.deckbox-remove:hover {
    color: #dc3232;
    transform: scale(1.3);
    text-shadow: 0 0 8px rgba(220,50,50,0.8);
}

/* ---------------- Footer ---------------- */
.footer { 
    position: fixed; 
    left: 0; 
    bottom: 0; 
    width: 100%; 
    background: linear-gradient(135deg, #0d141c, #001900);
    color: white; 
    text-align: center; 
    padding: 6px 0; 
    font-size: 14px; 
    user-select: none; 
    display: flex; 
    justify-content: center; 
    align-items: center; 
    gap: 12px; 
    z-index: 9999; 
}
@keyframes mana-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes mana-counter { from { transform: rotate(0deg); } to { transform: rotate(-360deg); } }
.mana-spinner-wrap { display:flex; flex-direction:column; align-items:center; justify-content:center; margin: 12px 0 18px; }
.mana-spinner { position: relative; width: 120px; height: 120px; border-radius: 50%; animation: mana-spin 3s linear infinite; }
.mana { position: absolute; top: 50%; left: 50%; width: 36px; height: 36px; margin: -18px 0 0 -18px; transform: rotate(calc(var(--i) * 72deg)) translate(50px) rotate(calc(-1 * var(--i) * 72deg)); transform-origin: center center; }
.mana .face { width: 100%; height: 100%; animation: mana-counter 3s linear infinite; transition: animation-play-state 0.2s ease; }
.mana-spinner:hover .face { animation-play-state: paused; }
.mana img { width: 100%; height: 100%; display:block; }
.mana-msg { margin-top: 6px; font-size: 14px; opacity: 0.9; text-align:center; }
</style>
""", unsafe_allow_html=True)

# ------------------ Custom spinner helper ------------------
def show_mana_spinner(message="Bezig met laden..."):
    ph = st.empty()
    html = f"""
    <div class="mana-spinner-wrap">
        <div class="mana-spinner">
            <div class="mana" style="--i:0"><div class="face"><img src="https://svgs.scryfall.io/card-symbols/W.svg" /></div></div>
            <div class="mana" style="--i:1"><div class="face"><img src="https://svgs.scryfall.io/card-symbols/U.svg" /></div></div>
            <div class="mana" style="--i:2"><div class="face"><img src="https://svgs.scryfall.io/card-symbols/B.svg" /></div></div>
            <div class="mana" style="--i:3"><div class="face"><img src="https://svgs.scryfall.io/card-symbols/R.svg" /></div></div>
            <div class="mana" style="--i:4"><div class="face"><img src="https://svgs.scryfall.io/card-symbols/G.svg" /></div></div>
        </div>
        <div class="mana-msg">{message}</div>
    </div>
    """
    ph.markdown(html, unsafe_allow_html=True)
    return ph

# ------------------ Session State Init ------------------
for key, default in {
    'bear_search_active': False, 'deck_loaded': False, 'show_deck': False,
    'alt_commander_toggle': False, 'start_analysis': False,
    'keywords_list': [], 'cards': [], 'deck_card_names': set(),
    'full_deck': [], 'commanders': [], 'color_identity': set(),
    'commander_types': set(), 'selected_deck_name': '', 'added_decks': [],
    'sheriff_active': False
}.items():
    st.session_state.setdefault(key, default)

# ------------------ User Decks Init ------------------
if "user_name" in st.session_state and st.session_state["user_name"]:
    user_deck_key = get_user_deck_key()
    
    # 1. Probeer decks uit cache te halen
    cached_decks = cache.get(user_deck_key)
    if cached_decks is not None:
        st.session_state["added_decks"] = cached_decks
    else:
        # 2. Fallback: probeer JSON bestand
        json_file = os.path.join("data", f"{user_deck_key}.json")
        if os.path.exists(json_file):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    st.session_state["added_decks"] = json.load(f)
            except Exception:
                st.session_state["added_decks"] = []
        else:
            st.session_state["added_decks"] = []

    # 3. Laad kaarten in de Deck-Box
    deck_box_cards = cache.get(user_deck_key + "_cards")
    if deck_box_cards:
        st.session_state["deck_box"] = deck_box_cards

# ------------------ User-specific Deck Cache ------------------
import hashlib
import uuid

def get_user_deck_key():
    # maak unieke key per gebruiker op basis van gebruikersnaam
    user_name = st.session_state.get("user_name", "").strip().lower()
    if not user_name:
        # fallback: genereer tijdelijk session-id
        if "session_id" not in st.session_state:
            st.session_state["session_id"] = str(uuid.uuid4())
        user_name = st.session_state["session_id"]
    # unieke key voor cache
    return f"added_decks_{hashlib.md5(user_name.encode()).hexdigest()}"

def load_user_decks():
    key = get_user_deck_key()
    decks = cache.get(key)
    if decks is None:
        decks = []
    st.session_state.setdefault("added_decks", decks)
    return decks

def save_user_decks():
    key = get_user_deck_key()
    decks = st.session_state.get("added_decks", [])
    
    # opslaan in cache
    cache[key] = decks
    
    # extra fallback: opslaan in JSON
    os.makedirs("data", exist_ok=True)
    json_file = os.path.join("data", f"{key}.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)

# ------------------ Cache Setup ------------------
import tempfile
import diskcache
import requests
import logging
import time

# Tijdelijke cache-map gebruiken op Streamlit Cloud
cache_dir = tempfile.mkdtemp()
cache = diskcache.Cache(cache_dir)

logging.basicConfig(level=logging.INFO)

def safe_api_call(url):
    """Haalt data op uit cache of via API. Voorkomt KeyErrors en crasht niet."""
    cached = cache.get(url)
    if cached is not None:
        logging.info(f"Cache hit: {url}")
        return cached
    
    try:
        logging.info(f"Calling API: {url}")
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            cache.set(url, data)
            logging.info(f"API success: {url}")
            return data
        else:
            logging.warning(f"API returned {r.status_code} for {url}")
    except Exception as e:
        logging.error(f"API call failed: {url} | Error: {e}")
    
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
        except Exception as e:
            logging.error(f"Scryfall search failed for query '{query}': {e}")
            break
    return cards[:max_cards]


# ------------------ Deck-box helper ------------------
def add_to_deck_box(card):
    if card["name"] not in [c["name"] for c in st.session_state["deck_box"]]:
        st.session_state["deck_box"].append(card)
        st.experimental_rerun()

def render_cards_with_add(cards):
    with st.container():
        card_html = "<div class='card-grid'>"
        for card in cards:
            img_url = card.get("image_uris", {}).get("normal") or \
                      card.get("card_faces", [{}])[0].get("image_uris", {}).get("normal")
            name = card.get("name", "Onbekend")
            if img_url:
                card_html += f"""
                <div class="card-grid-item">
                    <img src="{img_url}" />
                    <div class="card-name" title="{name}">{name}</div>
                    <form>
                        <button onclick="window.location.href=window.location.href+'?add={quote_plus(name)}'">✚</button>
                    </form>
                </div>
                """
        card_html += "</div>"
        st.markdown(card_html, unsafe_allow_html=True)
        
# ------------------ Color Identity helpers ------------------
WUBRG_ORDER = "WUBRG"

def order_colors_wubrg(colors_set):
    order = {c: i for i, c in enumerate(WUBRG_ORDER)}
    return "".join(sorted(list(colors_set), key=lambda c: order.get(c, 99)))

def render_cards_with_add(cards, columns=None):
    """Render kaarten in een grid met hover-effect en gecentreerde Add-to-Deck knop.
       Toegevoegde kaarten worden per gebruiker persistent opgeslagen."""
    
    if not cards:
        st.info("Geen kaarten om weer te geven.")
        return

    # Kolommen bepalen
    if columns is None:
        columns = st.session_state.get("cards_per_row", 6)

    for i in range(0, len(cards), columns):
        row_cards = cards[i:i+columns]
        cols = st.columns(columns)  # altijd gekozen aantal kolommen

        for col_idx, card in enumerate(row_cards):
            with cols[col_idx]:
                img_url = card.get("image_uris", {}).get("normal") or \
                          card.get("card_faces", [{}])[0].get("image_uris", {}).get("normal") or \
                          "https://via.placeholder.com/223x310?text=Geen+afbeelding"
                name = card.get("name", "Onbekend")

                # Kaart afbeelding + naam
                st.markdown(f"""
                <div class="card-hover-container">
                    <img src="{img_url}" title="{name}" />
                    <div class="card-name" title="{name}">{name}</div>
                </div>
                """, unsafe_allow_html=True)

                # Unieke key per kaart
                button_key = f"add_card_{card.get('id', name)}"

                if st.button("✚", key=button_key, help="Voeg toe aan Deck-Box"):
                    # per-gebruiker Deck-Box laden
                    if "deck_box" not in st.session_state:
                        st.session_state["deck_box"] = []

                    # checken of kaart al toegevoegd is
                    if name not in [c["name"] for c in st.session_state["deck_box"]]:
                        st.session_state["deck_box"].append(card)

                        # persistente opslag per gebruiker in cache
                        user_deck_key = get_user_deck_key()  # hergebruik helper uit eerdere stap
                        cache[user_deck_key + "_cards"] = st.session_state["deck_box"]

                        st.toast(f"{name} toegevoegd aan Deck-Box ✅")


def get_all_keywords():
    keywords = [
        "+1/+1 Counter", "Copy", "Haste", "Flying", "Trample", "Lifelink", "Menace",
        "Deathtouch", "Vigilance", "First Strike", "Double Strike", "Hexproof",
        "Indestructible", "Reach", "Goad", "Fight", "Flash", "Defender", "Proliferate", "Charge Counter"
    ]
    return sorted(keywords, key=lambda x: x.lower())
    
if not st.session_state['keywords_list']:
    st.session_state['keywords_list'] = get_all_keywords()

# ------------------ Sidebar ------------------
with st.sidebar:
    try:
        logo = Image.open("12.png")
        st.image(logo, use_container_width=True)
    except:
        st.warning("Logo niet gevonden. Upload '12.png'.")

    with st.expander("Deck", expanded=False):
    # Zorg dat de map 'data' altijd bestaat
        os.makedirs("data", exist_ok=True)

        deck_file = "data/added_decks.json"

        st.caption("Beheer je eigen decks")

        # --- Gebruiker identificeren en onthouden ---
        if "user_name" not in st.session_state:
            st.session_state["user_name"] = ""
        st.session_state["user_name"] = st.text_input(
            "Gebruikersnaam",
            value=st.session_state["user_name"],
            help="Vul een naam of ID in om je decks op te slaan"
        ).strip()

        if st.session_state["user_name"]:
            # Decks en Deck-Box van deze gebruiker laden
            load_user_decks()
            deck_box_cards = cache.get(get_user_deck_key() + "_cards")
            if deck_box_cards:
                st.session_state["deck_box"] = deck_box_cards

            # Deck opties vullen
            deck_options = {}
            for deck_id in st.session_state["added_decks"]:
                data = safe_api_call(f"https://archidekt.com/api/decks/{deck_id}/")
                if data:
                    deck_options[data.get("name", f"Deck {deck_id}")] = deck_id
            st.session_state["deck_options"] = deck_options

            # Nieuw deck toevoegen
            new_deck_id = st.text_input(
                "Import Deck from Archidect",
                help="Noteer hier de getallenreeks in de URL van je deck op archidect.com"
            )
            if new_deck_id:
                new_data = safe_api_call(f"https://archidekt.com/api/decks/{new_deck_id}/")
                if new_data:
                    new_deck_name = new_data.get("name", f"Deck {new_deck_id}")
                    if new_deck_id not in st.session_state["added_decks"]:
                        st.session_state["added_decks"].append(new_deck_id)
                        save_user_decks()  # <-- voeg deze regel toe
                    st.session_state["deck_options"][new_deck_name] = new_deck_id
                    st.success(f"Deck '{new_deck_name}' toegevoegd.")
                else:
                    st.error("Ongeldige Archidekt Deck ID.")


            # Deck selecteren
            st.session_state["selected_deck_name"] = st.selectbox(
                "My Decks",
                [""] + list(st.session_state["deck_options"].keys()),
                index=0,
                help="Selecteer een deck | Geen selectie = geen kaarten"
            )

            # ------------------ Reset deck state bij geen selectie ------------------
            if st.session_state["selected_deck_name"] == "":
                st.session_state['deck_loaded'] = False
                st.session_state['cards'] = []
                st.session_state['deck_card_names'] = set()
                st.session_state['full_deck'] = []
                st.session_state['commanders'] = []
                st.session_state['color_identity'] = set()
                st.session_state['commander_types'] = set()
                st.session_state['last_loaded_deck'] = ""
            else:
                # Alleen load_deck aanroepen als functie gedefinieerd is
                if "load_deck" in globals() and st.session_state["selected_deck_name"] != st.session_state.get('last_loaded_deck', ''):
                    st.session_state['last_loaded_deck'] = st.session_state["selected_deck_name"]
                    load_deck(st.session_state["selected_deck_name"])

            # Opties
            st.session_state["show_deck"] = st.checkbox(
                "Show Deck",
                value=st.session_state.get("show_deck", False),
                help="Toont alle kaarten in je deck"
            )
            st.session_state["alt_commander_toggle"] = st.checkbox(
                "Alternative Commanders",
                value=st.session_state.get("alt_commander_toggle", False),
                help="Op zoek naar een andere Commander voor je Deck?"
            )

            # Deck verwijderen
            reset_checkbox = st.session_state.get("reset_delete_deck_checkbox", False)
            delete_deck_checkbox = st.checkbox(
                "Remove Deck",
                value=False if reset_checkbox else st.session_state.get("delete_deck_checkbox", False),
                key="delete_deck_checkbox",
                help="Verwijder geselecteerde deck uit deze lijst"
            )
            if reset_checkbox:
                st.session_state["reset_delete_deck_checkbox"] = False

            if delete_deck_checkbox and st.session_state["selected_deck_name"]:
                st.warning(f"Weet je zeker dat je '{st.session_state['selected_deck_name']}' wilt verwijderen?")
                col_confirm1, col_confirm2 = st.columns(2)
                with col_confirm1:
                    if st.button("Ja", key="confirm_delete_selected"):
                        deck_id_to_remove = st.session_state["deck_options"].get(st.session_state["selected_deck_name"])
                        if deck_id_to_remove in st.session_state["added_decks"]:
                            st.session_state["added_decks"].remove(deck_id_to_remove)
                            save_user_decks()
                        st.success(f"Deck '{st.session_state['selected_deck_name']}' is verwijderd.")
                        st.session_state["reset_delete_deck_checkbox"] = True
                        st.rerun()
                with col_confirm2:
                    if st.button("Nee", key="cancel_delete_selected"):
                        st.session_state["reset_delete_deck_checkbox"] = True
                        st.rerun()
        else:
            st.info("Vul eerst je gebruikersnaam in om decks te beheren.")

# ------------------ Helper: Multiselect auto-close ------------------
def close_multiselect_on_select(widget_key: str):
    st.markdown(f"""
    <script>
    const observer = new MutationObserver(() => {{
        const el = window.parent.document.querySelector('div[data-testid="stMultiSelect"]');
        if (el) {{
            el.blur();  // sluit de multiselect direct na een selectie
        }}
    }});
    observer.observe(window.parent.document.body, {{ childList: true, subtree: true }});
    </script>
    """, unsafe_allow_html=True)


# ---------------- Search & Find Expander ----------------
with st.sidebar.expander("Search & Find", expanded=False):
    st.caption("Zoek gericht naar kaarten voor je deck")

    # ---------------- Filters ----------------
    set_filter = st.text_input(
        "Set Filter (bijv. MH2,SPM)",
        help="voer hier 1 of meerdere MTG setcodes in gescheiden met een komma",
        key="set_filter"
    )

    analyse_types = [
        "Ramp", "Card Advantage", "Protection",
        "Interruption", "Mass Interruption",
        "Keywords", "Kindred"
    ]
    selected_analyses = st.multiselect(
        "Category Filter",
        analyse_types,
        key="analyse_multiselect"
    )
    close_multiselect_on_select("analyse_multiselect")

    type_filter = st.selectbox(
        "Cardtype Filter",
        ["All", "Creature", "Instant", "Sorcery", "Enchantment", "Artifact", "Land", "Legendary"],
        key="type_filter"
    )

    rarity_filter = st.selectbox(
        "Rarity Filter",
        ["All", "Common", "Uncommon", "Rare", "Mythic"],
        key="rarity_filter"
    )

    deck_include = st.checkbox(
        "Met bestaande kaarten",
        value=False,
        key="deck_include_checkbox"
    )

    # --- Kindred selectie ---
    if "Kindred" in selected_analyses and st.session_state.get('commander_types', []):
        auto_kindred = st.multiselect(
            "Selecteer Kindred creature types",
            sorted(st.session_state['commander_types']),
            key="kindred_multiselect"
        )
        close_multiselect_on_select("kindred_multiselect")

        custom_kindred = st.text_input(
            "Of voeg zelf een creature type toe:",
            key="custom_kindred_input"
        )

    # --- Keywords selectie ---
    if "Keywords" in selected_analyses:
        keywords_options = ["Andere"] + st.session_state.get('keywords_list', [])
        selected_keywords = st.multiselect(
            "Selecteer Keywords",
            keywords_options,
            key="keywords_multiselect"
        )
        close_multiselect_on_select("keywords_multiselect")

        if "Andere" in selected_keywords:
            custom_keyword = st.text_input("Voer een eigen keyword in:", key="custom_keyword_input")

    # ---------------- Submit Button ----------------
    start_btn = st.button("Show Results")

    # ---------------- Sort Option ----------------
    sort_option = st.selectbox(
        "Sort Results:",
        ["Geen", "Naam A-Z", "Naam Z-A", "Mana Value Laag-Hoog",
         "Mana Value Hoog-Laag", "Releasedatum Oud-Nieuw", "Releasedatum Nieuw-Oud"]
    )
# Controleer of er iets is ingevuld/geklikt in de analyse-sectie
user_changed_input = (
    bool(set_filter.strip()) or
    bool(selected_analyses) or
    type_filter != "All" or
    deck_include
)

# Als er een wijziging is, trigger de analyse alsof op de knop is gedrukt
if user_changed_input and not start_btn:
    start_btn = True


# ------------------ Export expander ------------------

with st.sidebar.expander("Deck-Box", expanded=False):
    st.caption("Toegevoegde kaarten, klaar voor export")

    # Knop om Deck-Box in hoofdscherm te tonen (unieke key)
    if st.button("Bekijk Deck-Box", key="show_deck_box_btn"):
        st.session_state["show_deck_box_in_main"] = True

    deck_box = st.session_state.get("deck_box", [])
    if deck_box:
        # Alleen de namen voor export
        export_data = [c["name"] for c in deck_box]

        # --- CSV genereren ---
        csv_buffer = io.StringIO()
        for name in export_data:
            csv_buffer.write(f"{name}\n")
        csv_data = csv_buffer.getvalue()

        # Download button
        st.download_button(
            label="Download als CSV",
            data=csv_data,
            file_name="deck_box.csv",
            mime="text/csv"
        )

        # Clipboard copy via text area
        st.text_area("Copy to Clipboard", value=csv_data, height=200)

    else:
        st.info("Je Deck-Box is nog leeg.")

# ------------------ Weergave Instellingen ------------------
with st.sidebar.expander("Weergave instellingen", expanded=False):
    st.session_state["cards_per_row"] = st.slider(
        "Kaarten per rij",
        min_value=1,
        max_value=9,
        value=6,        # standaardwaarde
        step=1,
        help="Kies hoeveel kaarten je naast elkaar wilt zien in de resultaten"
    )

# ------------------ OVERRIDE: als Deck-Box open is, toon alléén Deck-Box ------------------
if st.session_state.get("show_deck_box_in_main", False):
    deck_box = st.session_state.get("deck_box", [])
    st.subheader("Mijn Deck-Box")

    if not deck_box:
        st.info("Je Deck-Box is nog leeg.")
    else:
        # gebruik de waarde uit de slider (default 6 als er nog niets ingesteld is)
        columns_per_row = st.session_state.get("cards_per_row", 6)

        for i in range(0, len(deck_box), columns_per_row):
            row_cards = deck_box[i:i+columns_per_row]
            cols = st.columns(columns_per_row)  # altijd gekozen aantal kolommen

            # vul alleen zoveel kolommen als er kaarten zijn
            for col, card in zip(cols, row_cards):
                with col:
                    img_url = card.get("image_uris", {}).get("normal") or \
                              card.get("card_faces", [{}])[0].get("image_uris", {}).get("normal") or \
                              "https://via.placeholder.com/223x310?text=Geen+afbeelding"
                    name = card.get("name", "Onbekend")

                    st.markdown(f"""
                    <div class="card-hover-container" style="height: 320px;">
                        <img src="{img_url}" title="{name}" style="height:260px; width:auto; object-fit:contain;" />
                        <div class="card-name" title="{name}">{name}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    remove_key = f"deckbox_remove_{card.get('id', name)}"
                    if st.button("✖", key=remove_key, help="Verwijder uit Deck-Box"):
                        st.session_state["deck_box"] = [
                            c for c in st.session_state.get("deck_box", [])
                            if c.get("id", c.get("name")) != card.get("id", name)
                        ]
                        # persistente opslag bijwerken
                        user_deck_key = get_user_deck_key()
                        cache[user_deck_key + "_cards"] = st.session_state["deck_box"]

                        st.session_state["show_deck_box_in_main"] = True
                        st.toast(f"{name} verwijderd uit Deck-Box ❌")

            # de overige lege kolommen blijven vanzelf leeg

    if st.button("Sluit Deck-Box", key="close_deck_box_btn"):
        st.session_state["show_deck_box_in_main"] = False

    st.stop()

# ------------------ Deck laden ------------------
def load_deck(deck_name):
    if not deck_name or deck_name not in st.session_state.get("deck_options", {}):
        st.session_state.update({
            "deck_loaded": False,
            "deck_card_names": set(),
            "color_identity": set(),
            "commander_types": set(),
            "commanders": [],
            "cards": []
        })
        return

    spinner_ph = show_mana_spinner(f"Deck '{deck_name}' wordt geladen...")
    deck_id = st.session_state["deck_options"][deck_name]
    archidekt_data = safe_api_call(f"https://archidekt.com/api/decks/{deck_id}/")
    if not archidekt_data:
        spinner_ph.empty()
        st.warning("Kan deck niet laden")
        return

    cards = archidekt_data.get("cards", [])
    st.session_state["cards"] = cards
    st.session_state["deck_card_names"] = {
        c["card"]["oracleCard"]["name"].lower()
        for c in cards
        if "card" in c and "oracleCard" in c["card"]
    }

    commanders_tmp = []
    for c in cards:
        cname = c["card"]["oracleCard"]["name"]
        if any(cat in c.get("categories", []) for cat in ["Commander", "Partner", "Background"]):
            if cname not in commanders_tmp:
                commanders_tmp.append(cname)

    ci_from_commanders = set()
    commander_types_tmp = set()
    for cname in commanders_tmp:
        scry = safe_api_call(f"https://api.scryfall.com/cards/named?exact={quote_plus(cname)}")
        if scry:
            ci_from_commanders.update(scry.get("color_identity", []))
            type_line = scry.get("type_line", "")
            if "—" in type_line:
                sub = type_line.split("—", 1)[1]
                for t in re.split(r"[ /]", sub):
                    t = t.strip()
                    if t:
                        commander_types_tmp.add(t)

    st.session_state.update({
        "full_deck": [],
        "commanders": commanders_tmp,
        "color_identity": ci_from_commanders,
        "commander_types": commander_types_tmp,
        "deck_loaded": True
    })
    spinner_ph.empty()


# ------------------ Laad deck bij selectie ------------------
if st.session_state.get("selected_deck_name", "") != st.session_state.get("last_loaded_deck", ""):
    st.session_state["last_loaded_deck"] = st.session_state.get("selected_deck_name", "")
    if st.session_state["selected_deck_name"]:
        load_deck(st.session_state["selected_deck_name"])

# ------------------ Commander weergeven ------------------
if st.session_state.get("deck_loaded") and st.session_state.get("commanders"):
    st.subheader(f"Commander(s): {', '.join(st.session_state['commanders'])}")
    cols = st.columns(len(st.session_state["commanders"]))
    for i, name in enumerate(st.session_state["commanders"]):
        with cols[i]:
            scry = safe_api_call(f"https://api.scryfall.com/cards/named?exact={quote_plus(name)}")
            if scry and "image_uris" in scry:
                st.image(scry["image_uris"]["normal"], width=200, caption=name)

# ------------------ Show my Deck ------------------
if st.session_state.get("deck_loaded") and st.session_state.get("show_deck", False):
    st.subheader(f"Volledig Deck: {st.session_state['selected_deck_name']}")

    # Spinner starten
    spinner_ph = show_mana_spinner("2 woorden-9 letters: Deck Laden...")

    card_objs = []
    for c in st.session_state["cards"]:
        scry = safe_api_call(f"https://api.scryfall.com/cards/named?exact={quote_plus(c['card']['oracleCard']['name'])}")
        if scry:
            card_objs.append(scry)
        else:
            card_objs.append({
                "name": c["card"]["oracleCard"]["name"],
                "image_uris": {"normal": "https://via.placeholder.com/223x310?text=Geen+afbeelding"}
            })

    # Kaarten renderen nadat alles geladen is
    render_cards_with_add(card_objs)

    # Spinner verwijderen
    spinner_ph.empty()

# ------------------ Alternative Commanders Block ------------------
selected_commanders = st.session_state.get("commanders", [])
combined_colors = set()

if selected_commanders:
    for cname in selected_commanders:
        cdata = safe_api_call(f"https://api.scryfall.com/cards/named?exact={quote_plus(cname)}")
        if cdata:
            combined_colors.update(cdata.get("color_identity", []))

if st.session_state.get("alt_commander_toggle", False):
    if not selected_commanders:
        st.info("Selecteer eerst een commander in je deck.")
    else:
        show_backgrounds = st.checkbox("Toon Backgrounds")
        extra_cards = []
        if show_backgrounds:
            spinner_ph = show_mana_spinner("Laden van backgrounds...")
            bg_results = scryfall_search_all_limited(
                "type:background game:paper legal:commander", max_cards=300
            )
            for card in bg_results:
                colors = set(card.get("color_identity", []))
                if colors.issubset(combined_colors):
                    extra_cards.append(card)

            cab_results = scryfall_search_all_limited(
                'type:legendary oracle:"choose a background" game:paper legal:commander', max_cards=300
            )
            for card in cab_results:
                colors = set(card.get("color_identity", []))
                if colors.issubset(combined_colors):
                    extra_cards.append(card)

            spinner_ph.empty()
            if extra_cards:
                st.subheader("Backgrounds & Choose a Background")
                render_cards_with_add(extra_cards)
            else:
                st.info("Geen backgrounds gevonden.")

        spinner_ph = show_mana_spinner("Laden van alt commanders...")
        alt_commanders = []
        if combined_colors:
            ci_string = "".join(sorted(combined_colors))
            alt_query = f"is:commander game:paper legal:commander ci={ci_string}"
            results = scryfall_search_all_limited(alt_query, max_cards=300)
            for card in results:
                type_line = card.get("type_line", "").lower()
                if "legendary creature" in type_line or (
                    "legendary artifact" in type_line and any(sub in type_line for sub in ["vehicle", "spaceship"])
                ):
                    alt_commanders.append(card)
        spinner_ph.empty()

        if alt_commanders:
            sort_option_alt = st.selectbox(
                "Sorteer Alt Commanders op:",
                [
                    "Naam A-Z",
                    "Naam Z-A",
                    "Mana Value Laag-Hoog",
                    "Mana Value Hoog-Laag",
                    "Releasedatum Oud-Nieuw",
                    "Releasedatum Nieuw-Oud",
                ],
            )
            if sort_option_alt == "Naam A-Z":
                alt_commanders.sort(key=lambda c: c.get("name", "").lower())
            elif sort_option_alt == "Naam Z-A":
                alt_commanders.sort(key=lambda c: c.get("name", "").lower(), reverse=True)
            elif sort_option_alt == "Mana Value Laag-Hoog":
                alt_commanders.sort(key=lambda c: c.get("cmc", 0))
            elif sort_option_alt == "Mana Value Hoog-Laag":
                alt_commanders.sort(key=lambda c: c.get("cmc", 0), reverse=True)
            elif sort_option_alt == "Releasedatum Oud-Nieuw":
                alt_commanders.sort(key=lambda c: c.get("released_at", ""))
            elif sort_option_alt == "Releasedatum Nieuw-Oud":
                alt_commanders.sort(key=lambda c: c.get("released_at", ""), reverse=True)

            st.subheader("Alternative Commanders")
            render_cards_with_add(alt_commanders)
        else:
            st.info("Geen alternatieve commanders gevonden.")

# ------------------ Analyse functies ------------------
def filter_card(card, analyse, kindred_selection=None, keywords_selection=None):
    text = card.get("oracle_text", "").lower()
    name = card.get("name", "").lower()
    type_line = card.get("type_line", "").lower()
    cmc = card.get("cmc", 0)

    if analyse == "Card Advantage":
        draw_keywords = ["draw a card", "draw two cards", "draw three cards", "draw x cards", "draw"]
        tutor_keywords = ["search your library", "find a", "put into your hand", "reveal"]
        graveyard_keywords = ["return target", "from your graveyard to your hand"]
        return any(k in text for k in draw_keywords+tutor_keywords+graveyard_keywords)
    elif analyse == "Ramp":
        if type_line.startswith("land"):
            return False
        ramp_artifacts = ["sol ring", "arcane signet", "mana crypt", "fellwar stone", "mana vault", "grisly salvage"]
        if "ramp" in card.get("oracle_tags", []) or any(x in name for x in ramp_artifacts) or any(k in text for k in ["add", "search", "basic land"]) or cmc <= 3 and any(k in text for k in ["add", "search"]):
            return True
        return False
    elif analyse == "Protection":
        return any(k in text for k in ["hexproof","shroud","indestructible","protection from"])
    elif analyse == "Interruption":
        return any(k in text for k in ["counter target","destroy target","exile target","bounce target","tap target","return target"])
    elif analyse == "Mass Interruption":
        return any(k in text for k in ["each opponent","each player","all creatures","all artifacts","all enchantments","all lands","destroy all","exile all","sacrifice all","discard all"])
    elif analyse == "Keywords":
        return any(kw.lower() in text for kw in (keywords_selection or []))
    elif analyse == "Kindred":
        return any(k.lower() in type_line for k in (kindred_selection or []))
    return False

# ------------------ Kindred / Keywords ------------------
kindred_selection = []
keywords_selection = []

# --- Kindred selectie ---
if "Kindred" in selected_analyses:
    st.write("**Kindred creature types**")
    auto_kindred = st.multiselect(
        "Selecteer Kindred creature types", 
        sorted(st.session_state.get('commander_types', [])),
        key="kindred_multiselect_sidebar"
    )
    custom_kindred = st.text_input(
        "Of voeg zelf een creature type toe:", 
        key="custom_kindred_input_sidebar"
    )
    kindred_selection = auto_kindred.copy()
    if custom_kindred.strip():
        kindred_selection.append(custom_kindred.strip().capitalize())

# --- Keywords selectie ---
if "Keywords" in selected_analyses:
    st.write("**Keyword selectie**")
    # Plaats "Andere" bovenaan
    keywords_options = ["Andere"] + st.session_state.get('keywords_list', [])
    selected_keywords = st.multiselect(
        "Selecteer Keywords", 
        keywords_options,
        key="keywords_multiselect_sidebar"
    )

    # Voeg custom keyword toe indien "Andere" is geselecteerd
    custom_keyword = ""
    if "Andere" in selected_keywords:
        custom_keyword = st.text_input(
            "Voer een eigen keyword in:", 
            key="custom_keyword_input_sidebar"
        )

    keywords_selection = [kw.lower() for kw in selected_keywords if kw != "Andere"]
    if custom_keyword.strip():
        keywords_selection.append(custom_keyword.strip().lower())


# ------------------ Analyse uitvoeren (met spinner) ------------------
if start_btn:
    codes = [code.strip() for code in set_filter.split(",") if code.strip()]
    deck_loaded = st.session_state.get('deck_loaded', False)
    ci = st.session_state.get('color_identity', set()) if deck_loaded else set()
    deck_card_names = st.session_state.get('deck_card_names', set())

    if codes:
        base_query = " OR ".join([f"set:{code}" for code in codes])
        if deck_loaded and ci:
            base_query += " ci<=" + order_colors_wubrg(ci)
    else:
        base_query = "game:paper legal:commander"
        from datetime import datetime
        current_year = datetime.now().year
        base_query += f" year>={current_year-3}"

    spinner_ph = show_mana_spinner("Analyseren kaarten...")
    results = scryfall_search_all_limited(base_query, max_cards=5000)

    if type_filter != "All" and results:
        type_filter_lower = type_filter.lower()
        if type_filter_lower == "legendary":
            results = [c for c in results if "legendary" in c.get("type_line","").lower()]
        elif type_filter_lower == "land":
            results = [c for c in results if "land" in c.get("type_line","").lower()]
        else:
            results = [c for c in results if type_filter_lower in c.get("type_line","").lower()]

    if selected_analyses and results:
        filtered_results = []
        for analyse in selected_analyses:
            for card in results:
                if filter_card(card, analyse, kindred_selection, keywords_selection):
                    filtered_results.append(card)
        results = list({c['id']: c for c in filtered_results}.values())

    if st.session_state.get('deck_loaded', False) and not deck_include:
        results = [c for c in results if c['name'].lower() not in deck_card_names]

    # Filter op rarity
    if rarity_filter != "All" and results:
        results = [c for c in results if c.get("rarity", "").lower() == rarity_filter.lower()]
    
    # --------- SORTEER RESULTATEN ----------
    if results and sort_option != "Geen":
        if sort_option == "Naam A-Z":
            results.sort(key=lambda c: c.get("name","").lower())
        elif sort_option == "Naam Z-A":
            results.sort(key=lambda c: c.get("name","").lower(), reverse=True)
        elif sort_option == "Mana Value Laag-Hoog":
            results.sort(key=lambda c: c.get("cmc",0))
        elif sort_option == "Mana Value Hoog-Laag":
            results.sort(key=lambda c: c.get("cmc",0), reverse=True)
        elif sort_option == "Releasedatum Oud-Nieuw":
            results.sort(key=lambda c: c.get("released_at",""))
        elif sort_option == "Releasedatum Nieuw-Oud":
            results.sort(key=lambda c: c.get("released_at",""), reverse=True)

    spinner_ph.empty()
    st.success(f"{len(results)} kaarten gevonden.")
    render_cards_with_add(results)


# ------------------ Bear Search, Zoek set, Sheriff & Ketchup ------------------
def bear_and_sheriff_toggle(selected_deck_name=None):
    deck_changed = selected_deck_name is not None and selected_deck_name != st.session_state.get('selected_deck_name', '')
    any_toggle_changed = (st.session_state.get('show_deck') or st.session_state.get('alt_commander_toggle') or st.session_state.get('start_analysis'))
    if st.session_state.get('bear_search_active', False) and (deck_changed or any_toggle_changed):
        st.session_state['bear_search_active'] = False
    if deck_changed:
        st.session_state['selected_deck_name'] = selected_deck_name
        load_deck(selected_deck_name)
    st.session_state.setdefault("bear_search_active", False)
    st.session_state.setdefault("sheriff_active", False)
    st.session_state.setdefault("ketchup_active", False)
    st.session_state.setdefault("zoekset_active", False)

    with st.sidebar:
        st.markdown(
            """
            <style>
            .toggle-button button { 
                width: 60px !important; 
                height: 60px !important; 
                border-radius: 12px !important; 
                font-size: 24px !important; 
                font-weight: bold !important; 
                cursor: pointer; 
                border: none !important; 
                transition: all 0.2s ease-in-out; 
                text-align: center; 
                margin: 4px; 
            }
            </style>
            """, unsafe_allow_html=True
        )
        
        col_empty_left, col_sets, col_ketchup, col_bear, col_sheriff, col_empty_right = st.columns([1, 1, 1, 1, 1, 1])

        with col_sets:
            btn_label = "📚" if not st.session_state["zoekset_active"] else "❌"
            hover_text = "Zoek Set Codes" if not st.session_state["zoekset_active"] else "Sluit Set Codes"
            if st.button(btn_label, key="sets_toggle_button", help=hover_text):
                st.session_state["zoekset_active"] = not st.session_state["zoekset_active"]
                st.rerun()

        with col_ketchup:
            btn_label = "🍅" if not st.session_state["ketchup_active"] else "❌"
            hover_text = "Ketch-Up" if not st.session_state["ketchup_active"] else "I like Mayo"
            if st.button(btn_label, key="ketchup_toggle_button", help=hover_text):
                st.session_state["ketchup_active"] = not st.session_state["ketchup_active"]
                st.rerun()

        with col_bear:
            btn_label = "🐻" if not st.session_state["bear_search_active"] else "❌"
            hover_text = "Bear Hunt" if not st.session_state["bear_search_active"] else "No more Bears"
            if st.button(btn_label, key="bear_toggle_button", help=hover_text):
                st.session_state["bear_search_active"] = not st.session_state["bear_search_active"]
                st.rerun()

        with col_sheriff:
            btn_label = "🌟" if not st.session_state["sheriff_active"] else "❌"
            hover_text = "Be the Sheriff" if not st.session_state["sheriff_active"] else "Shoot the Sheriff"
            if st.button(btn_label, key="sheriff_toggle_button", help=hover_text):
                st.session_state["sheriff_active"] = not st.session_state["sheriff_active"]
                st.rerun()
       
       # ------------------ Zoek Set actie ------------------
    if st.session_state.get("zoekset_active", False):
        spinner_ph = show_mana_spinner("Sets ophalen...")
        sets_data = safe_api_call("https://api.scryfall.com/sets")
        spinner_ph.empty()

        if sets_data and "data" in sets_data:
            # Categorieën
            set_type_options = {
                "main": "Main Sets",
                "commander": "Commander",
                "special": "Specials"
            }

            # Default = Main Sets
            selected_types = st.multiselect(
                "Selecteer Set Categories", list(set_type_options.values()), default=["Main Sets"]
            )

            # Filter de sets
            sets_list = []
            for s in sets_data["data"]:
                set_type = s.get("set_type","").lower()

                if "Main Sets" in selected_types and set_type in ["core","expansion"]:
                    sets_list.append(s)
                elif "Commander" in selected_types and set_type == "commander":
                    sets_list.append(s)
                elif "Specials" in selected_types and set_type in ["masters","funny","promo","draft_innovation","planechase"]:
                    sets_list.append(s)

            # Sorteren van nieuw naar oud
            sets_list.sort(key=lambda s: s.get("released_at", "1900-01-01"), reverse=True)

            st.subheader(f"Paper MTG Sets gevonden: {len(sets_list)}")

            cols_per_row = 8
            row_cols = []

            # CSS voor groene logos, subtiele glow en padding zodat logo niet wordt afgesneden
            st.markdown("""
                <style>
                .logo-green {
                    filter: invert(40%) sepia(100%) saturate(500%) hue-rotate(90deg);
                    transition: all 0.2s ease-in-out;
                    width: 64px;
                    height: 64px;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    border-radius: 50%;
                    padding: 4px; /* extra ruimte voor glow */
                    background-color: transparent;
                }
                .logo-green:hover {
                    filter: invert(40%) sepia(100%) saturate(700%) hue-rotate(90deg) brightness(1.2);
                    box-shadow: 0 0 10px 4px rgba(211, 40, 118, 0.6); /* subtiele glow */
                }
                .set-name {
                    text-align: center;
                    color: white;
                    font-size: 14px;
                    margin: 4px 0 0 0;
                    overflow: hidden;
                    white-space: nowrap;
                    text-overflow: ellipsis;
                }
                .set-code {
                    text-align: center;
                    font-size: 12px;
                    color: gray;
                }
                </style>
            """, unsafe_allow_html=True)

            for i, s in enumerate(sets_list):
                code = s.get("code", "").upper()
                name = s.get("name", "Onbekend")
                logo_url = s.get("icon_svg_uri", None)

                # Nieuwe rij voor elke 8 sets
                if i % cols_per_row == 0:
                    row_cols = st.columns(cols_per_row)

                col = row_cols[i % cols_per_row]
                with col:
                    if logo_url:
                        st.markdown(f'<img src="{logo_url}" class="logo-green" alt="{name}">', unsafe_allow_html=True)
                    st.markdown(f'<div class="set-name">{name}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="set-code">[{code}]</div>', unsafe_allow_html=True)

        else:
            st.error("Geen sets gevonden.")

    # ------------------ Ketchup actie ------------------
    if st.session_state["ketchup_active"]:
        spinner_ph = st.empty()
        with spinner_ph.container():
            st.info("🍅 Ketchup in actie... Even geduld!")
            import time
            time.sleep(1.5)  # Placeholder delay voor visueel effect
        spinner_ph.empty()

        st.subheader("Ketchup Items:")
        example_items = ["Ketchup Card 1", "Ketchup Card 2", "Ketchup Card 3"]
        for item in example_items:
            st.markdown(f"- {item}")

    # ------------------ Bear actie ------------------
    if st.session_state["bear_search_active"]:
        spinner_ph = show_mana_spinner("Bears Incoming...")
        bear_cards = scryfall_search_all_limited("art:bear", max_cards=200)
        spinner_ph.empty()
        st.subheader(f"Bears Found: ({len(bear_cards)})")
        render_cards_with_add(bear_cards)

    # ------------------ Sheriff actie ------------------
    if st.session_state["sheriff_active"]:
        try:
            sheriff_img = Image.open("Sherrif - Commander.png")
            st.image(sheriff_img, use_container_width=False, output_format="PNG", clamp=False, width=None, caption=None)
            st.markdown("<style>img[alt=''] {max-height:90vh; height:auto; width:auto;}</style>", unsafe_allow_html=True)
        except:
            st.error("Afbeelding 'Sherrif - Commander.png' niet gevonden.")

bear_and_sheriff_toggle(st.session_state.get('selected_deck_name'))

# ------------------ Footer ------------------
def footer():
    year = datetime.datetime.now().year
    
    footer_html = f"""
    <div class="footer">
        <div>CommanderDeckDoctor</div>
        <div>© SdB {year}</div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

footer()

 

