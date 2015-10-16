def get_all_servers_list():
  all_servers_list = []
  for server_name in wl_servers:
    all_servers_list.append(server_name)
  return all_servers_list

def get_all_managed_servers_list():
  managed_servers_list = []
  for server_name in wl_servers:
    if wl_servers[server_name]['server_type'] == 'M':
      managed_servers_list.append(server_name)
  return managed_servers_list

def get_admin_server_name():
  count = 0
  for server_name in wl_servers:
    if wl_servers[server_name]['server_type'] == 'A':
      count += 1
      admin_server_name = server_name
  if count == 1:
    return admin_server_name
  elif count == 0:
    print ('ERROR: There is no Admin Server in your configuration!' % count)
  elif count > 1:
    print ('ERROR: There is %s Admin Servers in your configuration!' % count)
  else:
    print ('ERROR: UNKNOWN PROBLEM')

def get_all_datasources():
  all_datasource_list = []
  for source_name in jdbc_parameters['data_sources']:
     all_datasource_list.append(source_name)
  return all_datasource_list 


admin_server_name     = get_admin_server_name()
admin_listen_address  = wl_servers[admin_server_name]['listen_address']
admin_server_t3_url   = 't3'  + '://' + hostname + ':' + str(wl_servers[admin_server_name]['http_port'])
admin_server_t3s_url  = 't3s' + '://' + hostname + ':' + str(wl_servers[admin_server_name]['https_port'])
admin_server_jvm_args =  wl_servers[admin_server_name]['jvm_args']

all_servers_list     = get_all_servers_list()
managed_servers_list = get_all_managed_servers_list()


# Domain environment

domain_config_home      = '/opt/' + osuser + '/config'
domain_home             = domain_config_home + '/domains/'      + domain_name
#domain_application_home = '/opt/' + osuser + '/applications/'   + domain_name
secure_dir              = domain_config_home + '/secure/'       + domain_name

wl_user_name = user_parameters['wl_user']['username']
wl_user_pass = user_parameters['wl_user']['password']
nm_user_name = user_parameters['nm_user']['username']
nm_user_pass = user_parameters['nm_user']['password']

wl_secure_conf  = secure_dir + '/' + user_parameters['wl_user']['user_config_file']
wl_secure_key   = secure_dir + '/' + user_parameters['wl_user']['user_key_file']

nm_home            = domain_home + '/nodemanager'
nm_properties_file = nm_home     + '/nodemanager.properties'

nm_jvm_opts        = nm_parameters['jvm_opts']
nm_listen_address  = nm_parameters['listen_address']
nm_listen_port     = nm_parameters['listen_port']
nm_secure_conf     = secure_dir + '/' + user_parameters['nm_user']['user_config_file']
nm_secure_key      = secure_dir + '/' + user_parameters['nm_user']['user_key_file']

# SSL

ssl_certificates_path               = ssl_parameters['certs_path']
Keystores                           = ssl_parameters['Keystores']['Keystores']
Custom_Identity_Keystore            = ssl_certificates_path + '/' + ssl_parameters['Keystores']['Custom_Identity']['Keystore']
Custom_Trust_Keystore               = ssl_certificates_path + '/' + ssl_parameters['Keystores']['Custom_Trust'   ]['Keystore']
Custom_Identity_Keystore_Type       = ssl_parameters['Keystores']['Custom_Identity']['Type']
Custom_Trust_Keystore_Type          = ssl_parameters['Keystores']['Custom_Trust'   ]['Type']
Custom_Identity_Keystore_Passphrase = ssl_parameters['Keystores']['Custom_Identity']['Passphrase']
Custom_Trust_Keystore_Passphrase    = ssl_parameters['Keystores']['Custom_Trust'   ]['Passphrase']
SSL_Identity_Private_Key_Alias      = ssl_parameters['SSL']['Private_Key_Alias']
SSL_Identity_Private_Key_Passphrase = ssl_parameters['SSL']['Private_Key_Passphrase']

# JDBC
ds_test_query    = jdbc_parameters['datasource_test_query']
ds_driver        = jdbc_parameters['datasource_driver_class']

#Application
domain_application_home = application_parameters['application_home']
app_path                = domain_application_home + '/app_versions'
app_plan_path           = domain_application_home + '/deploy_plan'
app_plan_file           = app_plan_path + '/plan.xml'


errors = {
  'application_errors' : {
     '20000': '=== wlst-20000: Can\'t get server name ===\n',
     '20001': '=== wlst-20001: Can\'t deploy application ===\n',
     '20002': '=== wlst-20002: Application is not deployed on server ===\n',
     '20003': '=== wlst-20003: Can\'t get application name ===\n',
     '20004': '=== wlst-20004: Unable to stop application ===\n',
     '20005': '=== wlst-20005: Unknown datasource! Check input param and/or jdbc settings in settings_custom.py ==='

},
   'server_errors' : {
      '21000': '=== wlst-21000: No such connection prefix! ===\n',
      '21001': '=== wlst-21001: Can\'t generate Boot, Startup properties for server ===\n',
      '21002': '=== wlst-21002: Can\'t get server status. Can\'t connect to Node Manager. ===\n'
}
}

messages = {
   'application_messages' : {
      'deploy_start'   : '=== Starting to deploy application %s on server %s ===',
      'undeploy_start' : '=== Starting to undeploy application %s on server %s ===',
      'deploy_done'    : '=== Deployment of application %s successfully done on server %s ===',
      'undeploy_done'  : '=== Undeployment of application %s successfully done on server %s ===',
      'app_try_stop'   : '=== Trying to stop application %s, if it\'s running',
      'app_stopped'    : '=== Application %s successfully stopped',
      'app_started'    : '=== Application %s successfully started '

}
}

