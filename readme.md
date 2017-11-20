# read
lianjia 使用协程 对链家数据的一个获取  
danmu 使用协程 获取大量弹幕信息。

要理解为什么这种方式最快

第一，先理清 同步 异步 阻塞 非阻塞这四个基本概念 
[同步 异步 阻塞 非阻塞](https://www.yunxcloud.cn/post/124)  

第二，理清进程 线程 协程的本质，理解什么时候该用什么
[理解 协程 线程 进程](https://www.yunxcloud.cn/post/138)

第三，理解IO复用
[io复用](https://www.yunxcloud.cn/post/138)

第四，理解python中的GIL
[GIL 理解](https://www.yunxcloud.cn/post/136)


lianjia的api接口  使用基于flask 的 eve 能够很方便的将mongodb的
数据转化为一个restful接口，
这里简单演示一下。  
 
Mongodb --> Eve --> Restful  

Eve 这里将很多重复操作抽象起来了，不用手动进行格式转化等重复性强的操作。
