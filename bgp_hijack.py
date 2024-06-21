#!/usr/bin/env python3

import os
import sys
import time
import textwrap
import random
import datetime
import subprocess
from bgp_pathfinder.pathfinder import main as pathfinder
from bgp_pathfinder.send_cmd import main as send_cmd
from bgp_pathfinder.engines.vultr import copy_file_from_node_name as copy_file

# Function that makes a single cert req and pulls the resulting logs from both nodes
def cert_request_and_log(cert_name, cert_req_cmd, node_a, node_b):

  #name files (first node is origin of log, second is hijack partner)
  a_filename = f"{node_a}_{node_b}_{cert_name}.log"
  b_filename = f"{node_b}_{node_a}_{cert_name}.log"
  # command to clear log files
  clear_logs = textwrap.dedent('''
    > /var/log/apache2/access.log;
    > /var/log/bind/query;
  ''')
  # command to pull from log files to create summary
  compose_log = lambda filename: textwrap.dedent(f'''
    > {filename};
    echo -e \"\tHTTP REQUESTS:\" >> {filename};
    cat /var/log/apache2/access.log >> {filename};
    echo -e \"\n\tDNS REQUESTS:\" >> {filename};
    cat /var/log/bind/query >> {filename};
    > /var/log/apache2/access.log;
    > /var/log/bind/query;
  ''')

  # runs clear_logs script (defined above) at both nodes
  send_cmd([clear_logs, "-d", node_a, node_b])

  # runs cert specific cert-req-cmd at main [1]
  print(cert_req_cmd)
  send_cmd([cert_req_cmd, "-d", "main"])
  #time.sleep(10)

  # create and compose log files in both nodes
  send_cmd([compose_log(a_filename), "-d", node_a]) # run at A, name a-b
  send_cmd([compose_log(b_filename), "-d", node_b]) # run at B, name b-a

  # copy files over locally from both nodes
  copy_file(a_filename, node_a, "./logs")
  copy_file(b_filename, node_b, "./logs")

def attack(node_a, node_b):
  args = ["-d", node_a,  node_b, "-i", "66.180.191.0/24"]
  pathfinder(["-w"])  # make announcments-- equivalent of calling pathfinder from command line with above args
  pathfinder(args)    # make announcments-- equivalent of calling pathfinder from command line with above args

  # wait five minutes
  time.sleep(300)
  
  start = time.time()
  for i in range(5):
    rand = random.randint(0, 100_000_000)
    cf_name, cf_req_cmd = f"cf-{i}",  f'curl -X POST -d \'{{"method":"acme/http-01","kaHash":"TfPD9o_Mg7J-nULJBDGnJJnxeHXIGlmbVmyYiblpZwM=","token":"aaaaaaaaaaaaaaaaaaaaa", "domain":"{rand}.arins.pretend-crypto-wallet.com","accessToken":"YTrWJscsDU2BJNF_AUaXjg=="}}\' https://dcvcheck.cloudflare.com/mpdcv/v1'
    cert_request_and_log(cf_name, cf_req_cmd, node_a, node_b)
  for i in range(5):
    rand = random.randint(0, 100_000_000)
    gg_name, gg_req_cmd = f"gg-{i}", f"certbot certonly --domains {rand}.arins.pretend-crypto-wallet.com --server https://dv.acme-v02.test-api.pki.goog/directory --force-renew --apache"
    cert_request_and_log(gg_name, gg_req_cmd, node_a, node_b)
  rand = random.randint(0, 100_000_000)
  le_name, le_req_cmd = "le", f"certbot certonly --manual --manual-auth-hook \"bash -c 'exit 1'\" -d {rand}.arins.pretend-crypto-wallet.com --server https://acme-staging-v02.api.letsencrypt.org/directory --non-interactive --agree-tos --email ari.l.braun@gmail.com"
  cert_request_and_log(le_name, le_req_cmd, node_a, node_b)
  end = time.time()
  print("Total MPDV time= ", end-start)


 
if __name__ == "__main__":
  script_dir = os.path.dirname(os.path.abspath(__file__))

  # check arguments
  if len(sys.argv)==1: 
    print("Please add arguments.")
    exit()
  if len(sys.argv)%2 == 0: #script call throws off by 1
    print("Number of args must be even. Number is", len(sys.argv)-1)
    exit()

  # for each pair
  for i in range(0, len(sys.argv)//2): 
    node_a = sys.argv[2*i+1]
    node_b = sys.argv[2*i+2]
    start = time.time()
    attack(node_a, node_b)
    end = time.time()
    print("Total attack time = ", end-start)
    
    

# [1] currently run at main bc it's set up with everything. Once this entire module is downloaded to a server fully fitted with certbot 
# and everything, can run certbot command locally. technically each cert has different requirements for request to be run: cf uses curl,
# so it actually can be run anywhere, let's encrypt uses certbot so it needs that, google requires gcloud sign-in. 



