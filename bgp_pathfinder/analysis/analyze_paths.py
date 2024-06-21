#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import matplotlib.pyplot as plt
import numpy as np


def parse_args():
	parser = argparse.ArgumentParser()
	# This is a CAIDA AS topology.
	parser.add_argument("-p", "--paths_file",
	                    default="../output/paths.txt")
	return parser.parse_args()


def main(args):
	pathsList = []
	for line in open(args.paths_file):
		sline = line.strip()
		if sline == "":
			continue
		jline = json.loads(sline)
		pathsList.append(jline['paths'])
	pathCounts = [len(p) for p in pathsList]
	flattendPaths = [p for pl in pathsList for p in pl]
	asPaths = [p[0] for p in flattendPaths]
	communitySets = [p[1] for p in flattendPaths]
	#allUsedCommunities = set()
	#for communitySet in communitySets:
	#	for community in communitySet:
	#		allUsedCommunities.add(community)
	#print(json.dumps(list(allUsedCommunities)))
	#exit()
	asns = [asn for asPath in asPaths for asn in asPath]
	asnsAndCounts = [(asn, asns.count(asn)) for asn in set(asns)]
	asnsAndCounts.sort(key = lambda asnAndCount: -asnAndCount[1])
	print(asnsAndCounts[3:20])
	pathCounts.sort()
	pathCountAverage = sum(pathCounts) / len(pathCounts)
	print(f"Max paths: {pathCounts[-1]}, min paths: {pathCounts[0]}, median paths: {pathCounts[int(len(pathCounts) * .5)]}, average paths: {pathCountAverage}")
	plt.plot(pathCounts, np.arange(0, 1, 1 / len(pathCounts)))
	plt.xlabel("Path Count")
	plt.ylabel("CDF")

	plt.show()
	#plt.hist(pathCounts, cumulative=True, label='CDF',
    #     histtype='step', alpha=0.8, color='k')
	#plt.show()

	for i in range(pathCounts[-1]):
		pathCount = i + 1
		print(f"node pairs with {pathCount} different paths: {len([l for l in pathCounts if l == pathCount])}")
	#print([pl for pl in pathsList if len(pl) == 12])



if __name__ == '__main__':
    main(parse_args())