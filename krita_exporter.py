from argparse import ArgumentParser
from pathlib import Path
import sys
import shutils

def get_args():
    parser = ArgumentParser('krita-exporter')
    parser.add_argument('src')
    parser.add_argument('dst')
    parser.add_argument('--format', default='png')
    parser.add_argument('--force', default=False, action='store_true')
    return parser.parse_args()

def err(text):
    print(f'ERROR: {text}', file=sys.stderr)
    sys.exit(1)

def export_command(src, dst, dry=True, alt_krita=None):
    krita = alt_krita or 'krita'
    return f'{krita} --export {src} --export-filename {dst};'

def krita_is_installed() -> bool:
    return shutils.which('krita') is not None

def run():
    args = get_args()
    src = Path(args.src)
    dst = Path(args.dst)
    if not krita_is_installed():
        err('krita is not found in PATH. I guess you wouldn\'t be trying to run this if you don\'t have Krita installed, so something is weird. This should work when the command "which krita" runs successfully. if krita is called something else on your system, put that in the --alt option.')
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
        if args.force or not dst_path.exists():
            print(export_command(src_path, dst_path))

if __name__ == '__main__':
    run()
