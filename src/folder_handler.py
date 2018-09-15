"""
Folder Handler to easily sort through contents and apply changes
Stores all files and information in a dictionary with the key being the original
    file location
"""

from pathlib import Path
import mp3_tag_functions as tag
import time

class Folder_Handler:
    def __init__(self, path):
        self.folder_path = path

        # Variables to hold files and a copy of the files
        self.Folder = []
        self.Folder_Dict = dict()
        self.Update_Files(path)
        self.Folder_Dict = self._make_dict(self.Folder)

        # Variables for toggle
        self.file_numbers = 0
        self.modify_date = 0
        self.creation_date = 0
        self.song_length = 0

        self.max_name_length = 125

    def _make_dict(self, Folder):
        d = dict()
        for file in Folder:
            d[file] = dict([
                ('path',file),
                ('suffix',file.suffix),
                ('name',file.stem),
                ('temp_name',file.stem),
                ('num', str(tag.track_num(file))),
                ('temp_num', str(tag.track_num(file))),
                ('modify_date', str(time.ctime(tag.get_mod_date(file)))),
                ('creation_date', str(time.ctime(tag.get_creation_date(file)))),
                ('album', str(tag.get_album(file))),
                ('temp_album', str(tag.get_album(file))),
                ('title', str(tag.get_title(file))),
                ('temp_title', str(tag.get_title(file))),
                ('length', str(tag.get_length(file)))])
        return d

    def Update_Files(self, path):
        # Used when a new path is defined
        self.Folder = []
        for file in path.iterdir():
            if file.suffix.lower()=='.mp3':
                self.Folder.append(file)
        self.temp_Folder = list(self.Folder)

    def temp_info(self):
        # Returns a list of string with info about each file
        # Info can be changed with variables
        
        return_folder = []
        
        name_length = 50
        max_name_length = self.max_name_length
        max_length=0
        
        max_length = max(self.temp_Folder, key = lambda x: len(x.stem))
        max_length = len(max_length.stem)
        
        if max_length > name_length and max_length < max_name_length:
            name_length = max_length


        header = ""
        header+="{:{width}.{width}s}".format("Name", width=name_length)
        if self.file_numbers:
                header+="  {:4.4s}".format("#")

        return_folder.append(header)
        
        for file in self.Folder:
            info = ""
            info+="{:{width}.{width}s}".format(file.stem, width=name_length)

            if self.file_numbers:
                info+="  {:4.4s}".format(self.Folder_Dict[file]['temp_num'])
            if self.modify_date:
                info+=str(time.ctime(tag.get_mod_date(file)))
            
            return_folder.append(info)
        
        return return_folder

    def get_info(self):
        # returns all the info for each object in previously set order
        info = []
        for item in self.Folder:
            info.append(self.Folder_Dict[item])
        return info

    def toggle_file_numbers(self, toggle):
        # Toggles wether or not the file number will be displayed
        self.file_numbers = toggle

    def toggle_modify_date(self, toggle):
        # Toggles wether or not the modify date will be displayed
        self.modify_date = toggle

    def toggle_creation_date(self, toggle):
        # Toggles wether or not the creation date will be displayed
        self.creation_date = toggle

    def set_name_length(self, num):
        self.max_name_length=num

    def set_album(self, album):
        for file in self.Folder:
            self.Folder_Dict[file]['temp_album']=album
    """
    Sorting Functions
    """
    def sort_name(self, r=False):
        # Sort by file name
        self.Folder.sort(key=self._temp_name, reverse=r)

    def _temp_name(self, path):
        return self.Folder_Dict[path]['temp_name']

    def sort_mod_date(self, r=False):
        # Sort by modification date
        self.Folder.sort(key=tag.get_mod_date, reverse=r)

    def sort_create_date(self, r=False):
        # Sort by modification date
        self.Folder.sort(key=tag.get_creation_date, reverse=r)

    def sort_num(self, r=False):
        # Sort by file number
        self.Folder.sort(key=tag.get_num_int, reverse=r)

    def sort_album(self, r=False):
        # Sort by Album
        self.Folder.sort(key=tag.get_album, reverse=r)

    def sort_title(self, r=False):
        # Sort by track name
        self.Folder.sort(key=tag.get_title, reverse=r)


    """
    Additional Functions
    """
    def auto_number(self):
        # Auto numbers the files based on the current sorting
        for i, file in enumerate(self.Folder):
            self.Folder_Dict[file]['temp_num']=i+1

    def remove_numbers(self):
        # Removes all numbering
        for file in self.Folder:
            self.Folder_Dict[file]['temp_num']='None'

    def file_name_to_title(self):
        # Copies file name as ID3 title field
        for file in self.Folder:
            self.Folder_Dict[file]['temp_title']=self.Folder_Dict[file]['temp_name']

    """
    Naming Functions
    """
    def remove_from_name(self, remove):
        # Removes the specified phrase "remove" from the name
        for file in self.Folder:
            self.Folder_Dict[file]['temp_name']=self.Folder_Dict[file]['temp_name'].replace(remove, '')

    def fix_whitespace(self):
        # Makes all space between words only one and strips whitespace on ends
        for file in self.Folder:
            name = self.Folder_Dict[file]['temp_name']
            new_name = " ".join(name.split(' '))
            self.Folder_Dict[file]['temp_name'] = new_name

    def strip_left(self, amount=1):
        # Strips characters from the left side of the name
        #   Strips 1 character by default
        for file in self.Folder:
            self.Folder_Dict[file]['temp_name']=self.Folder_Dict[file]['temp_name'][amount:]

    def strip_right(self, ammount=1):
        # Strips characters from the right side of the name
        #   Strips 1 character by default
            for file in self.Folder:
                self.Folder_Dict[file]['temp_name']=self.Folder_Dict[file]['temp_name'][:((-1)*ammount)]

    def revert(self):
        # Puts back the original data into the temporary data
        for file in self.Folder:
            self.Folder_Dict[file]['temp_name']=self.Folder_Dict[file]['name']
            self.Folder_Dict[file]['temp_num']=self.Folder_Dict[file]['num']
            self.Folder_Dict[file]['temp_title']=self.Folder_Dict[file]['title']
            self.Folder_Dict[file]['temp_album']=self.Folder_Dict[file]['album']

    """
    Saving Functions
    """
    def save_info(self):
        # Saves info
        for file in self.Folder:
            path = self.Folder_Dict[file]['path']
            tag.save_number(path, self.Folder_Dict[file]['temp_num'])
            tag.save_title(path, self.Folder_Dict[file]['temp_title'])
            self.save_name(file)
            # Need save album

    def save_name(self, file):
        # Save file name
        if self.Folder_Dict[file]['temp_name']!='':
            path = self.Folder_Dict[file]['path']
            new_path = Path(str(Path(path).parent) + '/' + self.Folder_Dict[file]['temp_name'] + \
                            str(self.Folder_Dict[file]['suffix']))
            Path(path).rename(new_path)
            self.Folder_Dict[file]['path']=new_path
        else:
            print('Invalid name,"{}", for "{}"'.format(\
                self.Folder_Dict[file]['temp_name'],
                self.Folder_Dict[file]['path']))
