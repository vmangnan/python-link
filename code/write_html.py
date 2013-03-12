# -*- coding: utf-8 -*-

from moy_emboit import *
from classes import *

pre="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
		      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" >
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta name="author" content="Author's name" />
	<meta name="keywords" content="" />
	<meta name="description" content="" />
	<meta name="robots" content="all" />
	<title>Page's title</title>
</head>

<body>

<div>
	<table style="collapse:collapse;" cellspacing="0">"""

post="""
</table>
</div>

</body>

</html>"""


#ECRITURE DANS UN FICHIER
def write_file(path_file, s) :
  f = open(path_file, 'w')
  f.write(s)
  f.close()

#COMPTER FEUILLE D'UN ARBRE
def compter_feuille(nd):
	if nd==None:
		return 0
	if not isinstance(nd,Noeud):
		return 1
	return compter_feuille(nd.bg)+compter_feuille(nd.bd)

#REND UNE LISTE ORDONNEE D'UN ARBRE
def lecture(nd):
	if nd==None:
		return None
	if not isinstance(nd,Noeud):
		return [nd]
	if compter_feuille(nd.bg)>=compter_feuille(nd.bd):
		return lecture(nd.bg)+lecture(nd.bd)
	else:
		return lecture(nd.bd)+lecture(nd.bg)

def lecture_va(nd):
	if nd==None:
		return []
	if not isinstance(nd,Noeud):
		return []
	if compter_feuille(nd.bg)>=compter_feuille(nd.bd):
		return lecture_va(nd.bg)+[nd.va]+lecture_va(nd.bd)
	else:
		return lecture_va(nd.bd)+[nd.va]+lecture_va(nd.bg)

#TRONCATURE D'UN FLOTTANT
def tronc(floa):
  return float(str(floa)[0:4])

#APPLATISSEMENT D'UN DICO
def dicotolst(d):
  l=[]
  for x in d:
	  l+=[d[x]]
  return l

#CREATION D'UN TABLEAU
def tableau(dendro,mode,nbit):
  tmp=""
  d_emboit=moy_emboitees(dicotolst(dendro.dico_interne.liste),nbit)

  if mode=="min":
	arbre=lecture(dendro.racine_min)
  elif mode=="max":
	arbre=lecture(dendro.racine_max)
  else:
	arbre=lecture(dendro.racine_moy)

  for i in arbre:
	  tmp+="<tr>"
	  for j in arbre:
		  i=str(i)
		  j=str(j)
		  res=0
		  if dendro.dico_interne.liste.has_key((i,j)):res=dendro.dico_interne.liste[(i,j)]
		  else: res=dendro.dico_interne.liste[(j,i)]
		  
		  #print int(categorie(d_emboit,res))
		  tmp+='<td style="background-color:hsl(' + str(int(categorie(d_emboit,res)))  +', 100%, 50%);">'    +str(tronc(res))   +"</td>\n"

	  tmp+="<td>"+str(i)+"</td>\n" #nom du fichier a droite
	  tmp+="</tr>\n\n"
  tmp+="<tr>"
  for e in arbre:
	  tmp+='<td valign="top" style="font-size:11px;">'
	  for k in str(e): 
	          tmp+=str(k)+"<br/>"
	  tmp+="</td>\n" #nom du fichier en bas
  tmp+="</tr>"
  return tmp
