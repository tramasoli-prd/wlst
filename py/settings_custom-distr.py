# Variables to Change

domain_name = 'vista_3ds'
user_parameters = {
  'wl_user'    : {'username': 'weblogic', 'password': '', 'user_config_file': 'wlsconfigfile.secure', 'user_key_file': 'wlskeyfile.secure'},
  'nm_user'    : {'username': 'nmadmin' , 'password': '', 'user_config_file': 'ndmconfigfile.secure', 'user_key_file': 'ndmkeyfile.secure'}
  
  }

ssl_parameters = {
  'certs_path': '/opt/oracle/ssl',
  'Keystores' : {
    'Keystores'      : 'CustomIdentityAndCustomTrust',
    'Custom_Identity': {'Keystore': 'CustomIdentity.jks', 'Type': 'jks', 'Passphrase': ''},
    'Custom_Trust'   : {'Keystore': 'CustomTrust.jks'   , 'Type': 'jks', 'Passphrase': ''}
  },
  'SSL': {'Private_Key_Alias': hostname, 'Private_Key_Passphrase': ''}
}

jdbc_parameters = {
  'datasource_test_query'  : 'SQL SELECT 1 FROM DUAL',
  'datasource_driver_class': 'oracle.jdbc.OracleDriver',
  'data_sources' : {
     'FE'            : { 'db_user' : 'svista',   'password': '',      'jndi_name' : 'jdbc/svwi/FE', 'URL' : 'jdbc:oracle:thin:@smartfedb.osmp.ru:1521/wl_smartfe'},
     'FE Authorized' : { 'db_user' : 'svista',   'password': '',      'jndi_name' : 'jdbc/svwi/FEAuthorized', 'URL' : 'jdbc:oracle:thin:@smartfedb.osmp.ru:1521/wl_smartfe'},
     'BO'            : { 'db_user' : 'vista',    'password': '',      'jndi_name' : 'jdbc/svwi/BO', 'URL' : 'jdbc:oracle:thin:@smartbodb.osmp.ru:1521/wl_smartbo'},
     'BO Authorized' : { 'db_user' : 'vista',    'password': '',      'jndi_name' : 'jdbc/svwi/BOAuthorized', 'URL' : 'jdbc:oracle:thin:@smartbodb.osmp.ru:1521/wl_smartbo'},
     'CG Authorized' : { 'db_user' : 'svcg',     'password': '',      'jndi_name' : 'jdbc/svwi/CGAuthorized','URL':'jdbc:oracle:thin:@smartcgdb.osmp.ru:1521/wl_smartcg'},
     'WI'            : { 'db_user' : 'svista',   'password': '',      'jndi_name' : 'jdbc/svwi/WI','URL':'jdbc:oracle:thin:@smartfedb.osmp.ru:1521/wl_smartfe'},
     'ACS'           : { 'db_user' : 'vista_3ds','password': '',      'jndi_name' : 'jdbc/acs/db', 'URL':'jdbc:oracle:thin:@smartfedb.osmp.ru:1521/wl_3ds'}

  }
}

       

jms_resources = {
 'jms_server_name' : 'SVWI',
 'jms_module_name' : 'Audit',
 'jms_resources' :{
 

}
}

java_diag_parameters = ''
java_app_parameters = ''
#java_app_parameters = '-Dru.bpc.acs-home=/opt/oracle/acs_home -Dru.bpc.BpcThalesProvider.conf=/opt/oracle/acs_home/conf/BpcThalesProvider.properties -Dru.bpc.acs.smsSenderProfile=SMS_SEND_WS -Dorg.apache.cxf.Logger=org.apache.cxf.common.logging.Slf4jLogger'
#java_diag_parameters = '-Dru.bpc.acs-home=/opt/oracle/acs_home -XX:+UnlockDiagnosticVMOptions -XX:+PrintFlagsFinal' 
#java_diag_parameters = '-XX:LargePageSizeInBytes=2m -XX:+UnlockDiagnosticVMOptions -XX:+PrintFlagsFinal' # deep diagnostic java settings - check AdminServer.out or ManagedServer.out

wl_servers = {
  # server_type = 'A' - WebLogic Administration Server
  # server_type = 'M' - WebLogic Managed Server
  # For 12c deploy keep listen_address empty on AdminServer before deploy. You can change it later.
  'AdminServer': {'server_type': 'A', 'http_port': 7001, 'https_port': 7002, 'listen_address': ''       , 'machine': hostname , 'jvm_args': '-Xms1024m -Xmx2048m -XX:+UseLargePages -XX:LargePageSizeInBytes=2m '  +  java_diag_parameters},
  'wls_dms1'    : {'server_type': 'M', 'http_port': 8001, 'https_port': 8002, 'listen_address': hostname , 'machine': hostname , 'jvm_args': '-Xms2048m -Xmx4096m -XX:+UseLargePages -XX:LargePageSizeInBytes=2m ' + java_app_parameters + java_diag_parameters}
  #'wls_dms2'    : {'server_type': 'M', 'http_port': 9001, 'https_port': 9002, 'listen_address': hostname , 'machine': hostname , 'jvm_args': '-Xms2048m -Xmx4096m -XX:+UseLargePages -XX:LargePageSizeInBytes=2m ' + java_app_parameters + java_diag_parameters}                 
  }

nm_parameters = {
  'listen_port'   : '5556',
  'jvm_opts'      : '-Xms128m,-Xmx128m,-XX:+UseLargePages,-XX:LargePageSizeInBytes=2m',
  'listen_address': hostname
  }


application_parameters = {
  'application_home': '/opt/oracle/applications/' + domain_name,
  'applications' : {
      'jsf-1.2_14.war' : {'app_name':'jsf#1.2@1.2.14.0', 'createPlan' : 'False', 'libraryModule' : 'True', 'libSpecVersion' : '1.2','libImplVersion' : '1.2.14.0' },
      'acs_232359.ear' : {'app_name':'acs_232359',       'createPlan' : 'True',  'libraryModule' : 'False','libSpecVersion' : ''   ,'libImplVersion' : ''} 
  }
}
