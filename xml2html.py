#!/usr/bin/python
# -*- coding: latin-1 -*-
#
# parse Library.xml from iTunes to generate HTML
#
# To get robust playing of songs, we use the id in the "Music"
# playlist to identify songs. This avoids such problems as trying
# to quote UTF-8 strings passed to osascript. The id recognized by
# iTunes via osascript appears to correspond to the rank order of
# the song in the playlist as it appears in
# ~/Music/iTunes Music Library.xml.
#
import re
import os
import unicodedata
import trackid2index
from pyItunes import *

XMLFile = os.environ.get("HOME") + "/Music/iTunes/iTunes Music Library.xml"

gCollections = ("Classic Recordings - The Commitments",
                "Shrek",
                "An Introduction To The Mowtown Elite 9000 Series",
                "Sound Response",
                "Lambada",
                "Natural Born Killers",
                "Mediterranean Lullaby",
                "O Sisters! The Women's Bluegrass Collection",
                "O Brother, Where Art Thou?")

def removeaccents(s):
    nkfd_form = unicodedata.normalize("NFKD", unicode(s))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii

def sortstring(s0):
    s = removeaccents(s0).lower()
    m = re.match("^the\s+(\S.*)", s)
    if m: return m.group(1)
    m = re.match("^a\s+(\S.*)", s)
    if m: return m.group(1)
    m = re.match("^an\s+(\S.*)", s)
    if m: return m.group(1)
    return s

## a little test code
# ss = u"Zoltán Kocsis"
# print("sortstring(%s) => %s\n" % (ss.encode('UTF-8'), sortstring(ss)))

def PreCleanXMLString(s, ifnone):
    if not s: return ifnone
    return s.strip()

def BuildDict(xmlfile):
    plibrary = XMLLibraryParser(xmlfile)
    tidlookup = trackid2index.TrackID2Index(xmlfile)
    library = Library(plibrary.dictionary)
    byArtist = {}
    byAlbum = {}
    byGenre = {}
    bySong = {}
    # In AlbumByArtist, each album shows up exactly once, sorted by artist
    AlbumByArtist = {}
    for song in library.songs:
        sname = PreCleanXMLString(song.name, u"[no name]")
        artist = PreCleanXMLString(song.artist, u"[no artist]")
        album = PreCleanXMLString(song.album, u"[no album]")
        genre = PreCleanXMLString(song.genre, u"[no genre]")
        track_index = str(tidlookup.ID2Index(int(song.track_id)))
        bySong[sortstring(sname)] = (
            sname, artist + "-" + album + "-" + sname)
        byArtist[sortstring(artist)] = (artist, artist)
        ssalbum = sortstring(album)
        if not byAlbum.get(ssalbum):
            byAlbum[ssalbum] = (album, artist, track_index)
        else:
            (xalbum, xartist, xtrack_index) = byAlbum[ssalbum]
            if xtrack_index > track_index:
                byAlbum[ssalbum] = (album, artist, track_index)
        byGenre[genre] = (genre, genre)
    for key in byAlbum.keys():
        (album, artist, track_index) = byAlbum[key]
        if album in gCollections:
            artist = "Various Artists"
        newkey = sortstring(artist) + ":" + sortstring(album)
        AlbumByArtist[newkey] = (track_index, artist + ":" + album)
    return (byArtist, AlbumByArtist, byGenre, bySong)

def HTMLEpilog():
    return ("</BODY>\n"
            "</HTML>\n")

def GenHTMLFile(fname, urlprefix, adict):
    fd = open(fname, "w")
    if not fd:
        print("could not open ", fname)
        return
    fd.write(HTMLProlog())
    fd.write("<ul>\n")
    for key in sorted(adict.keys()):
        (alink, astr) = adict[key]
        alink = alink.replace("'", "&#39;")
        fd.write('<li>')
        fd.write('<a href=\'javascript:doit(\"%s&%s\")\'>%s</a><BR>\n'
                 % (urlprefix.encode("UTF-8"),
                    alink.encode("UTF-8"),
                    astr.encode("UTF-8")))
    fd.write("</ul>\n")
    fd.write(HTMLEpilog())
    fd.close()

def GenHTMLFiles():
    return BuildDict(XMLFile)
