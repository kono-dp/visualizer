## Third-Party Libraries

This project uses the following third-party libraries:

- SwitchControlLibrary by celclow, licensed under the MIT License.
  - Copyright (c) 2019 celclow

Please see the included LICENSE files for each library for details.


## 内容
解説動画：https://youtu.be/CfzkOoiG0gY?si=66gtPxYi44bCXKdg  

Nintendo Switch Proコントローラーからの信号を、Arduinoを利用することでPCとSwitchの両方に渡し、ついでにPC上でコントローラの入力をグラフィカルに可視化できるツールです。  
to_arduino.py：PCがArduinoに信号を渡すためのコード  
to_switch.ino：ArduinoがPCから受け取った信号をSwitch用のコマンドに変換し、Switchに送るためのスケッチ  
visualize.py：PCがプロコンから受け取った信号をもとにリアルタイムにコントローラの画像を生成し、表示するためのコード  
