# CommanderDeckDoctor

CommanderDeckDoctor is een app voor Commander-spelers van Magic: The Gathering.  
De app helpt om snel nieuwe kaarten te vinden voor bestaande decks, alternatieve commanders te ontdekken en eigen decks te beheren.  
Alle gegevens worden automatisch geladen via Archidekt en Scryfall.

---

## 🧭 Gebruikersinformatie

### Getting Started

1. **Voer je gebruikersnaam in** bij het onderdeel *Decks*.  
   De app onthoudt al je decks, instellingen en Deck-Box-inhoud voor volgende sessies.

2. **Importeer een deck** via Archidekt door de ID uit de deck-URL te kopiëren.  
   Zodra het deck geladen is, worden de kaarten automatisch weergegeven in een overzichtelijke grid.

3. **Gebruik de knop ‘Show Deck’** om het volledige deck te tonen of te verbergen.  
   Kaarten verschijnen in een responsieve weergave met hover-effect en sortering volgens je voorkeur.

---

### 📘 Expander: Deck Management

In deze expander beheer je je persoonlijke decks.  
Je kunt decks importeren, verwijderen en bekijken.  
De app herkent automatisch de commander(s), hun kleuridentiteit en types.  
De kaarten in je deck worden weergegeven in een responsieve grid met hover-effecten en knoppen om kaarten toe te voegen of te verwijderen.  
Sortering en layout worden centraal geregeld via de *Weergave*-expander.

---

### 🧙‍♀️ Expander: Alternative Commanders & Backgrounds

Toont alternatieve commanders die passen binnen de kleuridentiteit van je huidige deck.  
Daarnaast kun je *Backgrounds* en *Choose a Background*-kaarten tonen die compatibel zijn met jouw commander.  
De kaarten worden gesorteerd op basis van de gekozen optie in de Weergave-expander (standaard: **Releasedatum Nieuw–Oud**).  
Je kunt kiezen of je alleen backgrounds wilt tonen of ook alternatieve commanders.

---

### 🔍 Expander: Analyse

Met de analysefunctie zoek je naar kaarten die passen bij de strategie van je deck.  
Je kunt filteren op kaarttype, setcode, zeldzaamheid of categorie zoals Ramp, Card Advantage of Protection.  
Resultaten worden automatisch ontdubbeld en in een grid getoond, gesorteerd volgens de actieve weergave-instelling.

---

### 📦 Expander: Deck-Box

De Deck-Box is je persoonlijke verzamelplek voor kaarten die je wilt bewaren of later wilt toevoegen aan een deck.  
Kaarten kunnen worden toegevoegd met de plusknop (✚) en verwijderd met de kruis-knop (✖).  
De inhoud blijft per gebruiker bewaard en wordt automatisch geladen bij het opstarten van de app.  
Je kunt de inhoud exporteren, kopiëren of downloaden als CSV-bestand.  
De Deck-Box werkt live zonder dat de pagina opnieuw hoeft te laden.

---

### 🖥️ Expander: Weergave

De Weergave-expander bepaalt centraal de layout en sortering van alle kaarten in de app.  
De instelling geldt voor *Deck Management*, *Alternative Commanders*, *Bear Search* en *Ketch-Up*.  
Beschikbare sorteeropties:

- Naam A–Z  
- Naam Z–A  
- Mana Value Laag–Hoog  
- Mana Value Hoog–Laag  
- Releasedatum Oud–Nieuw  
- Releasedatum Nieuw–Oud *(standaard)*  

Daarnaast kun je instellen hoeveel kaarten per rij worden weergegeven.  
De gekozen instellingen worden per sessie onthouden.

---

### 🎒 Expander: Good Stuff

De *Good Stuff*-sectie bevat extra tools die de app uitbreiden met handige of leuke functies:

- **🔍 Set Search** – doorzoek Magic-setcodes en bekijk recente uitbreidingen.  
- **🍅 Ketch-Up** – bekijk aankomende releases en kaartpreviews.  
- **🐻 Bear Search** – toont kaarten met beren in de afbeelding.  
- **⭐ Sheriff** – toont spelregels of richtlijnen.  
- **🎵 Sound of Magic** – speelt een Spotify-playlist voor Commander-avonden.  

Elke tool opent automatisch in het hoofdscherm zodra de toggle is geactiveerd.

---

### 🍅 Expander: Ketch-Up (vernieuwd)

De vernieuwde Ketch-Up toont aankomende Magic: The Gathering-sets en kaartpreviews.  

**Weergave:**
- Links een afbeelding van het releasejaar.  
- Rechts een releasekalender met toekomstige sets, automatisch gesorteerd van eerstkomende naar laatstkomende datum.  
- Daaronder kaartpreviews van komende sets, opgehaald via Scryfall.  

De sortering is gekoppeld aan de Weergave-expander en kan worden aangepast op releasedatum, naam of mana value.  
Je kunt filteren op specifieke sets via multiselectie.  
Alle gegevens worden automatisch gecachet en dagelijks vernieuwd.

---

### 🐻 Expander: Bear Search

Toont alle kaarten met beren in de art.  
De resultaten worden gesorteerd volgens de huidige weergaveoptie en weergegeven in een responsieve grid.  
Ook deze functie gebruikt caching voor snellere laadtijden.

---

## ⚙️ Technische informatie

### API en Dataverwerking

- **Archidekt API** – haalt deckinformatie en kaartlijsten op.  
- **Scryfall API** – verzorgt kaartdata, zoekopdrachten, analyses en previews.  
- **Supabase** – slaat gebruikersspecifie
