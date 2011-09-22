#
# extract track index from library
#
import re

class TrackID2Index:
    def __init__(self, xmlLibrary):
        reTrackID = re.compile('<key>Track ID</key><integer>(\d+)</integer>')
        inMusic = False
        inPlaylists = False
        tindex = 0
        self.dict = {}
        fd = open(xmlLibrary)
        if not fd:
            print "could not open iTunes Music Library.xml"
            raise SystemExit
        s = fd.read()
        lines = s.split("\n")
        for line in lines:
            if re.search('<key>Playlists</key>', line):
                inPlaylists = True
                continue
            if re.search('<key>Name</key><string>Music</string>', line):
                inMusic = True
                continue
            if inMusic:
                m = reTrackID.search(line)
                if m:
                    tindex += 1
                    self.dict[int(m.group(1))] = tindex
                elif re.search('</array>', line):
                    break
        fd.close()

    def foo(self):
        return 1

    def ID2Index(self, id):
        return self.dict.get(id, 0)
