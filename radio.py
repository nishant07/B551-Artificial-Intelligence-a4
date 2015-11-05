f = open("adjacent-states","r")

#states stores name of state as a key and values as a tuple storing its neighbour states 
states = dict()
for line in f:
	states[line.split()[0]] = tuple(line.split()[1:])

#domain value in a CSP	
domain = ('A','B','C','D')
#states_domain stores a state as a key and possible assignment of frequencies to that particular state
states_domain = dict()
for key in states.keys():
	states_domain[key] = list(domain)
#assignment = {}
last_assignment = []
#assignment = {'California': 'A','Ohio': 'A','Texas': 'B'}
assignment = {'Florida': 'A','Texas': 'B','California': 'A','Washington' :'A','New_York': 'B','Pennsylvania': 'C','Maine': 'A','Minnesota': 'A','Idaho': 'C','Alaska': 'A','Louisiana': 'A','Nebraska':'A','Montana': 'A','Indiana': 'C','Georgia': 'D','Nevada': 'D'}
for key in assignment.keys():
	states_domain[key] = [assignment[key]]
neighbour_stack = []
for i in assignment.keys():
	for j in states[i]: 
		if j not in neighbour_stack:
				neighbour_stack.append(j)
	last_assignment.append(i)
def assign(state,frequency,assignment):	
	assignment[state] = frequency
	last_assignment.append(state)
	print "Last assi",last_assignment
	#print assignment
#	return assignment

def unassign(state,assignment):
	states_domain[state] = list(set(domain) - set(assignment[state]))
	neighbour_stack.append(state)
	del assignment[state]

#	return assignment

#Return the state having maximum no of neighbourhood states and unassigned frequency  
def selUnassignedVar(states,states_domain,assignment,neighbour_stack):
	#print states_domain
	print "In selVar neighbour_stack",neighbour_stack
	if len(neighbour_stack) != 0:
		for key in assignment.keys():
			if key in neighbour_stack:
				neighbour_stack.remove(key)
		print "after removal",neighbour_stack
		if len(neighbour_stack) != 0:
			return neighbour_stack.pop()
		else:
			temp = sorted(states_domain, key = lambda k: len(states_domain[k]))
	#print len(assignment.keys())
			temp = [i for i in temp if len(states_domain[i]) == len(states_domain[temp[len(assignment.keys())]])]
			return max(set(temp) - set(assignment.keys()), key = lambda k: len(states[k]))
	else:
			temp = sorted(states_domain, key = lambda k: len(states_domain[k]))
	#print len(assignment.keys())
			temp = [i for i in temp if len(states_domain[i]) == len(states_domain[temp[len(assignment.keys())]])]
			return max(set(temp) - set(assignment.keys()), key = lambda k: len(states[k]))
	#temp = states_domain.keys()
	#print len(temp)
	#print temp
	#return temp[c]
#selUnassignedVar(states,states_domain)

def arc_consistency(states,state,states_domain,assignment):
	for key in states[state]:
		#print key
		#for state in states[key]:
		if assignment[state] in states_domain[key]:
			states_domain[key].remove(assignment[state])
		#print states_domain[key]
	states_domain[state] = [assignment[state]]
	print states_domain[state]
	if min(states_domain, key = lambda k: len(states_domain[k])) == 0:
		print 'Zero domain'
		return False
	else:
		return True
#	return states_domain			

def isConsistent(neighbour_states,freq,assignment):
	for neighbour in neighbour_states:
		if (assignment.get(neighbour,None) == freq):
			print 'Not consistent'
			return False
	return True
#Solves CSP
c = 0

def csp(states,states_domain,assignment):
	global c
	global neighbour_stack
	global last_assignment
	
	#print c
	if len(assignment.keys()) == len(states.keys()):
		return assignment
	
	var = selUnassignedVar(states,states_domain,assignment,neighbour_stack)
	print "Var",var,":neighbour",states[var]
	if len(states[var])!=0:
		for i in states[var]:
			if i not in neighbour_stack:
				neighbour_stack.append(i)
	print "Neighbour_stack",neighbour_stack
	print "Remaining domain",var,states_domain[var]
	for value in states_domain[var]:
		print var,":",value
		if (isConsistent(states[var],value,assignment)):
		#if arc_consistency(states,var,states_domain,assignment):
			#print var,value,assignment
			assign(var,value,assignment)
			print var, value,c, str(len(assignment)), assignment,
			#new_state_domain 
			#if (isConsistent(states[var],value,assignment)):
			if arc_consistency(states,var,states_domain,assignment):
				result = csp(states,states_domain,assignment)
				#print assignment
				#print result
				if result != None:
					print 'Result True'
					return result
				else:
					c+=1
					print 'Backtrack'
					unassign(last_assignment.pop(),assignment)

sol = csp(states,states_domain,assignment)
print c
print len(sol)
for k,v in states.items():
	if sol[k] in [sol[i] for i in v]:
		'Alert'
	print sol[k],":",[sol[i] for i in v]

	#print i, sol[i], [i+sol[i] for i in states[i]]
			






