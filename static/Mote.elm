module Mote where

import JavaScript.Experimental (toRecord)
import Json (fromString, toJSObject)
import Graphics.Input (button, buttons, customButtons)
import Window (middle)
import Http (sendGet, send, post)
import Maybe (maybe)

----- Signal Declarations
uriDir str = "/show-directory?dir=" ++ str
reqPlay str = post ("/play?target=" ++ (maybe "" id str)) ""
reqCmd str = post ("/command?command=" ++ (maybe "" id str)) ""

command = buttons Nothing
playing = buttons Nothing
files = buttons "root"

dir = sendGet $ lift uriDir files.events
cmd = send $ lift reqCmd command.events
ply = send $ lift reqPlay playing.events

----- Utility
fromJust maybe = case maybe of
  Just val -> val
  _ -> error "No value"

jstrToRec jStr = case fromString jStr of
  Just val -> Just . toRecord $ toJSObject val
  _ -> Nothing

----- Application
box n = container 350 n midTop

cmdButton name = height 42 $ width 80 $ command.button (Just name) name

controls = flow down [ box 48 $ flow right $ map cmdButton ["backward", "stop", "pause", "forward"]
                     , box 50 $ flow right $ map cmdButton ["volume-down", "volume-off", "volume-up"]]
           
entry { name, path, entryType } = let btn = if | entryType == "return" -> files.button path
                                               | entryType == "directory" -> files.button path
                                               | otherwise -> playing.button (Just path)
                                           in width 350 $ btn name

showEntries res = case res of
  Success str -> flow down . map entry . fromJust $ jstrToRec str
  _ -> plainText "Waiting..."

main = flow down [ box 100 $ controls
                 , showEntries $ id <~ dir ]