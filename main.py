from __future__ import unicode_literals
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.lang import Builder
from tkinter import filedialog
import requests
import youtube_dl

def durate(s):
    m = s//60
    s = "0"*(2-len(str(s%60))) + str(s%60)
    h = "0"*(2-len(str(m//60))) + str(m//60)
    m = "0"*(2-len(str(m%60))) + str(m%60)
    return f"{h}:{m}:{s}"

def check_video_url(video_id):
    checker_url = "https://www.youtube.com/oembed?url="
    video_url = checker_url + video_id
    request = requests.get(video_url)
    return request.status_code == 200

url_helper = """
MDTextField:
		id: data
		hint_text: "Paste the YouTube video URL Here"
		pos_hint: {"center_x":.4,"center_y":.7}
		width: 600
		size_hint : None,None
		font_size : "20dp"
		line_color_focus : 0/255,0/255,0/255,1
		mode : "rectangle"
        pos : 93,280
"""
screenn = """
MDScreen:
	md_bg_color : [250/255,34/255,83/255,1]
"""

convertt = """
MDRaisedButton:
    text: "CONVERT"
    font_size : 20
    md_bg_color: 0, 0, 0, 1
    pos : 760, 280
    width : 400
    on_press : app.Convert()
"""

inf = """
MDLabel:
    text : ""
    pos : 300,28
    font_size : 18
    bold: True
"""

time = """
MDLabel:
    text : ""
    pos : 290,-1
    font_size : 18
"""

hqdefault = """
AsyncImage:
    source : "https://i.imgur.com/KiuCefX.png"
    pos : -15,101
    size_hint : .35,.35
"""
# source : f"https://i.ytimg.com/vi/{id}/hqdefault.jpg"


_3 = """
MDRaisedButton:
    text: "DOWNLOAD MP3"
    font_size : 20
    md_bg_color: 0, 0, 0, 1
    pos : 290, 115
    width : 400
    on_press : app.mp3_download()
    disabled : True
"""

_4 = """
MDRaisedButton:
    text: "DOWNLOAD MP4"
    font_size: 20
    md_bg_color: 0, 0, 0, 1
    pos : 500, 115
    width: 400
    on_press : app.mp4_download()
    disabled : True
"""
class mainApp(MDApp): 
    def mp3_download(n,**kwargs):
        a = url.text
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key' : 'FFmpegExtractAudio',
                'preferredcodec' : 'mp3',
                'preferredquality' : '192'
                }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([a])

    def mp4_download(n,**kwargs):
        a = url.text
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([a])
    def Convert(self):
        if url.text != "":
            thumbnail.source = "https://i.imgur.com/KiuCefX.png"
            info.text = ""
            info.pos = (290,30)
            info.font_size = 18
            t.text = ""
            if check_video_url(url.text):
                ydl_opts = {}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url.text, download=False)
                    title = info_dict.get('title',None)
                    s = info_dict['duration']
                info.text = title
                mp3.disabled, mp4.disabled = False, False
    
                t.text = durate(s)
                if "&" in url.text:
                    id = url.text[url.text.index("=")+1:url.text.index("&")]
                elif ".be" in url.text :
                    id = url.text[url.text.index("e")+2:]
                else : 
                    id = url.text[url.text.index("=")+1:]
                    
                thumbnail.source = f"https://i.ytimg.com/vi/{id}/hqdefault.jpg"

            else:
                info.font_size = 30
                info.pos = (320,10)
                info.text = "Video Unavailable"
                mp3.disabled, mp4.disabled = True,True

    
    def build(self):
        Window.size = (930,430)
        screen = Builder.load_string(screenn)
        
        global url
        url = Builder.load_string(url_helper)
        screen.add_widget(url)
		
        global info
        info = Builder.load_string(inf)
        screen.add_widget(info)
        
        global t
        t = Builder.load_string(time)
        screen.add_widget(t)

        convert = Builder.load_string(convertt)
        screen.add_widget(convert)

        global thumbnail
        thumbnail = Builder.load_string(hqdefault)
        screen.add_widget(thumbnail)
        
        global mp3,mp4
        mp3,mp4 = Builder.load_string(_3), Builder.load_string(_4)
        screen.add_widget(mp3)
        screen.add_widget(mp4)

        return screen

if __name__ == "__main__":
	mainApp().run()		
