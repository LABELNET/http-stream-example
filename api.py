import time
from datetime import datetime
from flask import Flask, Response,request
from task import Task

app = Flask(__name__)


def compute(a):
    return f'{(a/10) * 100}%'
 

def stream(task):
    try:
        print(f"{task} - start!")
        a = 1
        while True:
            yield f"{task}-{datetime.now().isoformat()}-{compute(a)}\n"
            a += 1
            time.sleep(2)
            # if a > 10:
            #     break
    except Exception as e:
        print(e)
        e.with_traceback()
    finally:
        print(f"{task} - finish!")

 
@app.route('/data')
def example():
    task = request.args.get("task")
    return Response(Task.get_stream(task), mimetype='text/plain')

if __name__ == '__main__':
   app.run()