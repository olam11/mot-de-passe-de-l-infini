#importations
import unidecode
#importation de la librairie qui permet d'enlever les accents et les cédilles
from database import*
#importation des listes de mots
import random
#importation du hasard pour déterminer un mot au hasard
from termcolor import*
#importation de la librairie qui permet de colorer le texte imprimer par print()

#class Chaine : une chaine de caractère 
class Chaine():
    def __init__(self,text,statut):
        self.text = text
        #le texte de la chaine de caractère
        self.statut = statut
        #son statut : si elle est choisie au hasard ou donnée par l'utilisateur
      
    def supprimer_accents(self):
        self.text = unidecode.unidecode(self.text)
        #méthodepour supprimer les accents et les cédilles 
        
    def mot_random(self):
        self.text = liste_des_mots_francais_courants[random.randint(0,len(liste_des_mots_francais_courants)-1)]
        #méthode pour choisir un mot au hasard
        
    def creer_lettres(self):
        lettres[self.statut] = [] 
        for i in range(5):
            lettres[self.statut].append(Caractere(self.text[i],i+1,self.statut)) 
        #méthode pour créer 5 objets "caractère" qui sont les 5 lettres du mot
  
#class Caractere : une lettre du mot de class Chaine    
class Caractere(Chaine):
    def __init__(self, text,position,statut):
        super().__init__(text,statut)
        #héritage de la class Chaine 
        self.color = ""
        #couleur du caractère
        self.text = text
        #le texte du caractère
        self.statut = statut
        #son statut : s'il est choisi au hasard ou donné par l'utilisateur
        self.position = position
        #sa position dans le mot
        

#fonction de vérification 
def check(mot_a_verifier, mot_a_trouve):
    for i in range(len(mot_a_verifier)):
        if mot_a_verifier[i] == mot_a_trouve[i]:
            lettres["donné"][i].color = "green"
        else:
            lettres["donné"][i].color = "white"
  
    a_verifier_temporaire = ""
  
    for i in range(len(mot_a_trouve)):
        if mot_a_trouve[i] != mot_a_verifier[i]:
            a_verifier_temporaire += mot_a_trouve[i]

    for i in range(len(mot_a_verifier)):
        if mot_a_verifier[i] != mot_a_trouve[i] and mot_a_verifier[i] in a_verifier_temporaire:
            lettres["donné"][i].color = "red"
            a_verifier_temporaire = a_verifier_temporaire.replace(mot_a_verifier[i], "", 1)
        
#assignations    
mot_a_trouve = Chaine("","à_trouvé")
mot_a_trouve.mot_random()
mot_a_trouve.creer_lettres()

#boucle pour les 5 essais 
i = 0
while i != 5:
    i = i+1
    #demander un mot de 5 lettres
    mot_donne = Chaine(input(str(i)+".proposez un mot de 5 lettres : "),"donné")
    mot_donne.supprimer_accents()
    #vérifier qu'il est francais et fait bien 5 lettres
    if mot_donne.text in liste_des_mots_francais and len(mot_donne.text) == 5:
        mot_donne.creer_lettres()
        check(mot_donne.text,mot_a_trouve.text)
        #affiche les résultats
        cprint(lettres["donné"][0].text,lettres["donné"][0].color, end="")
        cprint(lettres["donné"][1].text,lettres["donné"][1].color, end="")
        cprint(lettres["donné"][2].text,lettres["donné"][2].color, end="")
        cprint(lettres["donné"][3].text,lettres["donné"][3].color, end="")
        cprint(lettres["donné"][4].text,lettres["donné"][4].color)
        
        if mot_donne.text == mot_a_trouve.text:
            #si gagné alors arrêter la boucle
            print('Bravo vous avez trouvé !')
            i = 5
    elif mot_donne.text not in liste_des_mots_francais or len(mot_donne.text) != 5:
        #si pas francais alors enlever un essai
        print("Le mot n'est pas francais ou ne fait pas 5 lettres")
        i = i -1
   
if mot_donne.text != mot_a_trouve.text:        
    print("Vous avez perdu, le mot était : "+mot_a_trouve.text+" !")
