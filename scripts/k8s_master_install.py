#!/usr/bin/python3
#coding=utf-8

import os
import sys
import subprocess
import re
import time


def init_system():
    try:
        collock_data = {}
        hostname_k8s = subprocess.getstatusoutput('hostnamectl set-hostname k8s-master && echo "127.0.0.1   $(hostname)" >> /etc/hosts')
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
        collock_data = 'error'
        return collock_data

def install_k8s_master():
    try:
        collock_data = {}
        master_ip_tmp = subprocess.getstatusoutput("hostname -I | awk '{print $1}'")
        master_ip = master_ip_tmp[1]
        docker_status = []
        install_master = subprocess.getstatusoutput('export MASTER_IP={0} && export APISERVER_NAME=apiserver.demo && export POD_SUBNET=10.100.0.1/20 && echo "{1}    apiserver.demo " >> /etc/hosts && sh /tmp/init-master.sh '.format(master_ip,master_ip))
        i=0
        while (i<20):
            time.sleep(30)
            dock_all = os.popen("kubectl get pod -n kube-system -o wide | grep -v 'NAME'")
            while(True):
                dock_tme = dock_all.readline()
                if dock_tme != '':
                    if 'Running' in dock_tme.split():
                        continue
                    else:
                        docker_status.append('bad')
                else:
                    if 'bad' in docker_status:
                        docker_status.clear()
                        broker_status = False
                        break
                    else:
                        broker_status = True
                        break
                        time.sleep(10)
            if broker_status:
                collock_data["install_master_k8s"] = 'success'
                break
            i = i + 1
        if 'success' in str(collock_data):
            return_data = 'success'
            return return_data
        else:
            return_data = 'error'
            return return_data
    except Exception as e:
        return_data = 'python3_bad'
        return return_data


def main():
    install_docker = init_system()
    install_k8s = install_k8s_master()
    if install_docker == 'success' and install_k8s == 'success':
        print('success')
    else:
        print('error')



if __name__ == "__main__":
    main()


