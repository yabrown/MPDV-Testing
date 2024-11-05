# README

## Overview

This codebase tests the resilience of a Certificate Authority (CA) implementation using Multiple Perspective Issuance Control (MPIC). It sets up or takes an existing configuration of multiple servers and runs simulated hijacks between every possible server pair. For each hijack, it records which perspective (server) contacted which target server, providing insights into the CA’s MPIC resilience.

## Getting Started

### Configuration Setup

Before running the code, you need to provide specific configuration details. Follow these steps:

1. **Create a Config File**:
   - Copy `config.template` to `config.json`:
     ```bash
     cp config.template config.json
     ```
   - Edit `config.json` with the following information:

2. **Configure Server Details**:
   - **Existing Servers**: Add a list of server names and IP addresses to the `nodes` section in `config.json`.
   - **Automatic Server Creation (Optional)**:
     - If you want the code to create servers for you using Vultr, provide the following in `config.json`:
       - Vultr API Key
       - A set of node names mapped to Vultr regions (to specify server locations)
       - Vultr SSH key ID
      - Once the servers are created, their details will automatically be added to `config.json`.
   - Finally, put the servers' private SSH key--they should all be the same--in bgp_pathfinder/key/vultr/vultr.pem (this will be used to run commands on your nodes)


   

3. **Configure Certificate Authority Details**:
   - Specify each Certificate Authority’s:
     - Name
     - Endpoint
     - Any required arguments

### Running the Code

To start the full attack simulation, execute the `all_attacks.py` script:

```bash
python all_attacks.py


Note: This attack simulation can be time-consuming, depending on the number of nodes configured. The attack duration scales with the number of pairwise combinations of nodes, with each attack taking approximately 5–7 minutes.