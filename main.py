#!/usr/bin/python3
#coding=utf-8

import os
import sys
import subprocess
import re
from tqdm import tqdm
import string
import time
import json
from prettytable import PrettyTable
from multiprocessing import Process
import multiprocessing


def ipv4_addr_check(ipAddr):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ipAddr):
        return True
    else:
        return False
def source_master(master_check,num):
    try:
        check_main = master_check
        ansible_url = os.popen('which ansible')
        ansible_temp = ansible_url.read()
        ansible = ansible_temp.split()[0]
        if check_main == 'success':
            collok_host = subprocess.getstatusoutput(" {0} -i /opt/k8s-admin/scripts/master_hosts all -m 'shell' -a 'yum -y install python3' ".format(ansible))
            install_k8s_master = subprocess.getstatusoutput('python3 /opt/k8s-admin/scripts/k8s_master_asnible.py')
            file_master = open('/opt/k8s-admin/scripts/master_hosts', 'r')
            master_ip_data = file_master.readline()
            file_master.close()
            master_file_ip = master_ip_data.split()[0]
            install_return = json.loads(install_k8s_master[1]).get(master_file_ip).get('stdout')
            if install_return == 'success':
                master_token_tmp = subprocess.getstatusoutput('python3 /opt/k8s-admin/scripts/master_token_ansible.py')
                master_token = json.loads(master_token_tmp[1]).get(master_file_ip).get('stdout')
                token_data = master_file_ip + ',' + ' ' + master_token
                file_token = open('/opt/k8s-admin/scripts/master_token', 'w')
                file_token.writelines(token_data)
                file_token.close()
                num.value=20.0
                return_data = 'success'
                return return_data
            else:
                uninstall_kubeadm = subprocess.getstatusoutput(" {0} -i /opt/k8s-admin/scripts/master_hosts all -m 'shell' -a 'kubeadm reset -f ' ".format(ansible))
                print('\033[1;31m kubernetes-master安装失败,请再次执行脚本,重新安装 \033[0m')
        else:
            pass
    except:
         print('\033[1;31m 程序出现意外情况,已停止运行!!! \033[0m')

def system_info():
    try:
        system_table = PrettyTable(["hostname", "ip", "system_os", "cpu", "mem", "python3_kubernetesVS"])
        hostname = subprocess.getstatusoutput("hostname")[1]
        ip = subprocess.getstatusoutput("hostname -I | awk '{print $1}'")[1]
        system_os = subprocess.getstatusoutput("cat /etc/redhat-release")[1]
        cpu = subprocess.getstatusoutput("cat /proc/cpuinfo | grep 'physical id' | sort | uniq | wc -l")[1]
        mem_temp = subprocess.getstatusoutput("cat /proc/meminfo | grep MemTotal | awk '{print $2}'")[1]
        mem = str(int(((int(mem_temp) / 1024) / 1024))) + ' ' + 'GB'
        python3_Version = 'V1.1'
        system_table.add_row([hostname,ip,system_os,cpu,mem,python3_Version])
        print("\033[1;35m            >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>当前服务器资源<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  \033[0m")
        print(system_table)
    except:
        pass
def show_k8s():
    try:
        system_table = PrettyTable(["NAME", "STATUS", "ROLES", "AGE", "VERSION", "INTERNAL-IP","EXTERNAL-IP","OS-IMAGE","KERNEL-VERSION","CONTAINER-RUNTIME"])
        show_k8s_asnible = subprocess.getstatusoutput(" ansible -i /opt/k8s-admin/scripts/master_hosts all -m 'shell' -a ' kubectl get nodes -o wide' ")
        k8s_temp_data = show_k8s_asnible[1].split()
        k8s_master_index = k8s_temp_data.index('k8s-master')
        k8s_node1_index = k8s_temp_data.index('k8s-node1')
        k8s_node2_index = k8s_temp_data.index('k8s-node2')
        system_table.add_row([k8s_temp_data[k8s_master_index], k8s_temp_data[k8s_master_index + 1], k8s_temp_data[k8s_master_index + 2], k8s_temp_data[k8s_master_index + 3], k8s_temp_data[k8s_master_index + 4],k8s_temp_data[k8s_master_index + 5], k8s_temp_data[k8s_master_index + 6], "Linux", k8s_temp_data[k8s_master_index + 11], k8s_temp_data[k8s_master_index + 12]])
        system_table.add_row(
            [k8s_temp_data[k8s_node1_index], k8s_temp_data[k8s_node1_index + 1], k8s_temp_data[k8s_node1_index + 2],
             k8s_temp_data[k8s_node1_index + 3], k8s_temp_data[k8s_node1_index + 4], k8s_temp_data[k8s_node1_index + 5],
             k8s_temp_data[k8s_node1_index + 6], "Linux", k8s_temp_data[k8s_node1_index + 11],
             k8s_temp_data[k8s_node1_index + 12]])
        system_table.add_row(
            [k8s_temp_data[k8s_node2_index], k8s_temp_data[k8s_node2_index + 1], k8s_temp_data[k8s_node2_index + 2],
             k8s_temp_data[k8s_node2_index + 3], k8s_temp_data[k8s_node2_index + 4], k8s_temp_data[k8s_node2_index + 5],
             k8s_temp_data[k8s_node2_index + 6], "Linux", k8s_temp_data[k8s_node2_index + 11],
             k8s_temp_data[k8s_node2_index + 12]])
        print(system_table)
    except:
        system_table.add_row(
            ["Null", "Null", "Null","Null", "Null", "Null","Null", "Null", "Null","Null"])
        print(system_table)

def install_master():
    while (True):
        input_master_ip = input('请输入kubernetes-master的ip地址:    ')
        if ipv4_addr_check(input_master_ip):
            master_ip = input_master_ip
            input_master_password = input('请输入kubernetes-master的root用户密码:    ')
            ansible_host = master_ip + ' ' + 'ansible_ssh_user=root' + ' ' + 'ansible_ssh_port=22' + ' ' + 'ansible_ssh_pass=' + input_master_password
            master_hosts = open("/opt/k8s-admin/scripts/master_hosts", "w")
            master_hosts.writelines(ansible_host)
            master_hosts.close()
            ansible_url = os.popen('which ansible')
            ansible_temp = ansible_url.read()
            ansible = ansible_temp.split()[0]
            collok_host = subprocess.getstatusoutput(
                " {0} -i /opt/k8s-admin/scripts/master_hosts all -m 'shell' -a 'date' ".format(ansible))
            coll_host_split = collok_host[1].split()
            if coll_host_split[-1] == '2020':
                print("\033[1;32m kubernetes-master可以正常通讯,即将安装相关组件!! \033[0m")
                check_main = 'success'
                break
            else:
                print("\033[1;33m 无法与kubernetes-master建立通讯,请重新输入相关信息!!! \033[0m")
                print('\033[1;34m >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  \033[0m')
        else:
            print("\033[1;33m 请输入合法的ipv4地址!!! \033[0m")

    with tqdm(total=100) as pbar:
        num = multiprocessing.Value("d", 10.0)
        install_master_func = Process(target=source_master,args=('success',num))
        install_master_func.start()
        for i in range(50):
            if not install_master_func.is_alive():
                time.sleep(0.01)
            else:
                time.sleep(15)
            pbar.update(2)
    if num.value == 20.0:
        print("\033[1;32m kubernetes-master安装成功,接下来安装node1节点!!! \033[0m")
        print('\033[1;34m >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  \033[0m')
        return_data = 'success'
    else:
        return_data = 'error'
    return return_data


def source_node1(node1_check,num):
    try:
        check_main = node1_check
        ansible_url = os.popen('which ansible')
        ansible_temp = ansible_url.read()
        ansible = ansible_temp.split()[0]
        if check_main == 'success':
            j = 1
            while (j < 3):
                collok_host = subprocess.getstatusoutput(" {0} -i /opt/k8s-admin/scripts/node1_hosts all -m 'shell' -a 'yum -y install python3' ".format(ansible))
                install_k8s_node1 = subprocess.getstatusoutput('python3 /opt/k8s-admin/scripts/k8s_node1_asnible.py')
                file_node1 = open('/opt/k8s-admin/scripts/node1_hosts', 'r')
                node1_ip_data = file_node1.readline()
                file_node1.close()
                node1_ip = node1_ip_data.split()[0]
                install_return = json.loads(install_k8s_node1[1]).get(node1_ip).get('stdout')
                if install_return == 'success':
                    i = 1
                    node1_status = 'status'
                    while (i < 10):
                        show_status = subprocess.getstatusoutput(" {0} -i /opt/k8s-admin/scripts/master_hosts all -m 'shell' -a 'kubectl get nodes' ".format(ansible))
                        temp_stataus = show_status[1].split().count('Ready')
                        if temp_stataus == 2:
                            node1_status = 'success'
                            break
                        time.sleep(7)
                        i += 1
                    if node1_status == 'success':
                        num.value = 20.0
                        return_data = 'success'
                        return return_data
                        break
                    else:
                        uninstall_kubeadm = subprocess.getstatusoutput(" {0} -i /opt/k8s-admin/scripts/node1_hosts all -m 'shell' -a 'kubeadm reset -f ' ".format(ansible))
                        print('\033[1;31m kubernetes-node1安装失败,正在自动清除,并重新尝试安装 \033[0m')
                else:
                    uninstall_kubeadm = subprocess.getstatusoutput(" {0} -i /opt/k8s-admin/scripts/node1_hosts all -m 'shell' -a 'kubeadm reset -f ' ".format(ansible))
                    print('\033[1;31m kubernetes-node1安装失败,正在自动清除,并重新尝试安装 \033[0m')
                j += 1
        else:
            pass
    except:
        print('\033[1;31m 程序出现意外情况,已停止运行,请手动关闭卸载,并重新尝试安装!!! \033[0m')

def install_node1():
    try:
        while (True):
            input_node1_ip = input('请输入kubernetes-node1的ip地址:    ')
            if ipv4_addr_check(input_node1_ip):
                node1_ip = input_node1_ip
                input_node1_password = input('请输入kubernetes-node1的root用户密码:    ')
                ansible_host = node1_ip + ' ' + 'ansible_ssh_user=root' + ' ' + 'ansible_ssh_port=22' + ' ' + 'ansible_ssh_pass=' + input_node1_password
                node1_hosts = open("/opt/k8s-admin/scripts/node1_hosts", "w")
                node1_hosts.writelines(ansible_host)
                node1_hosts.close()
                ansible_url = os.popen('which ansible')
                ansible_temp = ansible_url.read()
                ansible = ansible_temp.split()[0]
                collok_host = subprocess.getstatusoutput(" {0} -i /opt/k8s-admin/scripts/node1_hosts all -m 'shell' -a 'date' ".format(ansible))
                coll_host_split = collok_host[1].split()
                if coll_host_split[-1] == '2020':
                    print("\033[1;32m kubernetes-node1可以正常通讯,即将安装相关组件!! \033[0m")
                    check_main = 'success'
                    break
                else:
                    print("\033[1;33m 无法与kubernetes-node1建立通讯，请重新输入相关信息!!! \033[0m")
                    print('\033[1;34m >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  \033[0m')
            else:
                print("\033[1;33m 请输入合法的ipv4地址!!! \033[0m")
        with tqdm(total=100) as pbar:
            num = multiprocessing.Value("d", 10.0)
            install_source_func = Process(target=source_node1, args=('success',num))
            install_node1_return = install_source_func.start()
            for i in range(50):
                if not install_source_func.is_alive():
                    time.sleep(0.01)
                else:
                    time.sleep(15)
                pbar.update(2)
        if num.value == 20.0:
            print("\033[1;32m kubernetes-node1安装成功,接下来安装node2节点!!! \033[0m")
            print('\033[1;34m >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  \033[0m')
            return_data = 'success'
        else:
            return_data = 'error'
        return return_data
    except:
        print('\033[1;31m 程序被强制中断!!!!!!!! \033[0m')



def source_node2(node2_check,num):
    try:
        check_main = node2_check
        ansible_url = os.popen('which ansible')
        ansible_temp = ansible_url.read()
        ansible = ansible_temp.split()[0]
        if check_main == 'success':
            j = 1
            while (j < 3):
                collok_host = subprocess.getstatusoutput(
                    " {0} -i /opt/k8s-admin/scripts/node2_hosts all -m 'shell' -a 'yum -y install python3' ".format(
                        ansible))
                install_k8s_node2 = subprocess.getstatusoutput('python3 /opt/k8s-admin/scripts/k8s_node2_asnible.py')
                file_node2 = open('/opt/k8s-admin/scripts/node2_hosts', 'r')
                node2_ip_data = file_node2.readline()
                file_node2.close()
                node2_ip = node2_ip_data.split()[0]
                install_return = json.loads(install_k8s_node2[1]).get(node2_ip).get('stdout')
                if install_return == 'success':
                    i = 1
                    node2_status = 'status'
                    while (i < 10):
                        show_status = subprocess.getstatusoutput(
                            " {0} -i /opt/k8s-admin/scripts/master_hosts all -m 'shell' -a 'kubectl get nodes' ".format(
                                ansible))
                        temp_stataus = show_status[1].split().count('Ready')
                        if temp_stataus == 3:
                            node2_status = 'success'
                            break
                        time.sleep(7)
                        i += 1
                    if node2_status == 'success':
                        num.value = 20.0
                        return_data = 'success'
                        return return_data
                        break
                    else:
                        uninstall_kubeadm = subprocess.getstatusoutput(
                            " {0} -i /opt/k8s-admin/scripts/node2_hosts all -m 'shell' -a 'kubeadm reset -f ' ".format(
                                ansible))
                        print('\033[1;31m kubernetes-node2安装失败,正在自动清除,并重新尝试安装 \033[0m')
                else:
                    uninstall_kubeadm = subprocess.getstatusoutput(
                        " {0} -i /opt/k8s-admin/scripts/node2_hosts all -m 'shell' -a 'kubeadm reset -f ' ".format(
                            ansible))
                    print('\033[1;31m kubernetes-node2安装失败,正在自动清除,并重新尝试安装 \033[0m')
                j += 1
        else:
            pass
    except:
        print('\033[1;31m 程序出现意外情况,已停止运行,请手动关闭卸载,并重新尝试安装!!! \033[0m')
def install_node2():
    try:
        while (True):
            input_node2_ip = input('请输入kubernetes-node2的ip地址:    ')
            if ipv4_addr_check(input_node2_ip):
                node2_ip = input_node2_ip
                input_node2_password = input('请输入kubernetes-node2的root用户密码:    ')
                ansible_host = node2_ip + ' ' + 'ansible_ssh_user=root' + ' ' + 'ansible_ssh_port=22' + ' ' + 'ansible_ssh_pass=' + input_node2_password
                node2_hosts = open("/opt/k8s-admin/scripts/node2_hosts", "w")
                node2_hosts.writelines(ansible_host)
                node2_hosts.close()
                ansible_url = os.popen('which ansible')
                ansible_temp = ansible_url.read()
                ansible = ansible_temp.split()[0]
                collok_host = subprocess.getstatusoutput(" {0} -i /opt/k8s-admin/scripts/node2_hosts all -m 'shell' -a 'date' ".format(ansible))
                coll_host_split = collok_host[1].split()
                if coll_host_split[-1] == '2020':
                    print("\033[1;32m kubernetes-node2可以正常通讯,即将安装相关组件!! \033[0m")
                    check_main = 'success'
                    break
                else:
                    print("\033[1;33m 无法与kubernetes-node1建立通讯，请重新输入相关信息!!! \033[0m")
                    print('\033[1;34m >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  \033[0m')
            else:
                print("\033[1;33m 请输入合法的ipv4地址!!! \033[0m")
        with tqdm(total=100) as pbar:
            num = multiprocessing.Value("d", 10.0)
            install_source_func = Process(target=source_node2, args=('success',num))
            install_node2_return = install_source_func.start()
            for i in range(50):
                if not install_source_func.is_alive():
                    time.sleep(0.01)
                else:
                    time.sleep(15)
                pbar.update(2)
        if num.value == 20.0:
            print("\033[1;32m kubernetes-node2安装成功,正在检查集群状态!!!!! \033[0m")
            print('\033[1;34m >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  \033[0m')
            return_data = 'success'
        else:
            return_data = 'error'
        return return_data
    except KeyboardInterrupt:
        print('\033[1;31m 程序被强制中断!!!!!!!! \033[0m')

def main():
    try:
        system_info()
        while(True):
            try:
                print("\033[1;36m >>>>>>>>>>>>>>>>>>>>>>>>功能菜单<<<<<<<<<<<<<<<<<<<<<<<<<<< \033[0m")
                print('\n'*2)
                print(" 1.install_kubernetes ")
                print(" 2.unstall_kubernetes")
                print(" 3.show_kubernetes ")
                print(" 4.quit ")
                print('\n')
                input_Function = input('请输入执行的选项序号或功能名称:    ')
                print('\n')
                if input_Function == 'install_kubernetes' or input_Function == '1':
                    return_master = install_master()
                    if return_master == 'success':
                        install_node1_return = install_node1()
                        if install_node1_return == 'success':
                            install_node2_return = install_node2()
                            show_k8s()
                elif input_Function == 'unstall_kubernetes' or input_Function == '2':
                    ansible_url = os.popen('which ansible')
                    ansible_temp = ansible_url.read()
                    ansible = ansible_temp.split()[0]
                    uninstall_kubeadm_master = subprocess.getstatusoutput(" {0} -i /opt/k8s-admin/scripts/master_hosts all -m 'shell' -a 'kubeadm reset -f && yum remove -y kubelet kubeadm kubectl ' ".format(ansible))
                    uninstall_kubeadm_node1 = subprocess.getstatusoutput(" {0} -i /opt/k8s-admin/scripts/node1_hosts all -m 'shell' -a 'kubeadm reset -f && yum remove -y kubelet kubeadm kubectl ' ".format(ansible))
                    uninstall_kubeadm_node2 = subprocess.getstatusoutput(" {0} -i /opt/k8s-admin/scripts/node2_hosts all -m 'shell' -a 'kubeadm reset -f && yum remove -y kubelet kubeadm kubectl ' ".format(ansible))
                    rm_hosts = subprocess.getstatusoutput("rm -rf /opt/k8s-admin/scripts/master_hosts  node1_hosts  node2_hosts ")
                    print('\033[1;32m kubernetes集群卸载完成!!!!!! \033[0m')
                elif input_Function == 'show_kubernetes' or input_Function == '3':
                    if os.path.exists('/opt/k8s-admin/scripts/master_hosts') and os.path.exists('/opt/k8s-admin/scripts/node1_hosts') and os.path.exists('/opt/k8s-admin/scripts/node2_hosts'):
                        show_k8s()
                    else:
                        print("\033[1;31m 未找到集群信息,请先安装集群,再执行查看集群状态操作!!!! \033[0m")
                elif input_Function == 'quit' or input_Function == '4':
                    sys.exit(1)
                else:
                    print('\n')
                    print('\033[1;33m 请输入正确的功能按键,如需退出,请输入quit!!! \033[0m')
            except KeyboardInterrupt:
                print('\n')
                print('\033[1;31m 如需退出,请输入quit!!! \033[0m')
    except KeyboardInterrupt:
        print('\n')
        print('\033[1;31m 程序被强制中断!!!!!!!! \033[0m')



if __name__ == "__main__":
    main()
