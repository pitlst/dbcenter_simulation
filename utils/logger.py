import os
import logging
import colorlog

'''获取日志记录器'''
def logger_make(name: str) -> logging.Logger:
    LOG = logging.getLogger(name)
    LOG.setLevel(logging.DEBUG)

    # 设置log日志的标准输出打印
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # 定义颜色输出格式
    color_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s: %(name)s %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        datefmt='## %Y-%m-%d %H:%M:%S'
    )
    console.setFormatter(color_formatter)
    LOG.addHandler(console)
    
    
    # 3、创建文件处理器，指定日志文件和日志级别（局部）---文件输出FileHandle（输出到指定文件）
    dir_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "data")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_handler = logging.FileHandler(os.path.join(dir_path, name + '.log') , mode = "w+")
    file_handler.setLevel(logging.DEBUG) # 设置日志级别(只输出对应级别INFO的日志信息)
    # 设置日志格式
    formatter = logging.Formatter('%(levelname)s: %(name)s %(message)s')
    file_handler.setFormatter(formatter) 
    LOG.addHandler(file_handler)
    return LOG