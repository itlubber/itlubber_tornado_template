FROM python:3.6

LABEL author="https://itlubber.art/"
LABEL desc="ITLubber、酱的基础镜像"
LABEL date="2021-07-19"

# 环境变量硬编码及时区
ENV TZ=Asia/Shanghai
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx vim \
    && apt-get install -y locales \
    && locale-gen zh_CN.UTF-8 \
    && apt-get install -y tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && localedef -c -f UTF-8 -i zh_CN zh_CN.utf8 \
    && mkdir -p /root/model/text_extractor/spacy_model \
    && apt-get install -y gcc python3-dev \
    && pip3 install -U setuptools -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com \
    && pip3 install -U pip -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

# 拷贝文件至容器
COPY requirements.txt /root/model

# 安装相应的python包
RUN pip3 install -r /root/model/requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

WORKDIR /root/model

EXPOSE 8080
EXPOSE 8084
EXPOSE 6379
EXPOSE 8867