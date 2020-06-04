yum install wget vim net-tools  -y  > /dev/null  2>&1 
yum install python3 ansible -y > /dev/null 2>&1
systemctl disable firewalld
systemctl stop firewalld
setenforce 0
sed -i 's/SELINUX=permissive/SELINUX=disabled/' /etc/sysconfig/selinux
sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
sed -i 's/#host_key_checking = False/host_key_checking = False/' /etc/ansible/ansible.cfg
swapoff -a
sed -i 's/.*swap.*/#&/' /etc/fstab
mkdir ~/.pip
cat >> ~/.pip/pip.conf << EOF
[global]
index-url = https://mirrors.aliyun.com/pypi/simple
EOF
pip3 install ansible==2.7.8 tqdm PrettyTable >/dev/null 2>&1
iptables -F 
echo "* soft nofile 655350" >> /etc/security/limits.conf
echo "* hard nofile 655350" >> /etc/security/limits.conf
echo "初始化完成!"


