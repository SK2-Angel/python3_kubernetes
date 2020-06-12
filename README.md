Kubernetes集群安装说明
1.服务器资源说明，确保三台服务器的资源大于或等于以下配置，
    4Core 4G  centos7.6+

2.执行过程要求：
(1)执行脚本是必须是root用户
(2)确保三台服务器可以连通公网
(3)确保将脚本解压至/opt目录下

3.执行脚本，安装集群环境
(1)解压脚本并执行初始化操作，安装依赖组件:
“””shell”””
tar -xf  k8s-admin.tar -C /opt  

“””shell”””
cd  /opt/k8s-admin 
sh init.sh

(2)执行python程序,打开交互式控制台:
“””python3”””
python3  /opt/k8s-admin/main.py

功能菜单:




 1.install_kubernetes
 2.unstall_kubernetes
 3.show_kubernetes
 4.quit

功能说明：
install_kubernetes(安装kubernetes集群)
注意：按照要求分别输入三台服务器的ip地址和root用户密码


unstall_kubernetes(卸载kubernetes集群)

show_kubernetes(查看集群运行状态及集群信息)

quit(退出交互式控制台)


