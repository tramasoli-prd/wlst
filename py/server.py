from time import sleep

def create_server_boot_properties(server_name):
  print('\n=== Create Server Boot properties for server: %s ===\n' % server_name)
  directory_name = domain_home + '/servers/' + server_name + '/security'
  file_name      = 'boot.properties'
  content        = 'username=' + wl_user_name + '\npassword=' + wl_user_pass + '\n'
  create_file_with_content(directory_name, file_name, content)

def create_admin_server_conf_and_key_files():
  create_server_boot_properties(admin_server_name)
  connect_to_node_manager_with_conf_and_key()
  nmStart(admin_server_name)
  connect(
    username = wl_user_name,
    password = wl_user_pass,
    url      = admin_server_t3s_url,
    adminServerName = admin_server_name
  )
  storeUserConfig(
    userConfigFile = wl_secure_conf,
    userKeyFile    = wl_secure_key,
    nm = 'false'
    )
  disconnect()
  nmDisconnect()

def connect_to_server(server_name, connection_prefix):
  if connection_prefix == 't3':
    connect(
      userConfigFile = wl_secure_conf,
      userKeyFile    = wl_secure_key,
      url            = connection_prefix  + '://' + hostname + ':' + str(wl_servers[server_name]['http_port'])
      )
  elif connection_prefix == 't3s':
    connect(
      userConfigFile = wl_secure_conf,
      userKeyFile    = wl_secure_key,
      url            = connection_prefix  + '://' + hostname + ':' + str(wl_servers[server_name]['https_port'])
      )
  else:
 #   print('\nERROR: No such connection prefix!')
    print(errors['server_errors']['21000'])

def generate_boot_startup_properties(server_name):
  print('\n=== Generate the Node Manager property files, boot.properties and startup.properties, for %s ===\n' % server_name)
  connect_to_server(admin_server_name, 't3s')
  nmGenBootStartupProps(server_name)
  disconnect()

def generate_boot_startup_properties_for_all_servers():
  for server_name in all_servers_list:
    try:
      generate_boot_startup_properties(server_name)
    except:
    #  print('\nERROR: Can\'t generate Boot, Startup properties for server %s \n' % server_name)
      print(errors['server_errors']['21001'])

def associate_server_with_unix_machine(server_name):
  machine = wl_servers[server_name]['machine']
  print('\n=== Associate Server %s with Unix Machine %s ===\n' % (server_name, machine))
  connect_to_server(server_name, 't3s')
  edit()
  startEdit()
  cd('/Servers/' + server_name)
  cmo.setMachine(getMBean('/Machines/' + machine))
  save()
  activate()
  disconnect()

def create_managed_server(server_name):
  listen_address  = wl_servers[server_name]['listen_address']
  http_port       = wl_servers[server_name]['http_port']
  https_port      = wl_servers[server_name]['https_port']
  machine         = wl_servers[server_name]['machine']
  server_jvm_args = wl_servers[server_name]['jvm_args']
  print('\n=== Create Managed Server %s ===\n' % server_name)
  connect_to_server(admin_server_name, 't3s')
  edit()
  startEdit()
  cd('/')
  # Create Managed Server
  cmo.createServer(server_name)
  cd('/Servers/' + server_name)
  cmo.setListenAddress(listen_address)
  cmo.setListenPort(http_port)
  # Enable SSL
  cd('/Servers/' + server_name + '/SSL/' + server_name)
  cmo.setEnabled(true)
  cmo.setListenPort(https_port)
  # Assosiate with Unix Machine
  cd('/Servers/' + server_name)
  cmo.setMachine(getMBean('/Machines/' + machine))
  # Configure Logs parameters
  cd('/Servers/' + server_name + '/Log/' + server_name)
  cmo.setRedirectStderrToServerLogEnabled(true)
  cmo.setRedirectStdoutToServerLogEnabled(true)
  # Configure Server start parameters
  cd('/Servers/' + server_name + '/ServerStart/' + server_name)
  cmo.setArguments(server_jvm_args)
  save()
  activate()
  disconnect()
  create_server_boot_properties(server_name)

def create_all_managed_servers():
  for server_name in managed_servers_list:
    create_managed_server(server_name)

def change_server_listen_address(server_name):
  listen_address = wl_servers[server_name]['listen_address']
  print('\n=== Change Server %s listen address to %s ===\n' % (server_name, listen_address))
  connect_to_server(admin_server_name, 't3')
  edit()
  startEdit()  
  cd('/Servers/' + server_name)
  cmo.setListenAddress(listen_address)
  save()
  activate()
  disconnect()

def get_server_status(server_name):
  try:
    connect_to_node_manager_with_conf_and_key()
    print('\n=== Server %s current status:' % server_name)
    status = nmServerStatus(server_name)
    nmDisconnect()
    return status
  except WLSTException:
    print(errors['server_errors']['21002'])
    return 'WLSTERROR'

def start_server(server_name):
  status = get_server_status(server_name)
  #For heavy loaded server need more time to shutdown before start
  if status == 'FORCE_SHUTTING_DOWN':
    print('\n=== Server %s is in status %s ..Waiting 5 sec and try start again  ===\n' % (server_name, status)) 
    for x in range(1,3): 
      sleep(10)  
      print('\n=== Checking status, %s attempt ===\n' % x)
      status = get_server_status(server_name) 
      if status != 'FORCE_SHUTTING_DOWN':
         print('\n=== Server %s is stopped.. Trying to startup ===\n' % server_name)
         start_server(server_name)
         break 
    else:
       print('\n=== Unable to stop server %s in 30 seconds ===\n' % server_name)
       print('\n=== Wait longer time or kill -9 process and try again  ===\n' % server_name) 
  
  elif status in ['SHUTDOWN','FAILED','FAILED_NOT_RESTARTABLE']:
    print('\n=== Starting Server %s ===\n' % server_name)
    start_time = systime.time()
    if server_name == admin_server_name:
      connect_to_node_manager_with_conf_and_key()
      nmStart(
        serverName = server_name
        )
      nmDisconnect()
    else:
      connect_to_server(admin_server_name, 't3s')
      start(\
        name = server_name,
        type = 'Server'
        )
      disconnect()
      '''startServer(
        adminServerName = admin_server_name,
        domainName = domain_name,
        url = admin_server_t3s_url,
        domainDir = domain_home
        )'''
    print('\n== Completed in %.2f second(s) ===\n' % (systime.time() - start_time))
  elif status == 'WLSTERROR':
    pass
  else:
    print('\n=== Server %s is in status %s ===\n' % (server_name, status))

def stop_server(server_name):
  status = get_server_status(server_name)
  if status == 'RUNNING':
    print('\n=== Stopping Server %s ===\n' % server_name)
    start_time = systime.time()
    connect_to_server(admin_server_name, 't3s')
    shutdown(
      name            = server_name,
      entityType      = 'Server',
      ignoreSessions  = 'true',
      force           = 'true'
      )
    disconnect()
    print('\n=== Completed in %.2f second(s) ===\n' % (systime.time() - start_time))
  elif status == 'WLSTERROR':
    pass
  else:
    print('\n=== Server %s is in status %s ===\n' % (server_name, status))


def update_jvm_parameters_server(server_name):
  server_jvm_args = wl_servers[server_name]['jvm_args']
  print('\n=== Update JVM parameters Managed Server %s ===\n' % server_name)
  connect_to_server(admin_server_name, 't3s')
  edit()
  startEdit()
  # Configure Server start parameters
  cd('/Servers/' + server_name + '/ServerStart/' + server_name)
  cmo.setArguments(server_jvm_args)
  save()
  activate()
  disconnect()
  if server_name == admin_server_name:
   restart_node_manager()
  restart_server(server_name) 

def update_jvm_parameters_all_managed_servers():
  for server_name in managed_servers_list:
    update_jvm_parameters_server(server_name) 

def update_jvm_parameters_all_servers():
  for server_name in all_servers_list:
    update_jvm_parameters_server(server_name)
   
def restart_server(server_name):
  stop_server(server_name)
  start_server(server_name)

def stop_all_managed_servers():
  for server_name in managed_servers_list:
    stop_server(server_name)

def start_all_managed_servers():
  for server_name in managed_servers_list:
    start_server(server_name)

def start_all():
  start_node_manager()
  start_server(admin_server_name)
  start_all_managed_servers()

def stop_all():
  stop_all_managed_servers()
  stop_server(admin_server_name)
  stop_node_manager()

def restart_all():
  stop_all()
  start_all()
