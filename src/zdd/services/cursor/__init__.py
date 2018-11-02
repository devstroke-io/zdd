import sys


class Cursor:
    @staticmethod
    def move(line, column):
        sys.stdout.write(f'\033[{line};{column}H')
        sys.stdout.flush()

    @staticmethod
    def move_start():
        sys.stdout.write(f'\r')
        sys.stdout.flush()

    @staticmethod
    def erase_to_the_end():
        sys.stdout.write(f'\033[K')
        sys.stdout.flush()

    @staticmethod
    def move_up(count):
        sys.stdout.write(f'\033[{count}A')
        sys.stdout.flush()

    @staticmethod
    def move_down(count):
        sys.stdout.write(f'\033[{count}B')
        sys.stdout.flush()

    @staticmethod
    def move_forward(count):
        sys.stdout.write(f'\033[{count}C')
        sys.stdout.flush()

    @staticmethod
    def move_backward(count):
        sys.stdout.write(f'\033[{count}D')
        sys.stdout.flush()

    @staticmethod
    def clear_screen():
        sys.stdout.write(f'\033[2J')
        sys.stdout.flush()

    @staticmethod
    def save_position():
        sys.stdout.write(f'\033[s')
        sys.stdout.flush()

    @staticmethod
    def restore_position():
        sys.stdout.write(f'\033[u')
        sys.stdout.flush()
