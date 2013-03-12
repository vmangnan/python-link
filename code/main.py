# -*- coding: utf-8 -*-
# Pour valentin:
# - Refaire et resumer le corpus (taille doc, langue choisie, taille corpus total) 8 doc traduit dans 5 langues
# - Diagramme min,moy,max (implique dendrogramme_moy et dendrogramme_max)
# - Parcours du dendrogramme selon les branches les plus peuples pour determiner un ordre de lecture
# - Mettre a jour le drive


#IMPORT ET CONSTANTES
#==============================================================================#

import sys
import os
import time
import re, string
import zlib as Z
import pylab as P
from write_html import *
from classes import *

#FONCTIONS PRATIQUES
#==============================================================================#

def compter_feuille(nd):
	if nd==None:
		return 0
	if not isinstance(nd,Noeud):
		return 1
	return compter_feuille(nd.bg)+compter_feuille(nd.bd)

def lecture(nd):
	if nd==None:
		return None
	if not isinstance(nd,Noeud):
		return [nd]
	if compter_feuille(nd.bg)>=compter_feuille(nd.bd):
		return lecture(nd.bg)+lecture(nd.bd)
	else:
		return lecture(nd.bd)+lecture(nd.bg)

#COMMANDES D'ACTIVATION
#==============================================================================#

try:
	os.mkdir("html")
except:
	pass

tmp=sys.argv[1].split('/')[1]

try:
	os.mkdir("html/"+tmp)
except:
	pass

den=Dendrogramme(sys.argv[1])

if sys.argv[2]=="all":
	write_file("html/"+tmp+"/index_min.html",pre+tableau(den,"min",int(sys.argv[3]))+post)
	write_file("html/"+tmp+"/index_max.html",pre+tableau(den,"max",int(sys.argv[3]))+post)
	write_file("html/"+tmp+"/index_moy.html",pre+tableau(den,"moy",int(sys.argv[3]))+post)

	P.plot([i for i in range(len(lecture_va(den.racine_min)))],sorted(lecture_va(den.racine_min)),"-b")
	P.plot([i for i in range(len(lecture_va(den.racine_max)))],sorted(lecture_va(den.racine_max)),"-r")
	P.plot([i for i in range(len(lecture_va(den.racine_moy)))],sorted(lecture_va(den.racine_moy)),"-g")

	P.savefig("html/"+tmp+"/figure.png")
else:
	write_file("html/"+tmp+"/index_"+sys.argv[2]+".html",pre+tableau(den,sys.argv[2],int(sys.argv[3]))+post)
