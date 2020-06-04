#!/usr/bin/python3
#coding=utf-8

import os
import sys
import subprocess
import re
import time

tokent_master_tmp = subprocess.getstatusoutput("kubeadm token create --print-join-command")
tokent_master = tokent_master_tmp[1]
print(tokent_master)
