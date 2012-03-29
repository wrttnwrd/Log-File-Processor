# /usr/bin/python
# Reads in botbase, compares to logfile and processes
# generates site bot report
from __future__ import generators
from sys import argv
import os, sys
import csv
import time

csv.field_size_limit(1000000000000000)
if len(sys.argv) != 3:
	print 'Usage: logprocessor.py <bot list file> <log file>'

botBase = sys.argv[1]
logFile = sys.argv[2]
resultsFile = 'botscanresults.txt'
brokeFile = 'bustedlinks.txt'
b = open(botBase,'U')

bots = csv.reader(b)

bBase = {}
results = []
badLinks = []
ips = []
tip = []
# first, read in the botbase and build a list of agent names and ips - not the most efficient but it's portable




print "Building robots database..."

for row in bots:
	bAgent = row[0]
	bAgent = bAgent.strip()
	bip = row[3]
	bip = bip.replace('#','')
	bip = bip.strip()
	bBase[bip] = bAgent


print "Processing log file..."

l = open(logFile,'U')
counter = 0
x = l.read()
l.close()
for r in x:
	if r.find(','):
		deLim = ','
	elif r.find('-'):
		deLim = '-'
	else:
		delim = 'none'
	counter = counter + 1
	if counter > 2:
		break 


l = open(logFile,'U')
log = csv.reader(l, delimiter = ' ')
counter = 0

header = 'Search engine\tIP address\tDate visited\tURL visited\tMode\tStatus code\tBytes transferred\tAgent\n'
results.append(header)

for row in log:
	counter = counter + 1
	ip = row[0]
	ip = ip.strip()
	agent = row[9]
	sCode = row[6]
	bytes = row[7]
	theDate = row[3]
	theDate = theDate.replace('[','')
	URL = row[5]
	URL = URL.split(' ')
	thisURL = URL[1]
	method = URL[0]
	if ip in bBase:
		nextline = bBase[ip] + '\t' + ip + '\t' + theDate + '\t' + thisURL + '\t' + method + '\t' + sCode  + '\t' + bytes + '\t' + agent
		results.append(nextline)
			

l.close()

r = open(resultsFile,'a')



for rs in results:
	rs = rs + "\n"
	r.write(rs)

print "Done - now looking for 404s. Processed ", counter, " lines of log file data, by the way."

l = open(logFile,'U')
log = csv.reader(l, delimiter = ' ')
counter = 0

header = "URL\tResponse code\tDate crawled\tReferrer\n"
badLinks.append(header)

for row in log:
	sCode = row[6]
	if (sCode.find('200') == -1) & (sCode.find('301') & (sCode.find('304'))):
		URL = row[5]
		URL = URL.split(' ')
		thisURL = URL[1]
		method = URL[0]
		theDate = row[3]
		theDate = theDate.replace('[','')
		referrer = row[8]
		nextline = thisURL + "\t" + sCode + "\t" + theDate + "\t" + referrer + "\n"
		badLinks.append(nextline)
		
l.close()

r = open(brokeFile,'a')

for rs in badLinks:
	r.write(rs)
	
print "Done. Files were saved to wherever you put the logs. They're called botscanresults.txt and bustedlinks.txt. Knock yourself out."