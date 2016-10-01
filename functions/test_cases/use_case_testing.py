#-*- encoding: utf-8 -*-
import os
import sys
import traceback


path = os.sep.join(__file__.split(os.sep)[:-2])
sys.path.append(path)

from render_state import mash

with open('test_grains.yml', 'r') as g:
	grains = g.read()
with open('test_pillar.yml', 'r') as p:
	pillar = p.read()
with open('test_states.sls', 'r') as s:
	states = s.read()

def parse_state_tests(states):
	""" yields each test state from test_states.sls """

	states      = states.split('\n')
	testname    = ""
	begin_state = False
	state_test  = []
	
	for line in states:
		if line.startswith("{# ====== TEST"):
			begin_state = True
			testname = line.replace("{# ====== ", "").replace("====== #}","")

		if line.startswith("{# ====== END"):
			begin_state = False

		if begin_state:
			state_test.append(line)

		if not begin_state and state_test != []:
			returnable_data = state_test
			test_name  = testname
			state_test = [] # reset
			testname   = ""
			state      = "\n".join(returnable_data)
			
			yield state, test_name


lj=60
for state in parse_state_tests(states):

	test = mash(grains, pillar, state[0])


	if test[1] == "fail" and not "FAIL_ON_PURPOSE" in state[1]:
		print state[1].ljust(lj, '-') + " FAILED"
		print test[0]

	elif test[1] != "fail" and "FAIL_ON_PURPOSE" in state[1]:
		print state[1].ljust(lj, '-') + " FAILED"
		print test[0]
	else:
		print state[1].ljust(lj, '-') + " OK"
	
