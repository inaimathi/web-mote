import os, json, re
import conf

def isExt(filename, extList):
    name, ext = os.path.splitext(filename)
    if ext[1:] in extList:
        return True
    return False

def isAudio(filename):
    return isExt(filename, conf.ext['audio'])

def isVideo(filename):
    return isExt(filename, conf.ext['video'])

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
    dirs, videos, music = [[],[],[]]
    for f in entries:
        res = entryToJSON(f)
        if os.path.isdir(res['path']):
            dirs.append(res)
        elif res['type'] in conf.ext['video']:
            videos.append(res)
        elif res['type'] in conf.ext['audio']:
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
