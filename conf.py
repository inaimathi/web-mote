from subprocess import call

## list of directories which contain things we might want to play
root = ["/home/inaimathi/videos",
        "/home/inaimathi/music"]

######################################################################
############################## back-end conf settings ################
############################## (edit if you know what you're doing) ##

## [command-name: command] mappings for each player we plan to use
commands = {
    'mplayer':
        {'rewind-big': "\x1B[B", 'rewind': "\x1B[D", 'ff': "\x1B[C", 'ff-big': "\x1B[A",
         ## down | left | right | up
         'volume-down': "9", 'mute': "m", 'volume-up': "0",
         'stop': "q", 'pause': " ", 'play': " "},
    'omxplayer':
        {'rewind-big': "\x1B[B", 'rewind': "\x1B[D", 'ff': "\x1B[C", 'ff-big': "\x1B[A",
         'mute': " ", #oxmplayer doesn't have a mute, so we pause instead
         'volume-down': "+", 'volume-up': "-", 
         'stop': "q", 'pause': " ", 'play': " "}
    }

## determining which player should be used for what file-type
player = {
    'audio': ["mplayer"],
    'video': ["omxplayer"]
    }

## if specified video player is absent, use fullscreened mplayer instead
try:
    call(player['video'])
except:
    player['video'] = ["mplayer", "-fs"]

######################################################################
######################################################################
######################################################################
