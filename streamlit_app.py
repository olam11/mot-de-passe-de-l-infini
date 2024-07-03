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
import pandas as pd
# importation du module de création de tableau pour le garphique

#configuration du titre et du favicon 
st.set_page_config(page_title="mot de passe de l'infini",
                   page_icon=":infinity:")

# boite de dialogue pour annoncer la nouvelle version
@st.experimental_dialog("Nouvelle version ! 😉 ")
def message_modif():
    st.markdown("""#### Les nouveautés :\n
👈 Des statistiques sur votre session apparaissent dans le panneau latéral ainsi qu'une aide
           
Les mot s'affichent de bas en haut et plus de haut en bas pour une meilleure expérience sur mobile :       
1.:grey[d]:red[a]:grey[ns]:green[e]        
2.:green[a]:grey[l]:grey[gu]:green[e] 
        
Mais plutôt :     
2.:green[a]:grey[l]:grey[gu]:green[e]         
1.:grey[d]:red[a]:grey[ns]:green[e]

Merci beaucoup aux 40 utilisateurs actuels pour leur participation et leurs retours très positifs ! 👍
             """)
    if st.button("j'ai compris !"):
        st.rerun()

# fonction pour afficher dans une baite de diaogue l'aide       
@st.experimental_dialog("Aide")
def aide():
    st.write(f"""
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
             """)   

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

# fonction pour écrire l'historique des mots 
def write_historique():
    container = st.container()
    len_historique = len(st.session_state.historique)
    for i in range(len_historique):
        with container:
            st.markdown(st.session_state.historique[-(i+1)])
                        
#configurartion du titre 
st.title("MOT DE PASSE DE L'INFINI")

#configuration de la variable run qui indique le nombre d'itération du programme 
if "run" not in st.session_state:
    st.session_state.run = 0
    
# ajout de 1 à run   
st.session_state.run = st.session_state.run+1

#configuration de la variable game qui indique le nombre de partie(s) jouée(s)
if "game" not in st.session_state:
    st.session_state.game = 0 
    
#configuration de la variable game_perdue qui indique le nombre de partie(s) perdue(s)
if "game_perdue" not in st.session_state:
    st.session_state.game_perdue = 0 
    
#configuration de la variable game_gagnee qui indique le nombre de partie(s) gagnée(s)
if "game_gagnee" not in st.session_state:
    st.session_state.game_gagnee = 0 

#configuration de la liste des temps d'une session
if "historique_des_temps" not in st.session_state:
    st.session_state.historique_des_temps = []  

#configuration de la variable ligne qui indique le nombre d'essai dans une partie
if "ligne"not in st.session_state:
    st.session_state.ligne = 0
    
#configuration de la liste des mots proposés dans une partie
if "historique" not in st.session_state:
    st.session_state.historique = []  
    
#configuration du mot à trouver et création de ses 5 lettres
if "mot_a_trouver" not in st.session_state:
    st.session_state.mot_a_trouver = Chaine("","à_trouvé")
    # selection du mot au hasard
    st.session_state.mot_a_trouver.mot_random()
    # création de ses 5 lettres 
    st.session_state.mot_a_trouver.creer_lettres()

# configuation de mot
mot = ""

#nettoyage du champs de texte s'il existe et qu'il contient quelque chose
if "textinput" in st.session_state and st.session_state["textinput"] != "":
    # mot = le mot proposé dans le champs  de texte
    mot = st.session_state["textinput"]
    st.session_state["textinput"] = ""
   
#configuration du champs de texte
st.text_input(label="###### Proposez un mot de 5 lettres :",max_chars=5,key="textinput")

#configuration de l'objet mot_donne avec comme texte : mot
mot_donne = Chaine(mot,"donné")

# suppression de ses accent s'il y en a  
mot_donne.supprimer_accents()

#si le champs de text contient quelque chose
if mot_donne.text != "":
    
    #si le mot est français et contient 5 lettres
    if mot_donne.text in liste_des_mots_francais and len(mot_donne.text) == 5:
        
        #démarrer le chrono  
        if "start_time" not in st.session_state:
            st.session_state.start_time = time.time()
        
        #ajouter une ligne
        st.session_state.ligne = st.session_state.ligne+1
        
        #créer les lettres du mot donne
        mot_donne.creer_lettres()
        
        #fonction de vérification
        check(mot_donne.text,st.session_state.mot_a_trouver.text)
        
        #ajouter du mot avec ses couleurs à l'historique 
        st.session_state.historique.append(str(st.session_state.ligne)+". "+f":{lettres['donné'][0].color}[{lettres['donné'][0].text}]"+
                                           f":{lettres['donné'][1].color}[{lettres['donné'][1].text}]"+
                                           f":{lettres['donné'][2].color}[{lettres['donné'][2].text}]"+
                                           f":{lettres['donné'][3].color}[{lettres['donné'][3].text}]"+
                                           f":{lettres['donné'][4].color}[{lettres['donné'][4].text}]")

        #si le mot proposé et égal au mot à trouver
        if mot_donne.text == st.session_state.mot_a_trouver.text :
            
            #arrêter le chrono
            end_time = time.time()
            
            #ligne = 5 pour finir la partie
            st.session_state.ligne = 5
            
            # ajouter 1 à game gagnée
            st.session_state.game_gagnee = st.session_state.game_gagnee+1
            
            #écrire des félicitations
            st.write("****Bravo, vous avez trouvé !!****")
            
            # ajout du nouveau temps a l'historique des temps
            st.session_state.historique_des_temps.append(end_time-st.session_state.start_time)
            
            #définir le temps en secondes et minutes 
            if round(end_time-st.session_state.start_time)//60<1:
                temps = str(round(end_time-st.session_state.start_time)%60)+ " sec !"
            elif round(end_time-st.session_state.start_time)//60>0:
                temps = str(round(end_time-st.session_state.start_time)//60)+" min et "+ str(round(end_time-st.session_state.start_time)%60)+ " sec !"
                
            # configuration de meilleur temps avec le premier temps
            if "meilleur_temps" not in st.session_state:
                st.session_state.meilleur_temps = end_time-st.session_state.start_time
                
            # si le nouveau temps est meilleur que le meilleur temps alors remplacer le meilleur temps par le nouvaeu temps
            if end_time-st.session_state.start_time < st.session_state.meilleur_temps:
                st.session_state.meilleur_temps = end_time-st.session_state.start_time
                
            #écrire le temps pris
            st.write(f"Vous avez trouvé en {temps}")
            
    #ou si le mot n'est pas français ou ne contient pas 5 lettres
    elif mot_donne.text not in liste_des_mots_francais or len(mot_donne.text) != 5  :
        
            #écrire "Le mot n'est pas francais ou ne fait pas 5 lettres" 
            st.error("Le mot n'est pas francais ou ne fait pas 5 lettres",icon="⚠️")

#si ligne = 4 alors prévenir que cela seras la dernière proposition
if st.session_state.ligne == 4:
    
    st.info(f"Il vous reste 1 essai, vous y êtes presque !",icon="👍")

#  si la partie n'est pas terminée alors ecrire l'historique des mots   
if st.session_state.ligne != 5:
    write_historique()
              
#si ligne = 5 alors la partie est fini          
if st.session_state.ligne == 5:
    
    # si mot pas trouvé alors ajouter 1 a game_perdue
    if mot_donne.text != st.session_state.mot_a_trouver.text:
         st.session_state.game_perdue = st.session_state.game_perdue+1
         
    # ajouter 1 a game, une nouvelle partie a été jouée
    st.session_state.game = st.session_state.game+1
    
    #écrire "le mot était+lemot"
    st.write(f"Le mot était {st.session_state.mot_a_trouver.text} !")
    
    # bouton pour rejouer
    if st.button("rejouer") :
        st.rerun()
        
    #  si la partie est terminée alors ecrire l'historique des mots après les phrases de fin      
    write_historique()
    
    #supprimer les éléments de la partie pour rejouer au besoin  
    st.session_state.ligne = 0
    st.session_state.historique = []
    del st.session_state.mot_a_trouver
    del st.session_state.start_time



# nettoyage de la sidebar 
st.sidebar.empty()

# dans la sidebar
with st.sidebar:
    
    # afficher un titre : Sur cette session
    st.title("Sur cette session : ")
    
    # afficher le nombre de partie(s) jouée(s)
    st.write("Partie(s) jouée(s): ",f":green[{str(st.session_state.game)}]")
    
    # afficher le nombre de partie(s) gagnée(s)
    st.write("Partie(s) gagnée(s) : ",f":green[{str(st.session_state.game_gagnee)}]")
    
    # afficher le nombre de partie(s) perdue(s)
    st.write("Partie(s) perdue(s) : ",f":red[{str(st.session_state.game_perdue)}]")
    
    # si il y a un meilleur temps alors
    if "meilleur_temps" in st.session_state:
        
        # le mettre en minutes et secondes 
        if round(st.session_state.meilleur_temps)//60<1:
                    meilleur_temps_tmp = str(round(st.session_state.meilleur_temps)%60)+ " sec !"
        elif round(st.session_state.meilleur_temps)//60>0:
                    meilleur_temps_tmp = str(round(st.session_state.meilleur_temps)//60)+" min et "+ str(round(st.session_state.meilleur_temps)%60)+ " sec !"
                    
        #si c'est le deuxième temps alors afficher le meilleur temps et un graphique des temps
        if st.session_state.game_gagnee > 1 :
            st.write(f"Meilleur temps : :green[{meilleur_temps_tmp}]")
            chart_data = pd.DataFrame(st.session_state.historique_des_temps, columns=["Temps"])
            st.write("Vos temps : ")
            st.line_chart(chart_data)
            
        
    # si aide est cliquée  alors afficher l'aide dans une boite de diologue
    if st.button("Aide"):
        aide() 
# si c'est le premier run alors afficher les nouveautés avec des ballons 
if st.session_state.run == 1:
    st.balloons()
    time.sleep(1.20) 
    message_modif()
