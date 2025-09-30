# Multiplayer 2D single-screen game
Een coöperatief spel waarbij je niet zelf de speler bent, maar een drone leert het spel te spelen.

**Doel**

We zetten een server op die de communicatie tussen alle clients regelt. Die draait op een centrale computer. Daar draait ook het spel op en die kan het gezamenlijke speelveld op een grote televisie of beamer laten zien. De kinderen programmeren de client die verbinding maakt met de server. Wij maken instructies die ze kunnen volgen, maar ze hebben veel vrijheid om hun drone aan te passen, zowel qua uiterlijk als functionaliteit. Hoe slimmer zij hun drone maken, hoe beter hun drone het spel speelt en hoe meer succesvol hun team is.

**Gameplay**

Er zijn twee teams, rood en groen. Elk team heeft een bibliotheek waar drones boeken kunnen ophalen en een plek waar een toren gebouwd moet worden met de boeken.

Het spel is dat je een drone moet programmeren om mee te bouwen aan de toren van jouw team. Je speelt dus niet direct zelf, maar je leert een drone hoe hij het spel moet spelen.

Je drone moet in het spel een boek oppakken, naar de toren vliegen, het boek boven de toren loslaten en dan weer een nieuw boek ophalen.
Het team dat als eerste een toren heeft van 25 boeken hoog heeft gewonnen.

Het lastige is dat de toren van het andere team tussen de bibliotheek en de toren van jouw team in staat. De drones van beide teams moeten dus heen en weer vliegen tussen de bibliotheek en de toren maar daarbij goed in de gaten houden dat ze niet tegen een andere drone of een toren aan vliegen.

Als je met jouw computer inlogt op het spel (de server) dan verschijnt jouw drone. 
Je krijgt van de server informatie over waar jouw drone is, waar je boeken kunt ophalen, waar het hoogste boek van beide torens is en waar de andere drones zijn.

Jouw code moet aan de server laten weten waar je jouw drone heen wil laten vliegen (omhoog, omlaag, links en rechts, stil hangen) en wanneer hij een boek moet loslaten.

Je pakt een nieuw boek op door de drone direct boven de plank/bak met boeken van jouw team te laten hangen.
Om het boek los te kunnen laten moeten de drone eerst stil hangen.
Je kunt een boek loslaten op elke hoogte, maar als de drone te dicht boven de toren hangt of de toren raakt (of te ver naar links of rechts) dan valt het boek niet op de stapel maar helemaal naar beneden. Het helpt natuurlijk ook als er geen andere drones onder je vliegen op het moment dat je je boek loslaat.

Als je drone ergens tegenaan vliegt, dan stort hij neer.

Als je drone tegen de toren van je eigen team aanvliegt, dan valt het boek dat je geraakt hebt naar beneden. Jullie toren is dan dus één boek kleiner.

Als je drone de bodem raakt, dan verschijnt hij na een paar seconden opnieuw aan de zijkant van het scherm. 


**Wat er zo cool aan is en wat het een goede opdracht maakt**

- Het lijkt me ontzettend leuk dat de kinderen samenwerken in plaats van dat ze allemaal voor zichzelf bezig zijn. Met hun inzet helpen ze hun team. 
- Hun input is meteen zichtbaar voor iedereen, ik denk dat ze dat heel leuk vinden.
- Een game maken is sowieso tof.
- Het programmeren heeft een concreet doel; hoe slimmer zij programmeren, des te slimmer is hun drone en des te sterker ze hun team maken.
- De kinderen moeten logisch nadenken, bijvoorbeeld over 'waar kan mijn drone het beste heen vliegen als een andere drone in de weg zit' en 'hoe voorkom ik opstoppingen'.


**To do's voor dit project**

- [ ] Server opzetten
	- [ ] Hoeft niet ontzettend veel connecties aan te kunnen (max 20 kinderen) maar misschien is het voor de snelheid van de game beter om de server in Java of C# te maken. Of is een [server in Python](https://www.techwithtim.net/tutorials/python-online-game-tutorial/connecting-multiple-clients) inmiddels snel genoeg?
	- [ ] Server publiceert steeds de posities van alle drones en andere elementen
	- [ ] Server slaat steeds de input van de clients op (posities en andere eigenschappen van de drones)
- [ ] Code schrijven voor communicatie tussen client en server (en de handleiding voor de client maken). [Network Zero](https://networkzero.readthedocs.io/en/latest/index.html) is specifiek gemaakt voor een educatieve setting, dus als we Pygame Zero gebruiken voor de client (zie hieronder) dan ligt Network Zero voor de hand.
- [ ] Multiplayer game maken op basis van input van clients. Zie gameplay hierboven.
	- [ ] Game full-screen laten zien (voor op een groot scherm/projector)
	- [ ] De look-and-feel kan [ontzettend basic](https://berbasoft.com/simplegametutorials/pygamezero/snake/) zijn, in ieder geval om mee te beginnen.
	- [ ] Het spel is single-screen en 2D.
	- [ ] De drones en boeken zijn simpele rechthoeken met een middelpunt dat we gebruiken om afstanden tussen spel-objecten te bepalen.
	- [ ] Spelers worden op basis van verschijnen ingedeeld bij een team. Eenmaal ingedeeld blijven ze in dat team, ook na crashes, opnieuw inloggen of nieuwe rondes. 
	- [ ] Elke drone krijgt in beeld de kleur van het eigen team.
	- [ ] Bij elke drone de naam in beeld laten zien.
	- [ ] Als spelers disconnecten verdwijnt hun drone.
	- [ ] Als een nieuwe speler inlogt en het aantal drones is niet gelijk voor beide teams, laat de server dan even later een drone toevoegen voor het andere team (om het eerlijk te houden). Die drone vliegt weg als een nieuwe drone zich meldt voor dat team óf als het eerste team een speler kwijtraakt.
	- [ ] Geef alle drones dezelfde snelheid; spelers kunnen de drones alleen een richting geven of laten stilstaan.
	- [ ] Als een drone verder daalt dan de grond dan is dat een crash.
 	- [ ] De engine publiceert cliënt-specifieke info op een eigen topic voor iedere cliënt, zoals een soort foutmelding als de drone van die client ergens tegenaan is gebotst, zodat de programmeur weet wat er verbeterd moet worden. 
	- [ ] Het spel laat een feestelijk *win screen* zien als één team het doel bereikt heeft. (Eventueel met de ranglijst van de drones met de meest geplaatste boeken.)
	- [ ] Het spel begint opnieuw nadat we een tijdje het win screen gezien hebben. De overall score tussen beide teams wordt bijgehouden.
	- [ ] Als het spel opnieuw begint, wisselen de torens en bibliotheken van beide teams van plek.
	- [ ] Boeken laten ophalen bij meerdere planken/bakken, om opstoppingen te voorkomen?
	- [ ] Drones die te lang stilhangen verdwijnen (om opstoppingen te voorkomen).
	- [ ] Als een drone lang niet beweegt óf heel ver uit beeld vliegt, telt niet meer als teamlid (Hierdoor heeft een team geen last van spelers die bezig zijn met het verbeteren van hun software of 'away from keyboard' zijn.)
- [ ] Client-software maken. 
	- [ ] Ik heb zelf al eens een begin gemaakt met dit project in Pygame, maar ik heb inmiddels gezien dat er [Pygame Zero](https://pygame-zero.readthedocs.io/en/latest/index.html) is dat specifiek bedoeld is voor een educatieve setting. Zie ook [deze handleiding](https://electronstudio.github.io/pygame-zero-book/) en [deze](https://aposteriori.trinket.io/game-development-with-pygame-zero#/intro-to-pygame-zero/intro-and-installation) en [deze voorbeelden](https://berbasoft.com/simplegametutorials/pygamezero/).
	  (Alternatieven zijn [JavaScript/HTML](https://blog.logrocket.com/best-javascript-html5-game-engines/), [Javascript-Nodejs](https://neatpatel.github.io/multiplayer-game/) of [Godot](https://godotengine.org/).) Dit is trouwens alleen nodig als we ook willen dat de kinderen een lokale versie zien van hun game! De client hoeft (in ieder geval in het begin) alleen maar een script te zijn dat instructies geeft aan de drone op de server; we zouden het dus ook bij pure Python kunnen houden! Dat kunnen ze direct schrijven in Thonny of een andere editor en klaar, zonder dat er externe libraries geïnstalleerd hoeven te worden.
	- [ ] De client moet 'feedback' van de game engine kunnen laten zien die bedoeld is voor deze client. Zo kan de programmeur zien wat er mis is gegaan, bijvoorbeeld "Jouw drone is tegen drone 'SpaceInvader21' gebotst". Dan ziet de deelnemer wat er verbeterd moet worden. (Iedere cliënt heeft een eigen topic waarop hij moet subscriben. De engine publiceert daar de game state en cliënt-specifieke info op.) 
	- [ ] Ga uit van de gameplay hierboven en 'Wat kinderen zelf moeten programmeren' hieronder.
	- [ ] Maak de software zo overzichtelijk en eenvoudig mogelijk, zodat het goed te volgen is voor de kinderen.
	- [ ] Alle elementen in dit spel hebben één set coördinaten, voor hun middelpunt. Ze kunnen er anders uitzien op het gedeelde scherm, maar om het spel simpel te houden gaan we niet nadenken over ingewikkelde geometrieën en *hit tests*. 
	- [ ] Denk aan goede comments zodat we daar de instructies op kunnen baseren.
	- [ ] Ik denk aan letters voor het doorgeven van de gewenste richting. Aan het begin van de handleiding kunnen drones alleen stijgen en dalen (S en D), links en rechts (L en R) en stilhangen (H).
- [ ] Software uitproberen op Windows/Mac/Linux (eventueel verschillende installatie-instructies voor maken.)
- [ ] Instructies schrijven voor kinderen (deze klus neemt Jaap graag voor zijn rekening).
- [ ] Testen of de instructies makkelijk gedaan kunnen worden op Windows/Mac/Linux.
- [ ] Testen of de instructies ook gedaan kunnen worden op de oude Raspberry Pi's


**Wat kinderen zelf moeten programmeren**

- Verbinding maken met de server
- Naam opgeven voor hun drone ter identificatie in beeld
- Informatie van de server verwerken
- Bepalen waar we naar toe moeten vliegen (afhankelijk van 'hebben we al een boek te pakken of niet' en de coördinaten van onze bibliotheek en toren).
- Instructies voor de drone naar de server sturen
- Logica toevoegen voor het ophalen van boeken
- Logica toevoegen voor het stapelen van de boeken
- Steeds in de gaten houden of er obstakels zijn die ontweken moeten worden
- Vluchtplan slimmer maken door te anticiperen op de hoogte van de toren van de tegenpartij
- Logica toevoegen om vliegende/vallende obstakels te ontwijken


**Eventuele extra's voor het gedeelde scherm**

- Geluiden toevoegen voor de drones en andere elementen zoals boeken die neerploffen.
- Crash-geluid laten horen bij botsingen.
- Met een pijltje bij elke drone het doel laten aanwijzen (bibliotheek als de drone geen boek heeft, toren als hij wel een boek heeft).
- Bij elke drone ook laten zien hoeveel boeken hij al geplaatst heeft.
- Een commentator die live uitspreekt welke speler net een boek heeft neergelegd of net is neergestort en ook aankondigt welk team er bijna is.
- Laat met nummers zien hoeveel boeken hoog de toren is.
- Mooie graphics maken voor de drones, de achtergrond en de rest van de game-omgeving ([Pixelorama](https://orama-interactive.itch.io/pixelorama) gebruiken?)
- Ranglijst in beeld laten zien (à la Slither.io) met de drones en hoeveel boeken ze al hebben neergelegd in deze ronde.


**Eventuele extra's voor gameplay en handleiding**

- Het spel moeilijker maken met extra obstakels (zoals langzaam bewegende space-invaders-achtige aliens of stilstaande letters waar de drones omheen moeten vliegen). Spelers die minder dan X aantal boeken hebben daar nog geen last van (vliegen er gewoon doorheen), zodat ze extra moeten programmeren om dat stadium te overleven.
- Aan de server kunnen laten weten hoe jouw drone eruitziet (kleur/plaatje/sprites).
- Lokale representatie laten maken van het spel (alleen hun drone of het hele speelveld) met sprites, een achtergrond en geluiden zodat ze zien hoe ze zelf een spel kunnen maken.
- [Health](https://en.wikipedia.org/wiki/Health_(game_terminology)) toevoegen aan de drones. Als de accu bijna leeg is, dan moeten ze de drone laten opladen bij een oplaadpunt. Als de accu helemaal leeg is en de drone niet bij een oplaadpunt is, dan stort hij neer.
- Richting van de drone kunnen opgeven in graden.


**Instructie voor de kinderen**

- De verbale instructie aan het begin van de dojo beginnen door het speelveld te presenteren op TV/projector. Demonstreren dat een drone verschijnt als je verbinding maakt.
- Als voorbeeld Slither.io noemen/laten zien van een 2D multiplayer game.
- In de handleiding: spelers als eerste laten connecten met de server zodat ze meteen resultaat zien.

