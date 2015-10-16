from sets import Set;

def create_unix_machine(machine_name):
  print('\n=== Create Unix Machine: %s ===\n' % machine_name)
  connect_to_server(admin_server_name, 't3s')
  edit()
  startEdit()
  cd('/')
  cmo.createUnixMachine(machine_name)
  cd('/Machines/' + machine_name + '/NodeManager/' + machine_name)
  cmo.setListenAddress(machine_name)
  save()
  activate()
  disconnect()

def get_all_unix_machine_list():
  unix_machine_uniq_list = []
  for server_name in wl_servers:
    unix_machine_uniq_list.append(wl_servers[server_name]['machine'])
  unix_machine_set = Set(unix_machine_uniq_list)
  unix_machine_uniq_list = list(unix_machine_set)
  return unix_machine_uniq_list

def create_all_unix_machines():
  unix_machine_uniq_list = get_all_unix_machine_list()
  for machine_name in unix_machine_uniq_list:
    create_unix_machine(machine_name)