
'''

对celery最核心的封装

@classmethod
def clstasks(cls, **kwargs):
    return cls.app.task(bind=True, **kwargs)

@classmethod
def ptask(cls, **kwargs):
    @cls.clstasks(**kwargs)
    def _instance(**kwargs):
        cls(**kwargs).start()
    return _instance

'''

为什么这样做？

简单说明下原有的做法

tasks.py
app = Celery()

@app.task(bind=True, **kwargs)
def test():
    return xx

用一个py文件，所有的任务都在这里绑定到celery。这样做的时候集成就必须 去这个文件里，加上自己的sdk绑定，
这种方式增加了复杂度，还有一点蛋疼的事情是 @app.task(bind=True, **kwargs) 中的参数变更需要重新提交代码
重新启动服务。

而新方式会把celery的绑定封装在框架内部，参数也可以进行配置化，并提供接口很简单的进行修改
