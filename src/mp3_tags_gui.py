"""
Contains the code for using the GUI
Stores all files in Folder_Handler class
"""

from tkinter import *
from tkinter import filedialog      # For opening a folder
from tkinter.ttk import Treeview    # For listing the contents of a folder
from pathlib import Path
import mp3_tag_functions as tag
import folder_handler


class MP3_Tags_GUI:
    def __init__(self, master):
        self.master = master
        master.title("MP3 Batch Tags")
        master.columnconfigure(4, weight=1)
        #master.geometry("800x500")

        """
        GUI Widgets
        """
        # Folder Path
        self.Folder_Label = Label(master, text="Folder", width = 15, padx = 2, pady = 2)
        self.Folder_Label.grid(row=1, column=1, padx = 2, pady = 2)
        self.Folder_Entry = Entry(master)
        self.Folder_Entry.grid(row=1, column=4, sticky=W+E)
        self.Folder_Entry.config(state=DISABLED) # To prevent change of dir by typing (have to use open)
        self.Open_Button = Button(master, text="Open", width=15,
                command=self.File_Browser, padx = 2, pady = 2)
        self.Open_Button.grid(row=1, column=3, padx = 2, pady = 2)
        self.Folder_Path = ''
        
        # Folder path variables
        self.Path_Found = False
        self.Folder_Path = Path()
        self.Folder = folder_handler.Folder_Handler(self.Folder_Path)

        # Scrollbar for folder contents
        self.Folder_List_Span = 200

        # Old, now use treeview instead of listbox
        #self.Folder_List = Listbox(master, yscrollcommand=self.scrollbar.set, height = 30, width = 80)
        #self.Folder_List.grid(row=2, column=4, rowspan=self.Folder_List_Span, sticky=N+S+E+W,
        #                      padx = 2, pady = 2)

        # Set view of files as Treeview
        self.items = ['Name', 'Number', 'Modified', 'Created', 'Album', 'Title']
        self.sortables = [self.Sort_Name, self.Sort_Number, self.Sort_Modified, self.Sort_Created,\
                          self.Sort_Album, self.Sort_Title]
        self.Sort_Reverse = dict()
        for item in self.items:
            self.Sort_Reverse[item] = False # Will turn true after sorting once
        self.viewable_items = []
        
        self.tree = Treeview(master, selectmode='none', height=20)

        self.scrollbar = Scrollbar(orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=2, column=5, sticky=NS, rowspan = self.Folder_List_Span,
                            padx = 2, pady = 2)
        
        self.tree["columns"]=self.items[1:]
        for i,item in enumerate(self.items):
            self.tree.heading('#{}'.format(i), text=item, command=self.sortables[i])
            self.tree.column('#{}'.format(i))
        self.tree.column('#0', width=400)
        self.tree.column('#1', width=60)
        self.tree.grid(row=2, column=4,rowspan=self.Folder_List_Span, sticky=NSEW,
                            padx = 2, pady = 2)
        self.tree['displaycolumns']=[]
        
        self.scrollbar.config(command=self.tree.yview)

        Grid.rowconfigure(master, 200, weight=1)



        # Buttons for saving
        # Revert, Save
        start_row = 50
        self.Blank_Row(start_row,1)
        self.Revert_Button = Button(master, text="Revert Changes", width = 15, padx = 2, pady = 2,
                command=self.Revert_Changes)
        self.Revert_Button.grid(row=start_row+1,column=1, padx = 2, pady = 2)
        self.Save_Button = Button(master, text="Save", width = 15, padx = 2, pady = 2, command=self.Save_Info)
        self.Save_Button.grid(row=start_row+1,column=3, padx = 2, pady = 2)

        # Blank row
        self.Blank_Row(3,1)
        
        # Check boxes for view        
        start_row = 4 # if add something prior will make it easy to push down
        Label(master, text="View Toggles").grid(row=start_row, column=0, columnspan=4, padx=2, pady=2)
        self.file_num = IntVar()
        self.file_num_check = Checkbutton(master, text="File #", variable=self.file_num,
                            onvalue=1, offvalue=0, command=self.Toggle_Num)\
                              .grid(row=start_row+2, column=1, sticky=W)
        self.modify_date = IntVar()
        self.modify_date_check = Checkbutton(master, text="Modify Date", variable=self.modify_date,
                            onvalue=1, offvalue=0, command=self.Toggle_Modified)\
                              .grid(row=start_row+3, column=1, sticky=W)
        self.creation_date = IntVar()
        self.creation_date_check = Checkbutton(master, text="Creation Date", variable=self.creation_date,
                            onvalue=1, offvalue=0, command=self.Toggle_Created)\
                              .grid(row=start_row+3, column=2, sticky=W)

        """
        # Had issues getting song length, may implement later
        self.song_length = IntVar()
        self.song_length_check = Checkbutton(master, text="Song Length", variable=self.song_length,
                            onvalue=1, offvalue=0, command=self.Toggle_Length)\
                            .grid(row=start_row+2, column=3, sticky=W)
        """
        
        self.album_tog = IntVar()
        self.album_check = Checkbutton(master, text="Album", variable=self.album_tog,
                            onvalue=1, offvalue=0, command=self.Toggle_Album)\
                            .grid(row=start_row+2, column=3, sticky=W)
        self.title_tog = IntVar()
        self.title_check = Checkbutton(master, text="Title", variable=self.title_tog,
                            onvalue=1, offvalue=0, command=self.Toggle_Title)\
                            .grid(row=start_row+2, column=2, sticky=W)

        
        """
        # OLD Radio button for sorting
        self.start_row = 3
        self.Sort_Setting = IntVar()
        
        self.Sort_Button = Button(master, text="Sort", width = 15, padx = 2, pady = 2, command=self.Sort)
        self.Sort_Button.grid(row=start_row,column=3, padx = 2, pady = 2)
        Modes = ["File Name", "File #", "Modify Date", "Creation Date", "Song Length"]
        for i, setting in enumerate(Modes):
            Radiobutton(master, text=setting, variable=self.Sort_Setting, value=i, command=self.Sort)\
                                .grid(row=start_row+i+1,column=3, sticky=W)
        """
        
        """
        Actions (Auto Number, Name to Title, Album Name, etc.)
        """
        start_row = 10
        self.Blank_Row(start_row,1)
        Label(master, text="Actions", width = 15, padx = 2, pady = 2)\
                      .grid(row=start_row+1, column=1, padx = 2, pady = 2, columnspan=3)

        # Auto Number
        # Number files base on sort setting
        self.Auto_Number_Button = Button(master, text="Auto Number", width = 15, padx = 2, pady = 2,
                command=self.Auto_Number)
        self.Auto_Number_Button.grid(row=start_row+2,column=1, padx = 2, pady = 2)

        # Remove Numbers
        Button(master, text="Remove Numbers", width=15, padx=2, pady=2, command=self.Remove_Numbers)\
                       .grid(row=start_row+2, column=2, padx=2, pady=2)

        # File Name -> Track
        self.File_Name_Title_Button = Button(master, text="File Name -> Title", width = 15, padx = 2, pady = 2,
                command=self.File_Name_Title)\
                .grid(row=start_row+2,column=3, padx = 2, pady = 2)

        self.Blank_Row(start_row+3)
        # Set Album Name
        Label(master, text="Album Name", width = 15, padx = 2, pady = 2)\
                      .grid(row=start_row+4, column=2, padx = 2, pady = 2)
        self.Album_Entry = Entry(master)
        self.Album_Entry.grid(row=start_row+5, column=1,\
                        columnspan=2, sticky=W+E, padx = 2, pady = 2)
        self.Album_Set = Button(master, text="Set", command=self.Set_Album, width = 15, padx = 2, pady = 2)
        self.Album_Set.grid(row=start_row+5,column=3, padx = 2, pady = 2)

        """
        Naming Options
        """
        start_row = start_row + 6
        self.Blank_Row(start_row)
        Label(master, text="Naming Options", width = 15, padx = 2, pady = 2)\
                      .grid(row=start_row+1, column=2, padx = 2, pady = 2)
        self.Remove_Text_Entry = Entry(master)
        self.Remove_Text_Entry.grid(row=start_row+2, column=1, columnspan=2, sticky=W+E, padx = 2, pady = 2)
        self.Remove_Text_Button = Button(master, text="Remove Text", width = 15, padx=2, pady=2,\
                                         command=self.Remove_from_Name)
        self.Remove_Text_Button.grid(row=start_row+2, column=3, padx=2, pady=2)
        
        # Strip characters from left/right
        start_row = start_row+3
        self.Blank_Row(start_row)
        Label(master, text="Strip Characters", width = 15, padx = 2, pady = 2)\
                      .grid(row=start_row+1, column=1, padx = 2, pady = 2)
        Button(master, text="Left", width = 15, padx = 2, pady = 2, command=self.Strip_Left)\
                       .grid(row=start_row+1, column=2, padx=2, pady=2)
        Button(master, text="Right", width = 15, padx = 2, pady = 2, command=self.Strip_Right)\
                       .grid(row=start_row+1, column=3, padx=2, pady=2)

    """
    Setup Functions
    """
    def Open_Folder(self):
        # Opens folder stored in Folder_Entry
        print("Opening Folder")
        folder_name = self.Folder_Path
        if len(folder_name)==0:
            print("Folder not specified")
            return
        folder=folder_name.split('\\')
        new_folder_name = ''
        for part in folder:
            new_folder_name += part
            new_folder_name += '\\\\'
        #try:
        path = Path(new_folder_name)
        if path.is_dir():
            print("Folder Found!")
            self.Path_Found = True
            self.Folder_Path = path
            self.Folder = folder_handler.Folder_Handler(self.Folder_Path)
            self.Update_Tree()
            return
        else:
            print('NOT A FOLDER')
        #except:
        #    print('INVALID')

    def File_Browser(self):
        # Opens a file browser and stores it in Folder_Entry
        self.Folder_Path = filedialog.askdirectory()
        # View folder path in entry
        self.Folder_Entry.config(state='normal')
        self.Folder_Entry.delete(0,END)
        self.Folder_Entry.insert(0,self.Folder_Path)
        self.Folder_Entry.config(state='disabled')
        self.Open_Folder()

    def Update_List(self):
        # OLD, used to update list
        # replaced by Update_Tree
        self.Folder_List.delete(0,"end")

        # Set Toggles
        self.Folder.toggle_file_numbers(self.file_num.get())
        self.Folder.toggle_modify_date(self.modify_date.get())
        temp_info = self.Folder.temp_info()
        for i in temp_info:
            self.Folder_List.insert(END, i)

        self.Update_Tree()

    def Update_Tree(self):
        # Updated the tree view
        self.tree.delete(*self.tree.get_children())
        
        info = self.Folder.get_info()
        for item in info:
            self.tree.insert('', 'end', text=item['temp_name'],
                values=(item['temp_num'], item['modify_date'], item['creation_date'],\
                        item['temp_album'], item['temp_title'], item['length']))

    """
    Toggles for viewing file info
    """ 
    def Toggle_Num(self):
        # Shows numbers in list of files
        if self.file_num and 'Number' not in self.viewable_items:
            self.viewable_items.append('Number')
        else:
            self.viewable_items.remove('Number')
        self.tree['displaycolumns']=self.viewable_items

    def Toggle_Modified(self):
        # Shows modified date in list of files
        if 'Modified' not in self.viewable_items:
            self.viewable_items.append('Modified')
        else:
            self.viewable_items.remove('Modified')
        self.tree['displaycolumns']=self.viewable_items

    def Toggle_Created(self):
        # Shows numbers in list of files
        if 'Created' not in self.viewable_items:
            self.viewable_items.append('Created')
        else:
            self.viewable_items.remove('Created')
        self.tree['displaycolumns']=self.viewable_items

    def Toggle_Album(self):
        # Shows album in list of files
        if 'Album' not in self.viewable_items:
            self.viewable_items.append('Album')
        else:
            self.viewable_items.remove('Album')
        self.tree['displaycolumns']=self.viewable_items

    def Toggle_Title(self):
        # Shows the title in list of files
        if 'Title' not in self.viewable_items:
            self.viewable_items.append('Title')
        else:
            self.viewable_items.remove('Title')
        self.tree['displaycolumns']=self.viewable_items

    def Toggle_Length(self):
        # Shows the song length in list of files
        if 'Length' not in self.viewable_items:
            self.viewable_items.append('Length')
        else:
            self.viewable_items.remove('Length')
        self.tree['displaycolumns']=self.viewable_items
        
    """
    Sorts
    """
    def Sort(self):
        # Sorts the files based on original data
        setting = self.Sort_Setting.get()
        
        # Check Radio for which sort
        if setting==0:
            # Sort by name
            self.Folder.sort_name()
        elif setting==1:
            # Sort by file number
            self.Folder.sort_num()
        elif setting==2:
            print(2)
            # Sort by modification date
            self.Folder.sort_mod_date()

        # Update View
        self.Update_List()

    def Sort_Name(self):
        # Sorts by name, check if it should reverse name sort first
        self._Sort_Reverse_False('Name')
        r = self._Sort_Toggle('Name')
        self.Folder.sort_name(r)
        self.Update_Tree()

    def Sort_Number(self):
        # Sorts by number, check if it should reverse name sort first
        self._Sort_Reverse_False('Number')
        r = self._Sort_Toggle('Number')
        self.Folder.sort_num(r)
        self.Update_Tree()

    def Sort_Modified(self):
        # Sorts by modification date
        self._Sort_Reverse_False('Modified')
        r = self._Sort_Toggle('Modified')
        self.Folder.sort_mod_date(r)
        self.Update_Tree()

    def Sort_Created(self):
        # Sorts by creation date
        self._Sort_Reverse_False('Created')
        r = self._Sort_Toggle('Created')
        self.Folder.sort_create_date(r)
        self.Update_Tree()

    def Sort_Album(self):
        # Sorts by creation date
        self._Sort_Reverse_False('Album')
        r = self._Sort_Toggle('Album')
        self.Folder.sort_album(r)
        self.Update_Tree()

    def Sort_Title(self):
        # Sorts by creation date
        self._Sort_Reverse_False('Title')
        r = self._Sort_Toggle('Title')
        self.Folder.sort_title(r)
        self.Update_Tree()

    def Sort_Length(self):
        pass

    def _Sort_Reverse_False(self, name):
        for item in self.items:
            if item != name:
                self.Sort_Reverse[item] = False

    def _Sort_Toggle(self, name):
        if self.Sort_Reverse[name] == False:
            self.Sort_Reverse[name] = True
            return False
        else:
            self.Sort_Reverse[name] = False
            return True

    """
    Additional tag functions
    """
    def Auto_Number(self):
        # Auto Numbers based on sort, does not save
        self.Folder.auto_number()
        self.Update_Tree()

    def Remove_Numbers(self):
        # Removes Numbers from files
        self.Folder.remove_numbers()
        self.Update_Tree()

    def Revert_Changes(self):
        # Reverts changes, but has to be saved
        self.Folder.revert()
        self.Update_Tree()

    def File_Name_Title(self):
        # Copies File Name to Title Name
        self.Folder.file_name_to_title()
        self.Update_Tree()

    def Set_Album(self):
        # Sets the album name to whatever is in the Album_Entry
        album = self.Album_Entry.get()
        self.Folder.set_album(album)
        self.Update_Tree()

    def Save_Info(self):
        print('Saving Info')
        self.Folder.save_info()
        print('Done')

    """
    Naming Functions
    """
    def Remove_from_Name(self):
        remove = self.Remove_Text_Entry.get()
        self.Folder.remove_from_name(remove)
        self.Update_Tree()

    def Fix_Whitespace(self):
        # Makes all space between words only one and strips whitespace on ends
        self.Folder.fix_whitespace()

    def Strip_Left(self):
        # Strips a single character from the left side of the name
        self.Folder.strip_left()
        self.Update_Tree()

    def Strip_Right(self):
        # Strips a single character from the right side of the name
        self.Folder.strip_right()
        self.Update_Tree()

    """
    GUI Functions
    """
    def Blank_Row(self, row, col=1, height=2, col_span=1):
        # Inserts a blank row
        Label(self.master, text="").grid(row=row, column=col, columnspan=col_span, pady=height)


if __name__ == "__main__":
    # Starts the program
    test = Tk()
    gui =  MP3_Tags_GUI(test)
    test.mainloop()
