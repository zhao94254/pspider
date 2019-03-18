FROM daocloud.io/python:3.5-alpine

RUN echo http://mirrors.ustc.edu.cn/alpine/v3.6/main > /etc/apk/repositories; \
echo http://mirrors.ustc.edu.cn/alpine/v3.6/community >> /etc/apk/repositories


RUN apk add --update \
    supervisor

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt .

ADD . .

RUN pip3 install --upgrade pip

RUN pip3 --timeout=60 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
