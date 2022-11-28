#!/bin/bash

parse_options() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--dns_server)
                dns_server="$2"
                shift # past argument
                shift # past value
                ;;
            -*|--*)
                echo "Unknown option $1"
                exit 1
                ;;
            *)
                echo "Invalid value $1"
                exit 1
                ;;
        esac
    done
}

parse_options $@

exit_code=0

########################################################################
# start dns
########################################################################

# make dns str
str="#MYDNS_START\n"
for item in ${dns_server//,/ } ; do
    str=$str"nameserver $item\n"
done
str=$str"#MYDNS_END"

# add new dns
echo -e "$str\n$(cat /etc/resolv.conf)" > /etc/resolv.conf

exit $exit_code
