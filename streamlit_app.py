#importations
import streamlit as st
#importation de la librairie streamlit
import unidecode
#importation de la librairie qui permet d'enlever les accents et les cédilles
from database import*
#importation des listes de mots
import random
#importation du hasard pour déterminer un mot au hasard
import time
#importation du temps

st.set_page_config(page_title="mot de passe de l'infini",
                   page_icon=":infinity:",
                   menu_items={"about":"Ceci est un site en cours de développement"})
st.title("MOT DE PASSE DE L'INFINI")
st.subheader("Par Malo Gryspeerdt")
if "run" not in st.session_state:
    st.session_state.run = 0    
st.session_state.run = st.session_state.run+1
if "ligne"not in st.session_state:
    st.session_state.ligne = 0
if "historique" not in st.session_state:
    st.session_state.historique = []   
#class Chaine : une chaine de caractère 
class Chaine():
    def __init__(self,text,statut):
        self.text = text
        #le texte de la chaine de caractère
        self.statut = statut
        #son statut : si elle est choisie au hasard ou donnée par l'utilisateur
      
    def supprimer_accents(self):
        self.text = unidecode.unidecode(self.text).lower()
        #méthode pour supprimer les accents et les cédilles 
        
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
            lettres["donné"][i].color = "grey"
  
    a_verifier_temporaire = ""
  
    for i in range(len(mot_a_trouve)):
        if mot_a_trouve[i] != mot_a_verifier[i]:
            a_verifier_temporaire += mot_a_trouve[i]

    for i in range(len(mot_a_verifier)):
        if mot_a_verifier[i] != mot_a_trouve[i] and mot_a_verifier[i] in a_verifier_temporaire:
            lettres["donné"][i].color = "red"
            a_verifier_temporaire = a_verifier_temporaire.replace(mot_a_verifier[i], "", 1)
if "mot_a_trouve" not in st.session_state:
    st.session_state.mot_a_trouve = Chaine("","à_trouvé")
    st.session_state.mot_a_trouve.mot_random()
    st.session_state.mot_a_trouve.creer_lettres()

mot = ""
textinput1 = st.empty() 
if "textinput" in st.session_state and st.session_state["textinput"] != "":
    mot = st.session_state["textinput"]
    st.session_state["textinput"] = ""
textinput1.text_input(label="proposez un mot de 5 lettres :",max_chars=5,key="textinput")
for element in st.session_state.historique:
    st.markdown(element)

mot_donne = Chaine(mot,"donné")
mot_donne.supprimer_accents()


if mot_donne.text != "": 
    if mot_donne.text in liste_des_mots_francais and len(mot_donne.text) == 5:
        st.session_state.ligne = st.session_state.ligne+1
        mot_donne.creer_lettres()
        check(mot_donne.text,st.session_state.mot_a_trouve.text)
        st.session_state.historique.append("#"+str(st.session_state.ligne)+". "+f":{lettres['donné'][0].color}[{lettres['donné'][0].text}]"+
                                           f":{lettres['donné'][1].color}[{lettres['donné'][1].text}]"+
                                           f":{lettres['donné'][2].color}[{lettres['donné'][2].text}]"+
                                           f":{lettres['donné'][3].color}[{lettres['donné'][3].text}]"+
                                           f":{lettres['donné'][4].color}[{lettres['donné'][4].text}]")
        st.markdown(st.session_state.historique[st.session_state.ligne-1])
        
        if mot_donne.text == st.session_state.mot_a_trouve.text:
            st.session_state.ligne = 5
            st.write("Bravo, vous avez trouvé !!")
    elif   mot_donne.text not in liste_des_mots_francais or len(mot_donne.text) != 5  :
            #si pas francais alors enlever un essai
            st.write("Le mot n'est pas francais ou ne fait pas 5 lettres")
        
if st.session_state.ligne == 5:
    st.write(f"le mot était {st.session_state.mot_a_trouve.text} !")    
    del st.session_state.ligne
    del st.session_state.mot_a_trouve
st.write(":red[run]"+" "+str(st.session_state.run)+":red[ times]")

