# Software requirements voor de Drone Multi-player Game

## Systeem

- we gebruiken een centrale server met een domeinnaam: drone-game.coderdojo-nijmegen.nl
    - doordat we een centrale server gebruiken, hoeven we geen discovery mechanismen te implementeren (één van de functionaliteiten van Network Zero)
- we gebruiken MQTT voor de communicatie
    - want beschikbaar in de browser (Javascript) en in Python
    - want bi-directioneel, waardoor de client event-driven kan zijn en geen polling mechanisme hoeft te implementeren
    - overweging MQTT:
        - handig subscriben op topics (bijvoorbeeld game state)
        - kan eenvoudig event-driven worden gebruikt voor ontvangen van informatie
        - extra container, naast gameserver container
        - adresseren clients via topicnaam of message body?

### Architectuur

```mermaid
architecture-beta
    group game(cloud)[Multiplayer Drone Game]
    group laptop(server)[Laptop]

    service browser(internet)[browser client] in laptop
    service client(server)[Python client] in laptop

    service broker(server)[MQTT broker] in game
    service server(server)[web server] in game
    service engine(server)[Game Engine] in game

    engine:R -- L:broker
    server:T -- L:broker

    browser:T -- L:broker
    client:T -- L:broker

```

De Ninja speelt het spel op haar/zijn laptop. Dat kan met een Python script in Thonny, maar ook in Visual Studio Code met Javascript wat in de browser wordt uitgevoegd.

- Python client: 
- Browser client: 
- MQTT broker: berichten schakelpunt waar verschillende blokken in het systeem 
- Game engine: ontvangt berichten van de clients via het schakelpunt en verwerkt de informatie in de game state
- web server: serveert een dashboard dat een overzicht toont van de bibliotheken, boekentorens en vliegende drones, biedt ook een paar endpoints om een nieuwe client aan te melden bij de game engine

## Clients

### Javascript

#### Dashboard
```mermaid
sequenceDiagram
    Actor ninja
    participant dashboard as dashboard<br>in browser
    participant javascript_client
    participant webserver
    participant mqtt_broker
    participant engine

    ninja ->> dashboard: open dashboard in browser<br/>drone-game.coderdojo-nijmegen.nl
    dashboard ->> webserver: laadt client van server
    webserver -->> dashboard: javascript module
    dashboard ->> javascript_client: start client
    javascript_client ->> webserver: registreer client
    webserver ->> webserver: maak uniek ID<br/>(base64 gecodeerd IP adres van de client)
    webserver -) mqtt_broker: kondig client aan met uniek ID<br/>op topic "drone-game/client/register"
    mqtt_broker -) engine: onRegister: "drone-game/client/register"<br/>voeg client toe aan game state
    webserver -->> javascript_client: uniek ID

    javascript_client ->> mqtt_broker: abonneer op "drone-game/dashboard"
    engine -) mqtt_broker: publish: dashboard data<br>to "drone-game/dashboard"
    mqtt_broker -) javascript_client: onDashboardUpdate: "drone-game/dashboard"<br>teken dashboard
    javascript_client -) dashboard: update dashboard
   

```

#### Drone besturen
```mermaid
sequenceDiagram
    Actor ninja
    participant dashboard as dashboard<br>in browser
    participant javascript_client
    participant webserver
    participant mqtt_broker
    participant engine

    ninja ->> dashboard: open dashboard in browser<br/>drone-game.coderdojo-nijmegen.nl
    dashboard ->> webserver: laadt client van server
    webserver -->> dashboard: javascript module
    dashboard ->> javascript_client: start client
    javascript_client ->> webserver: registreer client
    webserver ->> webserver: maak uniek ID<br/>(base64 gecodeerd IP adres van de client)
    webserver -) mqtt_broker: kondig client aan met uniek ID<br/>op topic "drone-game/client/register"
    mqtt_broker -) engine: onRegister: "drone-game/client/register"<br/>voeg client toe aan game state
    webserver -->> javascript_client: uniek ID

    javascript_client ->> mqtt_broker: abonneer op "drone-game/client/<uniek ID>"

    loop voor elke game cycle
        mqtt_broker -) javascript_client: onGameStateChange: "drone-game/client/<uniek ID>"<br>verwerk game state wijziging
        javascript_client ->> javascript_client: bereken volgende stap
        javascript_client -) mqtt_broker: "drone-game/client/<uniek ID>/next_state"<br>publiceer volgende stap
        mqtt_broker -) engine: onClientNextState: "drone-game/client/<uniek ID>/next_state"<br>voeg client next state toe aan game state
        engine ->> engine: onGameStateTrigger:<br>bereken nieuwe game state op<br>basis van input alle clients
        engine -) mqtt_broker: publish: "drone-game/dashboard"<br>publiceer overall game state
        loop voor elke client
            engine -) mqtt_broker: publish: "drone-game/client/<uniek ID>"<br>publiceer game state voor client
        end
    end
```
