#!/bin/bash

#http://superuser.com/questions/747884/how-to-write-a-script-that-accepts-input-from-a-file-or-from-stdin
[ $# -ge 1 -a -f "$1" ] && input="$1" || input="-"
awk '{sum+=exp($'$2'/'-$3')};END{print sum,sum/NR,'-$3'*log(sum/NR)}' $input
