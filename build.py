import os
import logging
import shutil
import PyInstaller.__main__

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def run_pyinstaller():
    logging.info('Running PyInstaller...')
    script_name = 'main.py'
    try:
        PyInstaller.__main__.run([
            '--collect-all', 'bpy',
            '--collect-all', 'PIL',
            '--collect-all', 'pydub',
            '--collect-all', 'FastAPI',
            '-n', 'quvery-core',
            '--icon=icon.png',
            '-y',
            script_name
        ])
    except Exception as e:
        logging.error(f'PyInstaller failed: {e}')
        raise

def clean_pycache(srcdir):
    logging.info('Cleaning __pycache__ directories...')
    for root, dirs, files in os.walk(srcdir):
        for dir in dirs:
            if dir == '__pycache__':
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)
                logging.info(f'Deleted {dir_path}')

def copy_rules(srcdir, dstdir):
    logging.info(f'Copying rules from {srcdir} to {dstdir}...')
    try:
        if os.path.exists(dstdir):
            shutil.rmtree(dstdir)
            logging.info(f'Removed existing directory {dstdir}')
        shutil.copytree(srcdir, dstdir)
    except Exception as e:
        logging.error(f'Failed to copy rules: {e}')
        raise

def main():
    setup_logging()
    srcdir = 'rules'
    dstdir = 'dist/QuVery-Core/rules'
    try:
        run_pyinstaller()
        clean_pycache(srcdir)
        copy_rules(srcdir, dstdir)
        logging.info('Build process completed successfully.')
    except Exception as e:
        logging.error(f'Build process failed: {e}')
        exit(1)

if __name__ == '__main__':
    main()