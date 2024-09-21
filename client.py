import argparse
import socket

import playsound
from tool import record_audio

record_file = "temp_record.wav"
play_file = "temp_play.wav"

def main(ip, port):
    while True:
        # 记录并发送语音
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((ip, port))

        playsound.playsound('tone.mp3')
        record_audio(record_file)

        with open(record_file, 'rb') as f:
            conn.sendall(f.read())
        conn.close()
        print('Send voice data successfully.')

        # 接收并播放语音
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((ip, port))
        with open(play_file, 'wb') as f:
            while (data := conn.recv(1024)) != b'':
                f.write(data)
        conn.close()
        print('Receive voice data successfully.')

        playsound.playsound(play_file)

if __name__ == '__main__':
    paser = argparse.ArgumentParser()
    paser.add_argument('--ip', type=str, default='127.0.0.1', help='IP address of the server')
    paser.add_argument('--port', type=int, default=5000, help='Port number of the server')

    args = paser.parse_args()

    main(args.ip, args.port)