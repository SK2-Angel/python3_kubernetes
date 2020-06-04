#!/usr/bin/python3
#coding=utf-8

import os
import sys
import subprocess
import re
import time


def init_system():
    try:
        hostname_k8s = subprocess.getstatusoutput('hostnamectl set-hostname k8s-node2 && echo "127.0.0.1   $(hostname)" >> /etc/hosts')
        install_kuberadm = subprocess.getstatusoutput("sh /tmp/install-kubelet.sh")
        regis = '{"registry-mirrors": ["https://uyah70su.mirror.aliyuncs.com"],"insecure-registries":["harbor.runxsports.cn"]}'
        deamin_file = open("/etc/docker/daemon.json","w")
        deamin_file.writelines(regis)
        deamin_file.close()
        restart_docker = subprocess.getstatusoutput("systemctl restart docker && systemctl enable docker")
        docker_info = subprocess.getstatusoutput("docker info")
        if  'uyah70su.mirror.aliyuncs.com' in str(docker_info):
            collock_data = 'success'
        else:
            collock_data = 'error'
        return collock_data
    except:
        collock_data = 'python3_bad'
        return collock_data

def install_k8s_node2():
    try:
        master_ip_tmp = subprocess.getstatusoutput("cat /tmp/master_token | awk -F, '{print $1}'")
        master_ip = master_ip_tmp[1]
        master_token_tmp = subprocess.getstatusoutput("cat /tmp/master_token | awk -F, '{print $2}'")
        master_token = master_token_tmp[1]
        docker_status = []
        install_master = subprocess.getstatusoutput('echo "{0}   apiserver.demo " >> /etc/hosts &&  {1} '.format(master_ip,master_token))
        return_data = 'success'
        return return_data
    except Exception as e:
        return_data = 'python3_bad'
        return return_data
def main():
    install_docker = init_system()
    install_k8s = install_k8s_node2()
    if install_docker == 'success' and install_k8s == 'success':
        print('success')
    else:
        print('error')



if __name__ == "__main__":
    main()


