#! /bin/bash

echo Uploading files from $1 to nexus

cd $1
FILES=*
for f in $FILES
do
  echo "Processing $f file..."
  curl -T $f https://rizzo.airgap.us/content/repositories/yum/$2/$f -u $3:$4
done


