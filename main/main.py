# Import Packages
"""from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER"""

# TODO:
""" If selection from Tree is a filename, change elements of that file, if it's a directory, change elements of directory.
Select the filename or directory, and have a window appear to change...
File - Individual filename album name etc...
Directory - All individual filenames, a single one for album, etc..."""


# Import my files
import display

"""
Ref:
https://methodmatters.github.io/editing-id3-tags-mp3-meta-data-in-python/
"""

def main():
    display.init()

if __name__ == "__main__":
    main()

