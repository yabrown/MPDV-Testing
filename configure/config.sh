#!/bin/bash


# directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Update the config files for pathfinder
python3 "$SCRIPT_DIR/update_pathfinder_config.py"
cp -r "$SCRIPT_DIR/pathfinder_config/"* "$SCRIPT_DIR/../bgp_pathfinder/config/"
echo "*******UPDATED PATHFINDER CONFIG FILES*******"

# Test that everything works
python3 "$SCRIPT_DIR/../bgp_pathfinder/send_cmd.py" "hostname"

# Configure nodes for pathfinder
echo "*******CONFIGURING NODES FOR PATHFINDER*******"
"$SCRIPT_DIR/../bgp_pathfinder/scripts/configure_nodes.sh"

# Configure nodes for MPDV testing
echo "*******CONFIGURING NODES FOR MPDV TESTING*******"

echo "'~/' "$SCRIPT_DIR/testing_tools" -p"
#$SCRIPT_DIR/../bgp_pathfinder/multi_scp.py "'~/' '$SCRIPT_DIR/testing_tools'"

nodes="$SCRIPT_DIR/config.json"
ips=$(jq -r '.nodes[]' "$nodes")

for ip in $ips; do
  # Run the scp command in the background
  scp -i "$SCRIPT_DIR/../bgp_pathfinder/keys/vultr/vultr.pem" -r "$SCRIPT_DIR/testing_tools" root@$ip:~ \
  && echo -e "--COPIED TOOLS TO $ip\n" &
done

# Wait for all background jobs to finish
wait

echo "All tools copied to all nodes!"


python3 "$SCRIPT_DIR/../bgp_pathfinder/send_cmd.py" "cd ~/testing_tools; ./suit-up.sh"