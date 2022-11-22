#!/bin/bash

logrotate --skip-state-lock --force /etc/logrotate.d/app
