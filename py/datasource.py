def create_datasource(source_name):
 if source_name in jdbc_parameters['data_sources']:
  ds_jndi          = jdbc_parameters['data_sources'][source_name]['jndi_name']
  ds_url           = jdbc_parameters['data_sources'][source_name]['URL']
  ds_db_user       = jdbc_parameters['data_sources'][source_name]['db_user']
  ds_db_user_pass  = jdbc_parameters['data_sources'][source_name]['password']
 
  driver_param ='/JDBCSystemResources/'+source_name+'/JDBCResource/'+source_name+'/JDBCDriverParams/'+source_name
  connect_to_server(admin_server_name, 't3s')
  edit()
  startEdit()
  cmo.createJDBCSystemResource(source_name)
  resource='/JDBCSystemResources/'+source_name+'/JDBCResource/'+source_name
  cd(resource)
  set('Name',source_name)
  cd(resource+'/JDBCDataSourceParams/'+source_name)
  set('JNDINames',jarray.array([String(ds_jndi)], String))
  cd(driver_param)
  set('Url',ds_url)
  set('DriverName',ds_driver)
  set('Password',ds_db_user_pass)
  cd(driver_param+'/Properties/'+source_name)
  cmo.createProperty('user')
  cd(driver_param+'/Properties/'+source_name+'/Properties/user')
  set('Value',ds_db_user)

  cd(resource+'/JDBCConnectionPoolParams/'+source_name)
  cmo.setTestTableName(ds_test_query)
  cd('/JDBCSystemResources/'+source_name)
  #Bug fixed # added many targets
  #  set('Targets',jarray.array([ObjectName('com.bea:Name='+server+',Type=Server')], ObjectName))
  list=[]
  for server in managed_servers_list:
     s='com.bea:Name='+server+',Type=Server'
     list.append(ObjectName(str(s)))
  set('Targets',jarray.array(list, ObjectName))
  save()
  activate()
  disconnect()
 else: 
  print(errors['application_errors']['20005'])

def create_all_datasources():
 for source_name in get_all_datasources():
  create_datasource(source_name) 

def delete_datasource(source_name):
   connect_to_server(admin_server_name, 't3s')
   if source_name in get_all_datasources(): 
    edit()
    startEdit()
    cd('/')  
    cmo.destroyJDBCSystemResource(getMBean('/JDBCSystemResources/' + source_name))
    save()
    activate()
    disconnect()
   else:
    print(errors['application_errors']['20005'])


def delete_all_datasources():
   for source_name in get_all_datasources():
     delete_datasource(source_name)
