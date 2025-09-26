# CommanderDeckDoctor – Feature Map

### 

### 1\. Deck Management



#### Deck laden

Archidekt deck import via ID

Tonen van decknaam en volledige lijst kaarten

Fallback afbeelding bij ontbrekende Scryfall-data



#### Commander detectie

Automatisch identificeren van commander(s) in het deck

Tonen van commander-afbeeldingen (Scryfall)



#### Deck weergave opties

Toggle: “Show my Deck”

Responsive gridweergave met hover-effecten en kaartnamen

Alternative commanders weergeven

Backgrounds / “Choose a Background” kaarten weergeven



### 2\. Alternative Commanders \& Backgrounds

Alt commanders zoeken op exact color identity

Sorteeropties:

 	Naam A-Z / Z-A

 	Mana Value Laag-Hoog / Hoog-Laag

 	Releasedatum Oud-Nieuw / Nieuw-Oud

Backgrounds laden op basis van deck color identity

Optie om alleen backgrounds weer te geven



### 3\. Analyse Module



#### Filters

Setcode filter

Kaarttype filter: Alles, Creature, Instant, Sorcery, Enchantment, Artifact, Land

Inclusief bestaande kaarten toggle



#### Analyse types

Ramp (mana acceleratie)

Card Advantage (kaarttrek)

Protection (hexproof, indestructible, shroud)

Interruption (counter target, destroy target, exile target)

Mass Interruption (destroy all, each opponent)

Lands

Keywords (selecteerbaar uit lijst)

Kindred (selecteerbare creature types)



#### Analyse uitvoeren

Spinner bij analyse (mana spinner)

Deduplicatie van resultaten

Resultaten renderen in kaart-grid

Feedback: aantal gevonden kaarten



### 4\. Card Rendering \& UI

Responsive card grid

Hover scale effect

Kaartafbeelding + naam met tooltip

Fallback afbeelding bij ontbrekende Scryfall-afbeelding

Styling:

 	Background gradient

 	Buttons met hover-effect

 	Sidebar compact \& interactive expanders

Footer:

 	Jaar + copyright

 	Easter egg: “Waar is de Beer?” (🐻)



### 5\. API \& Caching

Archidekt API

 	Deck info ophalen

 	Kaartlijst ophalen

Scryfall API

 	Kaartinformatie per naam ophalen

 	Zoekopdrachten: commander, backgrounds, alt commanders, analyses

Caching

 	Diskcache lokaal om herhaalde API-calls te verminderen

Safe API calls

 	Fallback bij mislukte requests



### 6\. Easter Eggs \& Extra Fun

“Waar is de Beer?” footer link

Laadt 100 bear-art kaarten van Scryfall

Stopt verdere uitvoering bij bear-search



### 7\. Session State Management

Bewaart:

 	Geselecteerd deck

 	Deck geladen status

 	Toggle states (show deck, alt commanders)

 	Loaded commander(s)

 	Deck card names

 	Color identity van commanders

 	Commander types voor Kindred-analyse

