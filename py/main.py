#!/usr/bin/python
import os
import sys
import time as systime
script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
redirect(os.environ['LOG_PATH']+'/wlst.log', 'true')
#sys.path.append(script_path)
#Weblogic env
hostname     = os.getenv('HOSTNAME')
osuser       = os.getenv('USER')
java_home    = os.getenv('JAVA_HOME')
mw_home      = os.environ['MW_HOME']
wl_home      = os.environ['WL_HOME']
wl_template  = os.environ['WL_TEMPLATE']
wl_version   = os.environ['WL_VERSION']
#Weblogic env
#wl_user_pwd = (raw_input('Enter password for user %s: ' % wl_user))
#nm_user     = 'nmadmin'
#nm_user_pwd = (raw_input('Enter password for user %s: ' % nm_user))

execfile(script_path + '/settings_custom.py')
execfile(script_path + '/settings_common.py')
execfile(script_path + '/os_commands.py')
execfile(script_path + '/domain.py')
execfile(script_path + '/node_manager.py')
execfile(script_path + '/machine.py')
execfile(script_path + '/server.py')
execfile(script_path + '/ssl.py')
execfile(script_path + '/application.py')
execfile(script_path + '/datasource.py')
execfile(script_path + '/help.py')



#Create domain
def deploy_domain():
  start_time = systime.time()
  create_and_configure_domain()
  create_node_manager_conf_and_key_files()          # need fix to silent file generation # done
  create_admin_server_conf_and_key_files()
  create_all_unix_machines()
  create_all_managed_servers()
  generate_boot_startup_properties_for_all_servers() # jvm_args will not be used for AdminServer startup without this step
  restart_node_manager()                             # to get created boot and startup properties
  associate_server_with_unix_machine(admin_server_name)
  restart_server(admin_server_name) # require after association with machine
  start_all_managed_servers()
  stop_all()
  configure_ssl_node_manager()
  configure_ssl_all_servers()
  print('=== Script completed in %.2f second(s) ===' % (systime.time() - start_time))
  exit()

def deploy_domain_ssl():
  start_all()
  generate_boot_startup_properties_for_all_servers()
  create_datasource('ACS')
  exit()

