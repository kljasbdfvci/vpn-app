#!/bin/bash

if [[ ! -e /memory ]]; then
    mkdir /memory
fi

mount -t tmpfs -o size=32M,mode=0755 tmpfs /memory
