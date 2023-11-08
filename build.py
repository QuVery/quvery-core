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

shutil.copytree('rules', 'dist/QuVery-Core/rules')
