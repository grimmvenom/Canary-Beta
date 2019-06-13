# -*- mode: python -*-

block_cipher = None


a = Analysis(['src/main.py'],
             pathex=['src'],
             binaries=[],
             datas=[
			 ('src/base', 'base'),
			 ('src/modules', 'modules'),
			 ('src/resources', 'resources'),
			 ('src/resources/web_template', 'resources/web_template')
			 ],
             hiddenimports=['bottle'],
             hookspath=['hooks'],
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
          [],
          name='Canary',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=True,
          icon='src/resources/canary.ico' )
