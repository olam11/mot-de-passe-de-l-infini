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

#configuration du titre et du favicon 
st.set_page_config(page_title="mot de passe de l'infini",
                   page_icon=":infinity:")
#configurartion du titre 
st.title("MOT DE PASSE DE L'INFINI")
#configuration de la variable run qui indique le nombre d'itération du programme 
if "run" not in st.session_state:
    st.session_state.run = 0 
st.session_state.run = st.session_state.run+1

if "game" not in st.session_state:
    st.session_state.game = 0 
#configuration de la variable ligne qui indique le nombre d'essai dans une partie
if "ligne"not in st.session_state:
    st.session_state.ligne = 0
#configuration de la liste des mots proposés dans une partie
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
def check(mot_a_verifier, mot_a_trouver):
    for i in range(len(mot_a_verifier)):
        if mot_a_verifier[i] == mot_a_trouver[i]:
            lettres["donné"][i].color = "green"
        else:
            lettres["donné"][i].color = "grey"
  
    a_verifier_temporaire = ""
  
    for i in range(len(mot_a_trouver)):
        if mot_a_trouver[i] != mot_a_verifier[i]:
            a_verifier_temporaire += mot_a_trouver[i]

    for i in range(len(mot_a_verifier)):
        if mot_a_verifier[i] != mot_a_trouver[i] and mot_a_verifier[i] in a_verifier_temporaire:
            lettres["donné"][i].color = "red"
            a_verifier_temporaire = a_verifier_temporaire.replace(mot_a_verifier[i], "", 1)
#configuration du mot à trouver et création de ses 5 lettres
if "mot_a_trouver" not in st.session_state:
    st.session_state.mot_a_trouver = Chaine("","à_trouvé")
    st.session_state.mot_a_trouver.mot_random()
    st.session_state.mot_a_trouver.creer_lettres()

mot = ""
#nettoyage du chmps de texte s'il existe et qu'il contient quelque chose
if "textinput" in st.session_state and st.session_state["textinput"] != "":
    mot = st.session_state["textinput"]
    st.session_state["textinput"] = ""
#configuration du champs de texte avec l'aide
st.text_input(label="###### Proposez un mot de 5 lettres :",max_chars=5,key="textinput",help=f"""
             Vous devez trouver un mot de 5 lettres.    
            Vous pouvez faire 5 propositions de mot de 5 lettres de la langue française.      
            Pour vous aider les lettres seront colorées :       
                \t-en vert les lettres qui sont dans le mot recherché et à la bonne position      
                \t-en rouge les lettres qui sont dans le mot recherché mais pas à la bonne position       
                \t-en gris les lettres qui ne sont pas dans le mot recherché\n
            Exemple :              
            mot recherché : algue       
            mot proposé : danse         
            résultat : :grey[d]:red[a]:grey[ns]:green[e]        
            **Une fois que vous avez gagné (ou perdu), il vous suffit de proposer un nouveau mot pour rejouer !**       
            :grey[{st.session_state.mot_a_trouver.text}]               
             """)
#affichage de l'historique
conteneur = st.container()
for element in st.session_state.historique:
    with conteneur:
        st.markdown(element)
#configuration 
mot_donne = Chaine(mot,"donné")
mot_donne.supprimer_accents()

#si le champs de text contient quelque chose
if mot_donne.text != "":
    #démarrer le chrono  
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    #si le mot est français et contient 5 lettres
    if mot_donne.text in liste_des_mots_francais and len(mot_donne.text) == 5:
        #ajouter une ligne
        st.session_state.ligne = st.session_state.ligne+1
        #créer les lettres du mot
        mot_donne.creer_lettres()
        #fonction de vérification
        check(mot_donne.text,st.session_state.mot_a_trouver.text)
        #ajouter à l'historique le mot avec ses couleurs
        st.session_state.historique.append(str(st.session_state.ligne)+". "+f":{lettres['donné'][0].color}[{lettres['donné'][0].text}]"+
                                           f":{lettres['donné'][1].color}[{lettres['donné'][1].text}]"+
                                           f":{lettres['donné'][2].color}[{lettres['donné'][2].text}]"+
                                           f":{lettres['donné'][3].color}[{lettres['donné'][3].text}]"+
                                           f":{lettres['donné'][4].color}[{lettres['donné'][4].text}]")
        #écrire le mot avec ses couleurs
        st.markdown(st.session_state.historique[st.session_state.ligne-1])
        #si lemot proposé et égal au mot à trouver
        if mot_donne.text == st.session_state.mot_a_trouver.text:
            #ligne = 5 pour finir la partie
            st.session_state.ligne = 5
            #écrire des félicitations
            st.write("****Bravo, vous avez trouvé !!****")
            #arrêter le chrono
            end_time = time.time()
            #définir le temps en secondes et minutes 
            if round(end_time-st.session_state.start_time)//60<1:
                temps = str(round(end_time-st.session_state.start_time)%60)+ " sec !"
            elif round(end_time-st.session_state.start_time)//60>0:
                temps = str(round(end_time-st.session_state.start_time)//60)+" min et "+ str(round(end_time-st.session_state.start_time)%60)+ " sec !"
            if "meilleur_temps" not in st.session_state:
                st.session_state.meilleur_temps = end_time-st.session_state.start_time
            if end_time-st.session_state.start_time < st.session_state.meilleur_temps:
                st.session_state.meilleur_temps = end_time-st.session_state.start_time
            #écrire le temps pris
            st.write(f"***Vous avez trouvé en {temps}***")
    #ou si le mot n'est pas français ou ne contient pas 5 lettres
    elif mot_donne.text not in liste_des_mots_francais or len(mot_donne.text) != 5  :
            #écrire "Le mot n'est pas francais ou ne fait pas 5 lettres" 
            st.error("Le mot n'est pas francais ou ne fait pas 5 lettres",icon="⚠️")
#si ligne = 4 alors prévenir que cela seras la dernière proposition
if st.session_state.ligne == 4:
    st.write(f":red[Il vous reste 1 essai, vous y êtes presque !]")
#si ligne = 5 alors la partie est fini          
if st.session_state.ligne == 5:
    st.session_state.game = st.session_state.game+1
    #écrire "le mot était+lemot" et "Pour rejouer, proposez un nouveau mot !"
    st.write(f"Le mot était {st.session_state.mot_a_trouver.text} !") 
    st.write("Pour rejouer, proposez un nouveau mot !") 
    if st.button("rejouer") :
        conteneur = ""
    #supprimer les éléments de la partie pour rejouer au besoin  
    del st.session_state.ligne  
    del st.session_state.mot_a_trouver
    del st.session_state.historique
    del st.session_state.start_time
    
if "meilleur_temps" in st.session_state:
    if round(st.session_state.meilleur_temps)//60<1:
                meilleur_temps_tmp = str(round(st.session_state.meilleur_temps)%60)+ " sec !"
    elif round(st.session_state.meilleur_temps)//60>0:
                meilleur_temps_tmp = str(round(st.session_state.meilleur_temps)//60)+" min et "+ str(round(st.session_state.meilleur_temps)%60)+ " sec !"
    if st.session_state.game != 1 :
        st.caption(f"Votre meilleur temps sur cette session est {meilleur_temps_tmp}")
