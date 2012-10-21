import os, json, re
from subprocess import check_output
import conf

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

def isIn(entry, directory):
    [e, d] = map(os.path.realpath, [entry, directory])
    return os.path.commonprefix([e, d]) == d

def isInRoot(entry):
    for path in conf.root:
        if isIn(entry, path):
            return True
    return False

def nameToTitle(filename):
    return re.sub(" [ _-]+", " - ", re.sub("[-_]", " ", os.path.basename(filename).title()))

def entryToDict(entry):
    name, ext = os.path.splitext(entry)
    if ext == '':
        ext = "directory"
    else:
        ext = ext[1:]
    return {'path': entry, 'type': ext, 'name': nameToTitle(name), 'buttons': True}

def entriesToDicts(entries):
    dirs, files = [[],[]]
    for f in entries:
        res = entryToDict(f)
        if os.path.isdir(res['path']):
            dirs.append(res)
        else:
            files.append(res)
    return dirs + files

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

def deepListDir(directory):
    res = []
    for e in os.listdir(directory):
        path = os.path.join(directory, e)
        if os.path.isdir(path):
            res += deepListDir(path)
        else:
            res.append(path)
    return sorted(res)
