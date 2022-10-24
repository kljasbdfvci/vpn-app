#!/bin/bash

memory_path="/memory"

if [[ ! -e $memory_path ]]; then
    mkdir -p $memory_path
fi

mount -t tmpfs -o size=32M,mode=0755 tmpfs $memory_path
