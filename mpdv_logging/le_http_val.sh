#!/bin/bash

# Clear logs
> /var/log/apache2/access.log
> /var/log/bind/query

# Run certbot for google. Random subdomain added to get around cacheing behavior (done at CA level). 
rand=$(echo $RANDOM)
certbot certonly --manual --manual-auth-hook "bash -c 'exit 1'" -d ${rand}.arins.pretend-crypto-wallet.com --server https://acme-v02.api.letsencrypt.org/directory --non-interactive --agree-tos --email ari.l.braun@gmail.com

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
