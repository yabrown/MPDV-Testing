#!/usr/bin/env python3

from bgp_hijack import attack
import json
import time
import signal
import threading
import sys
import traceback

# Watchdog ensures threads that hang for too long raise an exception
def thread_watchdog(timeout=300, interval=300):
    start_times = {thread.ident: time.time() for thread in threading.enumerate()}
    
def load_nodes_from_config():
  try:
    with open('configure/config.json', 'r') as file:
      config = json.load(file)
      nodes = [node for node in config['nodes'].keys() if node != "main"] # filter out 'main'
    return nodes
  except Exception as error:
    raise error
  
def load_state_from_file():
  try:
      with open('results/state.json', 'r') as file:
          state_data = json.load(file)
      return state_data
  except Exception as error:
      raise error


if __name__ == "__main__":
  nodes = load_nodes_from_config()
  state = load_state_from_file()

  # starting point depends on whether we're continuing a previous run
  a_start = nodes.index(state['curr_node_a']) if state['mid_test'] == True else 0
  b_start = nodes.index(state['curr_node_b']) if state['mid_test'] == True else a_start+1

  for i, node_a in enumerate(nodes[a_start:], start=a_start):
    for node_b in nodes[b_start if i==a_start else i+1:]:
      # update state file to current attack pair
      with open('results/state.json', 'w') as file:
        state['mid_test'] = True
        state['curr_node_a'] = node_a
        state['curr_node_b'] = node_b
        json.dump(state, file)
      attack(node_a, node_b)

  with open('results/state.json', 'w') as file:
    state['mid_test'] = False
    json.dump(state, file)