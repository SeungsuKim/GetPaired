# -*- mode: python -*-

import sys


block_cipher = None


a = Analysis(['main_GUI.py'],
             pathex=['/Users/seungsukim/PycharmProjects/GetPaired'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('certificate.yml', 'certificate.yml', 'DATA'),
            ('data.pkl', 'data.pkl', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

if sys.platform == 'darwin':
  exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='GetPaired',
            debug=False,
            strip=False,
            upx=True,
            runtime_tmpdir=None,
            console=True)

if sys.platform == 'darwin':
   app = BUNDLE(exe,
                name='GetPaired.app',
                info_plist={
                  'NSHighResolutionCapable': 'True'
                })

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main_GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main_GUI')
