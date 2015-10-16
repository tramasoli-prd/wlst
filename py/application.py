def connect_to_app_mbean():
  connect_to_server(admin_server_name, 't3s')
  domainRuntime()
  cd('AppRuntimeStateRuntime/AppRuntimeStateRuntime')


def start_application(app_name):
  connect_to_app_mbean()
  if app_name in cmo.getApplicationIds(): 
     startApplication(app_name)
     print(messages['application_messages']['app_started']  % app_name )
  else:
     print(errors['application_errors']['20000'])
  disconnect()


def stop_application(app_name):
  connect_to_app_mbean()
  if app_name in cmo.getApplicationIds():
     stopApplication(app_name)
     print(messages['application_messages']['app_stopped'] % app_name)
  else:
     print(errors['application_errors']['20000'])
  disconnect()


def restart_application(app_name):
  stop_application(app_name)
  start_application(app_name)


def get_application_status(app_name,server_name):
  connect_to_app_mbean()
  app_list  =  cmo.getApplicationIds()
  if server_name in get_all_servers_list():
    if app_name in app_list:
     print('=== Application : ' + app_name)  
     print('=== Server : ' + server_name)
     try: 
       print('=== Status : ' + cmo.getIntendedState(app_name,server_name) )
       return cmo.getIntendedState(app_name,server_name)
     except:
       print(errors['application_errors']['20002'])
     return cmo.getIntendedState(app_name,server_name) 
    if app_name not in app_list: 
      print(errors['application_errors']['20003']) 
  else:
     print(errors['application_errors']['20000'])
  disconnect() 


def get_application_status_all_servers(app_name):
  connect_to_app_mbean()
  for server_name in get_all_servers_list():
    get_application_status(app_name,server_name)
  disconnect()



def get_all_application_status():
  connect_to_app_mbean()
  app_list  =  cmo.getApplicationIds()   
  print '=== All applications status :\n'
  for app_name in app_list:
   print '=== Application :',app_name ,':', cmo.getIntendedState(app_name)
   #return cmo.getIntendedState(app_name)
  disconnect()



def app_is_deployed(app_name,server_name):
  connect_to_app_mbean() 
  if cmo.getIntendedState(app_name,server_name) == None:
     return False 
  else: 
     return True 



def deploy_app(server_name):
  print('=== Application path is : %s' % app_path)
  print('=== Choose application to deploy to server %s ?' % server_name)
  print os.listdir(app_path)
  app_file = (raw_input('Enter application name : '))
  
  if app_file in application_parameters['applications']: 
     app_name      = application_parameters['applications'][app_file]['app_name']
     app_is_lib    = application_parameters['applications'][app_file]['libraryModule'] 
     app_spec_ver  = application_parameters['applications'][app_file]['libSpecVersion'] 
     app_impl_ver  = application_parameters['applications'][app_file]['libImplVersion']
     create_plan   = application_parameters['applications'][app_file]['createPlan']
# if app is deployed and runing - try to stop it and undeploy
  if app_is_deployed(app_name,server_name): 
     status  = get_application_status(app_name,server_name)
     app_state = ['STATE_ACTIVE','STATE_ADMIN','STATE_UPDATE_PENDING']
     if status in app_state:
        print(messages['application_messages']['app_try_stop'] % app_name)
        try:
           stop_application(app_name)
        except:
           print(errors['application_errors']['20004']) 
     #Need silent undeployment, undeploy_app - bad idea
     connect_to_server(admin_server_name, 't3s')
     print (messages['application_messages']['undeploy_start'] % (app_name, server_name))
     edit()
     startEdit()
     undeploy(
       appName = app_name,
       path    = app_path,
       targets = server_name
       )
     save()
     activate()
     print (messages['application_messages']['undeploy_done'] % (app_name, server_name))
  connect_to_server(admin_server_name, 't3s')
  #create_directory(app_plan_path)
  print (messages['application_messages']['deploy_start'] % (app_name, server_name))
  edit()
  startEdit()
  try:
   deploy(
     appName        = app_name,
     path           = app_path,
     targets        = server_name,
     libraryModule  = app_is_lib,
     libSpecVersion = app_spec_ver,
     libImplVersion = app_impl_ver
     )
   print (messages['application_messages']['deploy_done'] % (app_name, server_name))
  except:
   print(errors['application_errors']['20001'])
  save()
  activate()
  disconnect()


def undeploy_app(server_name):
  connect_to_app_mbean()
  print( "=== Choose application to undeploy from server %s :?" % server_name)
  #print listApplications() 
  for app_name in cmo.getApplicationIds():
    print ('Application : ' + app_name) 
  app_name = (raw_input('Enter application name: '))
  if app_is_deployed(app_name,server_name):
    edit()
    startEdit()
    undeploy(
      appName = app_name,
      path    = app_path,
      targets = server_name
      )
    save()
    activate()
    print (messages['application_messages']['undeploy_done'] % (app_name, server_name))
  else:
   print(errors['application_errors']['20002']) 
  disconnect()


def deploy_app_all_servers():
  for server_name in managed_servers_list:
    deploy_app(server_name)

def undeploy_app_all_servers(): 
  for server_name in managed_servers_list:
     undeploy_app(server_name)



