{-# LANGUAGE ExistentialQuantification #-}
{-# LANGUAGE OverloadedStrings #-}

import Data.ByteString.Lazy (ByteString)
import qualified Data.ByteString.Lazy as BSL
import Data.IORef
import Data.Map (Map)
import qualified Data.Map as Map
import Data.String
import qualified Data.Text as T
import Data.Time
import Data.Time.Clock
import qualified DroneGame
import Network.MQTT.Client
import Network.MQTT.Topic
import Network.MQTT.Types (ByteMe (toByteString))
import Network.URI (URI, parseURI)

hardcodedRunningSessionID :: SessionId
hardcodedRunningSessionID = "droneGame"

-- mqtt haskell doc: https://hackage-content.haskell.org/package/net-mqtt-0.8.6.3/docs/Network-MQTT-Client.html#g:1

-- Main function to run the server
main :: IO ()
main = do
  let username = "ninja"
  let password = "welkom!" -- TODO: store this in a file outside the git???
  let serverAddress = "drone-game.coderdojo-nijmegen.nl"
  let port = "443"
  case parseURI $ "wss://" ++ username ++ ":" ++ password ++ "@" ++ serverAddress ++ ":" ++ port ++ "/mqtt" of
    (Just uri) -> makeConnection uri
    Nothing -> print ("Error occurred, URI was not valid. did you change the username, password, serveradress or port?" :: String)

-- makeConnection is the main way to connect to the mqtt server. (mainly exist to limit nesting in main, could be inlined)
makeConnection :: Network.URI.URI -> IO ()
makeConnection uri = do
  clientsRef <- newIORef Map.empty
  runningSession <- case (Map.lookup "droneGame" sessions) of
    Just session -> makeRunningSession session
    Nothing -> error "\"droneGame\" does not exist in the sessions list but is loaded by default. we can not load something that does not exist this this is a critical startup error."
  runningSessionsRef <- newIORef $ Map.singleton hardcodedRunningSessionID runningSession

  let msgReceived :: (MQTTClient -> Topic -> ByteString -> [Property] -> IO ())
      msgReceived mqttClient topic message properties = case topic of
        "tmp/topic1" -> do
          print (topic, message, properties)
          timeString <- getLocalTimeString
          let timeMessage = fromString ("successful test at: " ++ timeString)
          publish mqttClient "tmp/topic2" timeMessage False
        "tmp/topic2" -> do
          print (topic, message, properties)
          timeString <- getLocalTimeString
          let timeMessage = fromString ("successful test at: " ++ timeString)
          publish mqttClient "tmp/topic1" timeMessage False
        str
          | "clients/drone-game/" `T.isPrefixOf` unTopic str ->
              print ("client joined with ", topic, message)
        _ -> case splitTopic topic of
          Just (clientId, command) -> do
            clientList <- readIORef clientsRef
            runningSessions <- readIORef runningSessionsRef
            case ( do
                     sessionId <- getSessionID clientList clientId
                     getSession runningSessions sessionId
                 ) of
              Just (RunningSession modelReference update view) -> do
                atomicModifyIORef modelReference (\model -> (update (command, message) model, ()))
                model <- readIORef modelReference
                view mqttClient model
              Nothing -> print ("ERROR! client not in any server! log in first, the message:", topic, message, properties)
          Nothing -> print ("ERROR! Cound not recognise the following command!", topic, message, properties)

  mqttClient <- connectURI mqttConfig {_msgCB = SimpleCallback msgReceived} uri
  timeString <- getLocalTimeString
  let timeMessage = fromString ("successful test at: " ++ timeString)
  publish mqttClient "tmp/topic" timeMessage False
  print =<< subscribe mqttClient [("tmp/topic1", subOptions), ("tmp/topic2", subOptions), ("clients/drone-game/#", subOptions), ("drone-game/client/#", subOptions)] []
  waitForClient mqttClient -- wait for the the client to disconnect

getLocalTimeString :: IO String
getLocalTimeString = do
  utcTime <- getCurrentTime
  timeZone <- getCurrentTimeZone
  let localTime = utcToLocalTime timeZone utcTime
  return $ formatTime defaultTimeLocale "%H:%M:%S on %-d/%-m/%Y" localTime

type ClientId = String

type SessionTypeId = String

type SessionId = String

type Command = (String, ByteString)

data Session = forall model. Session
  { initModel :: model,
    updateModel :: Command -> model -> model,
    viewMQTT :: MQTTClient -> model -> IO ()
  }

-- | splitTopic get's a topic like "drone-game/client/<IP>/<something>" and splits it into (<IP>,<something> )
splitTopic :: Topic -> Maybe (ClientId, String)
splitTopic topic =
  case T.splitOn "/" (unTopic topic) of
    "drone-game" : "client" : ip : rest -> Just (T.unpack ip, T.unpack $ T.intercalate (T.pack "/") rest)
    _ -> Nothing

-- | the list where we store all the different gameModes/levels These can be made into runningSessions. you can have multiple sessions of the same gameMode without defining it twice.
sessions :: Map SessionTypeId Session
sessions = Map.singleton "droneGame" (Session DroneGame.init DroneGame.update DroneGame.view)

data RunningSession = forall model. RunningSession
  { modelRef :: (IORef model),
    update :: (Command -> model -> model),
    view :: MQTTClient -> model -> IO ()
  }

makeRunningSession :: Session -> IO RunningSession
makeRunningSession (Session init update view) = do
  ref <- newIORef init
  pure (RunningSession ref update view)

getSessionID :: Map ClientId SessionId -> ClientId -> Maybe SessionId
getSessionID map clientId = Just ""

-- Map.lookup clientId map

getSession :: Map SessionId RunningSession -> SessionId -> Maybe RunningSession
getSession map sessionId = Map.lookup hardcodedRunningSessionID map -- Map.lookup sessionId map