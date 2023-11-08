import os
import PyInstaller.__main__
import shutil

script_name = 'main.py'

PyInstaller.__main__.run([
    # '--clean',
    # '--hidden-import=bpy.path',
    '--collect-all',
    'bpy',
    '-n',
    'quvery-core',
    '-y',
    script_name
])

srcdir = 'rules'
dstdir = 'dist/QuVery-Core/rules'

# delete __pycache__ folders under all subdirectories of srcdir
for root, dirs, files in os.walk(srcdir):
    for dir in dirs:
        if dir == '__pycache__':
            shutil.rmtree(os.path.join(root, dir))

shutil.copytree(srcdir, dstdir)
