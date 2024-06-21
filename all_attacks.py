#!/usr/bin/env python3

from bgp_hijack import attack
import json

if __name__ == "__main__":
  with open('configure/nodes.json', 'r') as file:
    nodes = list(json.load(file).keys())
  print(nodes)
  for i in range(len(nodes)):
    for j in range(i+1, len(nodes)):
      attack(nodes[i], nodes[j])