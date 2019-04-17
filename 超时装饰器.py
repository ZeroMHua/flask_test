# coding=utf-8
import signal
import time


def set_timeout(num, callback):
    def wrap(func):
        def handle(signum, frame):  # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
                signal.alarm(num)  # 设置 num 秒的闹钟
                print('start alarm signal.')
                r = func(*args, **kwargs)
                print('close alarm signal.')

                signal.alarm(0)  # 关闭闹钟
                return r
            except RuntimeError as e:
                callback()

        return to_do

    return wrap


if __name__ == '__main__':
    def after_timeout():  # 超时后的处理函数
        print
        "do something after timeout."


    @set_timeout(2, after_timeout)  # 限时 2 秒
    def connect():  # 要执行的函数
        time.sleep(1)  # 函数执行时间，写大于2的值，可测试超时
        return 'connect success.'


    print(connect())