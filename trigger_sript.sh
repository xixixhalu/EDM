#!/usr/bin/bash

DIR=`pwd`
export EDM_ROOT_DIR=$DIR
python $1
unset EDM_ROOT_DIR
