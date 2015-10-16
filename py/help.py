def aliases():
 upd_jvm=update_jvm_parameters_server(server_name)

def basic_man():
  print('===  Basic server functions:')
  print('start_all()                             Start all servers')
  print('stop_all()                              Stop all servers')
  print('restart_all()                           Restart all servers')
  print('get_all_application_status()            Get all deployed app status')
  server=str(managed_servers_list).replace("[","").replace("]","")
  print('start_server(' + server + ')                Start managed server')
  print('stop_server(' + server + ')                 Stop managed server')
  print('restart_server(' + server + ')              Restart managed server')
  print('get_server_status(' + server + ')           Check managed server status')
  print('===  Type man() for help on available functions\n')
  
basic_man()

def man():
 # App
  server=str(managed_servers_list).replace("[","").replace("]","")
  print('\n===  Applications (to check application directory: print app_path')
  print('deploy_app(' + server + ')                  Deploy app to server') 
  print('undeploy_app(' + server + ')                Undeploy app form server')
  print('deploy_app_all_servers()                Deploy app to all managed servers')
  print('undeploy_app_all_servers()              Undeploy app to all managed servers')
 # Configure jvm params
  print('\n===  Configure JVM/App parameters: \n'
        'a.Change java_app_parameters in settings_custom.py \n'
        'b.Execute one of func below:')
  print('update_jvm_parameters_all_servers()                    Changs JVM params and restart all servers')
  print('update_jvm_parameters_server(server_name)              Changs JVM params and restart server')
 # Create domain
  print('\n===  Deploy Domain:')
  print('a. Create SSL cert and keystore /*How to generate SSL self-sighed certs written in main.sh*/ ')
  print('b. Configure domain parameters in settings_custom.py')
  print('c. Invoke "./main.sh nossl"')
  print('deploy_domain()')
  print('d. Invoke "./main.sh"') 
  print('deploy_domain_ssl()')
  print('\n===  JVM hanged | invalid state | WLST throwing errors - kill proccesess and start:')
  print("ps -ef|grep java |egrep -v 'grep|WLST' | awk '{print $2}' | xargs kill -9")
  print('start_all()\n')
  

