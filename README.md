# real-world-mpdv-testing
Repo for testing mpdv deployments with real BGP attacks.

Steps to run:
1) spin up servers (on some service, now we're using vultr).
2) add all the node names and ip addresses that you want to be in the network to 'configure/nodes.json'-- that controls everything else.
3) run ./configure/config.sh, which configures all nodes in the network with everything needed (see that readme for details). 
4) run ./bgp-hijack node1 node2, which runs a single experiment (multiple cert requests from all CAs, logs each).
