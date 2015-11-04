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
assignment = dict()
def assign(state,frequency,assignment):	
	assignment[state] = frequency
	#print assignment
#	return assignment

def unassign(state,assignment):
	del assignment[state]
#	return assignment

#Return the state having maximum no of neighbourhood states and unassigned frequency  
def selUnassignedVar(states,states_domain,assignment,c):
	#print states_domain
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
		print 'True'
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
	c+=1
	#print c
	if len(assignment.keys()) == len(states.keys()):
		return assignment
	var = selUnassignedVar(states,states_domain,assignment,c)
	for value in states_domain[var]:
		if (isConsistent(states[var],value,assignment)):
			#print var,value,assignment
			assign(var,value,assignment)
			print var, value,c, str(len(assignment)), assignment,
			#new_state_domain 
			if arc_consistency(states,var,states_domain,assignment):
				result = csp(states,states_domain,assignment)
				#print assignment
				#print result
				if result != None:
					print 'Result True'
					return result
			else:
				print 'Backtrack'
				unassign(var,assignment)

sol = csp(states,states_domain,assignment)
print len(sol)
for i in states.keys():
	print i, sol[i], [i+sol[i] for i in states[i]]
			






