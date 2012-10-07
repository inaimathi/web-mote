ext = {
    'music': ['mp3', 'ogg', 'wav'],
    'video': ['mp4', 'ogv', 'mov', 'wmf']
    }

root = ["/home/inaimathi/videos",
        "/home/inaimathi/music"]

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
