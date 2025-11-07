# 🚢 Bataille Navale (Battleship Game)

Un jeu de bataille navale complet avec interface graphique développé en Python avec Tkinter.

## 📋 Description

Ce jeu de bataille navale permet de jouer contre l'ordinateur dans une interface graphique intuitive. Placez vos navires stratégiquement et tentez de couler la flotte ennemie avant que l'ordinateur ne coule la vôtre!

## ✨ Fonctionnalités

- **Interface graphique moderne** avec Tkinter
- **Placement de navires**:
  - Manuel avec rotation (touche R)
  - Automatique (placement aléatoire)
- **5 types de navires**:
  - Porte-avions (5 cases)
  - Croiseur (4 cases)
  - Contre-torpilleur (3 cases)
  - Sous-marin (3 cases)
  - Torpilleur (2 cases)
- **Système de jeu au tour par tour**
- **IA adverse** avec attaques aléatoires
- **Indicateurs visuels**:
  - ❌ Croix rouge pour les tirs réussis
  - ⭕ Cercle blanc pour les tirs ratés
  - 🟦 Cases bleues pour l'eau
  - 🟨 Cases grises pour vos navires
- **Détection de victoire/défaite**
- **Option de nouvelle partie**

## 🎮 Comment Jouer

### Lancement du jeu

```bash
python battleship.py
```

### Phase de placement des navires

1. **Placement manuel**:
   - Cliquez sur votre grille (à gauche) pour placer un navire
   - Utilisez la touche **R** ou le bouton "Rotation" pour changer l'orientation (horizontal/vertical)
   - Placez tous les 5 navires

2. **Placement automatique**:
   - Cliquez sur le bouton "Placement Aléatoire" pour placer automatiquement tous vos navires

### Phase de combat

1. Cliquez sur la grille ennemie (à droite) pour attaquer
2. **Raté (⭕)**: L'ordinateur joue à son tour
3. **Touché (❌)**: Vous pouvez rejouer
4. **Coulé**: Un navire ennemi est complètement détruit
5. Le jeu continue jusqu'à ce qu'une flotte soit complètement détruite

### Contrôles

- **Clic gauche**: Placer un navire / Attaquer
- **Touche R**: Rotation du navire (pendant le placement)
- **Bouton "Rotation"**: Changer l'orientation du navire
- **Bouton "Placement Aléatoire"**: Placer automatiquement tous les navires
- **Bouton "Nouvelle Partie"**: Recommencer une nouvelle partie

## 🛠️ Prérequis

- Python 3.6 ou supérieur
- Tkinter (généralement inclus avec Python)

### Vérification de Tkinter

Tkinter est normalement installé avec Python. Pour vérifier:

```bash
python -m tkinter
```

Si une fenêtre s'ouvre, Tkinter est correctement installé.

### Installation de Tkinter (si nécessaire)

**Windows**: Tkinter est inclus avec Python

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install python3-tk
```

**macOS**: Tkinter est inclus avec Python

## 📁 Structure du Projet

```
battleship-game/
│
├── battleship.py          # Fichier principal du jeu
├── README.md             # Ce fichier
└── .github/
    └── copilot-instructions.md
```

## 🎯 Règles du Jeu

1. Chaque joueur a une grille de 10x10
2. Les navires ne peuvent pas se chevaucher
3. Les navires ne peuvent pas se toucher (même en diagonal)
4. Un navire est coulé quand toutes ses cases sont touchées
5. Le premier à couler tous les navires adverses gagne

## 🤖 Intelligence Artificielle

L'IA utilise actuellement une stratégie simple d'attaque aléatoire. Les tirs sont effectués au hasard sur des cases non encore attaquées.

## 🎨 Personnalisation

Vous pouvez modifier dans le code:
- La taille de la grille (variable `board_size`)
- La taille des cellules (variable `cell_size`)
- Le nombre et la taille des navires (variable `ship_sizes`)
- Les couleurs de l'interface

## 🐛 Résolution de Problèmes

**Le jeu ne se lance pas**:
- Vérifiez que Python est correctement installé
- Vérifiez que Tkinter est disponible

**Erreur d'importation de tkinter**:
- Installez python3-tk (voir section Prérequis)

## 📝 License

Ce projet est libre d'utilisation pour l'apprentissage et le divertissement.

## 🎓 Apprentissage

Ce projet est excellent pour apprendre:
- La programmation orientée objet en Python
- Le développement d'interfaces graphiques avec Tkinter
- La gestion d'événements (clics, touches clavier)
- Les algorithmes de jeu et IA basique
- La gestion d'état dans une application

## 🚀 Améliorations Futures Possibles

- IA plus intelligente (ciblage après un touché)
- Mode multijoueur en réseau
- Sauvegarde/chargement de parties
- Effets sonores
- Animations
- Statistiques de jeu
- Difficulté réglable

---

**Amusez-vous bien! Que le meilleur stratège gagne! 🎮⚓**
