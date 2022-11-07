#!/bin/bash

PYSTRING="$(find . | grep -E "(__pycache__|\.pyc|\.pyo$)")"
IPYNBSTRING="$(find . | grep -E "(ipynb_checkpoints|\.ipynb$)")"
DBSTORESTRING="$(find . | grep -E "(DS_Store|\.DS_Store$)")"

# 删除 __pycache__ 缓存文件
if [ -n "$PYSTRING" ]; then
  echo "删除以下缓存文件 :"
  echo "-----------------------------------------------------"
  echo "$PYSTRING"
  echo "-----------------------------------------------------"
  find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
else
  echo "不存在 __pycache__ 缓存文件"
fi

# 删除 ipynb_checkpoints 缓存文件
if [ -n "$IPYNBSTRING" ]; then
  echo "删除以下缓存文件 :"
  echo "-----------------------------------------------------"
  echo "$IPYNBSTRING"
  echo "-----------------------------------------------------"
  find . | grep -E "(ipynb_checkpoints|\.ipynb$)" | xargs rm -rf
else
  echo "不存在 ipynb_checkpoints 缓存文件"
fi

# 删除 DS_Store 缓存文件
if [ -n "$DBSTORESTRING" ]; then
  echo "删除以下缓存文件 :"
  echo "-----------------------------------------------------"
  echo "$DBSTORESTRING"
  echo "-----------------------------------------------------"
  find . | grep -E "(DS_Store|\.DS_Store$)" | xargs rm -rf
else
  echo "不存在 DS_Store 缓存文件"
fi