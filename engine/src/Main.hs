{-# LANGUAGE OverloadedStrings #-}

import Data.Time.Clock
import Network.MQTT.Client
import Network.URI (URI, parseURI)
import Network.MQTT.Types (ByteMe(toByteString))
import Data.String
import Data.Time

-- mqtt haskell doc: https://hackage-content.haskell.org/package/net-mqtt-0.8.6.3/docs/Network-MQTT-Client.html#g:1

-- Define a custom data type for the response
data TimeResponse = TimeResponse
  { currentTime :: UTCTime
  }
  deriving (Show)

-- Main function to run the server
main :: IO ()
main = do
  let username = "ninja"
  let password = "welkom!" -- TODO: store this in a file outside the git???
  let serverAddress = "drone-game.coderdojo-nijmegen.nl"
  let port = "443"
  case parseURI $ "wss://" ++ username ++ ":" ++ password ++ "@" ++ serverAddress ++ ":" ++ port ++ "/mqtt" of
    (Just uri) -> makeConnection uri
    Nothing -> print ("Error occured, URI was not valid. did you change the username, password, serveradress or port?" :: String)

-- makeConnection is the main way to connect to the mqtt server. (mainly exist to limit nesting in main, could be inlined)
makeConnection :: Network.URI.URI -> IO ()
makeConnection uri = do
  mc <- connectURI mqttConfig uri
  timeString <- getLocalTimeString
  let message = fromString ("successful test at: " ++ timeString)
  publish mc "tmp/topic" message False
  print ("Done!" :: String)


getLocalTimeString :: IO String
getLocalTimeString = do
  utcTime <- getCurrentTime
  timeZone <- getCurrentTimeZone
  let localTime = utcToLocalTime timeZone utcTime
  return $ formatTime defaultTimeLocale "%H:%M:%S on %-d/%-m/%Y" localTime
