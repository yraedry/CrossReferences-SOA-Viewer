#!/usr/bin/env bash

if [[ -f $1"\\"$5 ]];
then
    rm -rf $5
fi
for i in {1..10};
do
    curl -s -u $2:$3 -X GET $4/repos\?page\=$i | grep -i full_name | grep -i Cibt- |cut -d'/' -f 2 | sed 's/",//' >>  $1/$5
done