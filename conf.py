from subprocess import call

## extensions for filetypes we plan to handle
ext = {
    'audio': ['mp3', 'ogg', 'wav'],
    'video': ['mp4', 'ogv', 'mov', 'wmf']
    }

## list of directories which contain things we might want to play
root = ["/home/inaimathi/videos",
        "/home/inaimathi/music"]

## [command-name: command] mappings for each player we plan to use
commands = {
    'mplayer':
        {'rewind-big': "\x1B[B", 'rewind': "\x1B[D", 'ff': "\x1B[C", 'ff-big': "\x1B[A",
         ## down | left | right | up
         'volume-down': "9", 'mute': "m", 'volume-up': "0",
         'stop': "q", 'pause': " ", 'play': " "},
    'omxplayer':
        {'rewind-big': "\x1B[B", 'rewind': "\x1B[D", 'ff': "\x1B[C", 'ff-big': "\x1B[A",
         'volume-down': "+", 'mute': " ", #oxmplayer doesn't have a mute, so we pause instead
         'volume-up': "-", 
         'stop': "q", 'pause': " ", 'play': " "}
    }

## determining which player should be used for what file-type
player = {
    'audio': ["mplayer"],
    'video': []
    }

## if omxplayer is absent, use mplayer instead
try:
    call(["omxplayer"])
    player['video'] = ["omxplayer"]
except:
    player['video'] = ["mplayer", "-fs"]

## don't touch this one; it's a hook to the active player
currentPlayer = False
