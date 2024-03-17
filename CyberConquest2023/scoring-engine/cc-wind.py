#!/usr/bin/env python
# @Name: cc-wind.py
# @Project: CyberConquest/scoring-engine
# @Author: Gaelin Shupe
# @Created: 3/25/23

# USAGE: ./cc-wind.py BOXIP USERNAME PASSWORD

import hashlib
import sys

import requests

box_ip = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]

auth_token = hashlib.md5(f"{user}:{password}".encode()).hexdigest()

requests.get(f"{box_ip}?auth_token={auth_token}")
