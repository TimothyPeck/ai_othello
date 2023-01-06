# Résumé pour Jeanne qui est malade, mais même quand elle n’était pas malade n’a pas fait d'IA le dernier cours

## Fonction evaluate

La fonction evaluate donne le score du board actuel pour le joueur en question.
Actuellement il existe deux versions, une simple, et une moins simple que j'ai fait en me basant sur ce [rapport](https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf).

### Version simple

La version simple calcule juste le score pour le joueur basé sur un tableau des poids de chaque case, pris de ce [rapport](https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/O-Thell-Us/Othellus.pdf).

```python
score = 0
for row, col in product(range(self.ROWS), range(self.COLS)):
    turn = board.get_turn()
    opp = "W" if turn == "B" else "B"
    if board.current_board[row][col] == turn:
        score += self.WEIGHTS[row][col]
    elif board.current_board[row][col] == opp:
        score -= self.WEIGHTS[row][col]
return score
```

Il est lent et inefficace.
Comme tu peux le voir, les pions du joueur sont additionnés et les pions de l'adversaire sont soustraits.
Ceci permet de varier le score de manière plus précise.

### Version moins simple

Cette version est moins simple simplement parce qu'elle est plus longue, et aussi chiante, et lente, et inefficace.

En gros, il calcule les valeurs du tableau à la volée au lieu de le faire avant, ceci a des avantages et inconvénients.

Avantages:

- plus flexible
- prends plus d'informations
- plus rapide, car ne parcourt pas tout le board

Inconvénients:

- Lent, car les fonctions du othello.py du prof sont lents comme tout et son truc c'est de la merde et je le déteste, s’il arrivait commenter correctement ce serait mille fois mieux.
- un peu dur à comprendre sur le coup
- long
- chiant

Tu te poses probablement plusieurs questions à ce stade, j'espère y répondre dans les paragraphes qui suivent, mais si je n'y arrive pas c'est probablement parce que moi même je ne sais pas.

**Pourquoi c'est si chiant et tout la?**

Alors, c'est principalement parce que les calculs se font (non linéairement) en rois étapes:

- Le calcul de la parité des pièces (en gros la statistique de qui a le plus de pièces en jeu en ce moment)
- La mobilité (en gros qui peut jouer au plus d'endroits)
- Les coins (qui a pris le plus de coins [je crois que celui-ci s'explique par soi-même, mais on ne sait jamais])

```python
coin_parity, mobility, corners = 0, 0, 0
```

Donc la parité: le calcul est simple 100 \* (pieces_jouer - pieces_adversaire)/(pieces_jouer + pieces_adversaire)

```python
(black_tokens, white_tokens) = board.compute_scores()
color = board.get_turn()

if color == "B":
    coin_parity = 100*(black_tokens - white_tokens) / (black_tokens + white_tokens)
elif color == "W":
    coin_parity = 100*(white_tokens - black_tokens) / (white_tokens + black_tokens)

```

Pour la mobilité, ce n’est réellement pas si compliqué que ça (je présume que tu arrives lire le code pour le calcul, je commence à avoir la flemme):

```python
player_moves = board.get_possible_move()
board.switch_turn()
opp_moves = board.get_possible_move()
board.switch_turn()

if len(player_moves)+len(opp_moves) != 0:
    mobility = 100*(len(player_moves)-len(opp_moves)) / (len(player_moves)+len(opp_moves))
else:
    mobility = 0
```

Les coins par contre sont chiant, pas parce que c'est compliqué, mais parce que c'est long, il faut vérifier chaque coin pour chaque joueur et j'ai oublié que j'avais copilote qui aurait pu me copier tout ça:

```python
player_corners = 0
opp_corners = 0

if board.current_board[0][0] == self.player_color:
    player_corners += 1
elif board.current_board[0][0] == self.opp_color:
    opp_corners += 1

if board.current_board[self.ROWS-1][0] == self.player_color:
    player_corners += 1
elif board.current_board[self.ROWS-1][0] == self.opp_color:
    opp_corners += 1

if board.current_board[0][self.COLS-1] == self.player_color:
    player_corners += 1
elif board.current_board[0][self.COLS-1] == self.opp_color:
    opp_corners += 1

if board.current_board[self.ROWS-1][self.COLS-1] == self.player_color:
    player_corners += 1
elif board.current_board[self.ROWS-1][self.COLS-1] == self.opp_color:
    opp_corners += 1

if player_corners+opp_corners != 0:
    corners = 100*(player_corners-opp_corners) / \
        (player_corners + opp_corners)

```

Et au final on renvoie la moyenne de tout ça:

```python
return (coin_parity+mobility+corners)/3
```

Vu que tu as bien sûr lu les rapports cités dans l'introduction, tu te demandes surement pourquoi je n'ai pas implémenté la stabilité. La réponse est simple, je ne sais pas comment.

## Fonction alpha_beta

La fonction alpha_beta est le coeur de notre IA, elle fait toutes les parties importantes.

### Ses arguments

La déclaration ressemble à ça:

```python
def alpha_beta(self, board: othello.OthelloGame, depth: int, alpha: int, beta: int, maximizing_player: bool) -> tuple[int, int]:
```

- self: dans une classe, voilà c'est tout
- board: le terrain de jeu à utiliser (tu verras plus tard qu'il change récursivement)
- depth: la profondeur max 😏
- alpha: la valeur d’alpha
- bêta: la valeur de bêta
- maximizing_player: un booléen si on est au max ou au min de l'arbre

Au début de la fonction, on vérifie si la profondeur est 0, si c'est le cas il faut **PAS** continuer, on évalue et on renvoie. (La fonction en entier est à la fin, flemme de diviser maintenant)

Ensuite, on vérifie si on maximise le joueur ou pas. Si c'est le cas, la meilleure valeur est littéralement de moins l'infini (temporaire tu verras), ensuite pour chaque move possible sur le board, on teste et on continue récursivement. On prend ensuite la meilleure valeur, et on compare avec alpha.

Pour le min, c'est la même chose, mais au lieu de faire moins l'infini, c'est l'infini, etc. Tu comprendras en lisant le code.

```python
def alpha_beta(self, board: othello.OthelloGame, depth: int, alpha: int, beta: int, maximizing_player: bool) -> tuple[int, int]:
        if depth == 0 or board.is_game_over():
            return self.evaluate(board), None

        if maximizing_player:
            best_score = -math.inf
            best_move = None
            for move in board.get_possible_move():
                board_copy = board.copy_game()
                board_copy.move(move[0], move[1])
                score = self.alpha_beta(
                    board_copy, depth - 1, alpha, bêta, False)[0]
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if best_score == score:
                    best_move = move
                if beta <= alpha:
                    break
            return best_score, best_move
        else:
            best_score = math.inf
            best_move = None
            for move in board.get_possible_move():
                board_copy = board.copy_game()
                board_copy.move(move[0], move[1])
                score = self.alpha_beta(
                    board_copy, depth - 1, alpha, beta, True)[0]
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if best_score == score:
                    best_move = move
                if beta <= alpha:
                    break
            return best_score, best_move

```
