#encoding: utf8
import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C
class ResultCallback(CallbackBase):

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        if result.task_name == 'k8s_install_node2':
            returen_data = json.dumps({host.name: result._result}, indent=4)
            print(returen_data)



Options=namedtuple('Options',['connection','module_path','forks','become','become_method','become_user','check','diff'])
options=Options(connection='smart', module_path=[], forks=10, become=None,
                                become_method=None, become_user=None, check=False, diff=False)
loader = DataLoader()
passwords = {}


results_callback = ResultCallback()


inventory = InventoryManager(loader=loader, sources='/opt/k8s-admin/scripts/node2_hosts')


variable_manager = VariableManager(loader=loader, inventory=inventory)


play_source = {
            'name': "k8s_install_node2_all",
            'hosts': "all",
            'gather_facts': 'no',
            'tasks': [
                {
                    'name': 'copyfile',
                    'copy': 'src={0} dest={1}'.format('/opt/k8s-admin/scripts/install-kubelet.sh',
                                                      '/tmp/install-kubelet.sh')

                },
                {
                    'name': 'copyfile',
                    'copy': 'src={0} dest={1}'.format('/opt/k8s-admin/scripts/master_token',
                                                      '/tmp/master_token')

                },
                {
                    'name': 'copyfile',
                    'copy': 'src={0} dest={1}'.format('/opt/k8s-admin/scripts/k8s_node2_install.py',
                                                      '/tmp/k8s_node2_install.py')

                },
                {
                    'name': 'k8s_install_node2',
                    'command': '/usr/bin/python3 /tmp/k8s_node2_install.py'

                },

            ]
    }


play = Play().load(play_source, variable_manager=variable_manager, loader=loader)


tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=passwords,
              stdout_callback=results_callback,
          )
    result = tqm.run(play)
finally:
      if tqm is not None:
        tqm.cleanup()

      shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

