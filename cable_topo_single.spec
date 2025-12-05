# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(SPEC))

# 收集所有相关的动态库
pandas_binaries = collect_dynamic_libs('pandas')
numpy_binaries = collect_dynamic_libs('numpy')
geopandas_binaries = collect_dynamic_libs('geopandas')
fiona_binaries = collect_dynamic_libs('fiona')
pyogrio_binaries = collect_dynamic_libs('pyogrio')
shapely_binaries = collect_dynamic_libs('shapely')

# 收集数据文件
pandas_datas = collect_data_files('pandas')
numpy_datas = collect_data_files('numpy')
fiona_datas = collect_data_files('fiona')
pyogrio_datas = collect_data_files('pyogrio')

# 分析入口文件
a = Analysis(
    ['cable_topo.py'],
    pathex=[current_dir],
    binaries=pandas_binaries + numpy_binaries + geopandas_binaries + fiona_binaries + pyogrio_binaries + shapely_binaries,
    datas=pandas_datas + numpy_datas + fiona_datas + pyogrio_datas + [
        ('img/icon.ico', 'img'),  # 包含图标文件
    ],
    hiddenimports=[
        # PyQt5相关
        'PyQt5.QtCore',
        'PyQt5.QtWidgets',
        'PyQt5.QtGui',
        # 系统模块
        'sqlite3',
        'tempfile',
        'shutil',
        # jaraco相关（pkg_resources依赖）
        'jaraco',
        'jaraco.text',
        'jaraco.functools',
        'jaraco.context',
        'jaraco.collections',
        # pandas相关
        'pandas',
        'pandas._libs',
        'pandas._libs.tslibs',
        'pandas._libs.tslibs.base',
        'pandas._libs.tslibs.ccalendar',
        'pandas._libs.tslibs.dtypes',
        'pandas._libs.tslibs.field_array',
        'pandas._libs.tslibs.nattype',
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.offsets',
        'pandas._libs.tslibs.parsing',
        'pandas._libs.tslibs.period',
        'pandas._libs.tslibs.strptime',
        'pandas._libs.tslibs.timedeltas',
        'pandas._libs.tslibs.timestamps',
        'pandas._libs.tslibs.timezones',
        'pandas._libs.tslibs.tzconversion',
        'pandas._libs.tslibs.vectorized',
        'pandas._libs.window.aggregations',
        'pandas._libs.window.indexer',
        'pandas._libs.algos',
        'pandas._libs.groupby',
        'pandas._libs.hashing',
        'pandas._libs.hashtable',
        'pandas._libs.index',
        'pandas._libs.indexing',
        'pandas._libs.internals',
        'pandas._libs.interval',
        'pandas._libs.join',
        'pandas._libs.lib',
        'pandas._libs.missing',
        'pandas._libs.ops',
        'pandas._libs.ops_dispatch',
        'pandas._libs.parsers',
        'pandas._libs.reduction',
        'pandas._libs.reshape',
        'pandas._libs.sparse',
        'pandas._libs.testing',
        'pandas._libs.writers',
        # 其他依赖
        'openpyxl',
        'geopandas',
        'shapely',
        'fiona',
        'fiona.crs',
        'fiona.drvsupport',
        'fiona.env',
        'fiona.errors',
        'fiona.io',
        'fiona.model',
        'fiona.ogrext',
        'fiona.rfc3339',
        'fiona.schema',
        'fiona.transform',
        'fiona._env',
        'fiona._geometry',
        'fiona._shim',
        'fiona._transform',
        'pyogrio',
        'pyogrio.raw',
        'pyogrio._io',
        'pyogrio._ogr',
        'numpy',
        'numpy.core._multiarray_umath',
        'numpy.core._multiarray_tests',
        'numpy.linalg._umath_linalg',
        'numpy.fft._pocketfft_internal',
        'numpy.random._common',
        'numpy.random._bounded_integers',
        'numpy.random._mt19937',
        'numpy.random._pcg64',
        'numpy.random._philox',
        'numpy.random._sfc64',
        'numpy.random._generator',
        'numpy.random.bit_generator',
        # 应用模块
        'topo_generator',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pkg_resources',  # 排除 pkg_resources 避免 jaraco 依赖问题
        # 排除不需要的模块以减小文件大小
        'tkinter',
        'matplotlib',
        'IPython',
        'jupyter',
        'test',
        'tests',
        'testing',
    ],
    noarchive=False,
)

# 处理PYZ
pyz = PYZ(a.pure)

# 创建可执行文件 - 单文件模式，显示控制台
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='线缆拓扑图生成器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 使用UPX压缩（如果可用）
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 显示命令行窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='img/icon.ico',  # 设置图标
    version_file=None,
)