import pip
from tkinter import messagebox




def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

# Example
if __name__ == '__main__':
    install('vlc-python')
    install('moviepy')
    messagebox.showinfo('App','Installation Libraries is Completed  now run videoplayer app with double click thanks ')
