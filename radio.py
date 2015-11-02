f = open("adjacent-states","r")

#states stores name of state as a key and values as a tuple storing its neighbour states 
states = dict()
for line in f:
	states[line.split()[0]] = tuple(line.split()[1:])
#domain value in a CSP	
domain = ('A','B','C','D')
#states_freq stores a state as a key and possible assignment of frequencies to that particular state
states_freq = dict()
for key in states.keys():
	states_freq[key] = list(domain)
max_state = max(states, key = lambda k: len(states[k]))	
print states[max_state]

