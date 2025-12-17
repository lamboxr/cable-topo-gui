# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# 获取当前脚本所在目录
current_dir = Path(__file__).parent.resolve()

a = Analysis(
    ['cable_topo.py'],  # 主程序入口脚本（根据实际文件名调整）
    pathex=[str(current_dir)],
    binaries=[],
    datas=[
        # 包含自定义包和数据文件
        (str(Path(sys.prefix) / 'Lib' / 'site-packages' / 'topo_creator'), 'topo_creator'),
        # 若有gpkg模板文件可添加此处，例如:
        # ('gpkg/*.gpkg', 'gpkg'),
    ],
    hiddenimports=[
        # 核心依赖的隐藏导入
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
    upx=True,  # 启用压缩
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 关闭控制台窗口（图形界面程序）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='img/icon.ico'
)