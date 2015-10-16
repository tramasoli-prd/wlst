#!/bin/bash
test_mode="n"
if [ "$test_mode" = "n" ]; then
# Gerrit synchronization
git_branch=`cat .git/config  |grep url |awk -F"@" '{print $2}'`
if [ -z "`git diff`" ]
then
printf "=== Getting last commited scripts from $git_branch \n"
git pull
else
printf "=== Local repository has uncommited changes!:
#1.Erase and pull. Warning! All local scripts will be replaced from $git_branch
#2.Exit and manually commit and push, then restart current script\n"
read -s a
case $a in
1) echo "=== Starting 'git reset --hard'"
git reset --hard
 echo "=== Done."
;;
2) echo "Exit."; exit 1
;;
*) echo "Wrong choice!";  exit 1
esac
fi
fi
# WLST env
JAVA_HOME=/usr/bin/java
WORK_DIR=`dirname $0`
if [ "$WORK_DIR" = "." ]; then WORK_DIR=`pwd`; fi; export WORK_DIR
export PY_PATH=$WORK_DIR/py
export LOG_PATH=$WORK_DIR/logs
if [ ! -d "$LOG_PATH" ]; then mkdir $LOG_PATH; fi
MAIN_PY_SCRIPT="$(basename $0 .sh).py"
WLST_PROPERTIES="-Dweblogic.management.confirmKeyfileCreation=true -Xms256m -Xmx256m"
export WL_VERSION="12c"

# Weblogic 12c
if [ $WL_VERSION = "12c" ]; then
export MW_HOME=/opt/oracle/product/fmw12c
export WL_HOME=$MW_HOME/wlserver
export WL_TEMPLATE=$WL_HOME/common/templates/wls/wls.jar
source $MW_HOME/wlserver/server/bin/setWLSEnv.sh

# Weblogic 11g - TEST mode
elif [ $WL_VERSION = "11g" ]; then 
export MW_HOME=/opt/oracle/product/fmw11g
export WL_HOME=$MW_HOME/wlserver_10.3
export WL_TEMPLATE=$WL_HOME/common/templates/domains/wls.jar
source $WL_HOME/server/bin/setWLSEnv.sh

else echo "=== Uknown Weblogic version"; exit 1
fi

TrustKeyStore=CustomTrust
CustomTrustKeyStoreFileName=/opt/oracle/ssl/CustomTrust.jks

#For deploymnents to fix main bug with plan.xml
#java weblogic.PlanGenerator -all /opt/oracle/applications/vista_3ds/app_versions/acs_232359.ear -plan /opt/oracle/applications/vista_3ds/deploy_plan/plan.xml

case $1 in
'nossl')
printf "\nStarting WLST without SSL\n"
java $WLST_PROPERTIES  weblogic.WLST -i $PY_PATH/$MAIN_PY_SCRIPT
;;
*)
printf "\nStarting WLST with SSL\n"
java $WLST_PROPERTIES -Dweblogic.security.TrustKeyStore=${TrustKeyStore} -Dweblogic.security.CustomTrustKeyStoreFileName=${CustomTrustKeyStoreFileName} weblogic.WLST -i $PY_PATH/$MAIN_PY_SCRIPT
;;
esac

### How to generate SSL self-sighed certs for WL 
### Save encrypted passwords(via encryptor.sh) in settings_custom.py + save it in clear type in 1password. 

#ssl_identity_private_key_alias=`hostname`
#ssl_identity_private_key_passphrase="***"
#custom_identity_keystore_passphrase="***"
#custom_trust_keystore_passphrase="***"

#custom_identity_keystore_file="/opt/oracle/ssl/CustomIdentity.jks"
#custom_trust_keystore_file="/opt/oracle/ssl/CustomTrust.jks"
#ssl_certificate="/opt/oracle/ssl/CustomIdentity.cer"

#keytool -genkey -alias ${ssl_identity_private_key_alias} -keyalg RSA -keysize 1024 -validity 1825 -dname "CN=${HOSTNAME},C=RU" -keypass ${ssl_identity_private_key_passphrase} -keystore ${custom_identity_keystore_file} -storepass ${custom_identity_keystore_passphrase}
#keytool -exportcert -v -alias ${ssl_identity_private_key_alias} -keystore ${custom_identity_keystore_file} -storepass ${custom_identity_keystore_passphrase} -rfc -file ${ssl_certificate}
#keytool -importcert -alias clientKey -file ${ssl_certificate} -keystore ${custom_trust_keystore_file} -storepass ${custom_trust_keystore_passphrase} -noprompt

