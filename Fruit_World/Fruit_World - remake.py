'''
    Fruit World est un jeu de simulation consistant à attraper le maximum de fruits tout en évitant les bombes avec votre panier.
    
    Contrôle:
    Flèches Gauche et Droite : Vous permet d'aller respectivement à gauche et à droite
    Barre Espace : Vous permet de sauter pour esquiver les bombes ou attraper des fruits en hauteur.
    Échap: Vous permet de fermer le jeu.
    
    Écran de jeu:
    Score: Affiche votre score en temps réel.
    Temps: Affiche le temps restant.
    
    Points:
    Pomme: Ajoute 1 points.
    Citron: Ajoute 3 points.
    Cerise: Ajoute 5 points.
    Ananas: Ajoute 10 points.
    Bombe: Retire 1 points.
    
    Bonus (Dure 15 secondes):
    Chrono: Ralenti la chute des objets.
    Ombre: Accélère la vitesse de base du personnage.
    Carotte: Permet une meilleur vision des objets.
    Bombe Dorée: Plus aucune bombe n'apparait.
    
================================================

    Fruit World is a simulation game consisting of catching the maximum amount of fruit while avoiding bombs with your hand.
    
    Control:
    Left and Right arrows or Q and D: Allows you to go left and right respectively.
    Space Bar: Lets you jump to dodge bombs or catch fruit in height.
    Esc: Allows you to close the game.
    
    Game screen:
    Score: Displays your score in real time.
    Time: Displays the remaining time.
    
    Points:
    Apple: Add 1 points.
    Lemon: Add 3 points.
    Cherry: Add 5 points.
    Pineapple: Add 10 points.
    Bomb: Remove 1 points.
    
    Bonus (Lasts 15 seconds):
    Chrono: Slows down the fall of objects.
    Shadow: Accelerates the basic speed of the character.
    Carrot: Allows a better vision of objects.
    Golden Bomb: No more bombs appear.
'''

#on ajoute les librairies random et pyxel / we add random and pyxel libraries
import pyxel, random

class Jeu:
    '''Création de la classe gérant le jeu. / Creation of the class managing the game.'''

    def __init__(self):
        '''Fonction créant toutes les variables utiles au jeu.'''

        #Chargement des visuels
        pyxel.load('Fruit_World.pyxres')

        #Info de base du personnage
        self.vitesse = 4
            #Coin Haut Gauche
        self.doodle_x1 = 60
        self.doodle_y1 = 110
            #Coin Bas Gauche
        self.doodle_x2 = 60
        self.doodle_y2 = 118
            #Coin Haut Droite
        self.doodle_x3 = 68
        self.doodle_y3 = 110
            #Coin Bas Droite
        self.doodle_x4 = 68
        self.doodle_y4 = 118

        #Variable pour le saut
        self.doodle_distance = 0
        self.doodle_pos = 0
        self.doodle_max = 0
        self.doodle_dy = 0
        
        #Position du Soleil/Lune
            #Coin Haut Gauche
        self.astre_dessin1 = 0
        self.astre_x1 = 120
        self.astre_y1 = 120
            #Coin Bas Gauche
        self.astre_dessin2 = 8
        self.astre_x2 = 128
        self.astre_y2 = 120
            #Coin Haut Droite
        self.astre_dessin3 = 0
        self.astre_x3 = 120
        self.astre_y3 = 128
            #Coin Bas Droite
        self.astre_dessin4 = 8
        self.astre_x4 = 128
        self.astre_y4 = 128

        #Score au début de la partie
        self.score = 0

        #Valeur pour les niveaux de difficultés
        self.ciel = 6
        self.ratio = (45, 20, 5, 20, 10)

        #Liste pour les éléments du jeu autre que le personnage
        self.objet_liste = [] #[ x, y, type, vitesse de chute]
        self.explosions_liste = []
        self.bonus_liste = [] #[ x, y, type, vitesse de chute]
        self.list_vitesse = [0.50, 1, 1.5, 2]
        
        #Variable pour les bonus
        self.tps_bonus = 0
        self.carotte = 0
        
        #Variable pour le temps
        self.timer = 90
        self.minute = 0
        self.seconde = 0
        
        #Lancement du jeu
        self.ecran = 0
        pyxel.run(self.update_accueil,self.draw_accueil)


    def doodle_deplacement(self):
        '''Fonction pour les déplacements.'''
        
        #Saut
        if pyxel.btn(pyxel.KEY_SPACE):

            if self.doodle_dy == 0:
                self.doodle_max = self.doodle_y1 - 23
                self.doodle_dy = -1
                
        if self.doodle_y1 < self.doodle_max:
            self.doodle_dy = 1

        if self.doodle_y1 > 110:
            self.doodle_y1, self.doodle_y3 = 110, 110
            self.doodle_y2, self.doodle_y4 = 118, 118
            self.doodle_dy = 0

        self.doodle_y1 = self.doodle_y1 + self.doodle_dy
        self.doodle_y2 = self.doodle_y2 + self.doodle_dy
        self.doodle_y3 = self.doodle_y3 + self.doodle_dy
        self.doodle_y4 = self.doodle_y4 + self.doodle_dy

        #Déplacement à droite.
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D)) and self.doodle_x1 <= 108:
            self.doodle_x1 = self.doodle_x1 + self.vitesse
            self.doodle_x2 = self.doodle_x2 + self.vitesse
            self.doodle_x3 = self.doodle_x3 + self.vitesse
            self.doodle_x4 = self.doodle_x4 + self.vitesse

        #Déplacement à gauche.
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q))and self.doodle_x1 >= 4:
            self.doodle_x1 = self.doodle_x1 - self.vitesse
            self.doodle_x2 = self.doodle_x2 - self.vitesse
            self.doodle_x3 = self.doodle_x3 - self.vitesse
            self.doodle_x4 = self.doodle_x4 - self.vitesse


    def objet_creation(self):
        '''Fonction gérant la création des objets.'''
        
        type_objet = [ 0, 1, 2, 3, 4] #0 = Pomme, 1 = Bombe, 2 = Ananas, 3 = Citron, 4 = Cerise
        if (pyxel.frame_count % 30 == 0): #Nouvel objet toutes les 30 frames (environ 1 seconde)
            
            #Aléatoire pour le type de fruit.
            int_objet = random.choices( type_objet, weights=self.ratio, k=1)
            
            #Créé une pomme.
            if int_objet[0] == 0:
                self.objet_liste.append([random.randint(0, 120), 0, int_objet[0], random.choices( self.list_vitesse, weights=(20, 25, 25, 30), k=1)])
                
            #Créé une bombe.
            elif int_objet[0] == 1:
                self.objet_liste.append([random.randint(0, 120), 0, int_objet[0], random.choices( self.list_vitesse, weights=(10, 20, 30, 40), k=1)])
            
            #Créé un Ananas.
            elif int_objet[0] == 2:
                self.objet_liste.append([random.randint(0, 120), 0, int_objet[0], random.choices( self.list_vitesse, weights=(10, 20, 30, 40), k=1)])
            
            #Créé un citron.
            elif int_objet[0] == 3:
                self.objet_liste.append([random.randint(0, 120), 0, int_objet[0], random.choices( self.list_vitesse, weights=(20, 20, 30, 30), k=1)])
            
            #Créé des cerises.
            elif int_objet[0] == 4:
                self.objet_liste.append([random.randint(0, 120), 0, int_objet[0], random.choices( self.list_vitesse, weights=(10, 20, 40, 30), k=1)])
                

    def bonus_creation(self):
        '''Fonction gérant la création des bonus.'''
        
        type_bonus = [ 5, 6, 7, 8] #5 = chrono, 6 = ombre, 7 = carotte, 8 = bombe dorée
        if (pyxel.frame_count % 900 == 0): #Nouveau bonus toutes les 900 frames (environ 30 secondes)
            if random.choices([ 0, 1], weights=(60, 40), k=1) == [1]:
                #Aléatoire pour le type de fruit.
                int_bonus = random.choices( type_bonus, weights=(25, 25, 25, 25), k=1)
                
                #Créé un chrono.
                if int_bonus[0] == 5:
                    self.bonus_liste.append([random.randint(0, 120), 0, int_bonus[0], random.choices( self.list_vitesse, weights=(20, 25, 25, 30), k=1)])
                    
                #Créé une ombre.
                elif int_bonus[0] == 6:
                    self.bonus_liste.append([random.randint(0, 120), 0, int_bonus[0], random.choices( self.list_vitesse, weights=(10, 20, 30, 40), k=1)])
                
                #Créé une carotte.
                elif int_bonus[0] == 7:
                    self.bonus_liste.append([random.randint(0, 120), 0, int_bonus[0], random.choices( self.list_vitesse, weights=(10, 20, 30, 40), k=1)])
                
                #Créé une bombe dorée.
                elif int_bonus[0] == 8:
                    self.bonus_liste.append([random.randint(0, 120), 0, int_bonus[0], random.choices( self.list_vitesse, weights=(20, 20, 30, 30), k=1)])
                    

    def objet_deplacement(self):
        '''Fonction gérant le déplacement des objets.'''
        
        #Fruits et Bombes
        for objet in self.objet_liste:
            objet[1] = objet[1] + objet[3][0]
            if  objet[1] > 120: #supprime l'objet de la liste si il est trop bas sur l'écran.
                self.objet_liste.remove(objet)
                

    def bonus_deplacement(self):
        '''Fonction gérant le déplacement des bonus.'''
        
        for bonus in self.bonus_liste:
            bonus[1] = bonus[1] + bonus[3][0]
            if  bonus[1] > 120: #supprime le bonus de la liste si il est trop bas sur l'écran.
                self.bonus_liste.remove(bonus)
                
                
    def colision_objet(self):
        '''Fonction gérant la colision entre le personnage et les objets.'''
        
        for objet in self.objet_liste:
            if (objet[0] >= self.doodle_x1 - 2 and objet[0] <= self.doodle_x1 + 13) and (objet[1] >= self.doodle_y1 and objet[1] <= self.doodle_y1 + 10): #Vérifie si les coordonnées de l'objet sont proche de celle du personnage.
                self.objet_liste.remove(objet) #Supprime l'objet de la liste des objets.
                
                if objet[2] == 0: #Pomme
                    self.score = self.score + 1 #Ajoute 1 au score.
                    pyxel.play(0,1)
                    
                elif objet[2] == 1: #Bombe
                    self.score = self.score - 1 #Retire 1 au score.
                    self.explosions_creation(self.doodle_x1 + 2, self.doodle_y1 + 2) #créé une explosion aux coordonnées du personnage.
                    pyxel.play(0,0)
                    
                elif objet[2] == 2: #Ananas
                    self.score = self.score + 10 #Ajoute 10 au score.
                    pyxel.play(0,1)
                    
                elif objet[2] == 3: #Citron
                    self.score = self.score + 3 #Ajoute 3 au score
                    pyxel.play(0,1)
                    
                elif objet[2] == 4: #Cerise
                    self.score = self.score + 5 #Ajoute 5 au score.
                    pyxel.play(0,1)
                    
                    
    def colision_bonus(self):
        '''Fonction gérant la colision entre le personnage et les bonus.'''
        
        for bonus in self.bonus_liste:
            if (bonus[0] >= self.doodle_x1 - 2 and bonus[0] <= self.doodle_x1 + 13) and (bonus[1] >= self.doodle_y1 and bonus[1] <= self.doodle_y1 + 10): #Vérifie si les coordonnées de l'bonus sont proche de celle du personnage.
                self.bonus_liste.remove(bonus) #Supprime le bonus de la liste des bonus.
                
                if bonus[2] == 5 and self.tps_bonus == 0: #Chrono
                    self.tps_bonus = 10
                    self.list_vitesse = [1, 1, 1, 1]
                    pyxel.play(0,2)
                    
                elif bonus[2] == 6 and self.tps_bonus == 0: #Ombre
                    self.tps_bonus = 10
                    self.vitesse = 8
                    pyxel.play(0,2)
                    
                elif bonus[2] == 7 and self.tps_bonus == 0: #Carotte
                    self.tps_bonus = 10
                    self.carotte = 1
                    pyxel.play(0,2)
                    
                elif bonus[2] == 8 and self.tps_bonus == 0: #Bombe dorée
                    self.tps_bonus = 10
                    self.ratio = (50, 0, 10, 25, 15)
                    pyxel.play(0,2)
                    
        if (pyxel.frame_count % 30 == 0) and self.tps_bonus >0 : 
            self.tps_bonus = self.tps_bonus - 1  
            if self.tps_bonus == 0:
                self.vitesse = 4
                self.ratio = (45, 20, 5, 20, 10)    
                self.list_vitesse = [0.50, 1, 1.5, 2]
                self.carotte = 0
                

    def explosions_creation(self, x, y):
        '''Fonction gérant la création d'une explosion.'''
        
        self.explosions_liste.append([x, y, 0])


    def explosions_animation(self):
        '''Fonction gérant l'animation des explosions (cercle de plus en plus grand)'''
        
        for explosion in self.explosions_liste:
            explosion[2] = explosion[2] + 1
            if explosion[2] == 12:
                self.explosions_liste.remove(explosion) #Supprime l'explosion si elle est trop grande.
                

    def astre(self):
        '''Permet le déplacement des astres.'''
        
        if (pyxel.frame_count % 10 == 0): #Mouvement toutes les 10 frame (environ 0.5 seconde)
            if self.astre_x1 > -20 and self.astre_y1 > 30:
                self.astre_x1, self.astre_x2, self.astre_x3, self.astre_x4 = self.astre_x1 - 1.5, self.astre_x2 - 1.5, self.astre_x3 - 1.5, self.astre_x4 - 1.5
                self.astre_y1, self.astre_y2, self.astre_y3, self.astre_y4 = self.astre_y1 - 1, self.astre_y2 - 1, self.astre_y3 - 1, self.astre_y4 - 1
                
            else:
                self.astre_y1, self.astre_y2, self.astre_y3, self.astre_y4 = 150, 150, 158, 158
                self.astre_x1, self.astre_x2, self.astre_x3, self.astre_x4 = 142, 150, 142, 150
        
        #Changement pour la lune à 50 secondes restante.  
        if 13 < self.timer <= 50:
            self.ciel = 5
            self.astre_dessin1, self.astre_dessin2, self.astre_dessin3, self.astre_dessin4 = 16, 24, 16, 24
            
        #Changement pour le soleil à 13 secondes restante.  
        elif self.timer <= 13:
            self.ciel = 6
            self.astre_dessin1, self.astre_dessin2, self.astre_dessin3, self.astre_dessin4 = 0, 8, 0, 8
            
            
    def temps(self):
        '''Fonction gérant le temps restant.'''
        
        if (pyxel.frame_count % 30 == 0): 
            self.timer = self.timer - 1 
            self.seconde = self.timer % 3600
            self.minute = int(self.timer/60) 
            self.seconde = self.timer % 60
            
            #Met l'écran de fin du jeu.
            if self.timer == 0:
                self.ecran = 0
                pyxel.run(self.update_fin,self.draw_fin)
            
            
    def lancement(self):
        '''Lancement du jeu après l'écran d'accueil, la fin de partie ou les paramètres.'''
        
        if pyxel.btn(pyxel.KEY_S) and self.ecran == 0:
            self.ecran = 1
            self.reset()
            pyxel.run(self.update_corps,self.draw_corps)
            
        elif pyxel.btn(pyxel.KEY_C) and self.ecran == 0:
            self.ecran = 2
            pyxel.run(self.update_param,self.draw_param)
            
        elif pyxel.btn(pyxel.KEY_P) and self.ecran == 0:
            self.ecran = 2
            pyxel.run(self.update_pts,self.draw_pts)
            
        elif pyxel.btn(pyxel.KEY_B) and self.ecran == 0:
            self.ecran = 2
            pyxel.run(self.update_bonus,self.draw_bonus)
            
        elif pyxel.btn(pyxel.KEY_R) and self.ecran == 2:
            self.ecran = 0
            pyxel.run(self.update_accueil,self.draw_accueil)
            
            
    def reset(self):
        '''Fonction remettant toutes les variables à leur états d'origine pour une nouvelle partie.'''
        if pyxel.btn(pyxel.KEY_S):
            
            #Reset du score
            self.score = 0
            
            #Retour au niveau 1
            self.ciel = 6
            self.ratio = (45, 20, 5, 20, 10)
            self.list_vitesse = [0.50, 1, 1.5, 2]
            
            #Vidage des listes
            self.objet_liste = []
            self.explosions_liste = []
            self.bonus_liste = []
            
            #Reset du timer
            self.timer = 90
            self.minute = 0
            self.seconde = 0
            self.tps_bonus = 0
            
            #Reset de l'écran 
            self.ecran = 0
            
            #Repositionnement du Personnage
            self.doodle_x1 = 60
            self.doodle_y1 = 110
            self.doodle_x2 = 60
            self.doodle_y2 = 118
            self.doodle_x3 = 68
            self.doodle_y3 = 110
            self.doodle_x4 = 68
            self.doodle_y4 = 118
            
            #Repositionnement du Soleil/Lune
            self.astre_dessin1 = 0
            self.astre_x1 = 120
            self.astre_y1 = 120
            self.astre_dessin2 = 8
            self.astre_x2 = 128
            self.astre_y2 = 120
            self.astre_dessin3 = 0
            self.astre_x3 = 120
            self.astre_y3 = 128
            self.astre_dessin4 = 8
            self.astre_x4 = 128
            self.astre_y4 = 128
            

 
                 
    def update_accueil(self):
        '''Vérifie le lancement du jeu.'''
        self.lancement()
        
    def draw_accueil(self):
        '''Affiche l'écran d'accueil.'''
        pyxel.cls(6)
        pyxel.text( 43, 10, 'Fruit World', 7)
        
        #Affiche la grosse pomme.
        pyxel.blt( 30, 0, 0, 0, 16, 8, 8, 15) #Haut gauche
        pyxel.blt( 38, 0, 0, 8, 16, 8, 8, 15) #Haut droite
        pyxel.blt( 30, 8, 0, 0, 24, 8, 8, 15) #Bas gauche
        pyxel.blt( 38, 8, 0, 8, 24, 8, 8, 15) #Bas droite
        
        #Affiche la grosse bombe.
        pyxel.blt( 84, 0, 0, 16, 16, 8, 8, 15) #Haut gauche
        pyxel.blt( 92, 0, 0, 24, 16, 8, 8, 15) #Haut droite
        pyxel.blt( 84, 8, 0, 16, 24, 8, 8, 15) #Bas gauche
        pyxel.blt( 92, 8, 0, 24, 24, 8, 8, 15) #Bas droite
        
        #Séparation.
        pyxel.rect(29, 17, 72, 0.5, 3)
        
        #Écran des points.
        pyxel.text( 14, 40, 'PRESSEZ P POUR LES POINTS', 7)
        
        #Écran des Controles.
        pyxel.text( 9, 60, 'PRESSEZ C POUR LES CONTROLES', 7)
        
        #Écran des Bonus.
        pyxel.text( 15, 80, 'PRESSEZ B POUR LES BONUS', 7)
        
        #Lancer le jeu.
        pyxel.text( 16, 100, 'PRESSEZ S POUR DEMARRER', 7)
        
        #Crédits.
        pyxel.text( 5, 120, 'RENAUD CORP.', 7)
        
        
    def update_pts(self):
        '''Vérifie le lancement du jeu.'''
        self.lancement()
           
    def draw_pts(self):
        '''Affiche l'écran des points.'''
        pyxel.cls(6)
        pyxel.text( 43, 10, 'Fruit World', 7)
        
        #Affiche la grosse pomme.
        pyxel.blt( 30, 0, 0, 0, 16, 8, 8, 15) #Haut gauche
        pyxel.blt( 38, 0, 0, 8, 16, 8, 8, 15) #Haut droite
        pyxel.blt( 30, 8, 0, 0, 24, 8, 8, 15) #Bas gauche
        pyxel.blt( 38, 8, 0, 8, 24, 8, 8, 15) #Bas droite
        
        #Affiche la grosse bombe.
        pyxel.blt( 84, 0, 0, 16, 16, 8, 8, 15) #Haut gauche
        pyxel.blt( 92, 0, 0, 24, 16, 8, 8, 15) #Haut droite
        pyxel.blt( 84, 8, 0, 16, 24, 8, 8, 15) #Bas gauche
        pyxel.blt( 92, 8, 0, 24, 24, 8, 8, 15) #Bas droite
        
        #Séparation.
        pyxel.rect(29, 17, 72, 0.5, 0)
        pyxel.text( 54, 20, 'POINTS', 7)

        #Affichage des points.
        pyxel.blt( 10, 35, 0, 0, 0, 8, 8, 0) #Pomme
        pyxel.text( 20, 38, '1 PTS', 7)        
        
        pyxel.blt( 70, 55, 0, 8, 0, 8, 8, 0) #Bombe
        pyxel.text( 80, 58, '-1 PTS', 7)

        pyxel.blt( 70, 35, 0, 0, 8, 8, 8, 0) #Ananas
        pyxel.text( 80, 38, '10 PTS', 7)

        pyxel.blt( 10, 55, 0, 8, 8, 8, 8, 0) #Citron
        pyxel.text( 20, 58, '3 PTS', 7)

        pyxel.blt( 10, 75, 0, 16, 8, 8, 8, 0) #Cerise
        pyxel.text( 20, 78, '5 PTS', 7)
        
        pyxel.blt(65, 70, 0, 32, 32, 8, 8, 7)
        pyxel.blt(65, 78, 0, 32, 40, 8, 8, 7)
        pyxel.blt(73, 70, 0, 40, 32, 8, 8, 7)
        pyxel.blt(73, 78, 0, 40, 40, 8, 8, 7) #Personnage
        pyxel.text( 83, 78, 'Vous', 7)
        
        #Retourner à l'écran d'acceuil.
        pyxel.text( 20, 110, 'PRESSEZ R POUR REVENIR', 7)
        
        
    def update_param(self):
        '''Vérifie le lancement du jeu.'''
        self.lancement()
           
    def draw_param(self):
        '''Affiche l'écran d'accueil.'''
        pyxel.cls(6)
        pyxel.text( 43, 10, 'Fruit World', 7)
        
        #Affiche la grosse pomme.
        pyxel.blt( 30, 0, 0, 0, 16, 8, 8, 15) #Haut gauche
        pyxel.blt( 38, 0, 0, 8, 16, 8, 8, 15) #Haut droite
        pyxel.blt( 30, 8, 0, 0, 24, 8, 8, 15) #Bas gauche
        pyxel.blt( 38, 8, 0, 8, 24, 8, 8, 15) #Bas droite
        
        #Affiche la grosse bombe.
        pyxel.blt( 84, 0, 0, 16, 16, 8, 8, 15) #Haut gauche
        pyxel.blt( 92, 0, 0, 24, 16, 8, 8, 15) #Haut droite
        pyxel.blt( 84, 8, 0, 16, 24, 8, 8, 15) #Bas gauche
        pyxel.blt( 92, 8, 0, 24, 24, 8, 8, 15) #Bas droite
        
                #Séparation.
        pyxel.rect(29, 17, 72, 0.5, 0)
        pyxel.text( 49, 20, 'CONTROLES', 7)
        
        #Affichage du déplacement à gauche.
        pyxel.blt( 34, 38, 0, 24, 0, 8, 8, 1)
        pyxel.text( 44, 40, 'ou', 7)
        pyxel.blt( 54, 38, 0, 40, 8, 8, 8, 1)
        pyxel.text( 65, 40, 'Gauche', 7)
        
        #Affichage du déplacement à droite.
        pyxel.blt( 34, 58, 0, 24, 8, 8, 8, 1)
        pyxel.text( 44, 60, 'ou', 7)
        pyxel.blt( 54, 58, 0, 40, 0, 8, 8, 1)
        pyxel.text( 65, 60, 'Droite', 7)
        
        #Affichage du saut.
        pyxel.rect( 39, 79, 20, 6, 0)
        pyxel.text( 65, 80, 'SAUT', 7)
        
        #Retourner à l'écran d'acceuil.
        pyxel.text( 20, 110, 'PRESSEZ R POUR REVENIR', 7)
        
        
    def update_bonus(self):
        '''Vérifie le lancement du jeu.'''
        self.lancement()
           
    def draw_bonus(self):
        '''Affiche l'écran des points.'''
        pyxel.cls(6)
        pyxel.text( 43, 10, 'Fruit World', 7)
        
        #Affiche la grosse pomme.
        pyxel.blt( 30, 0, 0, 0, 16, 8, 8, 15) #Haut gauche
        pyxel.blt( 38, 0, 0, 8, 16, 8, 8, 15) #Haut droite
        pyxel.blt( 30, 8, 0, 0, 24, 8, 8, 15) #Bas gauche
        pyxel.blt( 38, 8, 0, 8, 24, 8, 8, 15) #Bas droite
        
        #Affiche la grosse bombe.
        pyxel.blt( 84, 0, 0, 16, 16, 8, 8, 15) #Haut gauche
        pyxel.blt( 92, 0, 0, 24, 16, 8, 8, 15) #Haut droite
        pyxel.blt( 84, 8, 0, 16, 24, 8, 8, 15) #Bas gauche
        pyxel.blt( 92, 8, 0, 24, 24, 8, 8, 15) #Bas droite
        
        #Séparation.
        pyxel.rect(29, 17, 72, 0.5, 0)
        pyxel.text( 54, 20, 'BONUS', 7)

        #Affichage des points.
        pyxel.blt( 10, 36, 0, 48, 32, 8, 8, 15) #Chrono
        pyxel.text( 20, 38, 'RALENTIT LE TEMPS', 7)        
        
        pyxel.blt( 10, 56, 0, 56, 32, 8, 8, 15) #Ombre
        pyxel.text( 20, 58, 'ACCELERE VOTRE VITESSE', 7)

        pyxel.blt( 10, 76, 0, 48, 40, 8, 8, 15) #Carotte
        pyxel.text( 20, 78, 'MEILLEUR VISION', 7)

        pyxel.blt( 10, 96, 0, 56, 40, 8, 8, 15) #Bombe Dorée
        pyxel.text( 20, 98, 'PLUS DE BOMBES', 7)
        
        #Retourner à l'écran d'acceuil.
        pyxel.text( 20, 115, 'PRESSEZ R POUR REVENIR', 7)
        
        
    def update_corps(self):
        '''Mise à jour des variables (30 fois par seconde).'''
        
        #Déplacement du personnage.
        self.doodle_deplacement()
        
        #Création et déplacemnt des objets et bonus .
        self.objet_creation()
        self.objet_deplacement()
        self.bonus_creation()
        self.bonus_deplacement()
        
        #Vérification des collisions.
        self.colision_objet()
        self.colision_bonus()
        
        #Évolution de l'animation des explosions.
        self.explosions_animation()
        
        #Mise à jour du temps restant.
        self.temps()
        
        #Déplacement des astres.
        self.astre()
        
    def draw_corps(self):
        '''Création et positionnement des objets (30 fois par seconde).'''
            
        #Création du ciel.
        pyxel.cls(self.ciel)
        
            #Soleil/Lune
        pyxel.blt(self.astre_x1, self.astre_y1, 0, self.astre_dessin1, 32, 8, 8, 15)
        pyxel.blt(self.astre_x2, self.astre_y2, 0, self.astre_dessin2, 32, 8, 8, 15)
        pyxel.blt(self.astre_x3, self.astre_y3, 0, self.astre_dessin3, 40, 8, 8, 15)
        pyxel.blt(self.astre_x4, self.astre_y4, 0, self.astre_dessin4, 40, 8, 8, 15)
                
        #Décoration du fond
            #Buissons
        pyxel.blt(23, 112, 0, 32, 16, 8, 8, 15)
        pyxel.blt(31, 112, 0, 40, 16, 8, 8, 15)
        
        pyxel.blt(83, 112, 0, 32, 24, 8, 8, 15)
        pyxel.blt(91, 112, 0, 40, 24, 8, 8, 15)
        
        pyxel.blt(7, 112, 0, 32, 0, 8, 8, 15)        
        
            #Arbre
                #Ligne du bas
        pyxel.blt(45, 112, 0, 8, 72, 8, 8, 15)
        pyxel.blt(53, 112, 0, 16, 72, 8, 8, 15)
        pyxel.blt(61, 112, 0, 24, 72, 8, 8, 15)
        pyxel.blt(69, 112, 0, 32, 72, 8, 8, 15)
                #Ligne du milieu
        pyxel.blt(45, 104, 0, 8, 64, 8, 8, 15)
        pyxel.blt(53, 104, 0, 16, 64, 8, 8, 15)
        pyxel.blt(61, 104, 0, 24, 64, 8, 8, 15)
        pyxel.blt(69, 104, 0, 32, 64, 8, 8, 15)
                #Ligne du haut
        pyxel.blt(45, 96, 0, 8, 56, 8, 8, 15)
        pyxel.blt(53, 96, 0, 16, 56, 8, 8, 15)
        pyxel.blt(61, 96, 0, 24, 56, 8, 8, 15)
        pyxel.blt(69, 96, 0, 32, 56, 8, 8, 15)
        
            #Cailloux
        pyxel.blt(115, 112, 0, 48, 0, 8, 8, 15)
        pyxel.blt(123, 112, 0, 56, 0, 8, 8, 15)
        pyxel.blt(47, 112, 0, 48, 8, 8, 8, 15)
        
            #Nuages
        pyxel.blt(115, 51, 0, 48, 16, 8, 8, 15)
        pyxel.blt(18, 34, 0, 56, 16, 8, 8, 15)
        pyxel.blt(47, 6, 0, 48, 24, 8, 8, 15)
        pyxel.blt(81, 63, 0, 56, 24, 8, 8, 15)
        
        #Création du fond pour le bonus.
        if self.carotte == 1:
            pyxel.rect( 0, 0, 128, 128, 7)
            pyxel.text( 5, 5, str(self.minute) + ' MIN ' + str(self.seconde) + ' S', 0)  
            pyxel.text( 85, 5, str(self.score) + ' POINTS', 0)  
            
        #Création du sol
        pyxel.rect(0, 120, 128, 10, 3)   
              
        #Création du personnage.
        pyxel.blt(self.doodle_x1, self.doodle_y1, 0, 32, 32, 8, 8, 7)
        pyxel.blt(self.doodle_x2, self.doodle_y2, 0, 32, 40, 8, 8, 7)
        pyxel.blt(self.doodle_x3, self.doodle_y3, 0, 40, 32, 8, 8, 7)
        pyxel.blt(self.doodle_x4, self.doodle_y4, 0, 40, 40, 8, 8, 7)
        
        #Création des objets.
        for objet in self.objet_liste:
            if objet[2] == 0:
                pyxel.blt(objet[0], objet[1], 0, 0, 0, 8, 8, 0)
                
            elif objet[2] == 1:
                pyxel.blt(objet[0], objet[1], 0, 8, 0, 8, 8, 0)
                
            elif objet[2] == 2:
                pyxel.blt(objet[0], objet[1], 0, 0, 8, 8, 8, 0)
                
            elif objet[2] == 3:
                pyxel.blt(objet[0], objet[1], 0, 8, 8, 8, 8, 0)
                
            elif objet[2] == 4:
                pyxel.blt(objet[0], objet[1], 0, 16, 8, 8, 8, 0)
                
        #Création des bonus.
        for bonus in self.bonus_liste:

            if bonus[2] == 5:
                pyxel.blt(bonus[0], bonus[1], 0, 48, 32, 8, 8, 15)
                
            elif bonus[2] == 6:
                pyxel.blt(bonus[0], bonus[1], 0, 56, 32, 8, 8, 15)
                
            elif bonus[2] == 7:
                pyxel.blt(bonus[0], bonus[1], 0, 48, 40, 8, 8, 15)
                
            elif bonus[2] == 8:
                pyxel.blt(bonus[0], bonus[1], 0, 56, 40, 8, 8, 15)
     
        #Création des explosions.
        for explosion in self.explosions_liste:
                pyxel.circb(explosion[0] + 4, explosion[1] + 4, 2 * (explosion[2] // 4), 8 + explosion[2] % 3)
            
        #Affichage du temps et du score.
        if self.carotte == 0:                    
            pyxel.text( 5, 5, str(self.minute) + ' MIN ' + str(self.seconde) + ' S', 7)  
            pyxel.text( 85, 5, str(self.score) + ' POINTS', 7)
        
        
    def update_fin(self):
        '''Vérifie le lancement du jeu après la fin du jeu.'''
        self.lancement()
    
    def draw_fin(self):
        '''Affiche les informations de fin du jeu.'''
        
        #Vide la fenêtre et affiche le score final.
        pyxel.cls(6)
        pyxel.text( 43, 20, 'Fruit World', 7)
        pyxel.text( 32, 64,'SCORE: ' + str(self.score) + ' POINTS', 7)
        pyxel.text( 18, 110, 'PRESSEZ S POUR REDEMARRER', 7)
        
        #Affiche la grosse pomme.
        pyxel.blt( 30, 10, 0, 0, 16, 8, 8, 15) #Haut gauche
        pyxel.blt( 38, 10, 0, 8, 16, 8, 8, 15) #Haut droite
        pyxel.blt( 30, 18, 0, 0, 24, 8, 8, 15) #Bas gauche
        pyxel.blt( 38, 18, 0, 8, 24, 8, 8, 15) #Bas droite
        
        #Affiche la grosse bombe.
        pyxel.blt( 84, 10, 0, 16, 16, 8, 8, 15) #Haut gauche
        pyxel.blt( 92, 10, 0, 24, 16, 8, 8, 15) #Haut droite
        pyxel.blt( 84, 18, 0, 16, 24, 8, 8, 15) #Bas gauche
        pyxel.blt( 92, 18, 0, 24, 24, 8, 8, 15) #Bas droite
 
class Appli:
    '''Class gérant l'application./Class managing the application'''
    
    def __init__(self):
        '''Fonction créant la fenêtre./Function creating the window.'''

        #Taille de la fenêtre et chargement des visuels
        pyxel.init(128, 128, title="Fruit World", quit_key=pyxel.KEY_ESCAPE)
        pyxel.load('Fruit_World.pyxres')
        
        pyxel.run(self.update, self.draw)
        
    def lancement(self):
        '''Launch the game/Lance le jeu'''
        
        if pyxel.btn(pyxel.KEY_F): #Jeu en Français
            Jeu()
            
        elif pyxel.btn(pyxel.KEY_E): #Game in English
            Jeu()
            

    def update(self):
        '''Checks the launch of the game./Vérifie le lancement du jeu.'''
        self.lancement()
        
    def draw(self):
        '''Displays the home screen./Affiche l'écran d'acceuil'''
        pyxel.cls(6)
        pyxel.text( 43, 10, 'Fruit World', 7)
        
        #Display the big apple.
        pyxel.blt( 30, 0, 0, 0, 16, 8, 8, 15) #Top left
        pyxel.blt( 38, 0, 0, 8, 16, 8, 8, 15) #Top Right
        pyxel.blt( 30, 8, 0, 0, 24, 8, 8, 15) #Bottom left
        pyxel.blt( 38, 8, 0, 8, 24, 8, 8, 15) #Bottom right
        
        #Display the big bomb.
        pyxel.blt( 84, 0, 0, 16, 16, 8, 8, 15) #Top left
        pyxel.blt( 92, 0, 0, 24, 16, 8, 8, 15) #Top Right
        pyxel.blt( 84, 8, 0, 16, 24, 8, 8, 15) #Bottom left
        pyxel.blt( 92, 8, 0, 24, 24, 8, 8, 15) #Bottom right
        
        #Separation.
        pyxel.rect(29, 17, 72, 0.5, 3)
        
        #Jeu en Français.
        pyxel.text( 18, 50, 'PRESSEZ F POUR FRANCAIS', 7)
        
        #Game in English.
        pyxel.text( 24, 80, 'PRESS E FOR ENGLISH', 7)
        
        #credit.
        pyxel.text( 5, 120, 'RENAUD CORP.', 7)
        

#Lancement de l'application