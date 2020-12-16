from argparse import ArgumentParser
from os.path import getmtime
from pathlib import Path
import sys
import typing as T
from zipfile import ZipFile
from time import sleep

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
        '--force',
        default=False,
        action='store_true',
        help='Export even those files which already have not been modified since the last export.'
    )
    parser.add_argument(
        '--purge',
        action='store_true',
        help='empty destination folder before refilling'
    )
    parser.add_argument(
        '-c', '--confirm',
        default=False,
        action='store_true',
        help='manually confirm that the changed files are the ones you want to change',
    )
    parser.add_argument(
        '-w', '--watch',
        action='store_true',
        help='poll directory for changes, run until exited.',
    )
    return parser.parse_args()


def err(text: str):
    print(f'ERROR: {text}', file=sys.stderr)
    sys.exit(1)


def export_kra(src: T.Union[str, Path], dst: T.Union[str, Path]):
    with ZipFile(src) as src_zip:
        src_zip.extract('mergedimage.png', '/tmp/')
        Path('/tmp/mergedimage.png').rename(dst)


def only_updated(src, dst, pathgen: T.Iterable[Path], force) -> T.List[Path]:
    ret = []
    for src_path in pathgen:
        # Make destination dir
        relpath = src_path.relative_to(src)
        dst_relpath = relpath.with_suffix('.png')
        dst_path = dst / dst_relpath
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        src_modified = getmtime(str(src_path))
        dst_modified = getmtime(str(dst_path)) if dst_path.is_file() else -1
        if force or src_modified > dst_modified:
            ret.append((src_path, dst_path))
    return ret


def user_confirm_changes(path_pairs):
    for src_path, dst_path in path_pairs:
        print(f'{src_path} -> {dst_path}')
    users_approval = yesno_prompt('Ready to export?')
    if not users_approval:
        print('Come back when you\'re ready.')
        sys.exit(0)

def yesno_prompt(question: str) -> bool:
    res = input(f'{question} [y/n]')
    return res.lower().strip() in ['y', 'yes']


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
    if args.watch:
        poll_interval = 2
        print(f'polling for changes every {poll_interval} seconds...')
    while True:
        try:
            all_src_paths = src.glob('**/[!.]*.kra')
            path_pairs = only_updated(src, dst, all_src_paths, force=args.force)
            if len(path_pairs) == 0:
                if args.watch:
                    sleep(poll_interval)
                    continue
                else:
                    print('nothing new to export')
                    exit(0)
            if args.confirm:
                user_confirm_changes(path_pairs)
            for src_path, dst_path in path_pairs:
                relative_src_path = src_path.relative_to(src)
                print(f'exporting "{relative_src_path}"')
                export_kra(src_path, dst_path)
            if not args.watch:
                break
        except KeyboardInterrupt:
            break
    print('Done.')


if __name__ == '__main__':
    run()
