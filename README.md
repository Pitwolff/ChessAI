Ce fichier contient une implémentation du jeu d'échec en python, ainsi qu'un ordinateur qui joue à ce jeu. L'évaluation d'une position se fait en sommant la valeur estimée de chaque pièce. Cette valeur est
obtenue à partir de nombreux paramètres comme le nombre de coups jouables par la pièce, le nombre de pièces qu'elle attaque et par qui elle est attaquée ou encore le nombre de pièces qu'elle défend. Une grande
partie de la complexité du code réside dans le fait de mettre ces paramètres à jour en fonction du coup qui à été joué, pour ne pas avoir à les recalculer pour toutes les pièces à chaque coup. L'importance de
ces paramètres est pondérée par des paramètres qui peuvent être améliorés en les ajustant pour que l'évaluation de la position soit la plus proche possible de celles d'une base de donnée d'une centaine de
positions avec leur évaluation, obtenues à l'aide de l'analyseur de chess.com. Cette fonctionnalité à été désactivée par défault en raison de sa longue durée d'entrainement pour un résultat modéré. En exécutant
le programme, on peut donc observer la partie d'un ordinateur contre lui-même avec des paramètres ajustés à la main.
