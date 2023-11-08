import os
import PyInstaller.__main__
import shutil

PyInstaller.__main__.run([
    'main.py',
    '--collect-all',
    'bpy',
    '-n',
    'quvery-core',
    '-y'
])
srcdir = 'rules'
dstdir = 'dist/QuVery-Core/rules'

shutil.copytree(srcdir, dstdir)
