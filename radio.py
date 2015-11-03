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
def selUnassignedVar(states,states_domain,assignment):
	#print states_domain
	temp = sorted(states_domain, key = lambda k: len(states_domain[k]))
	print len(assignment.keys())
	temp = [i for i in temp if len(states_domain[i]) == len(states_domain[temp[len(assignment.keys())]])]
	#return max(set(temp) - set(assignment.keys()), key = lambda k: len(states[k]))
	temp = states_domain.keys()
	#print temp
	return temp[len(assignment.keys())]
#selUnassignedVar(states,states_domain)

def arc_consistency(states,state,states_domain,assignment):
	for key in states[state]:
		#print key
		#for state in states[key]:
		states_domain[key].remove(assignment[state])
	if min(states_domain, key = lambda k: len(states_domain[k])) == 0:
		return False
	else:
		return True
#	return states_domain			

def isConsistent(states,freq,assignment):
	for neighbour in states.keys():
		if (assignment.get(neighbour,None) == freq):
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
	var = selUnassignedVar(states,states_domain,assignment)
	for value in states_domain[var]:
		if (isConsistent(states,value,assignment)):
			#print var,value,assignment
			assign(var,value,assignment)
			print var, value, assignment
			#new_state_domain 
			if arc_consistency(states,var,states_domain,assignment):
				result = csp(states,states_domain,assignment)
				#print assignment
				#print result
				if result != None:
					return result
			else:
				unassign(var,assignment)

sol = csp(states,states_domain,assignment)
print sol
			






