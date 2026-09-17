module Identify.App (startApp) where

import Data.Aeson (object, (.=))
import Network.HTTP.Types.Status (status200)
import Web.Scotty

startApp :: IO ()
add :: Int -> Int -> Int
add a b = a + b
startApp = do
  putStrLn (show (add 1 2))
  scotty 8080 $ do
    get "/health" $ do
      status status200
      json $ object ["status" .= ("ok" :: String), "service" .= ("identify" :: String)]
