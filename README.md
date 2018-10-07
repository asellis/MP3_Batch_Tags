# MP3_Batch_Tags
This was created primarily to modify files whose names I wanted to trim and to add numbers to overcome poor sorting on an mp3 player. This program has a few naming tools as well as auto numbering which generally helps with sorting on an mp3 player. There are a few additional modification features to be performed in batch.

This is a work in progress and unpolished, however it fills many of my needs as is.

# Supported Features
- Sort (and reverse sort) by Name, #, Album, Title, Creation Date, Modification Date
- Auto number (based on current sort setting)
- File Name to Title (can be usefully for applications in which title is shown instead of file name)
- Naming features
    - Remove text string from all files (if found)
    - Strip characters from all files
- Revert (if a mistake was made you can revert to the initial input, but must be saved for changes to take effect)

# Installation
Download the repository and start MP3_Batch_Tags.py

# How to Use
![Image of Program](https://github.com/asellis/MP3_Batch_Tags/blob/master/img/Program%20Layout.PNG)

Clicking the Open will give a folder selection prompt which can be used for choosing the folder with the mp3 files you want to apply tags to.

Toggles will show the files information about the selected toggle. Files can be sorted by pressing the header in the view window. Reverse sorting is also available.

![Sort1](https://github.com/asellis/MP3_Batch_Tags/blob/master/img/Sort%201.PNG)
![Sort2](https://github.com/asellis/MP3_Batch_Tags/blob/master/img/Sort%202.PNG)

Auto number will number all the files based on their current sorting.

File changes will only occur after pressing the save button. There is also a revert button that will change the tags back to their original setting, however you must save again after doing this.

# Credits
Mutagen library was used for ID3 tag modifications
