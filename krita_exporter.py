from argparse import ArgumentParser
from pathlib import Path
from sys import stderr, exit

def get_args():
    parser = ArgumentParser('krita-exporter')
    parser.add_argument('src')
    parser.add_argument('dst')
    return parser.parse_args()

def run():
    args = get_args()
    src = Path(args.src)
    if not src.is_dir():
        print(f'no directory at "{src}"', file=stderr)
        exit(1)
    print(list(src.glob('**/*.kra')))


if __name__ == '__main__':
    run()
