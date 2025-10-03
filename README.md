# \# CommanderDeckDoctor – Feature Map



CommanderDeckDoctor is gemaakt voor \*\*Commander-spelers van Magic: The Gathering\*\* die hun decks snel willen upgraden met kaarten uit nieuwe sets.  

In plaats van zelf handmatig alle kaarten door te lopen, laat de app je meteen zien welke \*\*legal kaarten\*\* relevant zijn voor jouw decks.  

Met filters verfijn je eenvoudig de resultaten op categorie of kaarttype, zodat je een overzicht krijgt zonder ruis.  



Met je gebruikersnaam onthoudt de app jouw decks voor toekomstige sessies.  

Je kunt daarnaast een persoonlijke \*\*Deck-Box\*\* vullen met kaarten die je later wilt toevoegen of bestellen.  

Alle kaartweergaves komen rechtstreeks van \*\*Scryfall\*\*, en via \*\*drag \& drop\*\* sleep je ze direct naar Archidekt of Moxfield.  



---

## 

## \## 🚀 Getting Started



1\. \*\*Voer je gebruikersnaam in bij Decks\*\*  

&nbsp;  Zo onthoudt de app automatisch jouw decks en instellingen voor toekomstige sessies.  



2\. \*\*Importeer een deck vanuit Archidekt\*\*  

&nbsp;  Kopieer de deck-ID uit de Archidekt-URL en plak deze in de app. Het deck wordt geladen en de kaarten verschijnen in een overzichtelijke grid.  



3\. \*\*Bekijk je deck\*\*  

&nbsp;  Gebruik de toggle \*Show my Deck\* om de kaartenlijst weer te geven. Commander(s) en mogelijke backgrounds worden automatisch herkend.  



4\. \*\*Zoek naar kaarten uit nieuwe sets bij Search \& FInd\*\*  

&nbsp;  Kies een setcode (bijv. MH2, WOE) en verfijn je selectie met filters zoals kaarttype, categorie of keywords.  



5\. \*\*Vul je Deck-Box\*\*  

&nbsp;  Voeg interessante kaarten toe aan je Deck-Box. Deze blijft bewaard voor volgende sessies en kan gedownload of gekopieerd worden.  



6\. \*\*Gebruik extra tools\*\*  

&nbsp;  Probeer de \*\*Good Stuff\*\*-opties zoals Set Search, Bear Search en Sound of Magic voor extra gemak en fun.  



---



### \## 1. Deck Management

\*\*Deck laden \& beheer\*\*

\- Gebruikersnaam invoeren om persoonlijke decks op te slaan en te beheren  

\- Archidekt deck import via ID (deck-URL getallenreeks)  

\- Tonen van decknaam en volledige lijst kaarten  

\- Verwijderen van decks  

\- Fallback afbeelding bij ontbrekende Scryfall-data  



\*\*Commander detectie\*\*

\- Automatisch identificeren van commander(s) in het deck  

\- Tonen van commander-afbeeldingen (Scryfall)  

\- Bepalen van color identity en commander types  



\*\*Deck weergave opties\*\*

\- Toggle: \*Show my Deck\* – toont alle kaarten in het deck  

\- Responsive gridweergave met hover-effecten en kaartnamen  

\- Alternative commanders weergeven  

\- Backgrounds / “Choose a Background” kaarten tonen  



---



### \## 2. Alternative Commanders \& Backgrounds

\- Alternatieve commanders zoeken op \*\*exacte color identity\*\*  

\- Sorteeropties:  

&nbsp; - Naam A-Z / Z-A  

&nbsp; - Mana Value Laag-Hoog / Hoog-Laag  

&nbsp; - Releasedatum Oud-Nieuw / Nieuw-Oud  

\- Backgrounds laden op basis van deck color identity  

\- Optie om alleen Backgrounds weer te geven  



---



### \## 3. Analyse Module

\*\*Filters\*\*

\- Setcode filter (bijv. MH2, SPM)  

\- Kaarttype filter: Creature, Instant, Sorcery, Enchantment, Artifact, Land, Legendary  

\- Rarity filter: Common, Uncommon, Rare, Mythic  

\- Inclusief alle legal kaarten bij geen selectie  



\*\*Analyse types\*\*

\- Ramp (mana acceleratie)  

\- Card Advantage (kaarttrek, tutors, recursion)  

\- Protection (hexproof, indestructible, shroud)  

\- Interruption (counter, destroy, exile, bounce)  

\- Mass Interruption (destroy all, exile all, each opponent)  

\- Keywords (selecteerbaar of zelf in te vullen)  

\- Kindred (automatisch uit commander types of zelf in te vullen)  



\*\*Analyse uitvoeren\*\*

\- Spinner bij analyse (\*Mana Spinner\*)  

\- Deduplicatie van resultaten  

\- Resultaten in kaart-grid  

\- Feedback: aantal gevonden kaarten  



---



### \## 4. Deck-Box

\- Toevoegen van kaarten aan een persoonlijke Deck-Box  

\- Deck-Box blijft bewaard per gebruiker (persistent)  

\- Inzien van Deck-Box in het hoofdscherm  

\- Downloaden als CSV  

\- Kaartenlijst kopiëren naar klembord  

\- Kaarten verwijderen uit de Deck-Box  



---



### \## 5. Card Rendering \& UI

\- Responsive card grid (kaarten per rij instelbaar via slider)  

\- Hover scale effect bij kaarten  

\- Kaartafbeelding + naam met tooltip  

\- Add-to-Deck (✚) en Remove (✖) knoppen  

\- Fallback afbeelding bij ontbrekende Scryfall-data  



\*\*Styling \& Interface\*\*

\- Achtergrond gradient (donkerblauw/groen)  

\- Buttons met hover-effect en glow  

\- Sidebar met interactieve expanders  

\- Footer: copyright + jaar  



---



### \## 6. Good Stuff (Extra Tools)

Togglebare tools in de sidebar:  

\- 🛡️ \*\*Set Search\*\* – doorzoek en blader Magic setcodes  

\- 🍅 \*\*Ketch-Up\*\* – overzicht gemiste items  

\- 🐻 \*\*Bear Search\*\* – laadt kaarten met beren in de art  

\- ⭐ \*\*Sheriff\*\* – toont regel-/play-afbeelding  

\- 🎵 \*\*Sound of Magic\*\* – speel Commander-playlist via Spotify  



---



### \## 7. API \& Caching

\- \*\*Archidekt API\*\* – deck info en kaartlijsten ophalen  

\- \*\*Scryfall API\*\* – kaartinformatie, zoekopdrachten en analyses  

\- \*\*Caching\*\* – lokaal diskcache om herhaalde API-calls te verminderen  

\- Safe API calls met fallback bij mislukte requests  



---



### \## 8. Session State Management

Per gebruiker worden bewaard:  

\- Geselecteerd deck  

\- Deck geladen status  

\- Toggle states (show deck, filters, extra tools)  

\- Commander(s) en commander data  

\- Deck card names  

\- Color identity van commanders  

\- Commander types voor Kindred-analyse  

\- Deck-Box inhoud  



---



