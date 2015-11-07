'''
1)This is a classical CSP. I am using backtracking search algorithm to solve this CSP.
To optimize this code I have implmented arc_consistency, a type of constrained propogation method in the solution.
2)I haven't assumed anything which is not specified in problem statement. 
Only problem I have faced is lack of test cases. It would have been great if more test cases were given.
3)Solution & Analysis:
I am selecting unassigned variables such that it's having least possible domain values, i.e. MRV heuristic.
Then I am iterating over every possible value in its domain to find suitable assignment. If no assignment is found I try to backtrack. If still no solution, I return from recursion getting no solution.
If an assignment to variable is found then I chose a variable from its neighbours having least MRV value and continue to the resursion.
For backtrack I am maintaining a list(stack) of last_assignment.
This code can be optimized by applying degree heuristic in variable selection in case of tie for MRV heuristic.
'''
import sys

#states stores name of state as a key and values as a tuple storing its neighbour states 
f1 = open("adjacent-states","r")
states = dict()
for line in f1:
	states[line.split()[0]] = tuple(line.split()[1:])
f1.close()

#domain value in a CSP	
domain = ('A','B','C','D')
#states_domain stores a state as a key and possible assignment of frequencies to that particular state
states_domain = dict()
for key in states.keys():
	#Initialize every state's domain with all possible domains
	states_domain[key] = list(domain)

init_assignment = dict() #Stores value for legacy constraint. 
#Reading constrainst file
f2 = open(sys.argv[1],"r")
for line in f2:
	temp = line.split()
	if len(temp) > 1:
		init_assignment[temp[0]] = temp[1]
		states_domain[temp[0]] = list(temp[1])
f2.close()

def assign(state,frequency,states_domain,assignment,last_assignment):	
	assignment[state] = frequency
	states_domain[state] = [frequency]
	last_assignment.append(state)

def unassign(state,states_domain,assignment):
	states_domain[state] = list(set(domain) - set(assignment[state]))
	del assignment[state]

#Return the state having maximum no of neighbourhood states and unassigned frequency  
def selUnassignedVar(states,states_domain,assignment,neighbour_stack = []):
	for key in assignment.keys():
		if key in neighbour_stack:			
			neighbour_stack.remove(key)
	if len(neighbour_stack) != 0:
		#Return one of neighbour state having least number of domain possibilities remaining
		#MRV Heuristic
		temp = sorted(neighbour_stack, key = lambda k: len(states_domain[k]))
		return temp[0]
	else:
		#If no neighbour is remaining after particular assignment, return a state from remaining unassigned states having least number of domain possibilities remaining
		#MRV Heuristic
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
	return False

backtrack_counter = 0
neighbour_stack = []
last_assignment = [] #Works as a stack to store last assignment, so this can be used in backracking.
#Calling csp backtrack algo
sol = csp_backtrack(states,states_domain)
f3 = open("results.txt","w")
if sol is False or sol == None or len(sol) < 50:
	print 'No solution found'
	f3.write('')
else:
	for k,v in sol.items():
		f3.write(k+' '+v+'\n')
f3.close()	
print 'Number of backtracks: ',backtrack_counter