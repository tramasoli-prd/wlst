def connect_to_node_manager_with_username_and_password():
  nmConnect(
    username   = nm_user_name,
    password   = nm_user_pass,
    host       = hostname,
    port       = nm_listen_port,
    domainName = domain_name,
    domainDir  = domain_home
    )

def create_node_manager_conf_and_key_files():
  create_directory(secure_dir)
  startNodeManager(
    NodeManagerHome = nm_home,
    PropertiesFile  = nm_properties_file,
    jvmArgs         = nm_jvm_opts
    )
  connect_to_node_manager_with_username_and_password()
  storeUserConfig(
    userConfigFile = nm_secure_conf,
    userKeyFile    = nm_secure_key,
    nm = 'true'
  )
  nmDisconnect()

def connect_to_node_manager_with_conf_and_key():
  nmConnect(
    userConfigFile = nm_secure_conf,
    userKeyFile    = nm_secure_key,
    host           = hostname,
    port           = nm_listen_port,
    domainName     = domain_name,
    domainDir      = domain_home
    );

def get_node_manager_status():
  try:
    connect_to_node_manager_with_conf_and_key()
    nmDisconnect()
    return 0 # Node Manager is running
  except WLSTException:
    return 1 # Node Manager is not available

def start_node_manager():
  try:
    connect_to_node_manager_with_conf_and_key()
    nmDisconnect()
    print('\n=== Node Manager is already running. ===\n')
  except WLSTException:
    print('\n=== Node Manager is not running. Trying to start Node Manager. ===\n')
    startNodeManager(
      NodeManagerHome = nm_home,
      PropertiesFile  = nm_properties_file,
      jvmArgs         = nm_jvm_opts
      )

def stop_node_manager():
  try:
    connect_to_node_manager_with_conf_and_key()
    stopNodeManager()
    print('\n=== Node Manager stopped. ===\n')
  except WLSTException:
    print('\n=== Node Manager is not running. ===\n')

def restart_node_manager():
  stop_node_manager()
  start_node_manager()