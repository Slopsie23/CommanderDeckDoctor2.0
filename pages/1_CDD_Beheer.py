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

    # ----------------- Nieuwe kolom: Aantal kaarten in Deck-Box -----------------
    def get_deckbox_count(user_name):
        try:
            res = supabase.table("user_deckbox").select("cards").eq("user_name", user_name).maybe_single().execute()
            if res and hasattr(res, "data") and res.data:
                return len(res.data.get("cards", []))
            else:
                # Geen record, aanmaken
                supabase.table("user_deckbox").insert({"user_name": user_name, "cards": []}).execute()
                return 0
        except:
            return 0

    df["Aantal kaarten in Deck-Box"] = df["user_name"].apply(get_deckbox_count)

    # Filter op gebruikersnaam
    if filter_username:
        df = df[df["Gebruikersnaam"].str.lower().str.contains(filter_username)]

    # Tabel in dezelfde placeholder
    table_placeholder.dataframe(
        df[["Gebruikersnaam", "Aantal Decks", "Aantal kaarten in Deck-Box", "Decks"]],
        use_container_width=True
    )
    return all_users


# ------------------ Zoekveld ------------------
filter_username = st.text_input("Zoek gebruiker (optioneel):", value="").strip().lower()
all_users = render_user_table(filter_username)

st.markdown("---")

# ------------------ Functie: veilige Deck-Box ophalen ------------------
def get_user_deckbox_cards(user_name: str):
    """Robuuste manier om kaarten van de Deck-Box op te halen zonder 204-fouten of meldingen."""
    try:
        res = supabase.table("user_deckbox").select("cards").eq("user_name", user_name).maybe_single().execute()

        # 1️⃣ Controleer of 'res' een dict met 'message':'Missing response' bevat
        if isinstance(res, dict) and res.get("code") == "204":
            # Geen record -> stil aanmaken
            try:
                supabase.table("user_deckbox").insert({"user_name": user_name, "cards": []}).execute()
            except Exception:
                pass
            return []

        # 2️⃣ Controleer of het object zelf een .data attribuut heeft
        data = getattr(res, "data", None)
        error = getattr(res, "error", None)

        # Supabase kan hier ook een dict in .error zetten met code 204
        if isinstance(error, dict) and error.get("code") == "204":
            try:
                supabase.table("user_deckbox").insert({"user_name": user_name, "cards": []}).execute()
            except Exception:
                pass
            return []

        # 3️⃣ Geen data gevonden? Maak record aan
        if not data:
            try:
                supabase.table("user_deckbox").insert({"user_name": user_name, "cards": []}).execute()
            except Exception:
                pass
            return []

        # 4️⃣ Data bevat kaarten
        if isinstance(data, dict):
            return data.get("cards", [])
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            return data[0].get("cards", [])
        else:
            return []

    except Exception as e:
        # 5️⃣ Vang alleen echte Python-fouten
        if isinstance(e, dict) and e.get("code") == "204":
            try:
                supabase.table("user_deckbox").insert({"user_name": user_name, "cards": []}).execute()
            except Exception:
                pass
            return []
        else:
            st.warning(f"Fout bij ophalen Deck-Box voor {user_name}: {e}")
            return []

# ------------------ Gebruikers, decks en deckbox beheren ------------------
with st.container():
    container_style = "max-width:900px; margin:auto;"
    st.markdown(f"<div style='{container_style}'>", unsafe_allow_html=True)

    if not all_users:
        st.stop()

    user_names = [u["user_name"] for u in all_users]

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
    selected_user = st.selectbox("Selecteer gebruiker", user_names, key="deck_user_select")
    
    deck_action = st.radio("Actie", ["Deck toevoegen", "Deck verwijderen"], key="deck_action_radio")
    
    user_record = supabase.table("user_decks").select("*").eq("user_name", selected_user).execute()
    current_decks = user_record.data[0]["deck_data"] if user_record.data and user_record.data[0]["deck_data"] else []
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
            else:
                if deck_id_input in current_decks:
                    current_decks.remove(deck_id_input)
                    supabase.table("user_decks").update({"deck_data": current_decks}).eq("user_name", selected_user).execute()
                    placeholder = st.empty()
                    placeholder.success(f"Deck '{selected_deck_name}' verwijderd van {selected_user}.")
                    time.sleep(2)
                    placeholder.empty()
                    all_users = render_user_table(filter_username)
                else:
                    st.warning("Deck-ID niet gevonden voor deze gebruiker.")

    st.markdown("---")

    # --- Deck-Box beheren ---
    st.subheader("Deck-Box beheren")
    selected_user_box = st.selectbox("Selecteer gebruiker voor Deck-Box beheer", user_names, key="deckbox_user_select")

    # Haal kaarten veilig op
    deckbox_cards = get_user_deckbox_cards(selected_user_box)

    if not deckbox_cards:
        st.info("Deze gebruiker heeft nog geen kaarten in de Deck-Box.")
    else:
        st.markdown(f"**Kaarten in Deck-Box ({len(deckbox_cards)})**")
        for card in deckbox_cards:
            st.text(f"- {card.get('name', card)}")

    # Knop om Deck-Box leeg te maken
    if st.button("Leeg Deck-Box", key="clear_deckbox_btn"):
        st.session_state["pending_clear_deckbox_for"] = selected_user_box

    if st.session_state.get("pending_clear_deckbox_for"):
        pending = st.session_state["pending_clear_deckbox_for"]
        st.warning(f"Weet je zeker dat je de Deck-Box van '{pending}' wilt leegmaken?")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("Ja, leegmaken", key="confirm_clear_deckbox_yes"):
                try:
                    res = supabase.table("user_deckbox").update({"cards": []}).eq("user_name", pending).execute()
                    # Als update niet effectief is of er is een response.error, probeer insert/upsert
                    if getattr(res, "error", None):
                        # probeer insert (fallback)
                        try:
                            supabase.table("user_deckbox").insert({"user_name": pending, "cards": []}).execute()
                        except Exception:
                            pass
                    st.success(f"Deck-Box van gebruiker '{pending}' is geleegd.")
                    all_users = render_user_table(filter_username)
                except Exception as e:
                    st.error(f"Fout bij legen van Deck-Box: {e}")
                finally:
                    st.session_state.pop("pending_clear_deckbox_for", None)
        with col_no:
            if st.button("Nee, annuleer", key="confirm_clear_deckbox_no"):
                st.session_state.pop("pending_clear_deckbox_for", None)
                st.info("Actie geannuleerd.")

    st.markdown("---")

    # --- Gebruiker verwijderen ---
    st.subheader("Gebruiker verwijderen")
    user_to_delete = st.selectbox("Selecteer gebruiker om te verwijderen", user_names, key="delete_user_select")
    # --- Gebruiker verwijderen (met bevestiging) ---
    if st.button("Verwijder gebruiker", key="delete_user_btn"):
        # markeer pending delete
        st.session_state["pending_delete_user"] = user_to_delete

    # Toon bevestigingsbox als er een pending delete is
    if st.session_state.get("pending_delete_user"):
        pending = st.session_state["pending_delete_user"]
        st.warning(f"Weet je zeker dat je '{pending}' wilt verwijderen?")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("Ja, verwijder gebruiker", key="confirm_delete_user_yes"):
                try:
                    supabase.table("user_decks").delete().eq("user_name", pending).execute()
                    st.success(f"Gebruiker '{pending}' verwijderd.")
                    # refresh tabel
                    all_users = render_user_table(filter_username)
                except Exception as e:
                    st.error(f"Fout bij verwijderen gebruiker: {e}")
                finally:
                    st.session_state.pop("pending_delete_user", None)
        with col_no:
            if st.button("Nee, annuleer", key="confirm_delete_user_no"):
                st.session_state.pop("pending_delete_user", None)
                st.info("Actie geannuleerd.")

