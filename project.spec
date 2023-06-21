# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

# Get the current directory (where the .spec file is located)
current_directory = os.path.dirname(os.path.abspath(__name__))
bs_runner_directory = os.path.join(current_directory, 'BS_Runner', 'Debug')

# Build the paths relative to the current directory
ui_directory = os.path.join(current_directory, 'UI')

a = Analysis(['start_prog.py'],
             pathex=[current_directory],
             binaries=[],
             datas=[
              (os.path.join(ui_directory, '*'), 'UI'),
              (os.path.join(bs_runner_directory, 'BS_Runner.exe'), 'BS_Runner/Debug')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Behavior System',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='Behavior_System.ico')

# This will create a folder with your executable and all dependencies
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Behavior System')

# Note: Replace 'your_script.py' with the actual name of your script.
# Replace 'your_output_executable_name' with the desired name of your output executable.
