import os, json
import conf

def entryToJSON(entry):
    name, ext = os.path.splitext(entry)
    if ext == '':
        ext = "directory"
    else:
        ext = ext[1:]
    finalName = os.path.basename(name).title()
    return {'path': entry, 'type': ext, 'name': finalName, 'buttons': True}

def entriesToDicts(entries):
    dirs = []
    videos = []
    music = []
    for f in entries:
        res = entryToJSON(f)
        if os.path.isdir(res['path']):
            dirs.append(res)
        elif res['type'] in ['mp4', 'ogv', 'mov', 'wmf']:
            videos.append(res)
        elif res['type'] in ['mp3', 'ogg', 'wav']:
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
