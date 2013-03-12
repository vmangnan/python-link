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
import re, string
import zlib as Z

def distance(doc1,doc2):
	conc = doc1.indata+doc2.indata
	conc_compr = Z.compress(conc)
	distanc=1-((1.0*(doc1.t_outdata+doc2.t_outdata-len(conc_compr)))/max(doc1.t_outdata,doc2.t_outdata))
	return distanc

def applatir(element):
	if element==None:
		return None
	if not isinstance(element,tuple):
		return [element]
	return applatir(element[0])+applatir(element[1])

####################################
class Document(object):
	def __init__(self,chemin):
		self.chemin=chemin
		self.indata = open(chemin, "rb").read()
		self.outdata = Z.compress(self.indata)
		self.t_outdata = len(self.outdata)
	def __repr__(self):
		return self.chemin

####################################
class DicoDistance(object):
	def __init__(self,dossier):
		self.liste={}
		l=[Document(dossier+"/"+x) for x in os.listdir(dossier)]
		for x in l:
			for y in l:
				x1=str(x)
				y1=str(y)
				if not self.liste.has_key((y1,x1)):
					self.liste[(x1,y1)]=distance(x,y)
					
		
		self.l_fichier=l
		
	def __repr__(self):
		return str(self.liste)

####################################
class Noeud(object):
  def __init__(self,valeur,branche_gauche,branche_droite):
    self.va=valeur
    self.bg=branche_gauche
    self.bd=branche_droite
    
  def __repr__(self):
    return "Noeud"+str((self.va,self.bg,self.bd))

####################################
class Dendrogramme(object):
	def __init__(self,dossier):
		self.dico_interne=DicoDistance(dossier)
		self.racine_min=None
		self.racine_max=None
		self.racine_moy=None
		self.initialisation()
	   
	def initialisation(self):
		l_cle_min=[]
		l_cle_max=[]
		l_cle_moy=[]

		l_nd_min=[]
		l_nd_max=[]
		l_nd_moy=[]

		for x in self.dico_interne.l_fichier:
			l_cle_min+=[x]
			l_cle_max+=[x]
			l_cle_moy+=[x]

		a=self.min_dist
		b=self.max_dist
		c=self.moy_dist

                self.construction(l_cle_min,l_nd_min,a)
                self.construction(l_cle_max,l_nd_max,b)
                self.construction(l_cle_moy,l_nd_moy,c)

        def construction(self,l_cle,l_nd,fonction):
		tmp_len=len(l_cle)
                if tmp_len>1:
                          tampon_min=1
                          tampon_cle=(None,None)
                          for x in l_cle:
                                  for y in l_cle:
					if x<>y:
						try:
							if self.dico_interne.liste[(str(x),str(y))]<tampon_min:
								tampon_min=self.dico_interne.liste[(str(x),str(y))]
								tampon_cle=(x,y)
						except:
							if fonction(x,y)<tampon_min:
								tampon_min=fonction(x,y)
								tampon_cle=(x,y)

                          l_cle.append(tampon_cle)
                          l_cle.remove(tampon_cle[0])
                          l_cle.remove(tampon_cle[1])

			  l_nd.append(Noeud(tampon_min,tampon_cle[0],tampon_cle[1]))

                          self.construction(l_cle,l_nd,fonction)
		else:
			  tmp=l_nd[(len(l_nd)-1)]
			  if "min_dist" in str(fonction):
				  self.racine_min=tmp
				  self.assemblage(self.racine_min,fonction)
			  else:
				  if "max_dist" in str(fonction):
					  self.racine_max=tmp
					  self.assemblage(self.racine_max,fonction)
				  else:
					  self.racine_moy=tmp
					  self.assemblage(self.racine_moy,fonction)

	def assemblage(self,nd,fonction):
		if isinstance(nd,Noeud):
			nd.bg=self.assemblage(nd.bg,fonction)
			nd.bd=self.assemblage(nd.bd,fonction)
		else:
			if isinstance(nd,tuple):
				nd=Noeud(fonction(nd[0],nd[1]),nd[0],nd[1])
				nd.bg=self.assemblage(nd.bg,fonction)
				nd.bd=self.assemblage(nd.bd,fonction)
			else:
				return nd
		return nd

	def min_dist(self,g1,g2):
		tmp_g1=applatir(g1)
		tmp_g2=applatir(g2)
		tmp_min=1
		for x in tmp_g1:
			for y in tmp_g2:
				if x<>y:
					try:
						if self.dico_interne.liste[(str(x),str(y))]<tmp_min:
							tmp_min=self.dico_interne.liste[(str(x),str(y))]
					except:
						if self.dico_interne.liste[(str(y),str(x))]<tmp_min:
							tmp_min=self.dico_interne.liste[(str(y),str(x))]

		return tmp_min

	def max_dist(self,g1,g2):
		tmp_g1=applatir(g1)
		tmp_g2=applatir(g2)
		tmp_max=0
		for x in tmp_g1:
			for y in tmp_g2:
				if x<>y:
					try:
						if self.dico_interne.liste[(str(x),str(y))]>tmp_max:
							tmp_max=self.dico_interne.liste[(str(x),str(y))]
					except:
						if self.dico_interne.liste[(str(y),str(x))]>tmp_max:
							tmp_max=self.dico_interne.liste[(str(y),str(x))]
		return tmp_max

	def moy_dist(self,g1,g2):
		tmp_g1=applatir(g1)
		tmp_g2=applatir(g2)
		tmp_moy=0
		tmp_compteur=0
		for x in tmp_g1:
			for y in tmp_g2:
				if x<>y:
					try:
						tmp_moy+=self.dico_interne.liste[(str(x),str(y))]
					except:
						tmp_moy+=self.dico_interne.liste[(str(y),str(x))]
					tmp_compteur+=1
					

		tmp_moy=(tmp_moy/(tmp_compteur*1.0))
		return tmp_moy

       	def __repr__(self):
          	return "je suis un dendrogramme" 
