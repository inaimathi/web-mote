import os, json, re
from subprocess import check_output
import conf

## extensions for filetypes we plan to handle
extensions = {
    'audio': ['mp3', 'ogg', 'wav'],
    'video': ['mp4', 'ogv', 'mov', 'wmf']
    }

def fileInfo(filename):
    """Parses the output of mplayer to find file properties of the given media file."""
    lines = check_output(["mplayer", "-vo", "null", "-ao", "null", "-frames", "0", "-identify", filename, "2>/dev/null"]).split("\n")
    res, temp = ({}, "")
    for l in lines:
        s = l[3:].split("=")
        if len(s) == 2:
            [k, v] = s
            if l.startswith("ID_CLIP_INFO_NAME"):
                temp = k.lower()
            elif l.startswith("ID_CLIP_INFO_VALUE"):
                res[temp] = v
            elif l.startswith("ID_"):
                res[k.lower()] = v
    return dict(res)

def isExt(filename, extList):
    """Takes a filename and a list of extensions. 
Returns true if the filenames' extension is a member of the list."""
    name, ext = os.path.splitext(filename)
    if ext[1:] in extList:
        return True
    return False

def isAudio(filename):
    global extensions
    return isExt(filename, extensions['audio'])

def isVideo(filename):
    global extensions
    return isExt(filename, extensions['video'])

def isIn(entry, directory):
    [e, d] = map(os.path.realpath, [entry, directory])
    return os.path.commonprefix([e, d]) == d

def isInRoot(entry):
    for path in conf.root:
        if isIn(entry, path):
            return True
    return False

def typeOfFile(path):
    if isAudio(path):
        return 'audio'
    elif isVideo(path):
        return 'video'
    else:
        raise LookupError("can't decide filetype of '%s'" % [path])

def nameToTitle(filename):
    return re.sub(" [ ]+", " - ", re.sub("-", " ", os.path.basename(filename).title()))

def entryToJSON(entry):
    name, ext = os.path.splitext(entry)
    if ext == '':
        ext = "directory"
    else:
        ext = ext[1:]
    return {'path': entry, 'type': ext, 'name': nameToTitle(name), 'buttons': True}

def entriesToDicts(entries):
    global extensions
    dirs, videos, music = [[],[],[]]
    for f in entries:
        res = entryToJSON(f)
        if os.path.isdir(res['path']):
            dirs.append(res)
        elif res['type'] in extensions['video']:
            videos.append(res)
        elif res['type'] in extensions['audio']:
            music.append(res)
    return dirs + videos + music

def entriesToJSON(entries):
    return json.dumps(entriesToDicts(entries))

def dirToJSON(directory):
    entries = entriesToDicts(
        map(lambda p: os.path.join(directory, p), 
            sorted(os.listdir(directory))))
    if directory in conf.root:
        entries.insert(0, {'path': "root", 'name': "..", 'type': "directory"})
    else:
        entries.insert(0, {'path': os.path.dirname(directory), 'name': "..", 'type': "directory"})
    return json.dumps(entries)
