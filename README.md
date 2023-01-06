# Othello
Jeanne Michel et Timothy Peck

## Fonction alpha_beta

La fonction alpha_beta de notre implementation ne differe pas trop de celui du cours. Le plateau de jeu qui lui est envoie est, initialement, inchangé, mais au fur et a mesure, elle est copiée et modifiée pour chaque coup possible. Elle retourne le meilleur coup possible pour le joueur qui l'appelle. Ceci prends du temps car le deepcopy de python est assez lent. La fonction prends egalement la profondeur max, qui est decrementée a chaque appel recursif, et les valeurs alpha et beta qui sont utilisees pour l'optimisation de l'algorithme. On a aussi un boolean qui indique si on maximise ou minimise le joueur. Le déplacement precedent est également envoié pour le calcul de la fonction d'evaluation.

```python
def alpha_beta(self, board: othello.OthelloGame, depth: int, alpha: int, beta: int, maximizing_player: bool, test_move: tuple[int, int] = None) -> tuple[int, tuple[int, int]]:
    if depth == 0 or board.is_game_over(): 
        return self.compare_boards(board, test_move), None 

    if maximizing_player: 
        best_score = -math.inf 
        best_move = None 
        for move in board.get_possible_move(): 
            board_copy = board.copy_game() 
            board_copy.move(move[0], move[1]) 
            score = self.alpha_beta(board_copy, depth - 1, alpha, beta, not maximizing_player, move)[0] 
            best_score = max(score, best_score) 
            alpha = max(alpha, best_score) 
            if best_score == score: 
                best_move = move
            if best_score > beta: 
                break
        return best_score, best_move
    else:
        best_score = math.inf 
        best_move = None 
        for move in board.get_possible_move(): 
            board_copy = board.copy_game()
            board_copy.move(move[0], move[1])
            score = self.alpha_beta(board_copy, depth - 1, alpha, beta, not maximizing_player, move)[0] 
            best_score = min(score, best_score) 
            beta = min(beta, best_score) 
            if best_score == score: 
                best_move = move
            if best_score < alpha: 
                break
        return best_score, best_move
```
---
## Fonction de comparaison, compare_boards

A l'appel de next_move, on sauvegarde le plateau actuel. Ensuite, quand alpha_beta atteinds sa profondeur maximale, on compare le nombre de pions de chaque joueur sur le plateau actuel et le plateau sauvegardé.
On y ajoute également le score du l'emplacement joué pris dans le tableau des score pris de (A New Experience: O-Thell-Us – An AI Project.)[1], celui-ci etait initailement prévu pour un plateau de 8x8, mais nous l'avons adapté a un plateau 9x7. 
On retourne ensuite le score de ce coup.

```python
def compare_boards(self, board: othello.OthelloGame, move: tuple[int, int]) -> int:
    (new_black_tiles, new_white_tiles) = board.get_scores()
    (old_black_tiles, old_white_tiles) = self.init_board.get_scores()

    weight = self.WEIGHTS[move[0]][move[1]]
    player_score = 0
    if self.player_color == "B":
        player_score = (new_black_tiles-old_black_tiles) - (new_white_tiles-old_white_tiles)
    else:
        player_score = (new_white_tiles-old_white_tiles) - (new_black_tiles-old_black_tiles)

    player_score += weight
    return player_score
```

Cette fonction est que appelée lorsque la profondeur maximale est atteinte, il faut donc qu'elle soit plutot rapide. 
C'est pour cela que nous avons choisi cette fonction de comparaison, plutot qu'une autre qui calculait le score basé sur les poids des pions actuels, ce qui prennait deux for imbriqués et une eternité.

## References

[1] A New Experience: O-Thell-Us – An AI Project. (2011). courses.cs.washington.edu. Retrieved December 20, 2022, from https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/O-Thell-Us/Othellus.pdf