#!/usr/bin/env python3
import requests
import re
import os
import sys
import time
import textwrap
import random
import datetime
import subprocess
import json
from bgp_pathfinder.pathfinder import main as pathfinder
from bgp_pathfinder.send_cmd import main as send_cmd
from bgp_pathfinder.engines.vultr import copy_file_from_node_name as copy_file

dir_path = os.path.dirname(os.path.realpath(__file__)) 

def ips_from_file(filename, token):
  ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}')
  ips = []
  with open(filename, 'r') as file:
    for line in file:
      if token in line:
        ip = ip_pattern.match(line)
        if not ip: print(f"IP not found in matched line: {line}")
        ips.append(ip)
  return ips

# Function that makes a single cert req and pulls the resulting logs from both nodes
def cert_request_and_log(cert_name, cert_req_dict, node_a, node_b):

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
  

  retries = 3
  for attempt in range(retries):
      response = requests.post(**cert_req_dict)
      with open(f"{dir_path}/results/http.log", 'a') as file:
          now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + 'Z'
          if attempt>0: file.write(f"Attempt {attempt}:\n")
          file.write(f"\t{now} {cert_req_dict}\n")
          file.write(f"\t{now} {response.text}\n")
      if response.status_code == 200:
          break
      elif attempt < retries - 1:
          print(f"Attempt {attempt + 1} failed with status code {response.status_code}. Waiting 10 seconds and retrying...")
          time.sleep(10)
      else:
          raise Exception(f"Failed after {retries} attempts with status code {response.status_code}.")

  # create and compose log files in both nodes
  send_cmd([compose_log(a_filename), "-d", node_a]) # run at A, name a-b
  send_cmd([compose_log(b_filename), "-d", node_b]) # run at B, name b-a

  # copy files over locally from both nodes
  copy_file(a_filename, node_a, "./results/logs")
  copy_file(b_filename, node_b, "./results/logs")

  # get IPs
  token = "hijacks_are_bad"
  node_a_ips = ips_from_file(f"./results/logs/{a_filename}", token)
  node_b_ips = ips_from_file(f"./results/logs/{b_filename}", token)


  #log the relevant information
  with open(f"{dir_path}/results/summary.log", 'a') as file:
    formatted_line = f"{node_a} {node_b}:\t{len(node_a_ips)}, {len(node_b_ips)}\tTotal: {len(node_a_ips)+len(node_b_ips)}\n"
    file.write(formatted_line)


def attack(node_a, node_b):
  args = ["-d", node_a,  node_b, "-i", "66.180.191.0/24"]
  pathfinder(["-w"])  # make announcments-- equivalent of calling pathfinder from command line with above args
  pathfinder(args)    # make announcments-- equivalent of calling pathfinder from command line with above args

  # wait five minutes
  time.sleep(300)
  
  start = time.time()
  rand = random.randint(0, 100_000_000)
  
  gg_prem_name = "ggp"
  gg_prem_req = {
      "url": "http://34.75.246.52:5000/run-all",
      "headers": {
         'Content-Type': 'application/json'
      },
      "json": {
        "domain": "123123123.arins.pretend-crypto-wallet.com",
        "token": "hijacks_are_bad"
      }
  }
  gg_free_name = "ggf"
  gg_free_req = {
      "url": "http://35.211.239.179:5000/run-all",
      "headers": {
        'Content-Type': 'application/json'
      },
      "json": {
        "domain": "123123123.arins.pretend-crypto-wallet.com",
        "token": "hijacks_are_bad"
      }
  }

  with open("configure/config.json", "r") as file:
    open_mpic_api_key = json.load(file)["mpic_api_key"]
  open_mpic_name = "om"
  open_mpic_req = {
     "url": "https://anor3x6mtj.execute-api.us-east-2.amazonaws.com/v1/mpic",
     "headers": {
      "Content-Type": "application/json",
        "x-api-key": open_mpic_api_key
     },
     "json": {
        "orchestration_parameters": {
          "perspective_count": 13,
          "max_attempts": 1
        },
        "check_type": "dcv",
        "domain_or_ip_target": "123233.arins.pretend-crypto-wallet.com",
        "dcv_check_parameters": {
          "validation_method": "http-generic",
          "validation_details": {
            "http_token_path": "/bgp_hijacks_are_bad",
            "challenge_value": "test"
          }
        }
     }
  }
  with open(f"{dir_path}/results/http.log", 'a') as file:
      file.write(f"{node_a}, {node_b}:\n")
  cert_request_and_log(open_mpic_name, open_mpic_req, node_a, node_b)
  cert_request_and_log(gg_prem_name, gg_prem_req, node_a, node_b)
  cert_request_and_log(gg_free_name, gg_free_req, node_a, node_b)

  end = time.time()
  print("Total time for all attacks between this pair of nodes= ", end-start)


 
if __name__ == "__main__":
  script_dir = os.path.dirname(os.path.abspath(__file__))

  # check correct number of arguments
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



