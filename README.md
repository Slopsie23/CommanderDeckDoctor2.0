# CommanderDeckDoctor

CommanderDeckDoctor is een app voor Commander-spelers van Magic: The Gathering.  
De app helpt om snel nieuwe kaarten te vinden voor bestaande decks, alternatieve commanders te ontdekken en eigen decks te beheren.  
Alle gegevens worden automatisch geladen via Archidekt en Scryfall.

---

## 🚀 Getting Started



**1. Voer je gebruikersnaam in bij Decks**

Zo onthoudt de app automatisch jouw decks en instellingen voor toekomstige sessies.



**2. Importeer een deck vanuit Archidekt**

Kopieer de deck-ID uit de Archidekt-URL en plak deze in de app. Het deck wordt geladen en de kaarten verschijnen in een overzichtelijke grid.



**3. Bekijk je deck**

Gebruik de toggle Show my Deck om de kaartenlijst weer te geven. Commander(s) en mogelijke backgrounds worden automatisch herkend.



**4. Zoek naar kaarten uit nieuwe sets bij Search \& Find**

Kies een setcode (bijv. MH2, WOE) en verfijn je selectie met filters zoals kaarttype, categorie of keywords.



**5. Vul je Deck-Box**

Voeg interessante kaarten toe aan je Deck-Box. Deze blijft bewaard voor volgende sessies en kan gedownload of gekopieerd worden.



**6. Gebruik extra tools**

Probeer de Good Stuff-opties zoals Set Search, Ketch-Up, Bear Search, Sheriff en Sound of Magic voor extra gemak en fun.



---

## 🧭 Gebruikersinformatie

---

### 📘 Mijn Decks

In deze expander beheer je je persoonlijke decks.  
Je kunt decks importeren, verwijderen en bekijken.  
De app herkent automatisch de commander(s), hun kleuridentiteit en types.  
De kaarten in je deck worden weergegeven in een responsieve grid met hover-effecten en knoppen om kaarten toe te voegen of te verwijderen.  
Sortering en layout worden centraal geregeld via de *Weergave*-expander.

---

### 🧙‍♀️ Alternative Commanders

Toont alternatieve commanders die passen binnen de kleuridentiteit van je huidige deck.  
Daarnaast kun je *Backgrounds* en *Choose a Background*-kaarten tonen die compatibel zijn met jouw commander.  
De kaarten worden gesorteerd op basis van de gekozen optie in de Weergave-expander (standaard: **Releasedatum Nieuw–Oud**).  
Je kunt kiezen of je alleen backgrounds wilt tonen of ook alternatieve commanders.

---

### 🔍 Zoek en Vind

Met de analysefunctie zoek je naar kaarten die passen bij de strategie van je deck.  
Je kunt filteren op kaarttype, setcode, zeldzaamheid of categorie zoals Ramp, Card Advantage of Protection.  
Resultaten worden automatisch ontdubbeld en in een grid getoond, gesorteerd volgens de actieve weergave-instelling.

---

### 🖥️ Weergave

De Weergave-expander bepaalt centraal de layout en sortering van alle kaarten in de app.  
Beschikbare sorteeropties:

* Naam A–Z
* Naam Z–A
* Mana Value Laag–Hoog
* Mana Value Hoog–Laag
* Releasedatum Oud–Nieuw
* Releasedatum Nieuw–Oud *(standaard)*

Daarnaast kun je instellen hoeveel kaarten per rij worden weergegeven voor passende weergave bij verschillende schermformaten.  
De gekozen instellingen worden per sessie onthouden.

---

### 🎒 Good Stuff

De *Good Stuff*-sectie bevat extra tools die de app uitbreiden met handige of leuke functies:

* **🔍 Set Search** – doorzoek Magic-setcodes en bekijk recente uitbreidingen.
* **🍅 Ketch-Up** – bekijk aankomende releases en kaartpreviews.
* **🐻 Bear Search** – toont kaarten met beren in de afbeelding.
* **⭐ Sheriff** – toont spelregels en richtlijnen.
* **🎵 Sound of Magic** – speelt een Spotify-playlist voor Commander-avonden.

Elke tool opent automatisch in het hoofdscherm zodra de toggle is geactiveerd en moet uit worden gezet na gebruik.

---

### 📦 Deck-Box

De Deck-Box is je persoonlijke verzamelplek voor kaarten die je wilt bewaren of later wilt toevoegen aan een deck.  
Kaarten kunnen worden toegevoegd met de plusknop (✚) en verwijderd met de kruis-knop (✖).  
De inhoud blijft per gebruiker bewaard en wordt automatisch geladen bij het opstarten van de app.  
Je kunt de inhoud exporteren, kopiëren of downloaden als CSV-bestand.  
De Deck-Box werkt live zonder dat de pagina opnieuw hoeft te laden.

---

## ⚙️ Technische informatie

### API en Dataverwerking

* **Archidekt API** – haalt deckinformatie en kaartlijsten op.
* **Scryfall API** – verzorgt kaartdata, zoekopdrachten, analyses en previews.
* **Supabase** – slaat gebruikersspecifie
