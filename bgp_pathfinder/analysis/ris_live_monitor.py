#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import websocket



def parse_args():
	parser = argparse.ArgumentParser()
	# This is a CAIDA AS topology.
	parser.add_argument("-p", "--single_peer",
	                    default="")
	return parser.parse_args()


def main(args):
	ws = websocket.WebSocket()
	ws.connect("wss://ris-live.ripe.net/v1/ws/?client=py-example-1")
	params = {
		"prefix": "2604:4540:80::/47",
		#"prefix": None,
	    "moreSpecific": True,
	    "host": None,
	    #"host": "rrc21.ripe.net", # None means all collectors.
	    "socketOptions": {
	        "includeRaw": True,
	        "acknowledge": True
	    }
	}
	ws.send(json.dumps({
		"type": "ris_subscribe",
		"data": params
	}))
	maxASLength = 0
	for data in ws:
	    parsed = json.loads(data)
	    #print(parsed["type"], parsed["data"])
	    if parsed["type"] == "ris_subscribe_ok":
	    	print(parsed["type"], parsed["data"])
	    elif parsed["type"] == "ris_message":# and 'withdrawals' not in parsed["data"]:
	    	if args.single_peer != "":
	    		if parsed["data"]["peer_asn"] != args.single_peer:
	    			continue
	    	if "announcements" in parsed["data"]:
	    		for announcement in parsed["data"]["announcements"]:
	    			if "2604:4540:80::/48" in announcement["prefixes"] or "2604:4540:81::/48" in announcement["prefixes"]:
	    				print(parsed["type"], parsed["data"])
	    	if "withdrawals" in parsed["data"]:
	    		if "2604:4540:80::/48" in parsed["data"]["withdrawals"] or "2604:4540:81::/48" in parsed["data"]["withdrawals"]:
	    			print(parsed["type"], parsed["data"])
	    	
	    	#print(parsed["type"], parsed["data"])
	    	#try:
	    	#	asLength = len(parsed["data"]["path"])
	    	#	if asLength > maxASLength:
	    	#		maxASLength = asLength
	    	#	print(maxASLength)
	    	#except:
	    	#	print(parsed["type"], parsed["data"])



if __name__ == '__main__':
    main(parse_args())