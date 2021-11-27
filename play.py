if __name__ == '__main__':
    import argparse
    from qwirkle import QwirkleGame

    parser = argparse.ArgumentParser(description='Qwirkle')
    parser.add_argument('--players', nargs='+')

    winner = []
    for i in range(1):
        game = QwirkleGame()
        game.main(parser.parse_args().players)
        winner.append(game.get_winner())

    print(winner)
