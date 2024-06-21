#!/bin/bash


# directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Update the config files for pathfinder
$SCRIPT_DIR/update_pathfinder_config.py 
cp -r $SCRIPT_DIR/pathfinder_config/* $SCRIPT_DIR/../bgp_pathfinder/config/ 
echo "*******UPDATED PATHFINDER CONFIG FILES*******"

# Test that everything works
$SCRIPT_DIR/../bgp_pathfinder/send_cmd.py "hostname"

# Configure nodes for pathfinder
echo "*******CONFIGURING NODES FOR PATHFINDER*******"
$SCRIPT_DIR/../bgp_pathfinder/scripts/configure_nodes.sh

# Configure nodes for MPDV testing
echo "*******CONFIGURING NODES FOR MPDV TESTING*******"

echo "'~/' '$SCRIPT_DIR/testing_tools' -p"
#$SCRIPT_DIR/../bgp_pathfinder/multi_scp.py "'~/' '$SCRIPT_DIR/testing_tools'"

nodes_file="$SCRIPT_DIR/nodes.json"
ips=$(jq -r '.[]' "$nodes_file")
for ip in $ips; do
  scp -i $SCRIPT_DIR/../bgp_pathfinder/keys/vultr/vultr.pem -r $SCRIPT_DIR/testing_tools root@$ip:~ && echo -e "--COPIED TOOLS TO $ip\n"
done

$SCRIPT_DIR/../bgp_pathfinder/send_cmd.py "cd ~/testing_tools; ./suit-up.sh"