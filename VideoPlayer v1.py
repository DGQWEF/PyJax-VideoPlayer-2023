import vlc
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from time import sleep
from moviepy.video.io.VideoFileClip import VideoFileClip
from threading import Timer
v = ""
duration = 0
tim = None
tim2 = None
B=True
c =0

def center(win, * ,w,h):
    iwidth = (win.winfo_screenwidth() // 2) - (w // 2)
    iheight = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry('{}x{}+{}+{}'.format(w, h, iwidth,iheight-25))

# class MediaPlayer(tk.Tk):
#     def __init__():
#         tk.Tk.__init__()

#         self.create_player()
    

tim = None
tim2 = None
B=True
c =0
t=True
_stop = False
# def echoTime(check=True):
#     global duration,B,c,tim    
#     # #print(convert_to_time_format(int(pygame.mixer.music.get_pos() / 1000)))
#     c=1
#     if B:
#         # #print("B is =>",B)
#         #print("from echoTime => pygame...get_pos() => ",pygame.mixer.music.get_pos() / 1000)
#         #print("from echoTime => pygame...get_pos() => ",convert_to_time_format(
#             # int(pygame.mixer.music.get_pos()/1000)))
#         # root.update_idletasks()
#         duration_label['text'] = convert_to_time_format(int(scale['value'])) + '/' +\
#                 convert_to_time_format(int(duration))  
#         # c += 1 
#         scale.set(int(scale['value']))
#         # time.sleep(1)
#         # #print(f'[{c}] sleep')
#         tim = Timer(1,echoTime)
#         tim.start()
#     else:
#         pass

def change_volume(val):
    try:
        volume = float(val) / 100
        pygame.mixer.music.set_volume(volume)
    except Exception as e:
        pass

class Scale1(ttk.Scale):
    """a type of Scale where the left click is hijacked to work like a right click"""
    def __init__(self, master=None, **kwargs):
        ttk.Scale.__init__(self, master, **kwargs)
        self.bind('<Button-1>', self.set_value_Button1)
        self.bind('<B1-Motion>', self.set_value)
    def set_value_Button1(self, event):
        global B,player
        self.event_generate('<Button-3>', x=event.x, y=event.y)
        
        player.set_time(int(self['value']))

        duration_label['text'] = convert_to_time_format(int(self['value']/1000)) +\
         '/' +convert_to_time_format(int(duration/1000)) 
       
        self.update()
    def set_value(self, event):
        global B,player

        self.event_generate('<Button-3>', x=event.x, y=event.y)

        player.set_time(int(self['value']))

        duration_label['text'] = convert_to_time_format(int(self['value']/1000)) +\
         '/' +convert_to_time_format(int(duration/1000)) 

    def update(self):
        global B,tim,c,t,_stop
        B=False    
        if t:
            try:
                t.cancel()
            except Exception as x:
                pass

        duration_label.config(text=convert_to_time_format(int(float(self['value'])))+\
            "/"+convert_to_time_format(int(duration)))
        c += 1000 
       
        scale.set(self['value'])
        scale.set(self['value'] + 1 )
        t = Timer(1,self.update)
        if not _stop :
            t.start()
        else:
            t.cancel()
class Volume(ttk.Scale):
    """a type of Scale where the left click is hijacked to work like a right click"""
    def __init__(self, master=None, **kwargs):
        ttk.Scale.__init__(self, master, **kwargs)
        self.bind('<Button-1>', self.set_value)
        self.bind('<B1-Motion>', self.set_value)
    def set_value(self, event):
        self.event_generate('<Button-3>', x=event.x, y=event.y)
        #Volume
        change_volume(int(self['value']))

    
root=tk.Tk()
root.title("Media Player")
root.geometry('900x600+300+250')
root.config(bg='gray')
player = None
length = 0

def convert_to_time_format(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

def create_player():
    global v ,player,instance
    instance = vlc.Instance()
    player = instance.media_player_new()
    player.set_hwnd(videoframe.winfo_id())

        
    
def play():
    global player,instance
    if player is None:
        create_player()
        
    v=filedialog.askopenfilename()
    player.set_media(instance.media_new(v))
    player.play()
    
    videoframe['bd'] = 6;videoframe['relief']='ridge'
    print(f".player {player}")
    
    #=======get length==============
    # echoTime()
    # specify the path to the video file
    video_path =v

    # open the video file
    clip = VideoFileClip(video_path)
    # player.set_time(15000)
    # get the length of the video in seconds
    length = clip.duration

    # print the length of the video
    print("Video length: {} seconds".format(length))
    print(f'length => {length}')
    #===============================


    display_info()

    update_scale()

def stop():
    global player
    if player is not None:
        player.stop()
        
def pause():
    global player
    if player is not None:
        player.pause()
def unpause():
    global player
    if player is not None:
        player.play()
        
def change_volume(volume):
    global player
    if player is not None:
        try:
            player.audio_set_volume(int(volume))
            lb_vol.config(text=f"{int(volume)} %")
        except Exception as e:
            pass

        
def seek(position):
    global player
    if player is not None:
        player.set_position(position)

def open_file():
    global player
    filename = tk.filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.flv;*.wmv;*.mov")])
    # play_video(filename)
        
def display_info():
    global player
    global duration
    if player is not None:
        meta = player.get_media().get_meta(vlc.Meta.Title)
        title_label.config(text=meta)
        duration = player.get_length() 
        print(duration)
        duration_label.config(text=duration)

def update_scale():
    global player
    global length
    print('yes')
    if player is not None:
        scale.config(to=duration )
        print(f"length is => {length}")
    update()

def update():
    global player
    scale['from'] = 0
    scale['to'] = duration
    scale.config(value=int(player.get_time()))
    print(f"time => {player.get_time()/1000} ,\
        {convert_to_time_format(int(player.get_time()/1000))}")
    print(".player.get_time() => " , player.get_time()/1000)
    duration_label['text'] = convert_to_time_format(int(player.get_time()/1000)) + "/"+\
        convert_to_time_format(int(duration/1000))
    if player.get_state() == vlc.State.Ended:
        scale.set(0)
        stop()
        root.after_cancel(update)
    root.after(1000,update)
def fullscreen():
    global player
    if player is not None:
        player.set_fullscreen(True)

videoframe = tk.Frame(
    root,bg='black',width=700,height=400,bd=6,relief='ridge'
    )
videoframe.pack()


title_label = tk.Label(root,text="",font=('times',14),bg='gray')
title_label.pack()
# duration_label = tk.Label(root,text="",font=('times',20))
# duration_label.pack()
duration_label = tk.Label(root,text='00:00:00/00:00:00',font=('times',15),bg='gray',
                        fg= 'white')
# duration_label.place(x=300,y=375)
duration_label.pack()

scale = Scale1(root, orient='horizontal', length=700,)
scale.pack()

volume_scale = Volume(root, from_=0, to=100, orient='horizontal', command=change_volume)
volume_scale.set(100) # Set the initial volume to 50%
volume_scale.place(x=500,y=500,)

lb_vol = tk.Label(root,text='100%',bg='gray',fg='white',font=('times',15))
lb_vol.place(x=610,y=502)

play_button = tk.Button(root, text="Open", command=play,
    bg='black',fg='white',font=('times','15'))
play_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop,
    bg='black',fg='white',font=('times','15'))
stop_button.pack()

pause_button = tk.Button(root, text="pause", command=pause,
    bg='black',fg='white',font=('times','15'))
pause_button.pack()


unpause_button = tk.Button(root,text="unpause",command=unpause,
    bg='black',fg='white',font=('times','15'))
unpause_button.pack()

fullscreen_button = tk.Button(root,text="full screen",command=fullscreen,
    bg='black',fg='white',font=('times','15'))
fullscreen_button.pack()
if __name__ == "__main__":
    # player = MediaPlayer()
    # player.set_volume(50)
    center(root,w=800,h=700)
    root.mainloop()
