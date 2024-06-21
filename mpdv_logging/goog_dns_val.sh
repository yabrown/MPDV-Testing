#!/bin/bash

# Clear logs
> /var/log/apache2/access.log
> /var/log/bind/query

# Run certbot for google. Random subdomain added to get around cacheing behavior.
rand=$(echo $RANDOM)
certbot certonly --apache --force-renew --preferred-challenges dns-01 --domains ${rand}.arins.pretend-crypto-wallet.com --server https://dv.acme-v02.api.pki.goog/directory 

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
