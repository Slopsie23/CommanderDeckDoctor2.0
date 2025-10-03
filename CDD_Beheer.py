import streamlit as st
from supabase import create_client, Client
import pandas as pd
import requests
from PIL import Image
import time

st.set_page_config(layout="wide")

# ------------------ Achtergrond gradient ------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #001900, #150f30);
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Logo en titel ------------------
try:
    logo = Image.open("12.png")
    col1, col2 = st.columns([1,6])
    with col1:
        st.image(logo, use_container_width=True)
    with col2:
        st.markdown("<h1 style='margin:0; padding-top:15px;'>Beheer</h1>", unsafe_allow_html=True)
except:
    st.warning("Logo niet gevonden. Upload '12.png'.")

# ------------------ Supabase setup ------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------ Cache voor decknamen ------------------
@st.cache_data
def get_deck_name(deck_id):
    try:
        url_api = f"https://archidekt.com/api/decks/{deck_id}/"
        r = requests.get(url_api, timeout=5)
        if r.status_code == 200:
            return r.json().get("name", deck_id)
        return deck_id
    except:
        return deck_id

# ------------------ Placeholder voor tabel ------------------
table_placeholder = st.empty()

# ------------------ Functie tabel renderen ------------------
def render_user_table(filter_username=""):
    try:
        response = supabase.table("user_decks").select("*").execute()
        all_users = response.data
    except:
        all_users = []

    if not all_users:
        table_placeholder.info("Geen gebruikers gevonden.")
        return all_users

    df = pd.DataFrame(all_users)

    if "user_name" in df.columns:
        df["Gebruikersnaam"] = df["user_name"].apply(lambda x: x.capitalize())
    if "deck_data" in df.columns:
        df["Aantal Decks"] = df["deck_data"].apply(lambda x: len(x) if x else 0)

        def get_decks(deck_list):
            if not deck_list:
                return ""
            return "\n".join([f"[{d}] - {get_deck_name(d)}" for d in deck_list])
        df["Decks"] = df["deck_data"].apply(get_decks)

    # Filter op gebruikersnaam
    if filter_username:
        df = df[df["Gebruikersnaam"].str.lower().str.contains(filter_username)]

    # Tabel in dezelfde placeholder
    table_placeholder.dataframe(df[["Gebruikersnaam", "Aantal Decks", "Decks"]], use_container_width=True)
    return all_users

# ------------------ Zoekveld ------------------
filter_username = st.text_input("Zoek gebruiker (optioneel):", value="").strip().lower()
all_users = render_user_table(filter_username)

st.markdown("---")

# ------------------ Gebruikers en decks beheren ------------------
with st.container():
    container_style = "max-width:900px; margin:auto;"
    st.markdown(f"<div style='{container_style}'>", unsafe_allow_html=True)

    # --- Nieuwe gebruiker toevoegen ---
    st.subheader("Nieuwe gebruiker toevoegen")
    new_user = st.text_input("Naam nieuwe gebruiker", key="new_user_input")
    if st.button("Gebruiker toevoegen"):
        if new_user.strip():
            exists = supabase.table("user_decks").select("*").eq("user_name", new_user.lower()).execute()
            if exists.data:
                st.warning("Gebruiker bestaat al.")
            else:
                supabase.table("user_decks").insert({"user_name": new_user.lower(), "deck_data": []}).execute()
                st.success(f"Gebruiker '{new_user}' toegevoegd!")
                all_users = render_user_table(filter_username)
        else:
            st.error("Voer een geldige gebruikersnaam in.")

    st.markdown("---")

    # --- Decks beheren ---
    st.subheader("Decks beheren")
    if all_users:
        user_names = [u["user_name"] for u in all_users]
        selected_user = st.selectbox("Selecteer gebruiker", user_names, key="deck_user_select")
        
        deck_action = st.radio("Actie", ["Deck toevoegen", "Deck verwijderen"], key="deck_action_radio")
        
        user_record = supabase.table("user_decks").select("*").eq("user_name", selected_user).execute()
        current_decks = user_record.data[0]["deck_data"] if user_record.data and user_record.data[0]["deck_data"] else []

        # Mapping van naam -> ID
        deck_name_map = {get_deck_name(d): d for d in current_decks}

        if deck_action == "Deck toevoegen":
            deck_id_input = st.text_input("Deck ID (Archidekt)", key="deck_id_input_add")
        else:
            if deck_name_map:
                selected_deck_name = st.selectbox("Selecteer deck om te verwijderen", list(deck_name_map.keys()))
                deck_id_input = deck_name_map[selected_deck_name]
            else:
                st.info("Deze gebruiker heeft geen decks om te verwijderen.")
                deck_id_input = None

        if st.button("Uitvoeren", key="deck_action_btn"):
            if not deck_id_input:
                st.error("Voer een geldige deck-ID in.")
            else:
                if deck_action == "Deck toevoegen":
                    if deck_id_input in current_decks:
                        st.warning("Deck bestaat al voor deze gebruiker.")
                    else:
                        current_decks.append(deck_id_input)
                        supabase.table("user_decks").update({"deck_data": current_decks}).eq("user_name", selected_user).execute()
                        st.success(f"Deck '{deck_id_input}' toegevoegd aan {selected_user}.")
                        time.sleep(1)
                        all_users = render_user_table(filter_username)
                else:  # Deck verwijderen
                    if deck_id_input in current_decks:
                        current_decks.remove(deck_id_input)
                        supabase.table("user_decks").update({"deck_data": current_decks}).eq("user_name", selected_user).execute()
                        # Tijdelijke melding
                        placeholder = st.empty()
                        placeholder.success(f"Deck '{selected_deck_name}' verwijderd van {selected_user}.")
                        time.sleep(2)
                        placeholder.empty()
                        # Tabel opnieuw laden op dezelfde placeholder
                        all_users = render_user_table(filter_username)
                    else:
                        st.warning("Deck-ID niet gevonden voor deze gebruiker.")

    st.markdown("---")

    # --- Gebruiker verwijderen ---
    st.subheader("Gebruiker verwijderen")
    if all_users:
        user_to_delete = st.selectbox("Selecteer gebruiker om te verwijderen", user_names, key="delete_user_select")
        if st.button("Verwijder gebruiker", key="delete_user_btn"):
            supabase.table("user_decks").delete().eq("user_name", user_to_delete).execute()
            st.success(f"Gebruiker '{user_to_delete}' verwijderd.")
            all_users = render_user_table(filter_username)

    st.markdown("</div>", unsafe_allow_html=True)
