#!/bin/bash

input=$1
output=$2
docker run --rm -v $PWD:/data -w /data cyverseuk/muscle muscle -in $input -out $output
