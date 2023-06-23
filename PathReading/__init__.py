import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests


# 创建一个处理文件事件的类，继承自FileSystemEventHandler
class FileHandler(FileSystemEventHandler):
    # 当有新的文件被创建时，这个方法会被调用
    def on_created(self, event):
        # 检查新的文件是否是.gcode文件
        if event.src_path.endswith(".gcode"):
        # if event.src_path.endswith(".txt"):
            print(f"New file detected: {event.src_path}")
            # 如果是.gcode文件，调用write_file_path方法写入文件路径
            self.write_file_path(event.src_path)

'''
    # 将文件路径写入到一个文本文件中
    def write_file_path(self, file_path):
        with open("E:\PhD\Project\Remote_print\File_paths.txt", "a") as f:
            f.write(file_path + "\n")
'''


    # 上传文件到OctoPrint服务器
    def upload_file(self, file_path):
        # 你的OctoPrint API密钥
        api_key = "your_api_key"
        # 创建请求的头部，包含API密钥
        headers = {"X-Api-Key": api_key}
        # 读取文件的内容
        data = open(file_path, "rb").read()

        # 发送POST请求到OctoPrint服务器，上传文件
        response = requests.post("http://your_octoprint_server/api/files/local", headers=headers, files={"file": data})

        # 检查请求的结果
        if response.status_code == 201:
            print("File uploaded successfully")
        else:
            print("Error:", response.status_code)


if __name__ == "__main__":
    # 创建一个Observer对象来监控文件系统的事件
    observer = Observer()
    # 配置Observer对象，让它使用FileHandler对象来处理事件，监控指定的文件夹
    observer.schedule(FileHandler(), path="E:\PhD\Project\Remote_print\Test")
    # 开始监控
    observer.start()



    try:
        # 让主线程持续运行，直到用户按下Ctrl+C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # 用户按下Ctrl+C时，停止监控
        observer.stop()

    # 等待监控线程结束
    observer.join()
