from flask import Flask, Response
import cv2

app = Flask(__name__)


def stream():  
    try:
        print("camera start")
        camera = cv2.VideoCapture('rtsp://admin:q1w2e3r4@192.168.50.23/Streaming/Channels/101')  
        while True:
            success, frame = camera.read()  
            if not success:
                break
            else:
                # concat frame
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
    except Exception as e:
        print(e)
    finally:
        print("camera stop")
        camera.release()

@app.route('/video')
def example():
    # return frame
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    """
    访问：http://127.0.0.1:5000/video
    """
    app.run(debug=True)