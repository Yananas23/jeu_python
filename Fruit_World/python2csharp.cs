// 
//     Fruit World est un jeu de simulation consistant à attraper le maximum de fruits tout en évitant les bombes avec votre panier.
//     
//     Contrôle:
//     Flèches Gauche et Droite : Vous permet d'aller respectivement à gauche et à droite
//     Barre Espace : Vous permet de sauter pour esquiver les bombes ou attraper des fruits en hauteur.
//     Échap: Vous permet de fermer le jeu.
//     
//     Écran de jeu:
//     Score: Affiche votre score en temps réel.
//     Temps: Affiche le temps restant.
//     
//     Points:
//     Pomme: Ajoute 1 points.
//     Citron: Ajoute 3 points.
//     Cerise: Ajoute 5 points.
//     Ananas: Ajoute 10 points.
//     Bombe: Retire 1 points.
//     
//     Bonus (Dure 15 secondes):
//     Chrono: Ralenti la chute des objets.
//     Ombre: Accélère la doodle["speed"] de base du personnage.
//     Carotte: Permet une meilleur vision des objets.
//     Bombe Dorée: Plus aucune bombe n'apparait.
//     
// ================================================
// 
//     Fruit World is a simulation game consisting of catching the maximum amount of fruit while avoiding bombs with your hand.
//     
//     Control:
//     Left and Right arrows or Q and D: Allows you to go left and right respectively.
//     Space Bar: Lets you jump to dodge bombs or catch fruit in height.
//     Esc: Allows you to close the game.
//     
//     Game screen:
//     Score: Displays your score in real time.
//     Time: Displays the remaining time.
//     
//     Points:
//     Apple: Add 1 points.
//     Lemon: Add 3 points.
//     Cherry: Add 5 points.
//     Pineapple: Add 10 points.
//     Bomb: Remove 1 points.
//     
//     Bonus (Lasts 15 seconds):
//     Chrono: Slows down the fall of objects.
//     Shadow: Accelerates the basic speed of the character.
//     Carrot: Allows a better vision of objects.
//     Golden Bomb: No more bombs appear.
// 
namespace Namespace {
    
    using pyxel;
    
    using random;
    
    using System.Collections.Generic;
    
    using System;
    
    public static class Module {
        
        // Création de la classe gérant le jeu. / Creation of the class managing the game.
        public class Jeu {
            
            public Jeu() {
                //Chargement des visuels./Loading visuals.
                pyxel.init(128, 128, title: "Fruit World", quit_key: pyxel.KEY_ESCAPE);
                pyxel.load("Fruit_World.pyxres");
                //Info de base du personnage / Basic info of the character
                this.doodle = new Dictionary<object, object> {
                    {
                        "speed",
                        4},
                    {
                        "jump",
                        0},
                    {
                        "max",
                        0},
                    {
                        "dy",
                        0},
                    {
                        "distance",
                        0},
                    {
                        "x1",
                        60},
                    {
                        "y1",
                        110},
                    {
                        "x2",
                        60},
                    {
                        "y2",
                        118},
                    {
                        "x3",
                        68},
                    {
                        "y3",
                        110},
                    {
                        "x4",
                        68},
                    {
                        "y4",
                        118}};
                //Position du Soleil et Lune / Position of the Sun and Moon
                this.astre = new Dictionary<object, object> {
                    {
                        "dessin1",
                        0},
                    {
                        "x1",
                        120},
                    {
                        "y1",
                        120},
                    {
                        "dessin2",
                        8},
                    {
                        "x2",
                        128},
                    {
                        "y2",
                        120},
                    {
                        "dessin3",
                        0},
                    {
                        "x3",
                        120},
                    {
                        "y3",
                        128},
                    {
                        "dessin4",
                        8},
                    {
                        "x4",
                        128},
                    {
                        "y4",
                        128}};
                //Score au début de la partie / Score at the beginning of the game
                this.score = 0;
                //Valeur pour les niveaux de difficultés / Value for the levels of difficulty
                this.ciel = 6;
                this.ratio = (45, 20, 5, 20, 10);
                //Liste pour les éléments du jeu autre que le personnage / List for game elements other than the character
                this.objet_liste = new List<object>();
                this.explosions_liste = new List<object>();
                this.bonus_liste = new List<object>();
                this.list_vitesse = new List<object> {
                    0.5,
                    1,
                    1.5,
                    2
                };
                //Variable pour les bonus / Variable for bonuses
                this.tps_bonus = 0;
                this.carotte = 0;
                //Variable pour le temps / Variable for time
                this.timer = 90;
                this.minute = 0;
                this.seconde = 0;
                //Lancement du jeu / Launch of the game
                this.ecran = 0;
                pyxel.run(this.update_acceuil, this.draw_acceuil);
            }
            
            // Fonction pour les déplacements. / Function for movements.
            public virtual object doodle_deplacement() {
                //Saut / Jump
                if (pyxel.btn(pyxel.KEY_SPACE)) {
                    if (this.doodle["dy"] == 0) {
                        this.doodle["max"] = this.doodle["y1"] - 23;
                        this.doodle["dy"] = -1;
                    }
                }
                if (this.doodle["y1"] < this.doodle["max"]) {
                    this.doodle["dy"] = 1;
                }
                if (this.doodle["y1"] > 110) {
                    this.doodle["y1"] = 110;
                    this.doodle["y3"] = 110;
                    this.doodle["y2"] = 118;
                    this.doodle["y4"] = 118;
                    this.doodle["dy"] = 0;
                }
                this.doodle["y1"] = this.doodle["y1"] + this.doodle["dy"];
                this.doodle["y2"] = this.doodle["y2"] + this.doodle["dy"];
                this.doodle["y3"] = this.doodle["y3"] + this.doodle["dy"];
                this.doodle["y4"] = this.doodle["y4"] + this.doodle["dy"];
                //Déplacement à droite. / Right movement.
                if ((pyxel.btn(pyxel.KEY_RIGHT) || pyxel.btn(pyxel.KEY_D)) && this.doodle["x1"] <= 108) {
                    this.doodle["x1"] = this.doodle["x1"] + this.doodle["speed"];
                    this.doodle["x2"] = this.doodle["x2"] + this.doodle["speed"];
                    this.doodle["x3"] = this.doodle["x3"] + this.doodle["speed"];
                    this.doodle["x4"] = this.doodle["x4"] + this.doodle["speed"];
                }
                //Déplacement à gauche. / Left movement.
                if ((pyxel.btn(pyxel.KEY_LEFT) || pyxel.btn(pyxel.KEY_Q)) && this.doodle["x1"] >= 4) {
                    this.doodle["x1"] = this.doodle["x1"] - this.doodle["speed"];
                    this.doodle["x2"] = this.doodle["x2"] - this.doodle["speed"];
                    this.doodle["x3"] = this.doodle["x3"] - this.doodle["speed"];
                    this.doodle["x4"] = this.doodle["x4"] - this.doodle["speed"];
                }
            }
            
            // Fonction gérant la création des objets. / Function managing the creation of objects.
            public virtual object objet_creation() {
                var type_objet = new List<object> {
                    0,
                    1,
                    2,
                    3,
                    4
                };
                if (pyxel.frame_count % 30 == 0) {
                    //Nouvel objet toutes les 30 frames (environ 1 seconde) / New object every 30 frames (about 1 second)
                    //Aléatoire pour le type de fruit. / Random for the type of fruit.
                    var int_objet = random.choices(type_objet, weights: this.ratio, k: 1);
                    //Créé une pomme. / Create an apple.
                    if (int_objet[0] == 0) {
                        this.objet_liste.append(new List<object> {
                            random.randint(0, 120),
                            0,
                            int_objet[0],
                            random.choices(this.list_vitesse, weights: (20, 25, 25, 30), k: 1)
                        });
                    } else if (int_objet[0] == 1) {
                        //Créé une bombe. / Create a bomb.
                        this.objet_liste.append(new List<object> {
                            random.randint(0, 120),
                            0,
                            int_objet[0],
                            random.choices(this.list_vitesse, weights: (10, 20, 30, 40), k: 1)
                        });
                    } else if (int_objet[0] == 2) {
                        //Créé un Ananas. / Create a pineapple.
                        this.objet_liste.append(new List<object> {
                            random.randint(0, 120),
                            0,
                            int_objet[0],
                            random.choices(this.list_vitesse, weights: (10, 20, 30, 40), k: 1)
                        });
                    } else if (int_objet[0] == 3) {
                        //Créé un citron. / Create a lemon.
                        this.objet_liste.append(new List<object> {
                            random.randint(0, 120),
                            0,
                            int_objet[0],
                            random.choices(this.list_vitesse, weights: (20, 20, 30, 30), k: 1)
                        });
                    } else if (int_objet[0] == 4) {
                        //Créé des cerises. / Create cherries.
                        this.objet_liste.append(new List<object> {
                            random.randint(0, 120),
                            0,
                            int_objet[0],
                            random.choices(this.list_vitesse, weights: (10, 20, 40, 30), k: 1)
                        });
                    }
                }
            }
            
            // Fonction gérant la création des bonus. / Function managing the creation of bonuses.
            public virtual object bonus_creation() {
                var type_bonus = new List<object> {
                    5,
                    6,
                    7,
                    8
                };
                if (pyxel.frame_count % 900 == 0) {
                    //Nouveau bonus toutes les 900 frames (environ 30 secondes) / New bonus every 900 frames (about 30 seconds)
                    if (random.choices(new List<object> {
                        0,
                        1
                    }, weights: (60, 40), k: 1) == new List<object> {
                        1
                    }) {
                        //Aléatoire pour le type de bonus. / Random for the type of bonus.
                        var int_bonus = random.choices(type_bonus, weights: (25, 25, 25, 25), k: 1);
                        //Créé un chrono. / Create a chrono.
                        if (int_bonus[0] == 5) {
                            this.bonus_liste.append(new List<object> {
                                random.randint(0, 120),
                                0,
                                int_bonus[0],
                                random.choices(this.list_vitesse, weights: (20, 25, 25, 30), k: 1)
                            });
                        } else if (int_bonus[0] == 6) {
                            //Créé une ombre. / Create a shadow.
                            this.bonus_liste.append(new List<object> {
                                random.randint(0, 120),
                                0,
                                int_bonus[0],
                                random.choices(this.list_vitesse, weights: (10, 20, 30, 40), k: 1)
                            });
                        } else if (int_bonus[0] == 7) {
                            //Créé une carotte. / Create a carrot.
                            this.bonus_liste.append(new List<object> {
                                random.randint(0, 120),
                                0,
                                int_bonus[0],
                                random.choices(this.list_vitesse, weights: (10, 20, 30, 40), k: 1)
                            });
                        } else if (int_bonus[0] == 8) {
                            //Créé une bombe dorée. / Create a golden bomb.
                            this.bonus_liste.append(new List<object> {
                                random.randint(0, 120),
                                0,
                                int_bonus[0],
                                random.choices(this.list_vitesse, weights: (20, 20, 30, 30), k: 1)
                            });
                        }
                    }
                }
            }
            
            // Fonction gérant le déplacement des objets. / Function managing the movement of objects.
            public virtual object objet_deplacement() {
                //Fruits et Bombes / Fruits and Bombs
                foreach (var objet in this.objet_liste) {
                    objet[1] = objet[1] + objet[3][0];
                    if (objet[1] > 120) {
                        //supprime l'objet de la liste si il est trop bas sur l'écran. / remove the object from the list if it is too low on the screen.
                        this.objet_liste.remove(objet);
                    }
                }
            }
            
            // Fonction gérant le déplacement des bonus. / Function managing the movement of bonuses.
            public virtual object bonus_deplacement() {
                foreach (var bonus in this.bonus_liste) {
                    bonus[1] = bonus[1] + bonus[3][0];
                    if (bonus[1] > 120) {
                        //supprime le bonus de la liste si il est trop bas sur l'écran. / remove the bonus from the list if it is too low on the screen.
                        this.bonus_liste.remove(bonus);
                    }
                }
            }
            
            // Fonction gérant la colision entre le personnage et les objets. / Function managing the collision between the character and the objects.
            public virtual object colision_objet() {
                foreach (var objet in this.objet_liste) {
                    if (objet[0] >= this.doodle["x1"] - 2 && objet[0] <= this.doodle["x1"] + 13 && (objet[1] >= this.doodle["y1"] && objet[1] <= this.doodle["y1"] + 10)) {
                        //Vérifie si les coordonnées de l'objet sont proche de celle du personnage.
                        this.objet_liste.remove(objet);
                        if (objet[2] == 0) {
                            //Pomme / Apple
                            this.score = this.score + 1;
                            pyxel.play(0, 1);
                        } else if (objet[2] == 1) {
                            //Bombe / Bomb
                            this.score = this.score - 1;
                            this.explosions_creation(this.doodle["x1"] + 2, this.doodle["y1"] + 2);
                            pyxel.play(0, 0);
                        } else if (objet[2] == 2) {
                            //Ananas / Pineapple
                            this.score = this.score + 10;
                            pyxel.play(0, 1);
                        } else if (objet[2] == 3) {
                            //Citron / Lemon
                            this.score = this.score + 3;
                            pyxel.play(0, 1);
                        } else if (objet[2] == 4) {
                            //Cerise / Cherry
                            this.score = this.score + 5;
                            pyxel.play(0, 1);
                        }
                    }
                }
            }
            
            // Fonction gérant la colision entre le personnage et les bonus. / Function managing the collision between the character and the bonuses.
            public virtual object colision_bonus() {
                foreach (var bonus in this.bonus_liste) {
                    if (bonus[0] >= this.doodle["x1"] - 2 && bonus[0] <= this.doodle["x1"] + 13 && (bonus[1] >= this.doodle["y1"] && bonus[1] <= this.doodle["y1"] + 10)) {
                        //Vérifie si les coordonnées de l'bonus sont proche de celle du personnage.
                        this.bonus_liste.remove(bonus);
                        if (bonus[2] == 5 && this.tps_bonus == 0) {
                            //Chrono / Chrono
                            this.tps_bonus = 10;
                            this.list_vitesse = new List<object> {
                                1,
                                1,
                                1,
                                1
                            };
                            pyxel.play(0, 2);
                        } else if (bonus[2] == 6 && this.tps_bonus == 0) {
                            //Ombre / Shadow
                            this.tps_bonus = 10;
                            this.doodle["speed"] = 8;
                            pyxel.play(0, 2);
                        } else if (bonus[2] == 7 && this.tps_bonus == 0) {
                            //Carotte / Carrot
                            this.tps_bonus = 10;
                            this.carotte = 1;
                            pyxel.play(0, 2);
                        } else if (bonus[2] == 8 && this.tps_bonus == 0) {
                            //Bombe dorée / Golden bomb
                            this.tps_bonus = 10;
                            this.ratio = (50, 0, 10, 25, 15);
                            pyxel.play(0, 2);
                        }
                    }
                }
                if (pyxel.frame_count % 30 == 0 && this.tps_bonus > 0) {
                    this.tps_bonus = this.tps_bonus - 1;
                    if (this.tps_bonus == 0) {
                        this.doodle["speed"] = 4;
                        this.ratio = (45, 20, 5, 20, 10);
                        this.list_vitesse = new List<object> {
                            0.5,
                            1,
                            1.5,
                            2
                        };
                        this.carotte = 0;
                    }
                }
            }
            
            // Fonction gérant la création d'une explosion. / Function managing the creation of an explosion.
            public virtual object explosions_creation(object x, object y) {
                this.explosions_liste.append(new List<object> {
                    x,
                    y,
                    0
                });
            }
            
            // Fonction gérant l'animation des explosions (cercle de plus en plus grand) / Function managing the animation of the explosions (circle getting bigger)
            public virtual object explosions_animation() {
                foreach (var explosion in this.explosions_liste) {
                    explosion[2] = explosion[2] + 1;
                    if (explosion[2] == 12) {
                        this.explosions_liste.remove(explosion);
                    }
                }
            }
            
            // Permet le déplacement des astres. / Allows the movement of the stars.
            public virtual object astres() {
                if (pyxel.frame_count % 10 == 0) {
                    //Mouvement toutes les 10 frame (environ 0.5 seconde) / Movement every 10 frames (about 0.5 second)
                    if (this.astre["x1"] > -20 && this.astre["y1"] > 30) {
                        this.astre["x1"] = this.astre["x1"] - 1.5;
                        this.astre["x2"] = this.astre["x2"] - 1.5;
                        this.astre["x3"] = this.astre["x3"] - 1.5;
                        this.astre["x4"] = this.astre["x4"] - 1.5;
                        this.astre["y1"] = this.astre["y1"] - 1;
                        this.astre["y2"] = this.astre["y2"] - 1;
                        this.astre["y3"] = this.astre["y3"] - 1;
                        this.astre["y4"] = this.astre["y4"] - 1;
                    } else {
                        this.astre["y1"] = 150;
                        this.astre["y2"] = 150;
                        this.astre["y3"] = 158;
                        this.astre["y4"] = 158;
                        this.astre["x1"] = 142;
                        this.astre["x2"] = 150;
                        this.astre["x3"] = 142;
                        this.astre["x4"] = 150;
                    }
                }
                //Changement pour la lune à 50 secondes restante. / Change for the moon at 50 seconds remaining. 
                if (13 < this.timer <= 50) {
                    this.ciel = 5;
                    this.astre["dessin1"] = 16;
                    this.astre["dessin2"] = 24;
                    this.astre["dessin3"] = 16;
                    this.astre["dessin4"] = 24;
                } else if (this.timer <= 13) {
                    //Changement pour le soleil à 13 secondes restante. / Change for the sun at 13 seconds remaining.
                    this.ciel = 6;
                    this.astre["dessin1"] = 0;
                    this.astre["dessin2"] = 8;
                    this.astre["dessin3"] = 0;
                    this.astre["dessin4"] = 8;
                }
            }
            
            // Fonction gérant le temps restant. / Function managing the remaining time.
            public virtual object temps() {
                if (pyxel.frame_count % 30 == 0) {
                    this.timer = this.timer - 1;
                    this.seconde = this.timer % 3600;
                    this.minute = Convert.ToInt32(this.timer / 60);
                    this.seconde = this.timer % 60;
                    //Met l'écran de fin du jeu. / Put the end screen of the game.
                    if (this.timer == 0) {
                        this.ecran = 0;
                        pyxel.run(this.update_fin, this.draw_fin);
                    }
                }
            }
            
            // Fonction gérant la langue. / Function managing the language.
            public virtual object langue() {
                if (pyxel.btn(pyxel.KEY_F)) {
                    //jeu en français / game in french
                    this.langage = new List<object> {
                        pyxel.text(14, 40, "PRESSEZ P POUR LES POINTS", 7),
                        pyxel.text(9, 60, "PRESSEZ C POUR LES CONTROLES", 7),
                        pyxel.text(15, 80, "PRESSEZ B POUR LES BONUS", 7),
                        pyxel.text(16, 100, "PRESSEZ S POUR DEMARRER", 7),
                        pyxel.text(83, 78, "Vous", 7),
                        pyxel.text(20, 110, "PRESSEZ R POUR REVENIR", 7),
                        pyxel.text(49, 20, "CONTROLES", 7),
                        pyxel.text(44, 40, "ou", 7),
                        pyxel.text(65, 40, "Gauche", 7),
                        pyxel.text(44, 60, "ou", 7),
                        pyxel.text(65, 60, "Droite", 7),
                        pyxel.text(65, 80, "SAUT", 7),
                        (20, 110, "PRESSEZ R POUR REVENIR", 7),
                        pyxel.text(20, 38, "RALENTIT LE TEMPS", 7),
                        pyxel.text(20, 58, "ACCELERE VOTRE VITESSE", 7),
                        pyxel.text(20, 78, "MEILLEUR VISION", 7),
                        pyxel.text(20, 98, "PLUS DE BOMBES", 7),
                        pyxel.text(20, 115, "PRESSEZ R POUR REVENIR", 7),
                        pyxel.text(18, 110, "PRESSEZ S POUR REDEMARRER", 7)
                    };
                    Console.WriteLine(this.langage[0], this.langage);
                    pyxel.run(this.update_menu, this.draw_menu);
                } else if (pyxel.btn(pyxel.KEY_E)) {
                    //jeu en anglais / game in english
                    this.langage = new List<object> {
                        (24, 40, "PRESS P TO SEE POINTS", 7),
                        (20, 60, "PRESS C TO SEE CONTROLS", 7),
                        (25, 80, "PRESS B TO SEE BONUS", 7),
                        (31, 100, "PRESS S TO START", 7),
                        (83, 78, "YOU", 7),
                        (30, 110, "PRESS R TO RETURN", 7),
                        (49, 20, "CONTROLS", 7),
                        (44, 40, "or", 7),
                        (65, 40, "LEFT", 7),
                        (44, 60, "or", 7),
                        (65, 60, "RIGHT", 7),
                        (65, 80, "JUMP", 7),
                        (30, 110, "PRESS R TO RETURN", 7),
                        (54, 20, "BONUS", 7),
                        (20, 38, "SLOW THE TIME", 7),
                        (20, 58, "MAKE YOU FASTER", 7),
                        (20, 78, "YOU WILL SEE BETER", 7),
                        (20, 98, "NO BOMB", 7),
                        (30, 115, "PRESS R TO RETURN", 7),
                        (30, 110, "PRESS S TO RESTART", 7)
                    };
                    pyxel.run(this.update_menu, this.draw_menu);
                }
            }
            
            // Lancement du jeu après le menu, la fin de partie ou les paramètres. / Launch of the game after the menu, the end of the game or the parameters.
            public virtual object lancement() {
                if (pyxel.btn(pyxel.KEY_S) && this.ecran == 0) {
                    //Lancement du jeu. / Launch of the game.
                    this.ecran = 1;
                    this.reset();
                    pyxel.run(this.update_corps, this.draw_corps);
                } else if (pyxel.btn(pyxel.KEY_C) && this.ecran == 0) {
                    //Affichage des contrôles. / Display of the controls.
                    this.ecran = 2;
                    pyxel.run(this.update_param, this.draw_param);
                } else if (pyxel.btn(pyxel.KEY_P) && this.ecran == 0) {
                    //Affichage des points. / Display of the points.
                    this.ecran = 2;
                    pyxel.run(this.update_pts, this.draw_pts);
                } else if (pyxel.btn(pyxel.KEY_B) && this.ecran == 0) {
                    //Affichage des bonus. / Display of the bonuses.
                    this.ecran = 2;
                    pyxel.run(this.update_bonus, this.draw_bonus);
                } else if (pyxel.btn(pyxel.KEY_R) && this.ecran == 2) {
                    //Retour au menu. / Back to the menu.
                    this.ecran = 0;
                    pyxel.run(this.update_menu, this.draw_menu);
                }
            }
            
            // Fonction remettant toutes les variables à leur états d'origine pour une nouvelle partie. / Function putting all the variables back to their original state for a new game.
            public virtual object reset() {
                if (pyxel.btn(pyxel.KEY_S)) {
                    //Reset du score et du niveau / Reset of the score and the level
                    this.score = 0;
                    //Retour au niveau 1 et au ciel de base. / Back to level 1 and the basic sky.
                    this.ciel = 6;
                    this.ratio = (45, 20, 5, 20, 10);
                    this.list_vitesse = new List<object> {
                        0.5,
                        1,
                        1.5,
                        2
                    };
                    //Vidage des listes / Emptying the lists
                    this.objet_liste = new List<object>();
                    this.explosions_liste = new List<object>();
                    this.bonus_liste = new List<object>();
                    //Reset du timer / Reset of the timer
                    this.timer = 90;
                    this.minute = 0;
                    this.seconde = 0;
                    this.tps_bonus = 0;
                    //Reset de l'écran / Reset of the screen
                    this.ecran = 0;
                    //Repositionnement du Personnage / Repositioning of the Character
                    this.doodle["x1"] = 60;
                    this.doodle["y1"] = 110;
                    this.doodle["x2"] = 60;
                    this.doodle["y2"] = 118;
                    this.doodle["x3"] = 68;
                    this.doodle["y3"] = 110;
                    this.doodle["x4"] = 68;
                    this.doodle["y4"] = 118;
                    //Repositionnement du Soleil et Lune / Repositioning of the Sun and Moon
                    this.astre["dessin1"] = 0;
                    this.astre["x1"] = 120;
                    this.astre["y1"] = 120;
                    this.astre["dessin2"] = 8;
                    this.astre["x2"] = 128;
                    this.astre["y2"] = 120;
                    this.astre["dessin3"] = 0;
                    this.astre["x3"] = 120;
                    this.astre["y3"] = 128;
                    this.astre["dessin4"] = 8;
                    this.astre["x4"] = 128;
                    this.astre["y4"] = 128;
                }
            }
            
            // Checks the launch of the game./Vérifie le lancement du jeu.
            public virtual object update_acceuil() {
                this.lancement();
                this.langue();
            }
            
            // Displays the home screen./Affiche l'écran d'acceuil
            public virtual object draw_acceuil() {
                pyxel.cls(6);
                pyxel.text(43, 10, "Fruit World", 7);
                //Affiche la grosse pomme. / Display the big apple.
                pyxel.blt(30, 0, 0, 0, 16, 8, 8, 15);
                pyxel.blt(38, 0, 0, 8, 16, 8, 8, 15);
                pyxel.blt(30, 8, 0, 0, 24, 8, 8, 15);
                pyxel.blt(38, 8, 0, 8, 24, 8, 8, 15);
                //Affiche la grosse bombe. / Display the big bomb.
                pyxel.blt(84, 0, 0, 16, 16, 8, 8, 15);
                pyxel.blt(92, 0, 0, 24, 16, 8, 8, 15);
                pyxel.blt(84, 8, 0, 16, 24, 8, 8, 15);
                pyxel.blt(92, 8, 0, 24, 24, 8, 8, 15);
                //Séparation. / Separation.
                pyxel.rect(29, 17, 72, 0.5, 3);
                //Jeu en Français.
                pyxel.text(18, 50, "PRESSEZ F POUR FRANCAIS", 7);
                //Game in English.
                pyxel.text(24, 80, "PRESS E FOR ENGLISH", 7);
                //Crédit. / Credit.
                pyxel.text(5, 120, "RENAUD CORP.", 7);
            }
            
            // Vérifie le lancement du jeu. / Check the launch of the game.
            public virtual object update_menu() {
                this.lancement();
            }
            
            // Affiche l'écran d'accueil. / Displays the home screen.
            public virtual object draw_menu() {
                pyxel.cls(6);
                pyxel.text(43, 10, "Fruit World", 7);
                //Affiche la grosse pomme. / Displays the big apple.
                pyxel.blt(30, 0, 0, 0, 16, 8, 8, 15);
                pyxel.blt(38, 0, 0, 8, 16, 8, 8, 15);
                pyxel.blt(30, 8, 0, 0, 24, 8, 8, 15);
                pyxel.blt(38, 8, 0, 8, 24, 8, 8, 15);
                //Affiche la grosse bombe. / Displays the big bomb.
                pyxel.blt(84, 0, 0, 16, 16, 8, 8, 15);
                pyxel.blt(92, 0, 0, 24, 16, 8, 8, 15);
                pyxel.blt(84, 8, 0, 16, 24, 8, 8, 15);
                pyxel.blt(92, 8, 0, 24, 24, 8, 8, 15);
                //Séparation. / Separation.
                pyxel.rect(29, 17, 72, 0.5, 3);
                //Écran des points. / Points screen.
                this.langage[0::5];
                //Écran des Controles. / Controls screen.
                pyxel.text(9, 60, "PRESSEZ C POUR LES CONTROLES", 7);
                //Écran des Bonus. / Bonus screen.
                pyxel.text(15, 80, "PRESSEZ B POUR LES BONUS", 7);
                //Lancer le jeu. / Launch the game.
                pyxel.text(16, 100, "PRESSEZ S POUR DEMARRER", 7);
                //Crédits. / Credits.
                pyxel.text(5, 120, "RENAUD CORP.", 7);
            }
            
            // Vérifie le lancement du jeu. / Check the launch of the game.
            public virtual object update_pts() {
                this.lancement();
            }
            
            // Affiche l'écran des points. / Displays the points screen.
            public virtual object draw_pts() {
                pyxel.cls(6);
                pyxel.text(43, 10, "Fruit World", 7);
                //Affiche la grosse pomme. / Displays the big apple.
                pyxel.blt(30, 0, 0, 0, 16, 8, 8, 15);
                pyxel.blt(38, 0, 0, 8, 16, 8, 8, 15);
                pyxel.blt(30, 8, 0, 0, 24, 8, 8, 15);
                pyxel.blt(38, 8, 0, 8, 24, 8, 8, 15);
                //Affiche la grosse bombe. / Displays the big bomb.
                pyxel.blt(84, 0, 0, 16, 16, 8, 8, 15);
                pyxel.blt(92, 0, 0, 24, 16, 8, 8, 15);
                pyxel.blt(84, 8, 0, 16, 24, 8, 8, 15);
                pyxel.blt(92, 8, 0, 24, 24, 8, 8, 15);
                //Séparation. / Separation.
                pyxel.rect(29, 17, 72, 0.5, 3);
                pyxel.text(54, 20, "POINTS", 7);
                //Affichage des points. / Display of the points.
                pyxel.blt(10, 35, 0, 0, 0, 8, 8, 0);
                pyxel.text(20, 38, "1 PTS", 7);
                pyxel.blt(70, 55, 0, 8, 0, 8, 8, 0);
                pyxel.text(80, 58, "-1 PTS", 7);
                pyxel.blt(70, 35, 0, 0, 8, 8, 8, 0);
                pyxel.text(80, 38, "10 PTS", 7);
                pyxel.blt(10, 55, 0, 8, 8, 8, 8, 0);
                pyxel.text(20, 58, "3 PTS", 7);
                pyxel.blt(10, 75, 0, 16, 8, 8, 8, 0);
                pyxel.text(20, 78, "5 PTS", 7);
                pyxel.blt(65, 70, 0, 32, 32, 8, 8, 7);
                pyxel.blt(65, 78, 0, 32, 40, 8, 8, 7);
                pyxel.blt(73, 70, 0, 40, 32, 8, 8, 7);
                pyxel.blt(73, 78, 0, 40, 40, 8, 8, 7);
                pyxel.text(83, 78, "Vous", 7);
                //Retourner à l'écran d'acceuil. / Return to the home screen.
                pyxel.text(20, 110, "PRESSEZ R POUR REVENIR", 7);
            }
            
            // Vérifie le lancement du jeu. / Check the launch of the game.
            public virtual object update_param() {
                this.lancement();
            }
            
            // Affiche l'écran d'accueil. / Displays the home screen.
            public virtual object draw_param() {
                pyxel.cls(6);
                pyxel.text(43, 10, "Fruit World", 7);
                //Affiche la grosse pomme. / Displays the big apple.
                pyxel.blt(30, 0, 0, 0, 16, 8, 8, 15);
                pyxel.blt(38, 0, 0, 8, 16, 8, 8, 15);
                pyxel.blt(30, 8, 0, 0, 24, 8, 8, 15);
                pyxel.blt(38, 8, 0, 8, 24, 8, 8, 15);
                //Affiche la grosse bombe. / Displays the big bomb.
                pyxel.blt(84, 0, 0, 16, 16, 8, 8, 15);
                pyxel.blt(92, 0, 0, 24, 16, 8, 8, 15);
                pyxel.blt(84, 8, 0, 16, 24, 8, 8, 15);
                pyxel.blt(92, 8, 0, 24, 24, 8, 8, 15);
                //Séparation. / Separation.
                pyxel.rect(29, 17, 72, 0.5, 3);
                pyxel.text(49, 20, "CONTROLES", 7);
                //Affichage du déplacement à gauche. / Displays the left movement.
                pyxel.blt(34, 38, 0, 24, 0, 8, 8, 1);
                pyxel.text(44, 40, "ou", 7);
                pyxel.blt(54, 38, 0, 40, 8, 8, 8, 1);
                pyxel.text(65, 40, "Gauche", 7);
                //Affichage du déplacement à droite. / Displays the right movement.
                pyxel.blt(34, 58, 0, 24, 8, 8, 8, 1);
                pyxel.text(44, 60, "ou", 7);
                pyxel.blt(54, 58, 0, 40, 0, 8, 8, 1);
                pyxel.text(65, 60, "Droite", 7);
                //Affichage du saut. / Displays the jump.
                pyxel.rect(39, 79, 20, 6, 0);
                pyxel.text(65, 80, "SAUT", 7);
                //Retourner à l'écran d'acceuil. / Return to the home screen.
                pyxel.text(20, 110, "PRESSEZ R POUR REVENIR", 7);
            }
            
            // Vérifie le lancement du jeu. / Check the launch of the game.
            public virtual object update_bonus() {
                this.lancement();
            }
            
            // Affiche l'écran des points. / Displays the points screen.
            public virtual object draw_bonus() {
                pyxel.cls(6);
                pyxel.text(43, 10, "Fruit World", 7);
                //Affiche la grosse pomme. / Displays the big apple.
                pyxel.blt(30, 0, 0, 0, 16, 8, 8, 15);
                pyxel.blt(38, 0, 0, 8, 16, 8, 8, 15);
                pyxel.blt(30, 8, 0, 0, 24, 8, 8, 15);
                pyxel.blt(38, 8, 0, 8, 24, 8, 8, 15);
                //Affiche la grosse bombe. / Displays the big bomb.
                pyxel.blt(84, 0, 0, 16, 16, 8, 8, 15);
                pyxel.blt(92, 0, 0, 24, 16, 8, 8, 15);
                pyxel.blt(84, 8, 0, 16, 24, 8, 8, 15);
                pyxel.blt(92, 8, 0, 24, 24, 8, 8, 15);
                //Séparation. / Separation.
                pyxel.rect(29, 17, 72, 0.5, 3);
                pyxel.text(54, 20, "BONUS", 7);
                //Affichage des points. / Displays the points.
                pyxel.blt(10, 36, 0, 48, 32, 8, 8, 15);
                pyxel.text(20, 38, "RALENTIT LE TEMPS", 7);
                pyxel.blt(10, 56, 0, 56, 32, 8, 8, 15);
                pyxel.text(20, 58, "ACCELERE VOTRE VITESSE", 7);
                pyxel.blt(10, 76, 0, 48, 40, 8, 8, 15);
                pyxel.text(20, 78, "MEILLEUR VISION", 7);
                pyxel.blt(10, 96, 0, 56, 40, 8, 8, 15);
                pyxel.text(20, 98, "PLUS DE BOMBES", 7);
                //Retourner à l'écran d'acceuil. / Return to the home screen.
                pyxel.text(20, 115, "PRESSEZ R POUR REVENIR", 7);
            }
            
            // Mise à jour des variables (30 fois par seconde). / Update the variables (30 times per second).
            public virtual object update_corps() {
                //Déplacement du personnage. / Character movement.
                this.doodle_deplacement();
                //Création et déplacemnt des objets et bonus. / Creation and movement of objects and bonuses.
                this.objet_creation();
                this.objet_deplacement();
                this.bonus_creation();
                this.bonus_deplacement();
                //Vérification des collisions. / Check the collisions.
                this.colision_objet();
                this.colision_bonus();
                //Évolution de l'animation des explosions. / Evolution of the explosions animation.
                this.explosions_animation();
                //Mise à jour du temps restant. / Update the remaining time.
                this.temps();
                //Déplacement des astres. / Movement of the stars.
                this.astres();
            }
            
            // Création et positionnement des objets (30 fois par seconde). / Creation and positioning of objects (30 times per second).
            public virtual object draw_corps() {
                //Création du ciel. / Creation of the sky.
                pyxel.cls(this.ciel);
                //Soleil et Lune / Sun and Moon 
                pyxel.blt(this.astre["x1"], this.astre["y1"], 0, this.astre["dessin1"], 32, 8, 8, 15);
                pyxel.blt(this.astre["x2"], this.astre["y2"], 0, this.astre["dessin2"], 32, 8, 8, 15);
                pyxel.blt(this.astre["x3"], this.astre["y3"], 0, this.astre["dessin3"], 40, 8, 8, 15);
                pyxel.blt(this.astre["x4"], this.astre["y4"], 0, this.astre["dessin4"], 40, 8, 8, 15);
                //Décoration du fond / Background decoration
                //Buissons / Bushes
                pyxel.blt(23, 112, 0, 32, 16, 8, 8, 15);
                pyxel.blt(31, 112, 0, 40, 16, 8, 8, 15);
                pyxel.blt(83, 112, 0, 32, 24, 8, 8, 15);
                pyxel.blt(91, 112, 0, 40, 24, 8, 8, 15);
                pyxel.blt(7, 112, 0, 32, 0, 8, 8, 15);
                //Arbre / Tree
                //Ligne du bas / Bottom line
                pyxel.blt(45, 112, 0, 8, 72, 8, 8, 15);
                pyxel.blt(53, 112, 0, 16, 72, 8, 8, 15);
                pyxel.blt(61, 112, 0, 24, 72, 8, 8, 15);
                pyxel.blt(69, 112, 0, 32, 72, 8, 8, 15);
                //Ligne du milieu / Middle line
                pyxel.blt(45, 104, 0, 8, 64, 8, 8, 15);
                pyxel.blt(53, 104, 0, 16, 64, 8, 8, 15);
                pyxel.blt(61, 104, 0, 24, 64, 8, 8, 15);
                pyxel.blt(69, 104, 0, 32, 64, 8, 8, 15);
                //Ligne du haut / Top line
                pyxel.blt(45, 96, 0, 8, 56, 8, 8, 15);
                pyxel.blt(53, 96, 0, 16, 56, 8, 8, 15);
                pyxel.blt(61, 96, 0, 24, 56, 8, 8, 15);
                pyxel.blt(69, 96, 0, 32, 56, 8, 8, 15);
                //Cailloux / Rocks
                pyxel.blt(115, 112, 0, 48, 0, 8, 8, 15);
                pyxel.blt(123, 112, 0, 56, 0, 8, 8, 15);
                pyxel.blt(47, 112, 0, 48, 8, 8, 8, 15);
                //Nuages / Clouds
                pyxel.blt(115, 51, 0, 48, 16, 8, 8, 15);
                pyxel.blt(18, 34, 0, 56, 16, 8, 8, 15);
                pyxel.blt(47, 6, 0, 48, 24, 8, 8, 15);
                pyxel.blt(81, 63, 0, 56, 24, 8, 8, 15);
                //Création du fond pour le bonus. / Creation of the background for the bonus.
                if (this.carotte == 1) {
                    pyxel.rect(0, 0, 128, 128, 7);
                    pyxel.text(5, 5, this.minute.ToString() + " MIN " + this.seconde.ToString() + " S", 0);
                    pyxel.text(85, 5, this.score.ToString() + " POINTS", 0);
                }
                //Création du sol. / Creation of the ground.
                pyxel.rect(0, 120, 128, 10, 3);
                //Création du personnage. / Creation of the character.
                pyxel.blt(this.doodle["x1"], this.doodle["y1"], 0, 32, 32, 8, 8, 7);
                pyxel.blt(this.doodle["x2"], this.doodle["y2"], 0, 32, 40, 8, 8, 7);
                pyxel.blt(this.doodle["x3"], this.doodle["y3"], 0, 40, 32, 8, 8, 7);
                pyxel.blt(this.doodle["x4"], this.doodle["y4"], 0, 40, 40, 8, 8, 7);
                //Création des objets. / Creation of the objects.
                foreach (var objet in this.objet_liste) {
                    if (objet[2] == 0) {
                        pyxel.blt(objet[0], objet[1], 0, 0, 0, 8, 8, 0);
                    } else if (objet[2] == 1) {
                        pyxel.blt(objet[0], objet[1], 0, 8, 0, 8, 8, 0);
                    } else if (objet[2] == 2) {
                        pyxel.blt(objet[0], objet[1], 0, 0, 8, 8, 8, 0);
                    } else if (objet[2] == 3) {
                        pyxel.blt(objet[0], objet[1], 0, 8, 8, 8, 8, 0);
                    } else if (objet[2] == 4) {
                        pyxel.blt(objet[0], objet[1], 0, 16, 8, 8, 8, 0);
                    }
                }
                //Création des bonus. / Creation of the bonus.
                foreach (var bonus in this.bonus_liste) {
                    if (bonus[2] == 5) {
                        pyxel.blt(bonus[0], bonus[1], 0, 48, 32, 8, 8, 15);
                    } else if (bonus[2] == 6) {
                        pyxel.blt(bonus[0], bonus[1], 0, 56, 32, 8, 8, 15);
                    } else if (bonus[2] == 7) {
                        pyxel.blt(bonus[0], bonus[1], 0, 48, 40, 8, 8, 15);
                    } else if (bonus[2] == 8) {
                        pyxel.blt(bonus[0], bonus[1], 0, 56, 40, 8, 8, 15);
                    }
                }
                //Création des explosions. / Creation of the explosions.
                foreach (var explosion in this.explosions_liste) {
                    pyxel.circb(explosion[0] + 4, explosion[1] + 4, 2 * (explosion[2] / 4), 8 + explosion[2] % 3);
                }
                //Affichage du temps et du score. / Display of the time and the score.
                if (this.carotte == 0) {
                    pyxel.text(5, 5, this.minute.ToString() + " MIN " + this.seconde.ToString() + " S", 7);
                    pyxel.text(85, 5, this.score.ToString() + " POINTS", 7);
                }
            }
            
            // Vérifie le lancement du jeu après la fin du jeu. / Check the start of the game after the end of the game.
            public virtual object update_fin() {
                this.lancement();
            }
            
            // Affiche les informations de fin du jeu. / Display the end of the game information.
            public virtual object draw_fin() {
                //Vide la fenêtre et affiche le score final. / Empty the window and display the final score.
                pyxel.cls(6);
                pyxel.text(43, 20, "Fruit World", 7);
                pyxel.text(32, 64, "SCORE: " + this.score.ToString() + " POINTS", 7);
                pyxel.text(18, 110, "PRESSEZ S POUR REDEMARRER", 7);
                //Affiche la grosse pomme. / Display the big apple.
                pyxel.blt(30, 10, 0, 0, 16, 8, 8, 15);
                pyxel.blt(38, 10, 0, 8, 16, 8, 8, 15);
                pyxel.blt(30, 18, 0, 0, 24, 8, 8, 15);
                pyxel.blt(38, 18, 0, 8, 24, 8, 8, 15);
                //Affiche la grosse bombe. / Display the big bomb.
                pyxel.blt(84, 10, 0, 16, 16, 8, 8, 15);
                pyxel.blt(92, 10, 0, 24, 16, 8, 8, 15);
                pyxel.blt(84, 18, 0, 16, 24, 8, 8, 15);
                pyxel.blt(92, 18, 0, 24, 24, 8, 8, 15);
            }
        }
        
        static Module() {
            Jeu();
        }
    }
}
