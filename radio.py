f = open("adjacent-states","r")

#states stores name of state as a key and values as a tuple storing its neighbour states 
states = dict()
for line in f:
	states[line.split()[0]] = tuple(line.split()[1:])

'''
for key in states.keys():
	print key,len(states[key])
print  max(states, key = lambda k: len(states[k]))
'''
#domain value in a CSP	
domain = ('A','B','C','D')
#states_freq stores a state as a key and possible assignment of frequencies to that particular state
states_freq = dict()
for key in states.keys():
	states_freq[key] = list(domain)
#Return the state having maximum no of neighbourhood states and unassigned frequency  
def selUnassignedVar(states,states_freq):
	#print max(states, key = lambda k: len(states[k]))
	return max(states, key = lambda k: len(states[k]) + len(states_freq[k]))

assignment = dict()
def arc_consistency(states,states_freq,assignment):

#Solves CSP
def csp(states,domain):
	pass



