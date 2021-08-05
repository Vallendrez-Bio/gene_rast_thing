#!/bin/bash

# Umm the genome id?
file=$1
# Rast job number
job=$2
# Session that you steal from chrome's dev tools
session=$3

curl 'https://rast.nmpdr.org/rast.cgi' \
  -s \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36' \
  -H "Referer: https://rast.nmpdr.org/rast.cgi?page=JobDetails&job=${job}" \
  -F "page=DownloadFile" \
  -H "Cookie: WebSession=${session}" \
  -F "job=${job}" \
  -F "file=${file}.txt" \
  -F "do_download= Download" \
  --compressed > ${job}.${file}.tsv
