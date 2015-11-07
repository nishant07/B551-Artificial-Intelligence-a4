import time
import sys
init = time.clock()
f1 = open("adjacent-states","r")


#states stores name of state as a key and values as a tuple storing its neighbour states 
states = dict()
for line in f1:
	states[line.split()[0]] = tuple(line.split()[1:])
f1.close()

#states = {'NM':('OK','TX'),'OK':('NM','TX','AR'),'AR':('OK','TX','LA'),'LA':('AR','TX'),'TX':('NM','OK','LA')}
#domain value in a CSP	
domain = ('A','B','C','D')
#states_domain stores a state as a key and possible assignment of frequencies to that particular state
states_domain = dict()
for key in states.keys():
	#Initialize every state's domain with all possible domains
	states_domain[key] = list(domain)

init_assignment = dict()
#Reading constrainst file
f2 = open(sys.argv[1],"r")
for line in f2:
	temp = line.split()
	if len(temp) > 1:
		init_assignment[temp[0]] = temp[1]
		states_domain[temp[0]] = list(temp[1])
f2.close()

#init_assignment = {'California': 'A','Ohio': 'A','Texas': 'B'}
#init_assignment = {'Mississippi': 'B', 'Oklahoma': 'C', 'Wyoming': 'B', 'Minnesota': 'C', 'Illinois': 'C', 'Arkansas': 'D', 'Indiana': 'A', 'Maryland': 'C', 'Louisiana': 'A', 'New_Hampshire': 'A', 'Texas': 'B', 'New_York': 'A', 'Wisconsin': 'A', 'Iowa': 'B', 'Arizona': 'B', 'South_Carolina': 'C', 'Michigan': 'B', 'Kansas': 'B', 'Utah': 'C', 'Virginia': 'D', 'Oregon': 'B', 'Connecticut': 'B', 'Montana': 'C', 'California': 'A', 'Idaho': 'A', 'New_Mexico': 'D', 'South_Dakota': 'A', 'Massachusetts': 'C', 'Vermont': 'B', 'Georgia': 'B', 'Pennsylvania': 'B', 'Florida': 'C', 'Alaska': 'A', 'Kentucky': 'B', 'Hawaii': 'A', 'Nebraska': 'C', 'North_Dakota': 'B', 'Missouri': 'A', 'Ohio': 'C', 'Alabama': 'A', 'New_Jersey': 'C', 'Colorado': 'A', 'Washington': 'C', 'West_Virginia': 'A', 'Tennessee': 'C', 'Rhode_Island': 'A', 'North_Carolina': 'A', 'Nevada': 'D', 'Delaware': 'A', 'Maine': 'B'}
#init_assignment = {'Florida': 'A','Texas': 'B','California': 'A','Washington' :'A','New_York': 'B','Pennsylvania': 'C','Maine': 'A','Minnesota': 'A','Idaho': 'C','Alaska': 'A','Louisiana': 'A','Nebraska':'A','Montana': 'A','Indiana': 'C','Georgia': 'D','Nevada': 'D'}
#init_assignment = {'Alabama':'A','Mississippi':'A'}

def assign(state,frequency,states_domain,assignment,last_assignment):	
	assignment[state] = frequency
	states_domain[state] = [frequency]
	last_assignment.append(state)

def unassign(state,states_domain,assignment):
	states_domain[state] = list(set(domain) - set(assignment[state]))
	del assignment[state]

neighbour_stack = []
#Return the state having maximum no of neighbourhood states and unassigned frequency  
def selUnassignedVar(states,states_domain,assignment,neighbour_stack = []):
	for key in assignment.keys():
		if key in neighbour_stack:			
			neighbour_stack.remove(key)
	if len(neighbour_stack) != 0:
		#Return one of neighbour state having least number of domain possibilities remaining
		temp = sorted(neighbour_stack, key = lambda k: len(states_domain[k]))
		return temp[0]
	else:
		#If no neighbour is remaining after particular assignment, return a state from remaining unassigned states having least number of domain possibilities remaining
		temp = sorted(states_domain, key = lambda k: len(states_domain[k]))
		temp = [i for i in temp if len(states_domain[i]) == len(states_domain[temp[len(assignment.keys())]])]
		return max(set(temp) - set(assignment.keys()), key = lambda k: len(states[k]))

#Performs arc_consistency and return True if it has applied successfully(More than zero domain possibilities remains to neighbours), False otherwise
def arc_consistency(states,state,states_domain,assignment):
	for key in states[state]:
		if assignment[state] in states_domain[key]:
			states_domain[key].remove(assignment[state])
	states_domain[state] = [assignment[state]]
	if min(states_domain, key = lambda k: len(states_domain[k])) == 0:
		print 'Zero domain remaining for neighbours'
		return False
	else:
		return True			

#Check if a frequency assignment is consistent with neighbour states' frequency assignments
def isConsistent(neighbour_states,freq,assignment):
	for neighbour in neighbour_states:
		if (assignment.get(neighbour,None) == freq):
			print 'Not consistent with neighbours'
			return False
	return True

#Backtrack algo implementation
def csp_backtrack(states,states_domain,assignment={}):
	global neighbour_stack, last_assignment
	#Check if an assignment(solution) is found
	if len(assignment.keys()) == len(states.keys()):
		return assignment	
	#neighbour_stack = []
	var = selUnassignedVar(states,states_domain,assignment,neighbour_stack)
	if len(states[var])!=0:
		neighbour_stack = list(states[var])
	
	for value in states_domain[var]:
		if (isConsistent(neighbour_stack,value,assignment)):
			assign(var,value,states_domain,assignment,last_assignment)
			if arc_consistency(states,var,states_domain,assignment):
				result = csp_backtrack(states,states_domain,assignment)
				if result != None:
					return result
				else:
					backtrack_counter+=1
					print 'Backtrack'
					unassign(last_assignment.pop(),states_domain,assignment)

backtrack_counter = 0
neighbour_stack = []
last_assignment = []
#Calling csp backtrack algo
sol = csp_backtrack(states,states_domain)

if sol is False or sol == None:
	print 'No solution found'
else:
	f3 = open("results.txt","w")
	for k,v in sol.items():
		f3.write(k+' '+v+'\n')
	f3.close()	
print 'Total time taken:',time.clock()-init
print 'Number of backtracks: ',backtrack_counter