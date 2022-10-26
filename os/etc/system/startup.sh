#!/bin/bash

### Wait For ttyS0 Start
#sleep 5

### Const Variable
null_output="/dev/null"

my_print() {
   if [ $2 -eq 0 ]; then
      >&2 echo "$1: OK"
      echo -n "."
   else
      >&2 echo "$1: FAIL"
      echo -n "?"
   fi
}

initialApplication() {
   app_file_path=$1
   app_untar_path=$2
   app_init_path=$3
   app_init_log=$4
   app_init_log_error=$5
   if [ -f "$app_file_path" ]; then

      ### make app dir Application
      mkdir -p $app_untar_path >$null_output
      res_mkdir=$?
      my_print "make app dir Application" $res_mkdir

      ### rm app files Application
      rm -rf $app_untar_path/* >$null_output
      res_rm=$?
      my_print "rm app files Application" $res_rm

      ### extract Application
      tar -xzvf $app_file_path -C $app_untar_path 1>$null_output
      res_tar=$?
      my_print "extract Application" $res_tar

      ### run init Application
      $app_init_path 1>$app_init_log 2>$app_init_log_error
      res_init=$?
      my_print "run init Application" $res_init

      ### return
      if [ $res_rm = 0 ] && [ $res_tar = 0 ] && [ $res_init = 0 ] && [ $res_mkdir = 0 ]; then
         return 0
      else
         return 1
      fi
   else
      ### return
      return 1
   fi
}

decryptFile() {
   in=$1
   out=$2
   serial -d $in $out
   res_decrypt=$?
   my_print "decrypt file" $res_decrypt
   return $res_decrypt
}

### Move Cursor Down And Print Logo
printf "\n\n\n\n\n\n"
cat /etc/system/logo
printf "\n"

### Wait For Mount /memory
echo -n "Initial Storage"
for i in {1..20}
do
   ### check memory storage Mount
   mountpoint -q "/memory"
   res=$?
   my_print "check memory storage Mount try($i)" $res
   if [ $res -eq 0 ]; then
      break
   fi
   
   ### sleep Mount
   sleep 1
done

mountpoint -q "/memory"
if [ $? -eq 0 ]; then
   echo " OK"
else
   echo " ERROR"
fi

### System
app_file_path=$(find /disk/firmware -type f -name '*-app*' | sort | tail -n 1)
app_untar_path="/memory/"
app_init_path="/memory/bin/init.sh"
app_init_log="/tmp/app-init.log"
app_init_log_error="/tmp/app-init.log.error"

### Application
echo -n "Initial Application"
if [ -f "$app_file_path" ]; then

   temp_app_file_path="/tmp/app.tgz"
   decryptFile $app_file_path $temp_app_file_path
   if [ $? -eq 0 ]; then
      initialApplication $temp_app_file_path $app_untar_path $app_init_path $app_init_log $app_init_log_error
      if [ $? -eq 0 ]; then
         echo " OK"
      else
         echo " ERROR"
      fi
   else
      echo " ERROR"
   fi
   rm -f $temp_app_file_path
else
   my_print "No Firmware" 1
   echo " ERROR"
fi

exit 0
