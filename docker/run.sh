#!/bin/bash

docker run -d -it -p 8084:8084 -v /data/lpzhang/wuyi/:/root/model --name model_fengqiao_local_v0 itlubber/model:v0 python main.py