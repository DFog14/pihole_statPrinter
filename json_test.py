#!/usr/bin/env python

import json
import urllib2

url = "http://192.168.1.30/admin/api.php"
data = json.load(urllib2.urlopen(url))
blocked = data['ads_blocked_today']
percent = data['ads_percentage_today']
queries = data['dns_queries_today']
domains = data['domains_being_blocked']

print blocked, percent, queries, domains
