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
#	return assignment

def unassign(state,assignment):
	del assignment[state]
#	return assignment

#Return the state having maximum no of neighbourhood states and unassigned frequency  
def selUnassignedVar(states,states_domain,assignment):
	temp = sorted(states_domain, key = lambda k: len(states_domain[k]))
	temp = [i for i in temp if len(states_domain[i]) == len(states_domain[temp[0]])]
	#temp = sorted(states, key = lambda k: len(states[k]))
	#temp = [i for i in temp if len(states[i]) == len(states[temp[0]])]
	#states_domain[temp[0]] = [1,2,3,4,5,6]
	#print len(states_domain[temp[0]]),len(states_domain[temp[1]])
	return max(set(temp) - set(assignment.keys()), key = lambda k: len(states[k]))
#selUnassignedVar(states,states_domain)

def arc_consistency(states,state,states_domain,assignment):
	for key in states:
		for state in states[key]:
			states_domain[state].remove(assignment[key])
#	return states_domain			

def isConsistent(states,freq,assignment):
	for neighbour in states:
		if (assignment.get(neighbour,None) == freq):
			return False
	return True
#Solves CSP
def csp(states,states_domain,assignment):
	if len(assignment.keys()) == len(states.keys()):
		return assignment
	var = selUnassignedVar(states,states_domain,assignment)
	for value in states_domain[var]:
		if (isConsistent(states,value,assignment)):
			assign(var,value,assignment)
			#new_state_domain 
			arc_consistency(states,var,states_domain,assignment)
			if min(states_domain, key = lambda k: len(states_domain[k])) == 0:
				return False






