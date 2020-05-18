from argparse import ArgumentParser
from pathlib import Path
import sys

def get_args():
    parser = ArgumentParser('krita-exporter')
    parser.add_argument('src')
    parser.add_argument('dst')
    parser.add_argument('--format', default='png')
    return parser.parse_args()

def err(text):
    print(f'ERROR: {text}', file=sys.stderr)
    sys.exit(1)

def exec_export(src, dst, dry=True):
    print(f'krita --export {src} --export-filename {dst};')

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
    pathgen = src.glob('**/[!.]*.kra')
    for src_path in pathgen:
        relpath = src_path.relative_to(src)
        dst_relpath = relpath.with_suffix(f'.{args.format}')
        dst_path = dst / dst_relpath
        #TODO create needed directories
        exec_export(src_path, dst_path)

if __name__ == '__main__':
    run()
