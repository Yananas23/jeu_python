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
    Ombre: Accélère la doodle["speed"] de base du personnage.
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
        '''Fonction créant toutes les variables utiles au jeu./Function creating all variables useful to the game.'''

        #Chargement des visuels./Loading visuals.
        pyxel.init(128, 128, title="Fruit World", quit_key=pyxel.KEY_ESCAPE)
        pyxel.load('Fruit_World.pyxres')


        #Info de base du personnage / Basic info of the character
        self.doodle = {"speed":4, 
                       "jump":0, "max":0, "dy":0, "distance":0, 
                       "x1":60, "y1":110, 
                       "x2":60, "y2":118, 
                       "x3":68, "y3":110, 
                       "x4":68, "y4":118}

        
        #Position du Soleil et Lune / Position of the Sun and Moon
        self.astre = {"dessin1":0, "x1":120, "y1":120, 
                      "dessin2": 8, "x2":128, "y2":120, 
                      "dessin3": 0, "x3":120, "y3":128, 
                      "dessin4":8, "x4":128, "y4":128}


        #Score au début de la partie / Score at the beginning of the game
        self.score = 0

        #Valeur pour les niveaux de difficultés / Value for the levels of difficulty
        self.ciel = 6
        self.ratio = (45, 20, 5, 20, 10)

        #Liste pour les éléments du jeu autre que le personnage / List for game elements other than the character
        self.objet_liste = [] #[ x, y, type, vitesse de chute] / [x, y, type, fall speed]
        self.explosions_liste = []
        self.bonus_liste = [] #[ x, y, type, vitesse de chute] / [x, y, type, fall speed]
        self.list_vitesse = [0.50, 1, 1.5, 2]
        
        #Variable pour les bonus / Variable for bonuses
        self.tps_bonus = 0
        self.carotte = 0
        
        #Variable pour le temps / Variable for time
        self.timer = 90
        self.minute = 0
        self.seconde = 0
        
        #Lancement du jeu / Launch of the game
        self.ecran = 0
        pyxel.run(self.update_acceuil, self.draw_acceuil)
        

    def doodle_deplacement(self):
        '''Fonction pour les déplacements. / Function for movements.'''
        
        #Saut / Jump
        if pyxel.btn(pyxel.KEY_SPACE):

            if self.doodle["dy"] == 0:
                self.doodle["max"] = self.doodle["y1"] - 23
                self.doodle["dy"] = -1
                
        if self.doodle["y1"] < self.doodle["max"]:
            self.doodle["dy"] = 1

        if self.doodle["y1"] > 110:
            self.doodle["y1"], self.doodle["y3"] = 110, 110
            self.doodle["y2"], self.doodle["y4"] = 118, 118
            self.doodle["dy"] = 0

        self.doodle["y1"] = self.doodle["y1"] + self.doodle["dy"]
        self.doodle["y2"] = self.doodle["y2"] + self.doodle["dy"]
        self.doodle["y3"] = self.doodle["y3"] + self.doodle["dy"]
        self.doodle["y4"] = self.doodle["y4"] + self.doodle["dy"]

        #Déplacement à droite. / Right movement.
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D)) and self.doodle["x1"] <= 108:
            self.doodle["x1"] = self.doodle["x1"] + self.doodle["speed"]
            self.doodle["x2"] = self.doodle["x2"] + self.doodle["speed"]
            self.doodle["x3"] = self.doodle["x3"] + self.doodle["speed"]
            self.doodle["x4"] = self.doodle["x4"] + self.doodle["speed"]

        #Déplacement à gauche. / Left movement.
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q))and self.doodle["x1"] >= 4:
            self.doodle["x1"] = self.doodle["x1"] - self.doodle["speed"]
            self.doodle["x2"] = self.doodle["x2"] - self.doodle["speed"]
            self.doodle["x3"] = self.doodle["x3"] - self.doodle["speed"]
            self.doodle["x4"] = self.doodle["x4"] - self.doodle["speed"]


    def objet_creation(self):
        '''Fonction gérant la création des objets. / Function managing the creation of objects.'''
        
        type_objet = [ 0, 1, 2, 3, 4] #0 = Pomme / Apple, 1 = Bombe /Bomb, 2 = Ananas  / Pineapple, 3 = Citron  /Lemon, 4 = Cerise / Cherry
        if (pyxel.frame_count % 30 == 0): #Nouvel objet toutes les 30 frames (environ 1 seconde) / New object every 30 frames (about 1 second)
            
            #Aléatoire pour le type de fruit. / Random for the type of fruit.
            int_objet = random.choices( type_objet, weights=self.ratio, k=1)
            
            #Créé une pomme. / Create an apple.
            if int_objet[0] == 0:
                self.objet_liste.append([random.randint(0, 120), 0, int_objet[0], random.choices( self.list_vitesse, weights=(20, 25, 25, 30), k=1)])
                
            #Créé une bombe. / Create a bomb.
            elif int_objet[0] == 1:
                self.objet_liste.append([random.randint(0, 120), 0, int_objet[0], random.choices( self.list_vitesse, weights=(10, 20, 30, 40), k=1)])
            
            #Créé un Ananas. / Create a pineapple.
            elif int_objet[0] == 2:
                self.objet_liste.append([random.randint(0, 120), 0, int_objet[0], random.choices( self.list_vitesse, weights=(10, 20, 30, 40), k=1)])
            
            #Créé un citron. / Create a lemon.
            elif int_objet[0] == 3:
                self.objet_liste.append([random.randint(0, 120), 0, int_objet[0], random.choices( self.list_vitesse, weights=(20, 20, 30, 30), k=1)])
            
            #Créé des cerises. / Create cherries.
            elif int_objet[0] == 4:
                self.objet_liste.append([random.randint(0, 120), 0, int_objet[0], random.choices( self.list_vitesse, weights=(10, 20, 40, 30), k=1)])
                

    def bonus_creation(self):
        '''Fonction gérant la création des bonus. / Function managing the creation of bonuses.'''
        
        type_bonus = [ 5, 6, 7, 8] #5 = chrono / chrono, 6 = ombre / shadow, 7 = carotte / carrot, 8 = bombe dorée / golden bomb
        if (pyxel.frame_count % 900 == 0): #Nouveau bonus toutes les 900 frames (environ 30 secondes) / New bonus every 900 frames (about 30 seconds)
            if random.choices([ 0, 1], weights=(60, 40), k=1) == [1]:
                #Aléatoire pour le type de bonus. / Random for the type of bonus.
                int_bonus = random.choices( type_bonus, weights=(25, 25, 25, 25), k=1)
                
                #Créé un chrono. / Create a chrono.
                if int_bonus[0] == 5:
                    self.bonus_liste.append([random.randint(0, 120), 0, int_bonus[0], random.choices( self.list_vitesse, weights=(20, 25, 25, 30), k=1)])
                    
                #Créé une ombre. / Create a shadow.
                elif int_bonus[0] == 6:
                    self.bonus_liste.append([random.randint(0, 120), 0, int_bonus[0], random.choices( self.list_vitesse, weights=(10, 20, 30, 40), k=1)])
                
                #Créé une carotte. / Create a carrot.
                elif int_bonus[0] == 7:
                    self.bonus_liste.append([random.randint(0, 120), 0, int_bonus[0], random.choices( self.list_vitesse, weights=(10, 20, 30, 40), k=1)])
                
                #Créé une bombe dorée. / Create a golden bomb.
                elif int_bonus[0] == 8:
                    self.bonus_liste.append([random.randint(0, 120), 0, int_bonus[0], random.choices( self.list_vitesse, weights=(20, 20, 30, 30), k=1)])
                    

    def objet_deplacement(self):
        '''Fonction gérant le déplacement des objets. / Function managing the movement of objects.'''
        
        #Fruits et Bombes / Fruits and Bombs
        for objet in self.objet_liste:
            objet[1] = objet[1] + objet[3][0]
            if  objet[1] > 120: #supprime l'objet de la liste si il est trop bas sur l'écran. / remove the object from the list if it is too low on the screen.
                self.objet_liste.remove(objet)
                

    def bonus_deplacement(self):
        '''Fonction gérant le déplacement des bonus. / Function managing the movement of bonuses.'''
        
        for bonus in self.bonus_liste:
            bonus[1] = bonus[1] + bonus[3][0]
            if  bonus[1] > 120: #supprime le bonus de la liste si il est trop bas sur l'écran. / remove the bonus from the list if it is too low on the screen.
                self.bonus_liste.remove(bonus)
                
                
    def colision_objet(self):
        '''Fonction gérant la colision entre le personnage et les objets. / Function managing the collision between the character and the objects.'''
        
        for objet in self.objet_liste:
            if (objet[0] >= self.doodle["x1"] - 2 and objet[0] <= self.doodle["x1"] + 13) and (objet[1] >= self.doodle["y1"] and objet[1] <= self.doodle["y1"] + 10): #Vérifie si les coordonnées de l'objet sont proche de celle du personnage.
                self.objet_liste.remove(objet) #Supprime l'objet de la liste des objets. / Remove the object from the list of objects.
                
                if objet[2] == 0: #Pomme / Apple
                    self.score = self.score + 1 #Ajoute 1 au score. / Add 1 to the score.
                    pyxel.play(0,1)
                    
                elif objet[2] == 1: #Bombe / Bomb
                    self.score = self.score - 1 #Retire 1 au score. / Remove 1 from the score.
                    self.explosions_creation(self.doodle["x1"] + 2, self.doodle["y1"] + 2) #créé une explosion aux coordonnées du personnage.
                    pyxel.play(0,0)
                    
                elif objet[2] == 2: #Ananas / Pineapple
                    self.score = self.score + 10 #Ajoute 10 au score. / Add 10 to the score.
                    pyxel.play(0,1)
                    
                elif objet[2] == 3: #Citron / Lemon
                    self.score = self.score + 3 #Ajoute 3 au score / Add 3 to the score.
                    pyxel.play(0,1)
                    
                elif objet[2] == 4: #Cerise / Cherry
                    self.score = self.score + 5 #Ajoute 5 au score. / Add 5 to the score.
                    pyxel.play(0,1)
                    
                    
    def colision_bonus(self):
        '''Fonction gérant la colision entre le personnage et les bonus. / Function managing the collision between the character and the bonuses.'''
        
        for bonus in self.bonus_liste:
            if (bonus[0] >= self.doodle["x1"] - 2 and bonus[0] <= self.doodle["x1"] + 13) and (bonus[1] >= self.doodle["y1"] and bonus[1] <= self.doodle["y1"] + 10): #Vérifie si les coordonnées de l'bonus sont proche de celle du personnage.
                self.bonus_liste.remove(bonus) #Supprime le bonus de la liste des bonus. / Remove the bonus from the list of bonuses.
                
                if bonus[2] == 5 and self.tps_bonus == 0: #Chrono / Chrono
                    self.tps_bonus = 10
                    self.list_vitesse = [1, 1, 1, 1]
                    pyxel.play(0,2)
                    
                elif bonus[2] == 6 and self.tps_bonus == 0: #Ombre / Shadow
                    self.tps_bonus = 10
                    self.doodle["speed"] = 8
                    pyxel.play(0,2)
                    
                elif bonus[2] == 7 and self.tps_bonus == 0: #Carotte / Carrot
                    self.tps_bonus = 10
                    self.carotte = 1
                    pyxel.play(0,2)
                    
                elif bonus[2] == 8 and self.tps_bonus == 0: #Bombe dorée / Golden bomb
                    self.tps_bonus = 10
                    self.ratio = (50, 0, 10, 25, 15)
                    pyxel.play(0,2)
                    
        if (pyxel.frame_count % 30 == 0) and self.tps_bonus >0 : 
            self.tps_bonus = self.tps_bonus - 1  
            if self.tps_bonus == 0:
                self.doodle["speed"] = 4
                self.ratio = (45, 20, 5, 20, 10)    
                self.list_vitesse = [0.50, 1, 1.5, 2]
                self.carotte = 0
                

    def explosions_creation(self, x, y):
        '''Fonction gérant la création d'une explosion. / Function managing the creation of an explosion.'''
        
        self.explosions_liste.append([x, y, 0])


    def explosions_animation(self):
        '''Fonction gérant l'animation des explosions (cercle de plus en plus grand) / Function managing the animation of the explosions (circle getting bigger)'''
        
        for explosion in self.explosions_liste:
            explosion[2] = explosion[2] + 1
            if explosion[2] == 12:
                self.explosions_liste.remove(explosion) #Supprime l'explosion si elle est trop grande. / Remove the explosion if it is too big.
                

    def astres(self):
        '''Permet le déplacement des astres. / Allows the movement of the stars.'''
        
        if (pyxel.frame_count % 10 == 0): #Mouvement toutes les 10 frame (environ 0.5 seconde) / Movement every 10 frames (about 0.5 second)
            if self.astre["x1"] > -20 and self.astre["y1"] > 30:
                self.astre["x1"], self.astre["x2"], self.astre["x3"], self.astre["x4"] = self.astre["x1"] - 1.5, self.astre["x2"] - 1.5, self.astre["x3"] - 1.5, self.astre["x4"] - 1.5
                self.astre["y1"], self.astre["y2"], self.astre["y3"], self.astre["y4"] = self.astre["y1"] - 1, self.astre["y2"] - 1, self.astre["y3"] - 1, self.astre["y4"] - 1
                
            else:
                self.astre["y1"], self.astre["y2"], self.astre["y3"], self.astre["y4"] = 150, 150, 158, 158
                self.astre["x1"], self.astre["x2"], self.astre["x3"], self.astre["x4"] = 142, 150, 142, 150
        
        #Changement pour la lune à 50 secondes restante. / Change for the moon at 50 seconds remaining. 
        if 13 < self.timer <= 50:
            self.ciel = 5
            self.astre["dessin1"], self.astre["dessin2"], self.astre["dessin3"], self.astre["dessin4"] = 16, 24, 16, 24
            
        #Changement pour le soleil à 13 secondes restante. / Change for the sun at 13 seconds remaining.
        elif self.timer <= 13:
            self.ciel = 6
            self.astre["dessin1"], self.astre["dessin2"], self.astre["dessin3"], self.astre["dessin4"] = 0, 8, 0, 8
            
            
    def temps(self):
        '''Fonction gérant le temps restant. / Function managing the remaining time.'''
        
        if (pyxel.frame_count % 30 == 0): 
            self.timer = self.timer - 1 
            self.seconde = self.timer % 3600
            self.minute = int(self.timer/60) 
            self.seconde = self.timer % 60
            
            #Met l'écran de fin du jeu. / Put the end screen of the game.
            if self.timer == 0:
                self.ecran = 0
                pyxel.run(self.update_fin,self.draw_fin)
                
    def langue(self):
        """Fonction gérant la langue. / Function managing the language."""
        
        if pyxel.btn(pyxel.KEY_F): #jeu en français / game in french
            self.langage = [( 14, 40, 'PRESSEZ P POUR LES POINTS', 7), ( 9, 60, 'PRESSEZ C POUR LES CONTROLES', 7),
                            ( 15, 80, 'PRESSEZ B POUR LES BONUS', 7), ( 16, 100, 'PRESSEZ S POUR DEMARRER', 7),
                            ( 83, 78, 'Vous', 7), ( 20, 110, 'PRESSEZ R POUR REVENIR', 7), ( 49, 20, 'CONTROLES', 7),
                            ( 44, 40, 'ou', 7), ( 65, 40, 'Gauche', 7), ( 44, 60, 'ou', 7), ( 65, 60, 'Droite', 7),
                            ( 65, 80, 'SAUT', 7), ( 20, 110, 'PRESSEZ R POUR REVENIR', 7),
                            ( 20, 38, 'RALENTIT LE TEMPS', 7), ( 20, 58, 'ACCELERE VOTRE VITESSE', 7),
                            ( 20, 78, 'MEILLEUR VISION', 7), ( 20, 98, 'PLUS DE BOMBES', 7),
                            ( 20, 115, 'PRESSEZ R POUR REVENIR', 7), ( 18, 110, 'PRESSEZ S POUR REDEMARRER', 7)]
            pyxel.run(self.update_menu,self.draw_menu)
            
        elif pyxel.btn(pyxel.KEY_E): #jeu en anglais / game in english
            self.langage = [( 24, 40, 'PRESS P TO SEE POINTS', 7), ( 20, 60, 'PRESS C TO SEE CONTROLS', 7),
                            ( 25, 80, 'PRESS B TO SEE BONUS', 7), ( 31, 100, 'PRESS S TO START', 7),
                            ( 83, 78, 'YOU', 7),( 30, 110, 'PRESS R TO RETURN', 7), ( 49, 20, 'CONTROLS', 7),
                            ( 44, 40, 'or', 7), ( 65, 40, 'LEFT', 7), ( 44, 60, 'or', 7), ( 65, 60, 'RIGHT', 7),
                            ( 65, 80, 'JUMP', 7), ( 30, 110, 'PRESS R TO RETURN', 7), ( 54, 20, 'BONUS', 7),
                            ( 20, 38, 'SLOW THE TIME', 7), ( 20, 58, 'MAKE YOU FASTER', 7),
                            ( 20, 78, 'YOU WILL SEE BETER', 7), ( 20, 98, 'NO BOMB', 7),
                            ( 30, 115, 'PRESS R TO RETURN', 7), ( 30, 110, 'PRESS S TO RESTART', 7)]
            pyxel.run(self.update_menu,self.draw_menu)
            
            
    def lancement(self):
        '''Lancement du jeu après le menu, la fin de partie ou les paramètres. / Launch of the game after the menu, the end of the game or the parameters.'''
        
        if pyxel.btn(pyxel.KEY_S) and self.ecran == 0: #Lancement du jeu. / Launch of the game.
            self.ecran = 1
            self.reset()
            pyxel.run(self.update_corps,self.draw_corps)
            
        elif pyxel.btn(pyxel.KEY_C) and self.ecran == 0: #Affichage des contrôles. / Display of the controls.
            self.ecran = 2
            pyxel.run(self.update_param,self.draw_param)
            
        elif pyxel.btn(pyxel.KEY_P) and self.ecran == 0: #Affichage des points. / Display of the points.
            self.ecran = 2
            pyxel.run(self.update_pts,self.draw_pts)
            
        elif pyxel.btn(pyxel.KEY_B) and self.ecran == 0: #Affichage des bonus. / Display of the bonuses.
            self.ecran = 2
            pyxel.run(self.update_bonus,self.draw_bonus)
            
        elif pyxel.btn(pyxel.KEY_R) and self.ecran == 2: #Retour au menu. / Back to the menu.
            self.ecran = 0
            pyxel.run(self.update_menu,self.draw_menu)
            
            
    def reset(self):
        '''Fonction remettant toutes les variables à leur états d'origine pour une nouvelle partie. / Function putting all the variables back to their original state for a new game.'''
        if pyxel.btn(pyxel.KEY_S):
            
            #Reset du score et du niveau / Reset of the score and the level
            self.score = 0
            
            #Retour au niveau 1 et au ciel de base. / Back to level 1 and the basic sky.
            self.ciel = 6
            self.ratio = (45, 20, 5, 20, 10)
            self.list_vitesse = [0.50, 1, 1.5, 2]
            
            #Vidage des listes / Emptying the lists
            self.objet_liste = []
            self.explosions_liste = []
            self.bonus_liste = []
            
            #Reset du timer / Reset of the timer
            self.timer = 90
            self.minute = 0
            self.seconde = 0
            self.tps_bonus = 0
            
            #Reset de l'écran / Reset of the screen
            self.ecran = 0
            
            #Repositionnement du Personnage / Repositioning of the Character
            self.doodle["x1"] = 60
            self.doodle["y1"] = 110
            self.doodle["x2"] = 60
            self.doodle["y2"] = 118
            self.doodle["x3"] = 68
            self.doodle["y3"] = 110
            self.doodle["x4"] = 68
            self.doodle["y4"] = 118
            
            #Repositionnement du Soleil et Lune / Repositioning of the Sun and Moon
            self.astre["dessin1"] = 0
            self.astre["x1"] = 120
            self.astre["y1"] = 120
            self.astre["dessin2"] = 8
            self.astre["x2"] = 128
            self.astre["y2"] = 120
            self.astre["dessin3"] = 0
            self.astre["x3"] = 120
            self.astre["y3"] = 128
            self.astre["dessin4"] = 8
            self.astre["x4"] = 128
            self.astre["y4"] = 128
            
    def update_acceuil(self):
        '''Checks the launch of the game./Vérifie le lancement du jeu.'''
        self.lancement()
        self.langue()
        
    def draw_acceuil(self):
        '''Displays the home screen./Affiche l'écran d'acceuil'''
        pyxel.cls(6)
        pyxel.text( 43, 10, 'Fruit World', 7)
        
        #Affiche la grosse pomme. / Display the big apple.
        pyxel.blt( 30, 0, 0, 0, 16, 8, 8, 15) #Haut gauche / Top left
        pyxel.blt( 38, 0, 0, 8, 16, 8, 8, 15) #Haut droite / Top right
        pyxel.blt( 30, 8, 0, 0, 24, 8, 8, 15) #Bas gauche / Bottom left
        pyxel.blt( 38, 8, 0, 8, 24, 8, 8, 15) #Bas droite / Bottom right
        
        #Affiche la grosse bombe. / Display the big bomb.
        pyxel.blt( 84, 0, 0, 16, 16, 8, 8, 15) #Haut gauche / Top left
        pyxel.blt( 92, 0, 0, 24, 16, 8, 8, 15) #Haut droite / Top right
        pyxel.blt( 84, 8, 0, 16, 24, 8, 8, 15) #Bas gauche / Bottom left
        pyxel.blt( 92, 8, 0, 24, 24, 8, 8, 15) #Bas droite / Bottom right
        #Séparation. / Separation.
        pyxel.rect(29, 17, 72, 0.5, 3)
        
        #Jeu en Français.
        pyxel.text( 18, 50, 'PRESSEZ F POUR FRANCAIS', 7)
        
        #Game in English.
        pyxel.text( 24, 80, 'PRESS E FOR ENGLISH', 7)
        
        #Crédit. / Credit.
        pyxel.text( 5, 120, 'RENAUD CORP.', 7)
 
                 
    def update_menu(self):
        '''Vérifie le lancement du jeu. / Check the launch of the game.'''
        self.lancement()
        
    def draw_menu(self):
        '''Affiche l'écran d'accueil. / Displays the home screen.'''
        pyxel.cls(6)
        pyxel.text( 43, 10, 'Fruit World', 7)
        
        #Affiche la grosse pomme. / Displays the big apple.
        pyxel.blt( 30, 0, 0, 0, 16, 8, 8, 15) #Haut gauche / Top left
        pyxel.blt( 38, 0, 0, 8, 16, 8, 8, 15) #Haut droite / Top right
        pyxel.blt( 30, 8, 0, 0, 24, 8, 8, 15) #Bas gauche / Bottom left
        pyxel.blt( 38, 8, 0, 8, 24, 8, 8, 15) #Bas droite / Bottom right
        
        #Affiche la grosse bombe. / Displays the big bomb.
        pyxel.blt( 84, 0, 0, 16, 16, 8, 8, 15) #Haut gauche / Top left
        pyxel.blt( 92, 0, 0, 24, 16, 8, 8, 15) #Haut droite / Top right
        pyxel.blt( 84, 8, 0, 16, 24, 8, 8, 15) #Bas gauche / Bottom left
        pyxel.blt( 92, 8, 0, 24, 24, 8, 8, 15) #Bas droite / Bottom right
        
        #Séparation. / Separation.
        pyxel.rect(29, 17, 72, 0.5, 3)
        
        #Écran des points. / Points screen.
        pyxel.text(self.langage[0][0], self.langage[0][1], self.langage[0][2], self.langage[0][3])
        
        #Écran des Controles. / Controls screen.
        pyxel.text(self.langage[1][0], self.langage[1][1], self.langage[1][2], self.langage[1][3])
        
        #Écran des Bonus. / Bonus screen.
        pyxel.text(self.langage[2][0], self.langage[2][1], self.langage[2][2], self.langage[2][3])
        
        #Lancer le jeu. / Launch the game.
        pyxel.text(self.langage[3][0], self.langage[3][1], self.langage[3][2], self.langage[3][3])
        
        #Crédits. / Credits.
        pyxel.text( 5, 120, 'RENAUD CORP.', 7)
        
        
    def update_pts(self):
        '''Vérifie le lancement du jeu. / Check the launch of the game.'''
        self.lancement()
           
    def draw_pts(self):
        '''Affiche l'écran des points. / Displays the points screen.'''
        pyxel.cls(6)
        pyxel.text( 43, 10, 'Fruit World', 7)
        
        #Affiche la grosse pomme. / Displays the big apple.
        pyxel.blt( 30, 0, 0, 0, 16, 8, 8, 15) #Haut gauche / Top left
        pyxel.blt( 38, 0, 0, 8, 16, 8, 8, 15) #Haut droite / Top right
        pyxel.blt( 30, 8, 0, 0, 24, 8, 8, 15) #Bas gauche / Bottom left
        pyxel.blt( 38, 8, 0, 8, 24, 8, 8, 15) #Bas droite / Bottom right
        
        #Affiche la grosse bombe. / Displays the big bomb.
        pyxel.blt( 84, 0, 0, 16, 16, 8, 8, 15) #Haut gauche / Top left
        pyxel.blt( 92, 0, 0, 24, 16, 8, 8, 15) #Haut droite / Top right
        pyxel.blt( 84, 8, 0, 16, 24, 8, 8, 15) #Bas gauche / Bottom left
        pyxel.blt( 92, 8, 0, 24, 24, 8, 8, 15) #Bas droite / Bottom right
        
        #Séparation. / Separation.
        pyxel.rect(29, 17, 72, 0.5, 3)
        pyxel.text( 54, 20, 'POINTS', 7)

        #Affichage des points. / Display of the points.
        pyxel.blt( 10, 35, 0, 0, 0, 8, 8, 0) #Pomme / Apple
        pyxel.text( 20, 38, '1 PTS', 7)        
        
        pyxel.blt( 70, 55, 0, 8, 0, 8, 8, 0) #Bombe / Bomb
        pyxel.text( 80, 58, '-1 PTS', 7)

        pyxel.blt( 70, 35, 0, 0, 8, 8, 8, 0) #Ananas / Pineapple
        pyxel.text( 80, 38, '10 PTS', 7)

        pyxel.blt( 10, 55, 0, 8, 8, 8, 8, 0) #Citron / Lemon
        pyxel.text( 20, 58, '3 PTS', 7)

        pyxel.blt( 10, 75, 0, 16, 8, 8, 8, 0) #Cerise / Cherry
        pyxel.text( 20, 78, '5 PTS', 7)
        
        pyxel.blt(65, 70, 0, 32, 32, 8, 8, 7)
        pyxel.blt(65, 78, 0, 32, 40, 8, 8, 7)
        pyxel.blt(73, 70, 0, 40, 32, 8, 8, 7)
        pyxel.blt(73, 78, 0, 40, 40, 8, 8, 7) #Personnage / Character
        pyxel.text(self.langage[4][0], self.langage[4][1], self.langage[4][2], self.langage[4][3])
        
        #Retourner à l'écran d'acceuil. / Return to the home screen.
        pyxel.text(self.langage[5][0], self.langage[5][1], self.langage[5][2], self.langage[5][3])
        
        
    def update_param(self):
        '''Vérifie le lancement du jeu. / Check the launch of the game.'''
        self.lancement()
           
    def draw_param(self):
        '''Affiche l'écran d'accueil. / Displays the home screen.'''
        pyxel.cls(6)
        pyxel.text( 43, 10, 'Fruit World', 7)
        
        #Affiche la grosse pomme. / Displays the big apple.
        pyxel.blt( 30, 0, 0, 0, 16, 8, 8, 15) #Haut gauche / Top left
        pyxel.blt( 38, 0, 0, 8, 16, 8, 8, 15) #Haut droite / Top right
        pyxel.blt( 30, 8, 0, 0, 24, 8, 8, 15) #Bas gauche / Bottom left
        pyxel.blt( 38, 8, 0, 8, 24, 8, 8, 15) #Bas droite / Bottom right
        
        #Affiche la grosse bombe. / Displays the big bomb.
        pyxel.blt( 84, 0, 0, 16, 16, 8, 8, 15) #Haut gauche / Top left
        pyxel.blt( 92, 0, 0, 24, 16, 8, 8, 15) #Haut droite / Top right
        pyxel.blt( 84, 8, 0, 16, 24, 8, 8, 15) #Bas gauche / Bottom left
        pyxel.blt( 92, 8, 0, 24, 24, 8, 8, 15) #Bas droite / Bottom right
        
        #Séparation. / Separation.
        pyxel.rect(29, 17, 72, 0.5, 3)
        pyxel.text(self.langage[6][0], self.langage[6][1], self.langage[6][2], self.langage[6][3])
        
        #Affichage du déplacement à gauche. / Displays the left movement.
        pyxel.blt( 34, 38, 0, 24, 0, 8, 8, 1)
        pyxel.text(self.langage[7][0], self.langage[7][1], self.langage[7][2], self.langage[7][3])
        pyxel.blt( 54, 38, 0, 40, 8, 8, 8, 1)
        pyxel.text(self.langage[8][0], self.langage[8][1], self.langage[8][2], self.langage[8][3])
        
        #Affichage du déplacement à droite. / Displays the right movement.
        pyxel.blt( 34, 58, 0, 24, 8, 8, 8, 1)
        pyxel.text(self.langage[9][0], self.langage[9][1], self.langage[9][2], self.langage[9][3])
        pyxel.blt( 54, 58, 0, 40, 0, 8, 8, 1)
        pyxel.text(self.langage[10][0], self.langage[10][1], self.langage[10][2], self.langage[10][3])
        
        #Affichage du saut. / Displays the jump.
        pyxel.rect( 39, 79, 20, 6, 0)
        pyxel.text(self.langage[11][0], self.langage[11][1], self.langage[11][2], self.langage[11][3])
        
        #Retourner à l'écran d'acceuil. / Return to the home screen.
        pyxel.text(self.langage[12][0], self.langage[12][1], self.langage[12][2], self.langage[12][3])
        
        
    def update_bonus(self):
        '''Vérifie le lancement du jeu. / Check the launch of the game.'''
        self.lancement()
           
    def draw_bonus(self):
        '''Affiche l'écran des points. / Displays the points screen.'''
        pyxel.cls(6)
        pyxel.text( 43, 10, 'Fruit World', 7)
        
        #Affiche la grosse pomme. / Displays the big apple.
        pyxel.blt( 30, 0, 0, 0, 16, 8, 8, 15) #Haut gauche / Top left
        pyxel.blt( 38, 0, 0, 8, 16, 8, 8, 15) #Haut droite / Top right
        pyxel.blt( 30, 8, 0, 0, 24, 8, 8, 15) #Bas gauche / Bottom left
        pyxel.blt( 38, 8, 0, 8, 24, 8, 8, 15) #Bas droite / Bottom right
        
        #Affiche la grosse bombe. / Displays the big bomb.
        pyxel.blt( 84, 0, 0, 16, 16, 8, 8, 15) #Haut gauche / Top left
        pyxel.blt( 92, 0, 0, 24, 16, 8, 8, 15) #Haut droite / Top right
        pyxel.blt( 84, 8, 0, 16, 24, 8, 8, 15) #Bas gauche / Bottom left
        pyxel.blt( 92, 8, 0, 24, 24, 8, 8, 15) #Bas droite / Bottom right
        
        #Séparation. / Separation.
        pyxel.rect(29, 17, 72, 0.5, 3)
        pyxel.text( 54, 20, 'BONUS', 7)

        #Affichage des points. / Displays the points.
        pyxel.blt( 10, 36, 0, 48, 32, 8, 8, 15) #Chrono / Chrono
        pyxel.text(self.langage[13][0], self.langage[13][1], self.langage[13][2], self.langage[13][3])        
        
        pyxel.blt( 10, 56, 0, 56, 32, 8, 8, 15) #Ombre / Shadow
        pyxel.text(self.langage[14][0], self.langage[14][1], self.langage[14][2], self.langage[14][3])

        pyxel.blt( 10, 76, 0, 48, 40, 8, 8, 15) #Carotte / Carrot
        pyxel.text(self.langage[15][0], self.langage[15][1], self.langage[15][2], self.langage[15][3])

        pyxel.blt( 10, 96, 0, 56, 40, 8, 8, 15) #Bombe Dorée / Golden Bomb
        pyxel.text(self.langage[16][0], self.langage[16][1], self.langage[16][2], self.langage[16][3])
        
        #Retourner à l'écran d'acceuil. / Return to the home screen.
        pyxel.text(self.langage[17][0], self.langage[17][1], self.langage[17][2], self.langage[17][3])
        
        
    def update_corps(self):
        '''Mise à jour des variables (30 fois par seconde). / Update the variables (30 times per second).'''
        
        #Déplacement du personnage. / Character movement.
        self.doodle_deplacement()
        
        #Création et déplacemnt des objets et bonus. / Creation and movement of objects and bonuses.
        self.objet_creation()
        self.objet_deplacement()
        self.bonus_creation()
        self.bonus_deplacement()
        
        #Vérification des collisions. / Check the collisions.
        self.colision_objet()
        self.colision_bonus()
        
        #Évolution de l'animation des explosions. / Evolution of the explosions animation.
        self.explosions_animation()
        
        #Mise à jour du temps restant. / Update the remaining time.
        self.temps()
        
        #Déplacement des astres. / Movement of the stars.
        self.astres()
        
    def draw_corps(self):
        '''Création et positionnement des objets (30 fois par seconde). / Creation and positioning of objects (30 times per second).'''
            
        #Création du ciel. / Creation of the sky.
        pyxel.cls(self.ciel)
        
            #Soleil et Lune / Sun and Moon 
        pyxel.blt(self.astre["x1"], self.astre["y1"], 0, self.astre["dessin1"], 32, 8, 8, 15)
        pyxel.blt(self.astre["x2"], self.astre["y2"], 0, self.astre["dessin2"], 32, 8, 8, 15)
        pyxel.blt(self.astre["x3"], self.astre["y3"], 0, self.astre["dessin3"], 40, 8, 8, 15)
        pyxel.blt(self.astre["x4"], self.astre["y4"], 0, self.astre["dessin4"], 40, 8, 8, 15)
                
        #Décoration du fond / Background decoration
            #Buissons / Bushes
        pyxel.blt(23, 112, 0, 32, 16, 8, 8, 15)
        pyxel.blt(31, 112, 0, 40, 16, 8, 8, 15)
        
        pyxel.blt(83, 112, 0, 32, 24, 8, 8, 15)
        pyxel.blt(91, 112, 0, 40, 24, 8, 8, 15)
        
        pyxel.blt(7, 112, 0, 32, 0, 8, 8, 15)        
        
            #Arbre / Tree
                #Ligne du bas / Bottom line
        pyxel.blt(45, 112, 0, 8, 72, 8, 8, 15)
        pyxel.blt(53, 112, 0, 16, 72, 8, 8, 15)
        pyxel.blt(61, 112, 0, 24, 72, 8, 8, 15)
        pyxel.blt(69, 112, 0, 32, 72, 8, 8, 15)
                #Ligne du milieu / Middle line
        pyxel.blt(45, 104, 0, 8, 64, 8, 8, 15)
        pyxel.blt(53, 104, 0, 16, 64, 8, 8, 15)
        pyxel.blt(61, 104, 0, 24, 64, 8, 8, 15)
        pyxel.blt(69, 104, 0, 32, 64, 8, 8, 15)
                #Ligne du haut / Top line
        pyxel.blt(45, 96, 0, 8, 56, 8, 8, 15)
        pyxel.blt(53, 96, 0, 16, 56, 8, 8, 15)
        pyxel.blt(61, 96, 0, 24, 56, 8, 8, 15)
        pyxel.blt(69, 96, 0, 32, 56, 8, 8, 15)
        
            #Cailloux / Rocks
        pyxel.blt(115, 112, 0, 48, 0, 8, 8, 15)
        pyxel.blt(123, 112, 0, 56, 0, 8, 8, 15)
        pyxel.blt(47, 112, 0, 48, 8, 8, 8, 15)
        
            #Nuages / Clouds
        pyxel.blt(115, 51, 0, 48, 16, 8, 8, 15)
        pyxel.blt(18, 34, 0, 56, 16, 8, 8, 15)
        pyxel.blt(47, 6, 0, 48, 24, 8, 8, 15)
        pyxel.blt(81, 63, 0, 56, 24, 8, 8, 15)
        
        #Création du fond pour le bonus. / Creation of the background for the bonus.
        if self.carotte == 1:
            pyxel.rect( 0, 0, 128, 128, 7)
            pyxel.text( 5, 5, str(self.minute) + ' MIN ' + str(self.seconde) + ' S', 0)  
            pyxel.text( 85, 5, str(self.score) + ' POINTS', 0)  
            
        #Création du sol. / Creation of the ground.
        pyxel.rect(0, 120, 128, 10, 3)   
              
        #Création du personnage. / Creation of the character.
        pyxel.blt(self.doodle["x1"], self.doodle["y1"], 0, 32, 32, 8, 8, 7)
        pyxel.blt(self.doodle["x2"], self.doodle["y2"], 0, 32, 40, 8, 8, 7)
        pyxel.blt(self.doodle["x3"], self.doodle["y3"], 0, 40, 32, 8, 8, 7)
        pyxel.blt(self.doodle["x4"], self.doodle["y4"], 0, 40, 40, 8, 8, 7)
        
        #Création des objets. / Creation of the objects.
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
                
        #Création des bonus. / Creation of the bonus.
        for bonus in self.bonus_liste:

            if bonus[2] == 5:
                pyxel.blt(bonus[0], bonus[1], 0, 48, 32, 8, 8, 15)
                
            elif bonus[2] == 6:
                pyxel.blt(bonus[0], bonus[1], 0, 56, 32, 8, 8, 15)
                
            elif bonus[2] == 7:
                pyxel.blt(bonus[0], bonus[1], 0, 48, 40, 8, 8, 15)
                
            elif bonus[2] == 8:
                pyxel.blt(bonus[0], bonus[1], 0, 56, 40, 8, 8, 15)
     
        #Création des explosions. / Creation of the explosions.
        for explosion in self.explosions_liste:
                pyxel.circb(explosion[0] + 4, explosion[1] + 4, 2 * (explosion[2] // 4), 8 + explosion[2] % 3)
            
        #Affichage du temps et du score. / Display of the time and the score.
        if self.carotte == 0:                    
            pyxel.text( 5, 5, str(self.minute) + ' MIN ' + str(self.seconde) + ' S', 7)  
            pyxel.text( 85, 5, str(self.score) + ' POINTS', 7)
        
        
    def update_fin(self):
        '''Vérifie le lancement du jeu après la fin du jeu. / Check the start of the game after the end of the game.'''
        self.lancement()
    
    def draw_fin(self):
        '''Affiche les informations de fin du jeu. / Display the end of the game information.'''
        
        #Vide la fenêtre et affiche le score final. / Empty the window and display the final score.
        pyxel.cls(6)
        pyxel.text( 43, 20, 'Fruit World', 7)
        pyxel.text( 32, 64,'SCORE: ' + str(self.score) + ' POINTS', 7)
        pyxel.text(self.langage[18][0], self.langage[18][1], self.langage[18][2], self.langage[18][3])
        
        #Affiche la grosse pomme. / Display the big apple.
        pyxel.blt( 30, 10, 0, 0, 16, 8, 8, 15) #Haut gauche / Top left
        pyxel.blt( 38, 10, 0, 8, 16, 8, 8, 15) #Haut droite / Top right
        pyxel.blt( 30, 18, 0, 0, 24, 8, 8, 15) #Bas gauche / Bottom left
        pyxel.blt( 38, 18, 0, 8, 24, 8, 8, 15) #Bas droite / Bottom right
        
        #Affiche la grosse bombe. / Display the big bomb.
        pyxel.blt( 84, 10, 0, 16, 16, 8, 8, 15) #Haut gauche / Top left
        pyxel.blt( 92, 10, 0, 24, 16, 8, 8, 15) #Haut droite / Top right
        pyxel.blt( 84, 18, 0, 16, 24, 8, 8, 15) #Bas gauche / Bottom left
        pyxel.blt( 92, 18, 0, 24, 24, 8, 8, 15) #Bas droite / Bottom right

#Lancement du jeu. / Launch of the game.
Jeu()