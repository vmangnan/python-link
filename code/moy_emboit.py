#CALCUL D'UNE SIMPLE MOYENNE
def moy_simple(l):
           tot,n=0,0
           for x in l:
                      tot+=x
                      n+=1
           return (1.0*tot)/n

def decoup_liste(l):
	moy=moy_simple(l)
	res=[moy]
	res2=[moy]
	for i in range(len(l)):
		if l[i]<moy: res+=[l[i]]
		else:   res2+=[l[i]]
		
	res.sort();res2.sort()	
	return res,res2	

#CALCUL D'UNE MOYENNE EMBOITEE {intervalle:couleur}
def moy_emboitees(l,k):
	l.sort()
	l1=[(l,0)]
	for i in range(k):
		l_temp=[]
		nb=0
		for x in l1:
			if x[0]<>[]:
			#d_temp[tuple([y for y in x if y<=moy_simple(x)])]=nb
 
			    res,res2=decoup_liste(x[0])
			    l_temp+=[(res,nb)]
			    l_temp+=[(res2,nb+1)]
			    nb+=2
		l1=l_temp
	l1.sort()
	return [(y[0],y[1]*120/2.0**k) for y in l1]
	
#INTERVALLE POUR MOYENNE EMBOITEE  
def categorie(lmoy,x):
	for y in range(len(lmoy)):
		if x>lmoy[y][0][0] and x<=lmoy[y][0][-1]:
			return lmoy[y][1]
		elif x==lmoy[0][0][0]:
			return lmoy[0][1]
	return lmoy[-1][1]

if __name__=="__main__":
	l=[1.0/x**2 for x in range(1,20)]
	#print l
	print "\n"
	d=moy_emboitees(l,2)
	for e in d: print e
	print "\n"
	#print decoup_liste(l)
	print categorie(d,0.1)
      
