import pygame
import time
import serial



# Pygameを初期化し、ジョイスティック（コントローラー）を設定
pygame.init()
pygame.joystick.init()
num_joysticks = pygame.joystick.get_count()
print(f"Number of joysticks: {num_joysticks}")
controller = pygame.joystick.Joystick(0)
# Arduinoと繋ぐ
ser = serial.Serial('COM3', 115200) ##################################################################


button_before = [0] * 16
ZLR_before = [0] * 2
try:
    while True:
        start_time = time.time()
        # イベントをPygameのイベントキューに追加
        pygame.event.pump()

        # 入力を保存
        button = [0] * 16
        axis = [0] * 4
        ZLR = [0] * 2
        for i in range(16):
            button[i] = int(controller.get_button(i))
        for i in range(4):
            axis[i] = controller.get_axis(i)
        for i in range(2):
            ZLR[i] = controller.get_axis(i + 4)
            if ZLR[i] > 0.5:
                ZLR[i] = 1
            elif ZLR[i] < -0.5:
                ZLR[i] = 0
        
        # Arduinoに送る形に整える
        message = [0] * 22
        for i in range(16):
            if button[i] == button_before[i]: # 押されっぱ or 離しっぱ。Arduino → Switch は何も送らなくていい
                message[i] = 0
            elif button[i]: # ボタンが押された
                message[i] = 1
            else: # ボタンが離された
                message[i] = 2
            button_before[i] = button[i]
        for i in range(4):
            message[i + 16] = int(axis[i] * 128) + 128
        for i in range(2):
            if ZLR[i] == ZLR_before[i]: # 押されっぱ or 離しっぱ。Arduino → Switch は何も送らなくていい
                message[i + 20] = 0
            elif ZLR[i]: # ボタンが押された
                message[i + 20] = 1
            else: # ボタンが離された
                message[i + 20] = 2
            ZLR_before[i] = ZLR[i]
        
        # Arduinoに送る
        message = list(map(str, message))
        message = ",".join(message) + ";"
        print(message)
        # データをバイト列にエンコードして送る
        ser.write(message.encode())
        
        # 75Hzで通信する
        end_time = time.time()
        time_to_wait = 1 / 120 - (end_time - start_time)  #############################################################
        time.sleep(time_to_wait)

except KeyboardInterrupt:
    pygame.quit()