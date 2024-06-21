#!/bin/bash

# Clear logs
> /var/log/apache2/access.log
> /var/log/bind/query

# Run certbot for google. Random subdomain added to get around cacheing behavior.
rand=$(echo $RANDOM)
curl -X POST -d '{"method":"acme/http-01","kaHash":"TfPD9o_Mg7J-nULJBDGnJJnxeHXIGlmbVmyYiblpZwM=","token":"aaaaaaaaaaaaaaaaaaaaa", "domain":"'${rand}'.arins.pretend-crypto-wallet.com","accessToken":"YTrWJscsDU2BJNF_AUaXjg=="}' https://dcvcheck.cloudflare.com/mpdcv/v1

# Create file, copy both logs into it (DNS+HTTP)
file="${0%.*}.log" 
> $file 
echo -e "\tHTTP REQUESTS:" >> $file
cat /var/log/apache2/access.log >> $file
echo -e "\n\tDNS REQUESTS:" >> $file
cat /var/log/bind/query >> $file

# Clear logs again 
#> /var/log/apache2/access.log  
#> /var/log/bind/query 
 
# Print output
echo
cat $file
