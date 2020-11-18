from argparse import ArgumentParser
from pathlib import Path
import sys
import shutil
import subprocess
from typing import Union
import os
import kraconvert

def get_args():
    parser = ArgumentParser('krita-exporter')
    parser.add_argument(
        'src',
        type=str,
        help='The source directory containing the .kra files you want to export.\
              This directory will be searched recursively'
    )
    parser.add_argument(
        'dst',
        type=str,
        help='The destination directory where you want the exported files to appear. \
              This directory will have the same directory structure as src \
              and will be created if it does not exist.'
    )
    parser.add_argument(
        '--format',
        default='png',
        type=str,
        help='The format to export to. Default value: png'
    )
    parser.add_argument(
        '--force',
        default=False,
        action='store_true',
        help='Export even those files which already have an exported file in dst.'
    )
    parser.add_argument(
        '--alt',
        type=str,
        help='If krita is called something else in your system. \
              You can specify it with this argument.')
    return parser.parse_args()

def err(text: str):
    print(f'ERROR: {text}', file=sys.stderr)
    sys.exit(1)

def export_from_krita(src: Union[str, Path], dst: Union[str, Path], alt_krita=None):
    krita = alt_krita or 'krita'
    tmpdir = Path('./tmp_delete_dis')
    tmpfile = tmpdir / 'exporting.png'
    if tmpdir.is_dir():
        tmpdir.rmdir()
    tmpdir.mkdir()
    args = [krita, '--export', str(src), '--export-filename', str(tmpfile)]
    try:
        print(f'running {args}')
        proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if tmpfile.is_file():
            print('copying file to dst')
            os.rename(str(tmpfile), str(dst))

    except subprocess.CalledProcessError as e:
        cmd = ' '.join(args)
        err(f'Could not export "{src}".\n' +
                f'the command was:{cmd}')
    finally:
        tmpdir.rmdir()

def krita_is_installed() -> bool:
    return shutil.which('krita') is not None

def run():
    args = get_args()
    src = Path(args.src)
    dst = Path(args.dst)
    export_format = args.format if args.format[0] != '.' else args.format[0]
    if not krita_is_installed():
        err('krita is not found in PATH. \
             I guess you wouldn\'t be trying to run this if you don\'t have Krita installed, \
             so something is weird. \
             This should work when the command "which krita" runs successfully. \
             If krita is called something else on your system, put that in the --alt option.')
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
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        if args.force or not dst_path.exists():
            print(f'Exporting "{relpath}"...')
            export_from_krita(src_path, dst_path)
    print('Done.')


if __name__ == '__main__':
    run()
