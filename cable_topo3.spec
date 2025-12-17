# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path
import os  # 添加os模块导入

block_cipher = None

# 修改当前目录获取方式（解决.spec文件中__file__未定义问题）
current_dir = Path(os.path.dirname(os.path.realpath(__name__))).resolve()

a = Analysis(
    ['cable_topo.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=[
        # 确保gpkg文件夹被正确打包（根据实际路径调整）
        ('gpkg/*.gpkg', 'gpkg'),
        # 其他需要打包的数据文件
    ],
    hiddenimports=[
        # 保留之前的隐藏导入列表
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.timedeltas',
        'pandas._libs.tslibs.offsets',
        'pandas._libs.tslibs.parsing',
        'pandas._libs.tslibs.conversion',
        'geopandas._compat',
        'fiona._shim',
        'fiona.schema',
        'shapely.geos',
        'openpyxl.styles',
        'openpyxl.styles.colors',
        'sqlite3',
        # 项目内部模块
        'constraints',
        'constraints.field_name_mapper',
        'data_service',
        'data_service.base',
        'data_service.sro_service',
        'data_service.cable_service',
        'data_service.box_service',
        'data_service.service_manager',
        'utils.excel_utils',
        'utils.gda_utils',
        'utils.gpkg_utils',
        'utils.zip_utils',
        'constraints.field_name_mapper',
        'topo_creator',
        'topo_creator.gen_topo_from_point',
        'topo_creator.box_sheet_creator',
        'topo_creator.topo_generator',
        'topo_creator.init_data',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='线缆拓扑图生成器',  # 生成的EXE文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 暂时开启控制台窗口以便查看运行日志
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='img/icon.ico'
)