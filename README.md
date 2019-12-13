# AnkiTerminalImporter - Import Cards from the Terminal into Anki

## Description

Add a CSV-File with Anki Cards to any Anki Deck with this `python3`

If you have to 

## How to Install
find the `ANKI` folder where anki is installed

``` 
  cd AnkiTerminalImporter
  cp importAnki.py $ANKI
```

## How to Use

``` 
  python3 $ANKI/importAnki.py FILE
```

where `FILE` is the filename of a CSV-dile of the following format:

FRONTTEXT1;BACKTEXT1  
FRONTTEXT2;BACKTEXT2

The name `FILE` also has to be the same as the name of the deck in which the cards should be imported into.

So if you want to add the cards to the deck "Math", you have to rename your file to "Math" and execute the following command:

``` 
  python3 $ANKI/importAnki.py Math
```
