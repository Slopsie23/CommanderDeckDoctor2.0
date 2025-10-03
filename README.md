# CommanderDeckDoctor

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-orange?logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/jouwgebruikersnaam/CommanderDeckDoctor)](https://github.com/jouwgebruikersnaam/CommanderDeckDoctor/issues)

CommanderDeckDoctor is een interactieve Streamlit-app voor Magic: The Gathering spelers, gericht op Commander decks. Met deze app kun je decks importeren, analyseren, kaarten filteren en alternatieve commanders ontdekken. De app biedt daarnaast een visueel aantrekkelijke interface met hover-effecten, responsive grid-layouts en een geïntegreerde Deck-Box voor export.

---

## Features

- **Deck importeren**: Haal decks op van Archidekt via deck-ID.  
- **Deck-Box beheren**: Voeg kaarten toe of verwijder ze; exporteer naar CSV of kopieer naar clipboard.  
- **Kaarten zoeken en filteren**: Filter op Set, Type, Rarity, Keywords en Kindred.  
- **Alternatieve commanders & backgrounds**: Vind passende opties op basis van kleurenidentiteit en type.  
- **Visualisaties**: Responsive kaartweergave, mana-spinners en interactieve hover-effecten.  
- **Soundtrack integratie**: Stream een bijpassende Spotify-playlist rechtstreeks in de app.  
- **Persistente opslag**: Sla decks op in Supabase of lokaal JSON als fallback.  

---

## Technologieën

- Python 3  
- [Streamlit](https://streamlit.io)  
- [Supabase](https://supabase.com) voor opslag van gebruikersdecks  
- [Scryfall API](https://scryfall.com/docs/api) voor kaartgegevens  
- [DiskCache](https://pypi.org/project/diskcache/) voor lokale caching  
- HTML/CSS voor styling en hover-effecten  

---

## Installatie

1. Clone de repository:
```bash
git clone https://github.com/jouwgebruikersnaam/CommanderDeckDoctor.git
