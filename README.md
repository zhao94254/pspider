### pspider
---
开发环境 Python 3.7.1

**spider目录下**
一个简单的爬虫框架

**app**
celery要用到这个，放celery的各种配置，以及对celery的封装

[核心封装&说明](https://github.com/zhao94254/pspider/blob/master/app/read.md)

**sdks**
放集成进平台的爬虫sdk


爬虫任务一般也会分为两种
* 流式任务 - 要实时请求的
* 批任务 - 批量累积的

对于实时的任务，对延时、机器可靠性要求也就更高
批任务的话尽量优化执行性能即可

提供接口将结果进行统一管理
任务并发依靠框架，用的时候只需配置即可

