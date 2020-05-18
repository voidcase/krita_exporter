from argparse import ArgumentParser
from pathlib import Path
import sys

def get_args():
    parser = ArgumentParser('krita-exporter')
    parser.add_argument('src')
    parser.add_argument('dst')
    return parser.parse_args()

def err(text):
    print(f'ERROR: {text}', file=sys.stderr)
    sys.exit(1)

def exec_export(src, dst, dry=True):
    # TODO run command to export
    pass

def run():
    args = get_args()
    src = Path(args.src)
    dst = Path(args.dst)
    if not src.is_dir():
        err(f'no directory at "{src}"')
    if dst.exists() and not dst.is_dir():
        err(f'"{dst}" exists but is not a directory.')
    if not dst.is_dir():
        print(f'no directory at "{dst}", creating...')
        dst.mkdir()
    pathgen = src.glob('**/*.kra')
    for path in pathgen:
        print(path)
        pass

if __name__ == '__main__':
    run()
