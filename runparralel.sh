#!/bin/bash

for cmd in "$@"; do {
  $cmd & pid=$!
  PID_LIST+=" $pid";
} done

trap "kill $PID_LIST" SIGINT

wait $PID_LIST
