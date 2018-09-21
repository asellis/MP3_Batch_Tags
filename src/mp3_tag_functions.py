# Functions for getting and saving info for mp3 file
import sys
sys.path.append('../lib/mutagen-master')
sys.path.append('lib/mutagen-master')

from pathlib import Path
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

def safe_path(path):
    folder=path.split('\\')
    new_folder_name = ''
    for part in folder[0:-1]:
        new_folder_name += part
        new_folder_name += '/'
    new_folder_name+=folder[-1]
    return new_folder_name

def make_EasyID3(path):
    # If path has ID3 then will return EasyID3 object
    # If not then it will add ID3 and return
    file = safe_path(str(path))
    try:
        obj = EasyID3(file)
    except ID3NoHeaderError:
        obj = MP3(file, ID3=EasyID3)
        obj.add_tags(ID3=EasyID3)
    return obj

def track_num(path):
    file = make_EasyID3(path)
    num = file.get('tracknumber')
    try:
        return num[0]
    except TypeError:
        return num

def sort_name(folder):
    # Sort by file name
    folder.sort(key=get_name)
    return folder

def sort_mod_date(folder):
    # Sort by modification date
    folder.sort(key=get_mod_date)
    return folder

def sort_num(folder):
    # Sort by file number
    folder.sort(key=track_num)
    return folder


"""
Get info from file
"""
def get_creation_date(file):
    return file.stat().st_ctime

def get_mod_date(file):
    return file.stat().st_mtime

def get_name(file):
    return file.stem

def get_num_int(path):
    file = make_EasyID3(path)
    num = file.get('tracknumber')
    if str(num)=='None':
        return num
    return int(num[0])

def get_album(path):
    file = make_EasyID3(path)
    album = file.get('album')
    if str(album)=='None':
        return str(album)
    return album[0]

def get_title(path):
    file = make_EasyID3(path)
    title = file.get('title')
    if title==None:
        return str(title)
    return title[0]

def get_length(path):
    file = make_EasyID3(path)
    length = file.get('length')
    if length==None:
        return length
    return length[0]

"""
Saving Functions
"""
def save_number(path, number):
    file = make_EasyID3(path)
    file['tracknumber'] = str(number)
    if str(number)=='None':
        file['tracknumber']=''
    file.save()

def save_title(path, title):
    file = make_EasyID3(path)
    file['title'] = str(title)
    if str(title)=='None':
        file['title']=''
    file.save()

def save_album(path, album):
    file = make_EasyID3(path)
    file['album'] = str(album)
    file.save()

def save_name(path, name):
    # Saves the file name
    path.rename(new_name)

# def save_album(path, album):

#from mutagen.easyid3 import EasyID3
#print(EasyID3.valid_keys.keys())
