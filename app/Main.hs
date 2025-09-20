{-# LANGUAGE OverloadedStrings #-}

import Web.Scotty
import Data.Time.Clock
import Data.Aeson (Value(..), object, (.=))
import qualified Data.Text.Lazy as T

-- Define a custom data type for the response
data TimeResponse = TimeResponse
  { currentTime :: UTCTime
  } deriving (Show)

-- Main function to run the server
main :: IO ()
main = scotty 5000 $ do

    -- Endpoint 1: /hello
    -- Responds with a simple "Hello, World!" message
    get "/hello" $ do
        text "Hello, World!"

    -- Endpoint 2: /time
    -- Responds with the current time in JSON format
    get "/time" $ do
        now <- liftIO getCurrentTime
        json $ object [ "currentTime" .= show now ]
