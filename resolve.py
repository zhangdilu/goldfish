# -*- coding: UTF-8 -*-
import json
import re
def resolveJson(path):
	lines = []
	dicList=[json.loads(line) for line in open(path)]
	return dicList