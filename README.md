# real-world-mpdv-testing
Repo for testing mpdv deployments with real BGP attacks.

First thing you have to do is spin up servers (on some service, now we're using vultr).
Then, add all the node names and ip addresses that you want to be in the network to 'configure/nodes.json'-- that controls everything else.
Then, run ./configure/config.sh, which configures all nodes in the network with everything needed (see that readme for details). 
Then, can run ./bgp-hijack node1 node2, which runs a single experiment (multiple cert requests from all CAs, logs each).