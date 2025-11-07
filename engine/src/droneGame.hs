{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE DuplicateRecordFields #-}
{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}

{-# HLINT ignore "Replace case with fromMaybe" #-}

module DroneGame where

import Data.Aeson (FromJSON, ToJSON, decode, encode)
import Data.Array
import Data.List (find)
import GHC.Generics
import Data.ByteString.Lazy (ByteString)
import Network.MQTT.Client

sizeX = 20

sizeY = 20

type Coord = (Int, Int)

type Id = String

data Tile
  = Empty
  | Book Bool
  | Drone Id Bool

data Connection = Connection Id ConnectionPlatform

data ConnectionPlatform = JavaScript | Python | Dashboard

data Model = Model
  { grid :: Array Coord Tile,
    connectedPlayers :: [Connection]
  }

init :: Model
init =
  Model
    { grid = array ((0, 0), (sizeX, sizeY)) [((x, y), Empty) | x <- [0 .. sizeX], y <- [0 .. sizeY]] // [((10, 10), Drone "temp" False)],
      connectedPlayers = []
    }

update :: (String,ByteString) -> Model -> Model
update _ model = model

view :: MQTTClient -> Model -> IO ()
view _ _ = pure ()
-------------------------------
-- \/ converting to json  \/ --

data JsonState = JsonState
  { drone :: JsonDrone,
    game :: [JsonDrone],
    books :: [JsonBook]
  }
  deriving (Generic, Show)

data JsonDrone = JsonDrone
  { droneId :: String,
    position :: JsonPosition,
    hasBook :: Bool
  }
  deriving (Generic, Show)

data JsonBook = JsonBook
  { position :: JsonPosition,
    reachedBottom :: Bool
  }
  deriving (Generic, Show)

data JsonPosition = JsonPosition
  { x :: Int,
    y :: Int
  }
  deriving (Generic, Show)

modelToJsonState :: Model -> Id -> JsonState
modelToJsonState model currentPlayerID =
  let (drones, foundBooks) = foldr go ([], []) (assocs $ grid model)
        where
          go item@(_, tile) (drones, books) =
            case tile of
              Empty -> (drones, books)
              Drone _ _ -> (item : drones, books)
              Book _ -> (drones, item : books)
      drone = droneToJsonDrone $ case find
        ( \(_, x) -> case x of
            Drone id _ -> id == currentPlayerID
            _ -> False
        )
        drones of
        Just x -> x
        Nothing -> ((-1, -1), Drone "ERROR! no drone found!" False)
      game = map droneToJsonDrone drones
      books = map bookToJsonBook foundBooks
   in JsonState drone game books

droneToJsonDrone :: (Coord, Tile) -> JsonDrone
droneToJsonDrone (coord, Drone id bool) = JsonDrone id (coordToPosJson coord) bool

coordToPosJson :: Coord -> JsonPosition
coordToPosJson (x, y) = JsonPosition x y

bookToJsonBook :: (Coord, Tile) -> JsonBook
bookToJsonBook (coord, Book bool) = JsonBook (coordToPosJson coord) bool

-- /\ converting to json  /\ --
-------------------------------
