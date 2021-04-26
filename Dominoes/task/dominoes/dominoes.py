# Write your code here
import random
import re
from collections import Counter


def generate_set():
    full_set = []
    for i in range(0, 7):
        for j in range(0, 7):
            if [i, j] not in full_set and [j, i] not in full_set:
                full_set.append([i, j])
    random.shuffle(full_set)
    return full_set


def split_set(full_set):
    random.shuffle(full_set)
    player_ = full_set[0:7]
    computer_ = full_set[7:14]
    stock_ = full_set[14:]
    return player_, computer_, stock_


def first_player(player_, computer_):
    for i in range(6, -1, -1):
        if [i, i] in player_:
            return [[i, i]], "computer"
        elif [i, i] in computer_:
            return [[i, i]], "player"
    return [], "unknown"


def print_snake(snake_):
    if len(snake_) > 6:
        for i in range(0, 3):
            print(snake_[i], end='')
        print('...', end='')
        for i in range(-3, 0, 1):
            print(snake_[i], end='')
    else:
        for i in range(len(snake_)):
            print(snake_[i], end='')


def make_move(piece, snake, side):
    side_1, side_2 = piece
    if side_1 == snake[side][side]:
        piece.reverse() if side == 0 else piece
        snake.insert(len(snake) if side == -1 else 0, piece)
    elif side_2 == snake[side][side]:
        piece.reverse() if side == -1 else piece
        snake.insert(len(snake) if side == -1 else 0, piece)
    else:
        print("Illegal move. Please try again.")
        return
    return snake


def player_moves(player_, snake_, stock_, msg_):
    while True:
        move_ = input(f"Status: {msg_}")

        if re.match(r"-\d", move_) or re.match(r"\d", move_):
            move_ = int(move_)
            if abs(move_) - 1 > len(player_):
                while True:
                    move_ = input("Invalid input. Please try again.")
                    if re.match(r"-\d", move_) or re.match(r"\d", move_):
                        move_ = int(move_)
                        break

        else:
            while True:
                move_ = input("Invalid input. Please try again.")
                if re.match(r"-\d", move_) or re.match(r"\d", move_):
                    move_ = int(move_)
                    break

        status_ = "computer"

        if move_ != 0:
            snake = make_move(player_[abs(move_) - 1], snake_, side=0 if move_ < 0 else -1)
            if snake is None:
                continue
            snake_ = snake
            player_.remove(player_[abs(move_) - 1])
            break
        else:
            if len(stock_) > 0:
                player_ += [stock_.pop()]
                break
            else:
                break

    return player_, snake_, stock_, status_


def computer_moves_old(computer, snake, stock, msg):
    input(f"Status: {msg}")
    status = "player"

    while True:
        move = random.randint(-len(computer), len(computer))
        if move != 0:
            piece = computer[abs(move) - 1]
            side_1, side_2 = piece
            side = 0 if move < 0 else -1

            if side_1 == snake[side][side]:
                piece.reverse() if side == 0 else piece
                snake.insert(len(snake) if side == -1 else 0, piece)
            elif side_2 == snake[side][side]:
                piece.reverse() if side == -1 else piece
                snake.insert(len(snake) if side == -1 else 0, piece)
            else:
                continue
            computer.remove(computer[abs(move) - 1])
            break
        else:
            if len(stock) > 0:
                computer += [stock.pop()]
                break
            else:
                break

    return computer, snake, stock, status


def computer_moves(computer, snake, stock, msg):
    input(f"Status: {msg}")
    status = "player"
    counts = Counter([x for piece in snake for x in piece])

    piece_scores = []
    for piece in computer:
        piece_scores.append(counts[piece[0]] + counts[piece[1]])
    computer_ = computer[:]
    while True:
        if len(computer_) == 0:
            computer.append(stock.pop())
            break
        piece = computer_[piece_scores.index(max(piece_scores))]

        if piece[0] in snake[0]:
            computer.remove(piece)
            piece.reverse()
            snake.insert(0, piece)
            break
        elif piece[1] in snake[0]:
            computer.remove(piece)
            snake.insert(0, piece)
            break
        elif piece[0] in snake[-1]:
            computer.remove(piece)
            snake.insert(len(snake), piece)
            break
        elif piece[1] in snake[-1]:
            computer.remove(piece)
            piece.reverse()
            snake.insert(len(snake), piece)
            break
        else:
            computer_.remove(computer_[piece_scores.index(max(piece_scores))])
            piece_scores.remove(max(piece_scores))

    return computer, snake, stock, status


def check_if_draw(snake):
    left = snake[0][0]
    right = snake[-1][-1]
    count = 0
    if left == right:
        for piece in snake:
            side_1, side_2 = piece
            if side_1 == left:
                count += 1
            if side_2 == left:
                count += 1
        if count == 8:
            return True
    else:
        return False


def main():
    status = "unknown"
    player: list = []
    computer: list = []
    piece: list = []
    stock: list = []
    snake: list = []

    while status == "unknown":
        domino_set = generate_set()
        player, computer, stock = split_set(domino_set)
        piece, status = first_player(player, computer)

    player.remove(piece[0]) if status == "computer" else computer.remove(piece[0])
    snake.append(piece[0])

    while True:
        print("=" * 70)
        print(f"Stock size: {len(stock)}")
        print(f"Computer pieces: {len(computer)}")
        print()
        print_snake(snake)
        print()
        print("Your pieces:")
        for idx, p in enumerate(player):
            print(f"{idx + 1}:{p}")
        print()

        # Break if any of the players has no piece left
        if len(player) == 0:
            print("Status: The game is over. You won!")
            break
        elif len(computer) == 0:
            print("Status: The game is over. The computer won!")
            break
        if check_if_draw(snake):
            print("Status: The game is over. It's a draw!")
            break

        msg = 'It\'s your turn to make a move. Enter your command.' if status == 'player' else 'Computer is about to make a move. Press Enter to continue...'
        if status == "player":
            player, snake, stock, status = player_moves(player, snake, stock, msg)
        else:
            computer, snake, stock, status = computer_moves(computer, snake, stock, msg)


main()
