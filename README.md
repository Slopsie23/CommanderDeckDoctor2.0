# CommanderDeckDoctor

CommanderDeckDoctor is een app voor Commander-spelers van Magic: The Gathering.  
De app helpt om snel nieuwe kaarten te vinden voor bestaande decks.
Daarnaast zijn er handige tools om je game-time en spare-time mee te vullen. 

---

## 🚀 Getting Started

**1. Voer je gebruikersnaam in bij Decks**  
Zo onthoudt de app automatisch jouw decks en instellingen voor toekomstige sessies.

**2. Importeer een deck vanuit Archidekt**  
Kopieer de deck-ID uit de Archidekt-URL en plak deze in de app. Het deck wordt geladen en de kaarten verschijnen in een overzichtelijke grid.

**3. Bekijk je deck**  
Gebruik de toggle *Show Deck* om de kaartenlijst weer te geven. Commander(s) en mogelijke backgrounds worden automatisch herkend.

**4. Zoek naar kaarten uit nieuwe sets bij Search & Find**  
Kies een setcode (bijv. MH2, WOE) en verfijn je selectie met filters zoals kaarttype, categorie of keywords.

**5. Vul je Deck-Box**  
Voeg interessante kaarten toe aan je Deck-Box. Deze blijft bewaard voor volgende sessies en kan nu ook geëxporteerd, gekopieerd of verwijderd worden — alles live, zonder opnieuw te laden.

**6. Gebruik extra tools in Good Stuff**  
Activeer de modules zoals **Set Search**, **Ketch-Up**, **Bear Search**, **Sheriff**, **Sound of Magic**, of de nieuwe **AI Judge Ruxa** om regels, kaarten of muziek te ontdekken.

---

## 🧭 Gebruikersinformatie

### 📘 Mijn Decks
Beheer je persoonlijke decks.  
Je kunt decks importeren, verwijderen en bekijken.  
De app herkent automatisch commander(s), kleuridentiteit en types.  
Kaarten worden in een responsieve grid getoond met hover-effecten en knoppen om kaarten toe te voegen of te verwijderen.

---

### 🧙‍♀️ Alternative Commanders
Toont alternatieve commanders die passen binnen de kleuridentiteit van je huidige deck.  
Ook *Backgrounds* worden automatisch herkend.  
De kaarten worden gesorteerd op basis van de instelling in *Weergave*.

---

### 🔍 Zoek en Vind
Filter kaarten op type, setcode, zeldzaamheid of categorie (zoals Ramp, Card Advantage of Protection).  
Nieuwe filters voor **Kindred** en **Keywords** helpen je om kaarten te vinden die passen bij je thema of mechanica.  
De resultaten worden automatisch ontdubbeld en in een dynamisch grid weergegeven.

---

### 🖥️ Weergave
Pas het aantal kaarten per rij aan en kies je sorteerwijze:  
Naam, Mana Value of Releasedatum (standaard: *Nieuw–Oud*).  
De lay-out past zich automatisch aan aan het schermformaat (mobiel, tablet of desktop).

---

### 📦 Deck-Box
Je persoonlijke verzamelplek voor kaarten die je wilt bewaren of later wilt toevoegen aan een deck.  
Voeg kaarten toe met ✚ of verwijder ze met ✖.  
De inhoud wordt per gebruiker opgeslagen in Supabase en automatisch geladen bij het opstarten.  
Je kunt de inhoud **exporteren als CSV**, **kopiëren** of **leegmaken** met één klik.  
Alles werkt live zonder herladen van de pagina.

---

### ❤️ Good Stuff
De *Good Stuff*-sectie bevat uitbreidbare tools:

* **⚖️ Judge Ruxa (AI)** – beantwoordt regelsvragen over kaarten met behulp van Google Gemini AI.  
* **🔍 Set Search** – doorzoek Magic-setcodes en bekijk recente uitbreidingen.  
* **🍅 Ketch-Up** – bekijk aankomende releases en spoilerlijsten.  
* **🐻 Bear Search** – zoek naar kaarten met beren in de art.  
* **⭐ Sheriff** – toont Commander-regels en richtlijnen.  
* **🎵 Sound of Magic** – stream een Commander-playlist via Spotify.  

Alle tools openen direct in het hoofdscherm en kunnen eenvoudig aan/uit worden gezet.

---

## ⚙️ Technische informatie

### Gebruikte APIs en services
* **Archidekt API** – haalt deckinformatie en kaartlijsten op.  
* **Scryfall API** – verzorgt kaartdata, zoekopdrachten, analyses en afbeeldingen.  
* **Supabase** – beheert gebruikers, decks en Deck-Box-gegevens in de cloud.  
* **Google Gemini AI** – ondersteunt de *Judge Ruxa*-functie voor regelsanalyse.  

### Technologie
Gebouwd met **Streamlit**, **Python**, **Pandas** en **diskcache** voor snelle lokale caching.  
Volledig **responsief** ontworpen met moderne CSS en werkt naadloos op mobiel en desktop.
