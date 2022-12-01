#!/bin/bash

my_print() {
   if [ $2 -eq 0 ]; then
      echo "$1: Successed"
   else
      echo "$1: Failed"
   fi
}

initialApplication() {
   null_output="/dev/null"
   app_file_path=$1
   app_untar_path=$2
   os_untar_path=$3
   app_init_path=$4
   app_init_log=$5
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
      tar -xzvf $app_file_path -C $app_untar_path --exclude="os" 1>$null_output
      res_tar_app=$?
      my_print "extract Application" $res_tar_app

      ### extract Os
      tar -xzvf $app_file_path -C $os_untar_path os 1>$null_output
      res_tar_os=$?
      my_print "extract Os" $res_tar_os

      ### run init Application
      res_init=1
      if [ $res_tar_app = 0 ] && [ $res_tar_os = 0 ]; then
         $app_init_path &>$app_init_log &
         res_init=$?
      fi
      my_print "run init Application" $res_init

      ### return
      if [ $res_rm = 0 ] && [ $res_tar_app = 0 ] && [ $res_tar_os = 0 ] && [ $res_init = 0 ] && [ $res_mkdir = 0 ]; then
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
   return $res_decrypt
}

### Var
this_file_path=$(eval "realpath $0")
this_dir_path=$(eval "dirname $this_file_path")
disk_path="/disk"
memory_path="/memory"
tmp_path="/tmp"
logo_path="$this_dir_path/logo"
app_file_path=$(find $disk_path/firmware -type f -name '*-app*' | sort | tail -n 1)
temp_app_file_path="$tmp_path/app.tgz"
app_untar_path="$memory_path"
os_untar_path="$tmp_path"
app_init_path="$app_untar_path/bin/init.sh"
app_init_log="$tmp_path/app-init.log"

### Move Cursor Down And Print Logo
echo -e "\n\n\n\n\n\n"
cat $logo_path
echo -e "\n"

### Wait For Mount /memory
echo "Initial Storage... Started"
for i in {1..300}
do
   ### check memory storage Mount
   mountpoint -q $memory_path
   res=$?
   my_print "check memory storage Mount try($i)" $res
   if [ $res -eq 0 ]; then
      break
   fi
   
   ### sleep Mount
   sleep 1
done
echo "Initial Storage... End"

### Application
echo "Initial Application... Start"
if [ -f "$app_file_path" ]; then

   decryptFile $app_file_path $temp_app_file_path
   if [ $? -eq 0 ]; then
      my_print "Decrypt Firmware" 0
      initialApplication $temp_app_file_path $app_untar_path $os_untar_path $app_init_path $app_init_log
   else
      my_print "Decrypt Firmware" 1
   fi
   rm -f $temp_app_file_path
else
   my_print "No Firmware" 1
fi
echo "Initial Application... End"

exit 0
