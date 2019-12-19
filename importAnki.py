#!/usr/bin/python3
from anki.storage import Collection
from anki.importing.csvfile import TextImporter
from sqlite3 import OperationalError
import sys
import os
import re

#change relative to absolute path
#absolute path stays the same
#also check if file even exists
#have to do this first because otherwise directory changes
def getAbsPathFile(f):
    absPath = os.path.abspath(f)
    if not os.path.exists(absPath):
        print("Can't find file", absPath)
        sys.exit(1)
    return absPath

def getNumLinesFile(f):
    return sum(1 for line in open(f))

def openDB():
    home = os.path.expanduser("~")
    dbPath=home + "/.local/share/Anki2/User 1/collection.anki2" #TODO Do this using ProfileManager.collectionPath

    try:
        col = Collection(dbPath)
    except OperationalError as err:
        print(str(err) + " - Is Anki still open?")
        sys.exit(1)
    return col

#xxx/xxx/.../FILE -> FILE
#TODO Set Deck Name by argument?
def getDeckName(absPath):
    #Can assume non-empty because already checked that file exists
    deckName = re.compile('[^/]+').findall(absPath)[-1]
    return deckName

def getDeckID(col, absPath):
    deckName = getDeckName(absPath)
    deckID = col.decks.id(deckName, create=False)

    if deckID == None:
        print("Can't find Deck with Name", deckName)
        sys.exit(1)
    return deckID

#Which Deck should I import into?
def selectDeck(col, absPath, im):
    deckID = getDeckID(col, absPath)

    #Have to do both to work
    col.decks.select(deckID)
    im.model['did'] = deckID

def checkAllNewAdded(im, fileLen):
    #Get Numbers of how many cards where new, updated or unchanged
    (new, update, unchanged) = map(int, re.compile('\d+').findall(str(im.log)))
    # Not everything was added
    if (new, update, unchanged) != (fileLen, 0, 0):
        print("Something was not added as new")
        sys.exit(1)

def importFileInto(col, absPath, fileLen):
    im = TextImporter(col, absPath)
    im.initMapping() #Needed to assert NoteImpoter Line 65 self.mapping correctly
    im.importMode = 1 #Default =0, Ignore on first field equal

    selectDeck(col, absPath, im)

    im.run()
    im.col.save() #Needed as flush

    checkAllNewAdded(im, fileLen)

def main():
    if len(sys.argv) != 2:
        print("Usage: importAnki FILE")
        sys.exit(1)

    path = sys.argv[1]
    absPath = getAbsPathFile(path)
    fileLen = getNumLinesFile(absPath)

    col=openDB()
    importFileInto(col, absPath, fileLen)

if __name__ == "__main__":
    main()

#TODO Sync after import with SyncThread
