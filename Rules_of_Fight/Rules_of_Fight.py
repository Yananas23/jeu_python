'''
Rules of Fight et un jeu de combat où le but et de battre son adversaire en le frappant ou en utilisant son attaque spéciale.
'''

#on importe pyxel
import pyxel

class Jeu_2:
    '''Création de la classe gérant le jeu.'''

    def __init__(self):
        '''Fonction créant toutes les variables utiles au jeu.'''
        
        #Taille de la fenêtre et chargement des visuels
        pyxel.init(200, 80, title="Rules of Fight", quit_key=pyxel.KEY_ESCAPE)
        pyxel.load('Rules_of_Fight.pyxres')

        #Info relative au personnage 1
        self.p1 = { 'x': 16, 'y': 50, 'taille': 0, #Position
                    'frappe': 0, 'timer': 1, 'vie': 50, 'touchable': 0, #Attaque
                    'fireball': [], 'fb_timer': 0, #Boules de feu
                    'sol': 0, 'max': 0, 'dy': 0 #Saut
                   }

        #Info relative au personnage 2
        self.p2 = { 'x': 180, 'y': 50, 'taille': 0, #Position
                    'frappe': 0, 'timer': 1, 'vie': 50, 'touchable': 0, #Attaque
                    'fireball': [], 'fb_timer': 0, #Boules de feu
                    'sol': 0, 'max': 0, 'dy': 0 #Saut
                   }
                   
        #Variable pour le temps
        self.timer = 181
        self.minute = 0
        self.seconde = 0
        self.dcpt = 3
        self.music = 0
        
        #Variable de victoire
        self.victoire = 0

        #Lancement du jeu
        pyxel.run(self.update_acceuil,self.draw_acceuil)

    def p1_action(self):
        '''Fonction gérant toutes les actions du 1er personnage.'''
        
        #Saut
        if pyxel.btn(pyxel.KEY_Z):
            self.p1['sol'] = 1

            if self.p1['dy'] == 0:
                self.p1['max'] = self.p1['y'] - 20
                self.p1['dy'] = -2
                
        if self.p1['y'] < self.p1['max']:
            self.p1['dy'] = 2

        if self.p1['y'] > 50:
            self.p1['y'] = 50
            self.p1['dy'] = 0
            self.p1['sol'] = 0

        self.p1['y'] = self.p1['y'] + self.p1['dy']

        #Déplacement à droite.
        if pyxel.btn(pyxel.KEY_D) and self.p1['x'] <= 192:
            if self.p1['sol'] == 1:
                self.p1['x'] = self.p1['x'] + 2
            elif not self.p1['x'] == self.p2['x'] - 4:
                self.p1['x'] = self.p1['x'] + 2

        #Déplacement à gauche.
        if pyxel.btn(pyxel.KEY_Q) and self.p1['x'] >= 0:
            if self.p1['sol'] == 1:
                self.p1['x'] = self.p1['x'] - 2
            elif not self.p1['x'] - 4 == self.p2['x']:
                self.p1['x'] = self.p1['x'] - 2
      
        #S'accroupir
        if pyxel.btn(pyxel.KEY_S):
            self.p1['taille'] = 1  
        else:
            self.p1['taille'] = 0
            
        if pyxel.btn(pyxel.KEY_C):
            self.p1['frappe'] = 1 #frappe

        if self.p1['frappe'] == 1: #Cooldown de frappe
            if (pyxel.frame_count % 30 == 0):
                self.p1['timer'] = self.p1['timer'] - 1
                if self.p1['timer'] == 0:
                    self.p1['frappe'] = 0
                    self.p1['timer'] = 1
                               
        if self.p1['frappe'] != 0: #p1 frappe
            if self.p1['taille'] == self.p2['taille'] or self.p1['taille'] == 1:
                if self.p2['x'] - 5 < self.p1['x'] + 6 < self.p2['x'] + 6 and self.p2['touchable'] == 0: #Hitbox de p2
                    self.p2['vie'] = self.p2['vie'] - 5
                    pyxel.play( 0, 0)
                    self.p2['touchable'] = 3
                elif self.p2['x'] + 6 > self.p1['x'] - 6  > self.p2['x'] - 4 and self.p2['touchable'] == 0:             
                    self.p2['vie'] = self.p2['vie'] - 5
                    pyxel.play( 0, 0)
                    self.p2['touchable'] = 3
                    
    def p2_action(self):
        '''Fonction gérant toutes les actions du 2eme personnage.'''
        
        #Saut
        if pyxel.btn(pyxel.KEY_U):
            self.p2['sol'] = 1

            if self.p2['dy'] == 0:
                self.p2['max'] = self.p2['y'] - 20
                self.p2['dy'] = -2
                
        if self.p2['y'] < self.p2['max']:
            self.p2['dy'] = 2

        if self.p2['y'] > 50:
            self.p2['y'] = 50
            self.p2['dy'] = 0
            self.p2['sol'] = 0

        self.p2['y'] = self.p2['y'] + self.p2['dy']

        #Déplacement à droite.
        if pyxel.btn(pyxel.KEY_K) and self.p2['x'] <= 192:
            if self.p2['sol'] == 1:
                self.p2['x'] = self.p2['x'] + 2
            elif not self.p1['x'] - 4 == self.p2['x']:
                self.p2['x'] = self.p2['x'] + 2           

        #Déplacement à gauche.
        if pyxel.btn(pyxel.KEY_H) and self.p2['x'] >= 0:
            if self.p2['sol'] == 1:
                self.p2['x'] = self.p2['x'] - 2 
            elif not self.p1['x'] == self.p2['x'] - 4:
                self.p2['x'] = self.p2['x'] - 2           

        #S'accroupir
        if pyxel.btn(pyxel.KEY_J):
            self.p2['taille'] = 1  
        else:
            self.p2['taille'] = 0

        if pyxel.btn(pyxel.KEY_B):
            self.p2['frappe'] = 1 #frappe

        if self.p2['frappe'] == 1: #Cooldown de frappe
            if (pyxel.frame_count % 30 == 0):
                self.p2['timer'] = self.p2['timer'] - 1
                if self.p2['timer'] == 0:
                    self.p2['frappe'] = 0
                    self.p2['timer'] = 1

        if self.p2['frappe'] != 0: #p2 frappe
            if self.p1['taille'] == self.p2['taille'] or self.p2['taille'] == 1:
                if self.p1['x'] + 6 > self.p2['x'] - 6  > self.p1['x'] - 4 and self.p1['touchable'] == 0: #Hitbox de p1
                    pyxel.play( 0, 1)
                    self.p1['vie'] = self.p1['vie'] - 5
                    self.p1['touchable'] = 3
                elif self.p1['x'] - 5 < self.p2['x'] + 6 < self.p1['x'] + 6 and self.p1['touchable'] == 0:  
                    pyxel.play( 0, 1)
                    self.p1['vie'] = self.p1['vie'] - 5
                    self.p1['touchable'] = 3            
                 
    def fireball(self):
        '''Fonction gérant le déplacement des boules de feu.'''
        
        if self.p1['x'] < self.p2['x']:
            #P1
            if self.p1['fb_timer'] == 0:
                if pyxel.btn(pyxel.KEY_X):
                    self.p1['fireball'].append([self.p1['x'] + 6, self.p1['y'] + 6, 2, 'p1'])
                    self.p1['fb_timer'] = 10

            #P2
            if self.p2['fb_timer'] == 0:
                if pyxel.btn(pyxel.KEY_N):
                    self.p2['fireball'].append([self.p2['x'] - 6, self.p2['y'] + 6, -2,'p2'])
                    self.p2['fb_timer'] = 10
                         
        elif self.p1['x'] > self.p2['x']:
            #P1
            if self.p1['fb_timer'] == 0:
                if pyxel.btn(pyxel.KEY_X):
                    self.p1['fireball'].append([self.p1['x'] - 6, self.p1['y'] + 6, -2, 'p1'])
                    self.p1['fb_timer'] = 10
            
            #P2
            if self.p2['fb_timer'] == 0:
                if pyxel.btn(pyxel.KEY_N):
                    self.p2['fireball'].append([self.p2['x'] + 6, self.p2['y'] + 6, 2, 'p2'])
                    self.p2['fb_timer'] = 10
                    
        #Déplacement et collision
        for fb in self.p1['fireball']:
            fb[0] = fb[0] + fb[2]
            if  fb[0] > 210 or fb[0] < -10:
                self.p1['fireball'].remove(fb)
                
            elif self.p2['x'] - 2 <= fb[0] <= self.p2['x'] + 2 and self.p2['y'] <= fb[1] <= self.p2['y'] + 8 and self.p2['touchable'] == 0:
                self.p1['fireball'].remove(fb)
                self.p2['vie'] = self.p2['vie'] - 10
                self.p2['touchable'] = 3
                
        for fb in self.p2['fireball']:
            fb[0] = fb[0] + fb[2]
            if  fb[0] > 210 or fb[0] < -10:
                self.p2['fireball'].remove(fb)    
            
            elif self.p1['x'] - 2 <=  fb[0] <= self.p1['x'] + 2 and self.p2['y'] <= fb[1] <= self.p1['y'] + 8 and self.p1['touchable'] == 0:
                self.p2['fireball'].remove(fb)
                self.p1['vie'] = self.p1['vie'] - 10
                self.p1['touchable'] = 3


        if self.p1['fireball'] != [] and self.p2['fireball'] != []:
            if self.p1['fireball'][0][0] == self.p2['fireball'][0][0]:
                self.p1['fireball'] = []
                self.p2['fireball'] = []

    def temps(self):
        '''Fonction gérant les variables relative au temps.'''
        
        #Décompte du début de partie
        if self.dcpt > -1:
            if (pyxel.frame_count % 30 == 0):
                self.dcpt = self.dcpt - 1
            
        #Temps restant
        if self.dcpt < 0 and self.timer >= 0 and self.victoire == 0:
            if (pyxel.frame_count % 30 == 0): 
                self.timer = self.timer - 1 
                self.seconde = self.timer % 3600
                self.minute = int(self.timer/60) 
                self.seconde = self.timer % 60
            
        #Cooldown de protection  
        if (pyxel.frame_count % 30 == 0): 
            if self.p2['touchable'] != 0:
                self.p2['touchable'] = self.p2['touchable'] - 1
            if self.p1['touchable'] != 0:
                self.p1['touchable'] = self.p1['touchable'] - 1
                
        #Cooldown des boules de feu
        if (pyxel.frame_count % 30 == 0): 
            if self.p1['fb_timer'] > 0:
                self.p1['fb_timer'] = self.p1['fb_timer'] - 1
            if self.p2['fb_timer'] > 0:
                self.p2['fb_timer'] = self.p2['fb_timer'] - 1
      
    def reset(self):
        '''Fonction remettant toutes les variables à leurs valeurs d'origine.'''
        
        #Info relative au personnage 1
        self.p1 = { 'x': 16, 'y': 50, 'taille': 0, #Position
                    'frappe': 0, 'timer': 1, 'vie': 50, 'touchable': 0, #Attaque
                    'fireball': [], 'fb_timer': 0, #Boules de feu
                    'sol': 0, 'max': 0, 'dy': 0 #Saut
                   }

        #Info relative au personnage 2
        self.p2 = { 'x': 180, 'y': 50, 'taille': 0, #Position
                    'frappe': 0, 'timer': 1, 'vie': 50, 'touchable': 0, #Attaque
                    'fireball': [], 'fb_timer': 0, #Boules de feu
                    'sol': 0, 'max': 0, 'dy': 0 #Saut
                   }
                   
        #Variable pour le temps
        self.timer = 181
        self.minute = 0
        self.seconde = 0
        self.dcpt = 3
        self.music = 0
        
        #Variable de victoire
        self.victoire = 0
        
    def musique(self):
        '''Fonction gérant la musique de fond.'''
        
        if self.music != 1:
            pyxel.playm(0)
            self.music = 1
        

    '''UPDATE et DRAW'''
      
    def update_acceuil(self):
        '''Vérifie l'appuie des touches pour les controles ou le lancement du jeu.'''
        pyxel.mouse(True)
        
        if 78 <= pyxel.mouse_x <= 119 and 27 <= pyxel.mouse_y <= 38 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.run(self.update_control, self.draw_control)
            
        if 78 <= pyxel.mouse_x <= 119 and 45 <= pyxel.mouse_y <= 57 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.run(self.update_gameplay, self.draw_gameplay) 

    def draw_acceuil(self):
        '''Visuel de l'écran d'acceuil du jeu.'''
        
        pyxel.cls( 5)
        pyxel.text( 72, 5, 'RULES OF FIGHT', 7)
        pyxel.rect( 70, 11, 59, 1, 8)
        
        if 78 <= pyxel.mouse_x <= 119 and 27 <= pyxel.mouse_y <= 38:
            pyxel.rect( 78, 27, 42, 12, 8)
            pyxel.rectb( 78, 27, 42, 12, 0)
            pyxel.text( 82, 30, 'CONTROLES', 0)
        else :
            pyxel.rect( 78, 27, 42, 12, 7)
            pyxel.rectb( 78, 27, 42, 12, 0)
            pyxel.text( 82, 30, 'CONTROLES', 0)
               
        if 78 <= pyxel.mouse_x <= 119 and 45 <= pyxel.mouse_y <= 56:
            pyxel.rect( 78, 45, 42, 12, 8)
            pyxel.rectb( 78, 45, 42, 12, 0)
            pyxel.text( 89, 48, 'JOUER', 0)
        else :
            pyxel.rect( 78, 45, 42, 12, 7)
            pyxel.rectb( 78, 45, 42, 12, 0)
            pyxel.text( 89, 48, 'JOUER', 0)

        pyxel.text( 3, 72, 'RENAUD CORP.', 7)
        
    def update_control(self):
        '''Vérifie l'appuie des touches pour revenir à l'écran d'acceuil.'''
        pyxel.mouse(True)
        
        if 80 <= pyxel.mouse_x <= 119 and 62 <= pyxel.mouse_y <= 74 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.run(self.update_acceuil, self.draw_acceuil)

    def draw_control(self):
        '''Visuel du menu des controles.'''
        
        pyxel.cls( 5)
        pyxel.text( 82, 5, 'CONTROLES', 7)
        pyxel.rect( 80, 11, 39, 1, 8)
          
        #Frappe
        pyxel.blt( 15, 19, 0, 56, 0, 8, 8, 1)
        pyxel.text( 25, 20, 'OU', 7)
        pyxel.blt( 35, 19, 1, 56, 0, 8, 8, 1)
        pyxel.text( 45, 20, 'FRAPPE', 7)
        
        #Boules de feu
        pyxel.blt( 15, 34, 0, 64, 8, 8, 8, 1)
        pyxel.text( 25, 35, 'OU', 7)
        pyxel.blt( 35, 34, 1, 64, 8, 8, 8, 1)
        pyxel.text( 45, 35, 'BOULES DE FEU', 7)
        
        #Accroupie
        pyxel.blt( 15, 49, 0, 48, 8, 8, 8, 1)
        pyxel.text( 25, 50, 'OU', 7)
        pyxel.blt( 35, 49, 1, 48, 8, 8, 8, 1)
        pyxel.text( 45, 50, 'ACCROUPIE', 7)
        
        #Gauche
        pyxel.blt( 130, 19, 0, 48, 0, 8, 8, 1)
        pyxel.text( 140, 20, 'OU', 7)
        pyxel.blt( 150, 19, 1, 48, 0, 8, 8, 1)
        pyxel.text( 160, 20, 'GAUCHE', 7)
        
        #Droite
        pyxel.blt( 130, 34, 0, 56, 8, 8, 8, 1)
        pyxel.text( 140, 35, 'OU', 7)
        pyxel.blt( 150, 34, 1, 56, 8, 8, 8, 1)
        pyxel.text( 160, 35, 'DROITE', 7)
        
        #Saut
        pyxel.blt( 130, 49, 0, 64, 8, 8, 8, 1)
        pyxel.text( 140, 50, 'OU', 7)
        pyxel.blt( 150, 49, 1, 64, 8, 8, 8, 1)
        pyxel.text( 160, 50, 'Saut', 7)

        if 80 <= pyxel.mouse_x <= 118 and 62 <= pyxel.mouse_y <= 73:
            pyxel.rect( 80, 62, 39, 12, 8)
            pyxel.rectb( 80, 62, 39, 12, 0)
            pyxel.text( 88, 65, 'RETOUR', 0)
        else :
            pyxel.rect( 80, 62, 39, 12, 7)
            pyxel.rectb( 80, 62, 39, 12, 0)
            pyxel.text( 88, 65, 'RETOUR', 0)
        
    def update_gameplay(self):
        '''Update du jeu toutes les 30 frames.'''
        pyxel.mouse(False)
        
        #Fonctionnement du jeu
        if self.timer != 0 and self.dcpt < 0 and self.victoire == 0:
            self.p1_action()
            self.p2_action()
            self.musique()
            self.fireball()
            
        #Lancement des différents chrono
        self.temps()
            
        #Remise à zéro du jeu    
        if 78 <= pyxel.mouse_x <= 119 and 45 <= pyxel.mouse_y <= 56 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.victoire != 0:
            self.reset()

        #Arret de la musique
        if self.victoire == 1:
            pyxel.stop()
            
    def draw_gameplay(self):
        '''Visuel du jeu'''
        
        #Décors
            #Ciel
        pyxel.cls( 1)
            #Route
        pyxel.rect(0, 64, 200, 20, 0)
        pyxel.rect(10, 70, 15, 1, 7)
        pyxel.rect(60, 70, 15, 1, 7)
        pyxel.rect(110, 70, 15, 1, 7)
        pyxel.rect(160, 70, 15, 1, 7)
            #Voiture
        pyxel.blt(10, 56, 0, 48, 16, 8, 8, 14)
        pyxel.blt(18, 56, 0, 56, 16, 8, 8, 14)
        pyxel.blt(178, 56, 1, 48, 16, 8, 8, 14)
        pyxel.blt(186, 56, 1, 56, 16, 8, 8, 14)
            #Lune
        pyxel.blt(150, 16, 0, 0, 24, 8, 8, 14)
        pyxel.blt(158, 16, 0, 8, 24, 8, 8, 14)
        pyxel.blt(150, 24, 0, 0, 32, 8, 8, 14)
        pyxel.blt(158, 24, 0, 8, 32, 8, 8, 14)  

        #P1
        if self.p1['touchable'] % 2 == 0:
            if self.p1['taille'] == 0: #Debout
                pyxel.blt(self.p1['x'], self.p1['y'], 1, 0, 0, 8, 8, 14)
                pyxel.blt(self.p1['x'], self.p1['y'] + 8, 1, 0, 8, 8, 8, 14)
            elif self.p1['taille'] == 1: #Accroupie
                pyxel.blt(self.p1['x'], self.p1['y'] + 8, 0, 8, 8, 8, 8, 14)
 
        #P2
        if self.p2['touchable'] % 2 == 0:
            if self.p2['taille'] == 0: #Debout
                pyxel.blt(self.p2['x'], self.p2['y'], 1, 24, 0, 8, 8, 14)
                pyxel.blt(self.p2['x'], self.p2['y'] + 8, 1, 24, 8, 8, 8, 14)
            elif self.p2['taille'] == 1: #Accroupie
                pyxel.blt(self.p2['x'], self.p2['y'] + 8, 0, 16, 8, 8, 8, 14)
                      
        #P1 frappe
        if self.p1['touchable'] % 2 == 0:
            if self.p1['x'] < self.p2['x']:
                if self.p1['frappe'] == 1 and self.p1['taille'] == 0: #Debout
                    pyxel.blt(self.p1['x'], self.p1['y'], 0, 0, 0, 8, 8, 14)
                    pyxel.blt(self.p1['x'], self.p1['y'] + 8, 0, 0, 8, 8, 8, 14)
                    pyxel.blt(self.p1['x'] + 8, self.p1['y'], 0, 8, 0, 8, 8, 14) 
                elif self.p1['frappe'] == 1 and self.p1['taille'] == 1: #Accroupie
                    pyxel.blt(self.p1['x'], self.p1['y'] + 8, 0, 0, 16, 8, 8, 14) 
                    pyxel.blt(self.p1['x'] + 8, self.p1['y'] + 8, 0, 8, 16, 8, 8, 14)
            if self.p1['x'] > self.p2['x']:
                if self.p1['frappe'] == 1 and self.p1['taille'] == 0: #Debout
                    pyxel.blt(self.p1['x'], self.p1['y'], 0, 0, 0, -8, 8, 14)
                    pyxel.blt(self.p1['x'], self.p1['y'] + 8, 0, 0, 8, 8, 8, 14)
                    pyxel.blt(self.p1['x'] - 8, self.p1['y'], 0, 8, 0, -8, 8, 14) 
                elif self.p1['frappe'] == 1 and self.p1['taille'] == 1: #Accroupie
                    pyxel.blt(self.p1['x'], self.p1['y'] + 8, 0, 0, 16, -8, 8, 14) 
                    pyxel.blt(self.p1['x'] - 8, self.p1['y'] + 8, 0, 8, 16, -8, 8, 14)
                    
        #P2 frappe
        if self.p2['touchable'] % 2 == 0:
            if self.p1['x'] < self.p2['x']:
                if self.p2['frappe'] == 1 and self.p2['taille'] == 0: #Debout
                    pyxel.blt(self.p2['x'], self.p2['y'], 0, 24, 0, 8, 8, 14)
                    pyxel.blt(self.p2['x'], self.p2['y'] + 8, 0, 24, 8, 8, 8, 14)
                    pyxel.blt(self.p2['x'] - 8, self.p2['y'], 0, 16, 0, 8, 8, 14)                        
                elif self.p2['frappe'] == 1 and self.p2['taille'] == 1: #Accroupie
                    pyxel.blt(self.p2['x'], self.p2['y'] + 8, 0, 24, 16, 8, 8, 14) 
                    pyxel.blt(self.p2['x'] - 8, self.p2['y'] + 8, 0, 16, 16, 8, 8, 14)
            elif self.p1['x'] > self.p2['x']:
                if self.p2['frappe'] == 1 and self.p2['taille'] == 0: #Debout
                    pyxel.blt(self.p2['x'], self.p2['y'], 0, 24, 0, -8, 8, 14)
                    pyxel.blt(self.p2['x'], self.p2['y'] + 8, 0, 24, 8, 8, 8, 14)
                    pyxel.blt(self.p2['x'] + 8, self.p2['y'], 0, 16, 0, -8, 8, 14)                        
                elif self.p2['frappe'] == 1 and self.p2['taille'] == 1: #Accroupie
                    pyxel.blt(self.p2['x'], self.p2['y'] + 8, 0, 24, 16, -8, 8, 14) 
                    pyxel.blt(self.p2['x'] + 8, self.p2['y'] + 8, 0, 16, 16, -8, 8, 14)
                
        #Boule de feu
        if self.p1['x'] < self.p2['x']:
                #P1
            for fb in self.p1['fireball']:
                pyxel.blt( fb[0], fb[1], 0, 24, 24, 8, 8, 0)
                pyxel.blt( fb[0] - 8, fb[1], 0, 16, 24, 8, 8, 0)
                #P2
            for fb in self.p2['fireball']:
                pyxel.blt( fb[0], fb[1], 0, 24, 32, 8, 8, 0)
                pyxel.blt( fb[0] - 8, fb[1], 0, 16, 32, 8, 8, 0)
        elif self.p1['x'] > self.p2['x']:
                #P1
            for fb in self.p1['fireball']:
                pyxel.blt( fb[0], fb[1], 1, 24, 24, 8, 8, 0)
                pyxel.blt( fb[0] - 8, fb[1], 1, 16, 24, 8, 8, 0)
                #P2
            for fb in self.p2['fireball']:
                pyxel.blt( fb[0], fb[1], 1, 24, 32, 8, 8, 0)
                pyxel.blt( fb[0] - 8, fb[1], 1, 16, 32, 8, 8, 0)

        #Affichage du décompte
        if self.dcpt > 0:
            pyxel.text( 98, 35, str(self.dcpt), 7)
        elif self.dcpt > -1:
            pyxel.text( 90, 35, 'START', 7)

        #Affichage du temps restant
        pyxel.rect( 91, 3, 20, 9, 0)
        pyxel.rect( 93, 0, 1, 5, 0)
        pyxel.rect( 108, 0, 1, 5, 0)
        pyxel.text( 94, 5, str(self.minute) + '.' + str(self.seconde), 9)

        #Vie p1
        pyxel.rect( 4, 3, 49, 5, 13)
        pyxel.rect( 4, 4, 50, 3, 0)
        pyxel.rect( 4, 4, self.p1['vie'], 3, 8)
        pyxel.blt( 49, 1, 0, 32, 8, 8, 8, 0)
        pyxel.blt( 3, 1, 0, 40, 8, 8, 8, 0)
        pyxel.blt( 58, 2, 0, 32, 16, 8, 8, 14)

        #Vie p2
        pyxel.rect( 146, 3, 49, 5, 13)
        pyxel.rect( 145, 4, 50, 3, 0)
        pyxel.rect( 145 + 50 - self.p2['vie'] , 4, self.p2['vie'], 3, 8)
        pyxel.blt( 142, 1, 0, 32, 0, 8, 8, 0)
        pyxel.blt( 188, 1, 0, 40, 0, 8, 8, 0)
        pyxel.blt( 133, 2, 0, 40, 16, 8, 8, 14)

        #Affichage de la victoire
        if self.p1['vie'] <= 0:
            pyxel.mouse(True)
            pyxel.text( 65, 35, 'VICTOIRE DU JOUEUR 2', 10)
            
            if 78 <= pyxel.mouse_x <= 119 and 45 <= pyxel.mouse_y <= 56:
                pyxel.rect( 78, 45, 42, 12, 8)
                pyxel.rectb( 78, 45, 42, 12, 0)
                pyxel.text( 86, 48, 'REJOUER', 0)
            else :
                pyxel.rect( 78, 45, 42, 12, 7)
                pyxel.rectb( 78, 45, 42, 12, 0)
                pyxel.text( 86, 48, 'REJOUER', 0)
                
            self.victoire = 1
        elif self.p2['vie'] <= 0:
            pyxel.text( 65, 35, 'VICTOIRE DU JOUEUR 1', 4)
            pyxel.mouse(True)
            
            if 78 <= pyxel.mouse_x <= 119 and 45 <= pyxel.mouse_y <= 56:
                pyxel.rect( 78, 45, 42, 12, 8)
                pyxel.rectb( 78, 45, 42, 12, 0)
                pyxel.text( 86, 48, 'REJOUER', 0)
            else :
                pyxel.rect( 78, 45, 42, 12, 7)
                pyxel.rectb( 78, 45, 42, 12, 0)
                pyxel.text( 86, 48, 'REJOUER', 0)
                
            self.victoire = 1
        
        elif self.timer <= 0:
            if self.p1['vie'] > self.p2['vie']:
                pyxel.text( 65, 35, 'VICTOIRE DU JOUEUR 1', 4)
                pyxel.mouse(True)
            
                if 78 <= pyxel.mouse_x <= 119 and 45 <= pyxel.mouse_y <= 56:
                    pyxel.rect( 78, 45, 42, 12, 8)
                    pyxel.rectb( 78, 45, 42, 12, 0)
                    pyxel.text( 86, 48, 'REJOUER', 0)
                else :
                    pyxel.rect( 78, 45, 42, 12, 7)
                    pyxel.rectb( 78, 45, 42, 12, 0)
                    pyxel.text( 86, 48, 'REJOUER', 0)
                    
                self.victoire = 1
            else:
                pyxel.text( 65, 35, 'VICTOIRE DU JOUEUR 2', 10)
                pyxel.mouse(True)
            
                if 78 <= pyxel.mouse_x <= 119 and 45 <= pyxel.mouse_y <= 56:
                    pyxel.rect( 78, 45, 42, 12, 8)
                    pyxel.rectb( 78, 45, 42, 12, 0)
                    pyxel.text( 86, 48, 'REJOUER', 0)
                else :
                    pyxel.rect( 78, 45, 42, 12, 7)
                    pyxel.rectb( 78, 45, 42, 12, 0)
                    pyxel.text( 86, 48, 'REJOUER', 0)
                    
                self.victoire = 1


#Lancement de la Class
Jeu_2()