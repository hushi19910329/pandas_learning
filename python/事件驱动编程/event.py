# encoding: UTF-8

# 系统模块
from Queue import Queue, Empty
from threading import Thread

# 第三方模块
from PyQt4.QtCore import QTimer

# 自己开发的模块
from eventType import *


########################################################################
class EventEngine:
    """
    事件驱动引擎
    事件驱动引擎中所有的变量都设置为了私有，这是为了防止不小心
    从外部修改了这些变量的值或状态，导致bug。

    变量说明
    __queue：私有变量，事件队列
    __active：私有变量，事件引擎开关
    __thread：私有变量，事件处理线程
    __timer：私有变量，计时器
    __handlers：私有变量，事件处理函数字典


    方法说明
    __run: 私有方法，事件处理线程连续运行用
    __process: 私有方法，处理事件，调用注册在引擎中的监听函数
    __onTimer：私有方法，计时器固定事件间隔触发后，向事件队列中存入计时器事件
    start: 公共方法，启动引擎
    stop：公共方法，停止引擎
    register：公共方法，向引擎中注册监听函数
    unregister：公共方法，向引擎中注销监听函数
    put：公共方法，向事件队列中存入新的事件

    事件监听函数必须定义为输入参数仅为一个event对象，即：

    函数
    def func(event)
        ...

    对象方法
    def method(self, event)
        ...

    """
    #----------------------------------------------------------------------
    def __init__(self):
        """初始化事件引擎"""
        # 事件队列
        self.__queue = Queue()

        # 事件引擎开关
        self.__active = False

        # 事件处理线程
        self.__thread = Thread(target = self.__run)

        # 计时器，用于触发计时器事件
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__onTimer)

        # 这里的__handlers是一个字典，用来保存对应的事件调用关系
        # 其中每个键对应的值是一个列表，列表中保存了对该事件进行监听的函数功能
        self.__handlers = {}


    #----------------------------------------------------------------------
    def __init__(self):
        """初始化事件引擎"""
        # 初始化的时候，代码也是按顺序执行的
        self.__queue = Queue()# 事件队列
        self.__active = False  # 事件引擎开关
        self.__thread = Thread(target = self.__run)# 事件处理线程
        self.__timer = QTimer()# 计时器，用于触发计时器事件
        self.__timer.timeout.connect(self.__onTimer)
        # 这里的__handlers是一个字典，用来保存对应的事件调用关系
        # 其中每个键对应的值是一个列表，列表中保存了对该事件进行监听的函数功能
        self.__handlers = {}
    #----------------------------------------------------------------------
    def __run(self):
        """引擎运行"""
        while self.__active == True:


          # 先尝试获取事件，若没有事件就抛出empty错误，然后就pass掉！

            try:
                event = self.__queue.get(block = True, timeout = 1)  # 获取事件的阻塞时间设为1秒
                self.__process(event)
            except Empty:
                pass

    #----------------------------------------------------------------------
    def __process(self, event):
        """处理事件"""
        # 检查是否存在对该事件进行监听的处理函数
        if event.type_ in self.__handlers:
            # 若存在，则按顺序将事件传递给处理函数执行


            # self.__handlers[event.type_]本身按顺序有一个列表，以控制执行顺序
            [handler(event) for handler in self.__handlers[event.type_]]

            # 以上语句为Python列表解析方式的写法，对应的常规循环写法为：
            #for handler in self.__handlers[event.type_]:
                #handler(event)

            # 两种方法并没有什么区别
    #----------------------------------------------------------------------
    def __onTimer(self):
        """向事件队列中存入计时器事件"""
        # 创建计时器事件
        event = Event(type_=EVENT_TIMER)

        # 向队列中存入计时器事件
        self.put(event)

        event = Event(type_=EVENT_TIMER)# 创建计时器事件
        self.put(event)# 向队列中存入计时器事件


    #----------------------------------------------------------------------
    def start(self):
        """引擎启动"""
        # 将引擎设为启动
        self.__active = True

        # 启动事件处理线程
        self.__thread.start()

        # 启动事件处理线程
        self.__thread.start()
        # 启动计时器，计时器事件间隔默认设定为1秒
        self.__timer.start(1000)

    #----------------------------------------------------------------------
    def stop(self):
        """停止引擎"""
        # 将引擎设为停止
        self.__active = False

        # 停止计时器
        self.__timer.stop()

        # 等待事件处理线程退出
        self.__thread.join()

    #----------------------------------------------------------------------
    def register(self, type_, handler):
        """注册事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无则创建
        try:
            handlerList = self.__handlers[type_]
        except KeyError:
            handlerList = []
            self.__handlers[type_] = handlerList

        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        # 先创建一个空列表如上，若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handlerList:
            handlerList.append(handler)

    #----------------------------------------------------------------------
    def unregister(self, type_, handler):
        """注销事件处理函数监听"""
        # 尝试获取该事件类型对应的处理函数列表，若无则忽略该次注销请求
        try:
            handlerList = self.handlers[type_]

            # 如果该函数存在于列表中，则移除
            if handler in handlerList:
                handlerList.remove(handler)

            # 如果该函数存在于列表中，则移除
            if handler in handlerList:
                handlerList.remove(handler)

            # 如果函数列表为空，则从引擎中移除该事件类型
            if not handlerList:
                del self.handlers[type_]
        except KeyError:
            pass

    #----------------------------------------------------------------------
    def put(self, event):
        """向事件队列中存入事件"""
        self.__queue.put(event)
