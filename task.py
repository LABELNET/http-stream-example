


from threading import  Thread

import time

class  Task():

    def __init__(self,task):
        # 任务
        self.task = task
        # 状态
        self.is_start = False
        # 进度
        self.proecess = ""

    def start(self):
        """
        异步执行：启动线程
        """
        if self.is_start:
            return
        self.is_start = True
        # 异步执行
        local = Thread(target=self.__execute)
        local.setDaemon(True)
        local.start()

    def __execute(self):
        # 启动
        a = 1
        print(f"{self.task} - start!")
        # 异步执行的操作在这里实现
        # 例子为，每 2s 输出进度
        while self.is_start:
            a+=1
            self.proecess = f"{self.task}-{(a/10)*100}%"
            time.sleep(2)
        # 结束
        print(f"{self.task} stop!")

    def get_stream(task_id):
        """
        同步返回：返回执行中间结果
        """
        try:
            t = Task(task_id)
            # 异步执行
            t.start()
            # 同步等待结果，返回执行进度
            while True:
                yield t.proecess
                time.sleep(2)
        except Exception as e:
            print(e)
        finally:
            t.stop()
            print("finish")
        
    def stop(self):
        self.is_start = False