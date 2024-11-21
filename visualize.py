import customtkinter as ctk
import pygame
from PIL import ImageTk, Image
import os
import time


# CustomTkinterのウィンドウを作成
root = ctk.CTk()
root.title("Controller Input Viewer")
# ウィンドウサイズ不可変
root.resizable(False, False)

def on_closing():
    root.destroy()
    pygame.quit()
def on_key(event):
    if event.keysym == "Escape":
        on_closing()
    global window_size
    if event.keysym == "Up":
        window_size += 1
        window_size = min(24, window_size)
        image_label.configure(image=ImageTk.PhotoImage(pictures["background_black"].resize((window_size * 80, window_size * 45), Image.ANTIALIAS)))
    if event.keysym == "Down":
        window_size -= 1
        window_size = max(2, window_size)
        image_label.configure(image=ImageTk.PhotoImage(pictures["background_black"].resize((window_size * 80, window_size * 45), Image.ANTIALIAS)))

root.bind("<Key>", on_key)


# Pygameを初期化し、ジョイスティック（コントローラー）を設定
pygame.init()
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)

image_label = ctk.CTkLabel(root, text="")
image_label.pack()

# 予め、picturesフォルダ内の画像をすべて開いておく
pictures = dict()
for folder_name in ["ABXY", "UpDownLeftRight", "LR", "other", "stick"]:
    file_names = os.listdir(f"pictures/{folder_name}")
    for file_name in file_names:
        pictures[file_name[:-4]] = Image.open(f"pictures/{folder_name}/{file_name}")
print(pictures)

button_index = {0: 0, 1: 1, 2: 2, 3: 3, # ABXY
                4: 0, 5: 1, 6: 2, 15: 3, # -、HOME、+、キャプチャー
                9: 0, 10: 1, # LR
                11: 0, 12: 1, 13: 2, 14: 3} # 上下左右


window_size = 6
image_label.configure(image=ImageTk.PhotoImage(pictures["background_black"].resize((window_size * 80 * 2, window_size * 45 * 2), Image.ANTIALIAS)))
try:
    while True:
        a = time.time()
        # 画面の更新（なぜかここにこれを書かないと上手く動かない。。。どうして。。。）
        root.update_idletasks()
        root.update()

        # イベントをPygameのイベントキューに追加
        pygame.event.pump()

        # TkinterのLabelウィジェットには一つしか画像を載せられないので、
        # 重ねるべき画像を格納するリストをつくり、後で１つの画像に合成する
        pictures_to_combine = list()
        
        # ベースとなる画像を選択
        if controller.get_button(9) and controller.get_button(10):
            base = pictures["LR11"].copy()
        elif controller.get_button(9):
            base = pictures["LR10"].copy()
        elif controller.get_button(10):
            base = pictures["LR01"].copy()
        else:
            base = pictures["LR00"].copy()

        # ベースの上に貼る適当な画像を選択
        ABXY = ""
        UpDownLeftRight = ""
        other = ""
        for i in range(0, 4):
            if controller.get_button(i):
                ABXY += "1"
            else:
                ABXY += "0"
        for i in range(11, 15):
            if controller.get_button(i):
                UpDownLeftRight += "1"
            else:
                UpDownLeftRight += "0"
        for i in range(4, 7):
            if controller.get_button(i):
                other += "1"
            else:
                other += "0"
        if controller.get_button(15):
            other += "1"
        else:
            other += "0"

        if ABXY != "0000":
            pictures_to_combine.append(pictures[f"ABXY{ABXY}"])
        if UpDownLeftRight != "0000":
            pictures_to_combine.append(pictures[f"UpDownLeftRight{UpDownLeftRight}"])
        if other != "0000":
            pictures_to_combine.append(pictures[f"other{other}"])

        # スティックの偏りを計算
        Lstick_offset = (int(30 * controller.get_axis(0)), int(30 * controller.get_axis(1)))
        Rstick_offset = (int(30 * controller.get_axis(2)), int(30 * controller.get_axis(3)))

        # 画像を重ねる
        for picture in pictures_to_combine:
            base.paste(picture, box=None, mask=picture)
        base.paste(pictures["Lstick"], Lstick_offset, pictures["Lstick"])
        base.paste(pictures["Rstick"], Rstick_offset, pictures["Rstick"])

        # サイズ更新
        window_width_now = root.winfo_width()
        window_height_now = root.winfo_height()
        if window_width_now > window_height_now * 1320 / 880:
            new_size = (window_height_now * 1320 // 880, window_height_now)
        else:
            new_size = (window_width_now, window_width_now * 880 // 1320)
        base = base.resize(new_size, Image.ANTIALIAS)
        
        # 画像をTkinter対応の形に変換
        combined_picture = ImageTk.PhotoImage(base)
        
        # 画面の更新準備
        image_label.configure(image=combined_picture)
        
        
        b = time.time()
        print(b-a)  

except KeyboardInterrupt:
    pygame.quit()