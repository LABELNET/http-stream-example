from flask import Flask, Response
import cv2
import ffmpeg
import numpy as np

app = Flask(__name__)

def stream():  
    rtsp ='rtsp://admin:q1w2e3r4@192.168.50.23/Streaming/Channels/101'
    try:
        print("\n camera start \n")
        probe = ffmpeg.probe(rtsp)
        cap_info = next(x for x in probe['streams'] if x['codec_type'] == 'video')
        width = cap_info['width']           # 获取视频流的宽度
        height = cap_info['height']         # 获取视频流的高度
        cam_process = (
            ffmpeg
            .input(rtsp,rtsp_transport='tcp')
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .overwrite_output()
            .run_async(pipe_stdout=True)
        )
        while True:
            frame_bytes = cam_process.stdout.read(width * height * 3 )
            if not frame_bytes:
                break
            frame = (
                np
                .frombuffer(frame_bytes, np.uint8)
                .reshape([height, width, 3])
            )
            # 转成BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # concat frame one by one and show result
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
    except Exception as e:
        print(e)
    finally:
        cam_process.kill()
        print("\n camera stop \n")

@app.route('/video')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)