NFA = {
	0:{'a':[], 'b':[], 'ee':[1,7]},
	1:{'a':[], 'b':[], 'ee':[2,4]},
	2:{'a':[3], 'b':[], 'ee':[]},
	3:{'a':[], 'b':[], 'ee':[6]},
	4:{'a':[], 'b':[5], 'ee':[]},
	5:{'a':[], 'b':[], 'ee':[6]},
	6:{'a':[], 'b':[], 'ee':[1,7]},
	7:{'a':[8], 'b':[], 'ee':[]},
	8:{'a':[], 'b':[9], 'ee':[]},
	9:{'a':[], 'b':[], 'ee':[]},
}

NFA_info = {
	'start':0,
	'end':{
		9:'Name'
	},
	'edge':['a','b']
}

ee_closure ={}
start = 0

def update_closure(oldlist,currentlist):
	newlist = []
	for node in currentlist:
		oldlist.append(node)
		for newnode in NFA[node]['ee']:
			if newnode not in oldlist and newnode not in currentlist and newnode not in newlist:
				newlist.append(newnode)

	if newlist:
		newlist.sort()
		update_closure(oldlist,newlist)
		return
	else:
		return

def update_DFA(currentDFA,newelement,DFAcounter):
	currentDFA.setdefault(DFAcounter,newelement)
	DFAcounter += 1

	for edge in NFA_info['edge']:
		tempelement =[]
		for node in newelement:	
			for neighbernode in NFA[node][edge]:
				
				tempelement = list(set(tempelement+ee_closure[neighbernode]))

		tempelement.sort()
		elementstate=0
		for (number,element) in currentDFA.iteritems():
			if tempelement==element:
				elementstate=1
		if elementstate==0 and tempelement:
			update_DFA(currentDFA,tempelement,DFAcounter)


for (node,info) in NFA.iteritems():
	closurelist = [node]
	newlist = []
	for newnode in info['ee']:
		if newnode !=node:
			newlist.append(newnode)
	update_closure(closurelist,newlist)
	closurelist.sort()
	ee_closure.setdefault(node,closurelist)

print "eeclosrue:"
print ee_closure
DFA = {}
update_DFA(DFA,ee_closure[start],0)

print "DFA:"
print DFA







