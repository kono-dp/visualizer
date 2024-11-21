#include <SwitchControlLibrary.h>

void setup() {
  SwitchControlLibrary();
  Serial1.begin(115200);
}


int message_list[22]; // 長さ22の整数配列を定義
String received_message = ""; // 受信したメッセージを格納する文字列
void loop() {
  if (Serial1.available()) { // シリアル通信でデータが利用可能な場合
    char received_char = static_cast<char>(Serial1.read()); // 受信した文字を読み込む
    
    // セミコロンが送信された場合はメッセージの終わりとする
    if (received_char == ';') {
      int index = 0; // 配列のインデックス
      String current_str = ""; // 現在の数値を表す文字列

      // 受信したメッセージを配列に入れて整理
      for (int i = 0; i < received_message.length(); i++) {
        char c = received_message.charAt(i); // i番目の文字を取得
        if (c == ',') {
          message_list[index] = current_str.toInt(); // 文字列を整数に変換し、配列に格納
          current_str = "";
          index += 1;
        } else {
          current_str += c;
        }
      }
      message_list[index] = current_str.toInt();

      // 配列の内容をSwitchに送信
      // ABXYについて
      if (message_list[0] == 1){
        SwitchControlLibrary().pressButton(Button::A);
      }else if (message_list[0] == 2){
        SwitchControlLibrary().releaseButton(Button::A);
      }
      if (message_list[1] == 1){
        SwitchControlLibrary().pressButton(Button::B);
      }else if (message_list[1] == 2){
        SwitchControlLibrary().releaseButton(Button::B);
      }
      if (message_list[2] == 1){
        SwitchControlLibrary().pressButton(Button::X);
      }else if (message_list[2] == 2){
        SwitchControlLibrary().releaseButton(Button::X);
      }
      if (message_list[3] == 1){
        SwitchControlLibrary().pressButton(Button::Y);
      }else if (message_list[3] == 2){
        SwitchControlLibrary().releaseButton(Button::Y);
      }
      // -,HOME,+について
      if (message_list[4] == 1){
        SwitchControlLibrary().pressButton(Button::MINUS);
      }else if (message_list[4] == 2){
        SwitchControlLibrary().releaseButton(Button::MINUS);
      }
      if (message_list[5] == 1){
        SwitchControlLibrary().pressButton(Button::HOME);
      }else if (message_list[5] == 2){
        SwitchControlLibrary().releaseButton(Button::HOME);
      }
      if (message_list[6] == 1){
        SwitchControlLibrary().pressButton(Button::PLUS);
      }else if (message_list[6] == 2){
        SwitchControlLibrary().releaseButton(Button::PLUS);
      }
      // スティックのボタンについて
      // とりあえず必要ないので飛ばすね
      // LRについて
      if (message_list[9] == 1){
        SwitchControlLibrary().pressButton(Button::L);
      }else if (message_list[9] == 2){
        SwitchControlLibrary().releaseButton(Button::L);
      }
      if (message_list[10] == 1){
        SwitchControlLibrary().pressButton(Button::R);
      }else if (message_list[10] == 2){
        SwitchControlLibrary().releaseButton(Button::R);
      }
      // 上下左右ボタンについて
      if (message_list[11] == 1){
        SwitchControlLibrary().pressHatButton(HatButton::UP);
      }else if (message_list[11] == 2){
        SwitchControlLibrary().releaseHatButton(HatButton::UP);
      }
      if (message_list[12] == 1){
        SwitchControlLibrary().pressHatButton(HatButton::DOWN);
      }else if (message_list[12] == 2){
        SwitchControlLibrary().releaseHatButton(HatButton::DOWN);
      }
      if (message_list[13] == 1){
        SwitchControlLibrary().pressHatButton(HatButton::LEFT);
      }else if (message_list[13] == 2){
        SwitchControlLibrary().releaseHatButton(HatButton::LEFT);
      }
      if (message_list[14] == 1){
        SwitchControlLibrary().pressHatButton(HatButton::RIGHT);
      }else if (message_list[14] == 2){
        SwitchControlLibrary().releaseHatButton(HatButton::RIGHT);
      }
      // CAPTUREボタンについて
      if (message_list[15] == 1){
        SwitchControlLibrary().pressButton(Button::CAPTURE);
      }else if (message_list[15] == 2){
        SwitchControlLibrary().releaseButton(Button::CAPTURE);
      }
      // ZLRについて
      if (message_list[20] == 1){
        SwitchControlLibrary().pressButton(Button::ZL);
      }else if (message_list[20] == 2){
        SwitchControlLibrary().releaseButton(Button::ZL);
      }
      if (message_list[21] == 1){
        SwitchControlLibrary().pressButton(Button::ZR);
      }else if (message_list[21] == 2){
        SwitchControlLibrary().releaseButton(Button::ZR);
      }
      // スティックについて
      SwitchControlLibrary().moveLeftStick(message_list[16], message_list[17]);
      SwitchControlLibrary().moveRightStick(message_list[18], message_list[19]);
      
      // Switchに送信
      SwitchControlLibrary().sendReport();

      // 受信メッセージをリセット
      received_message = ""; 
    } else {
      received_message += received_char;
    }
  }
}