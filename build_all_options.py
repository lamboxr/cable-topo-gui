#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全选项构建脚本 - 提供多种打包选择
"""

import os
import sys
import subprocess
import shutil

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ["build", "dist"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✓ 清理 {dir_name} 目录")
            except PermissionError:
                print(f"! {dir_name} 目录清理失败，继续构建...")

def check_requirements():
    """检查必要文件和依赖"""
    # 检查必要文件
    required_files = ["cable_topo.py", "img/icon.ico"]
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"× 缺少必要文件: {file_path}")
            return False
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
    except ImportError:
        print("× PyInstaller 未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller 安装完成")
    
    return True

def build_option_1():
    """选项1: 单exe文件 + 显示命令行窗口"""
    print("\n=== 选项1: 单exe文件 + 显示命令行窗口 ===")
    
    cmd = [
        "pyinstaller",
        "cable_topo_single.spec",
        "--clean",
        "--noconfirm",
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        exe_path = "dist/线缆拓扑图生成器.exe"
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"✓ 成功生成: {exe_path} ({file_size:.1f} MB)")
            return True
    except subprocess.CalledProcessError as e:
        print(f"× 构建失败: {e}")
        if e.stderr:
            print(f"错误: {e.stderr}")
    
    return False

def build_option_2():
    """选项2: 单exe文件 + 隐藏命令行窗口"""
    print("\n=== 选项2: 单exe文件 + 隐藏命令行窗口 ===")
    
    # 创建临时spec文件
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

current_dir = os.path.dirname(os.path.abspath(SPEC))

pandas_binaries = collect_dynamic_libs('pandas')
numpy_binaries = collect_dynamic_libs('numpy')
geopandas_binaries = collect_dynamic_libs('geopandas')

pandas_datas = collect_data_files('pandas')
numpy_datas = collect_data_files('numpy')

a = Analysis(
    ['cable_topo.py'],
    pathex=[current_dir],
    binaries=pandas_binaries + numpy_binaries + geopandas_binaries,
    datas=pandas_datas + numpy_datas + [
        ('img/icon.ico', 'img'),
    ],
    hiddenimports=[
        'PyQt5.QtCore', 'PyQt5.QtWidgets', 'PyQt5.QtGui',
        'sqlite3', 'tempfile', 'shutil',
        'pandas', 'pandas._libs', 'pandas._libs.tslibs', 'pandas._libs.tslibs.base',
        'pandas._libs.window.aggregations', 'pandas._libs.algos', 'pandas._libs.groupby',
        'openpyxl', 'geopandas', 'shapely', 'numpy',
        'numpy.core._multiarray_umath', 'numpy.linalg._umath_linalg',
        'topo_creator.topo_generator',
    ],
    hookspath=[], hooksconfig={}, runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'IPython', 'jupyter'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name='线缆拓扑图生成器_无窗口',
    debug=False, bootloader_ignore_signals=False, strip=False,
    upx=True, upx_exclude=[], runtime_tmpdir=None,
    console=False,  # 隐藏命令行窗口
    disable_windowed_traceback=False, argv_emulation=False,
    target_arch=None, codesign_identity=None, entitlements_file=None,
    icon='img/icon.ico', version_file=None,
)'''
    
    with open("temp_windowed.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    cmd = ["pyinstaller", "temp_windowed.spec", "--clean", "--noconfirm"]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        exe_path = "dist/线缆拓扑图生成器_无窗口.exe"
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"✓ 成功生成: {exe_path} ({file_size:.1f} MB)")
            os.remove("temp_windowed.spec")  # 清理临时文件
            return True
    except subprocess.CalledProcessError as e:
        print(f"× 构建失败: {e}")
        if e.stderr:
            print(f"错误: {e.stderr}")
    
    if os.path.exists("temp_windowed.spec"):
        os.remove("temp_windowed.spec")
    return False

def build_option_3():
    """选项3: 目录模式 + 显示命令行窗口"""
    print("\n=== 选项3: 目录模式 + 显示命令行窗口 ===")
    
    cmd = [
        "pyinstaller",
        "cable_topo_dir.spec",
        "--clean",
        "--noconfirm",
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        exe_path = "dist/线缆拓扑图生成器/线缆拓扑图生成器.exe"
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)
            
            # 计算整个目录大小
            total_size = 0
            dist_dir = "dist/线缆拓扑图生成器"
            for dirpath, dirnames, filenames in os.walk(dist_dir):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
            
            total_size_mb = total_size / (1024 * 1024)
            print(f"✓ 成功生成: {exe_path} (exe: {file_size:.1f} MB, 总计: {total_size_mb:.1f} MB)")
            return True
    except subprocess.CalledProcessError as e:
        print(f"× 构建失败: {e}")
        if e.stderr:
            print(f"错误: {e.stderr}")
    
    return False

def main():
    print("=" * 60)
    print("线缆拓扑图生成器 - 全选项构建脚本")
    print("=" * 60)
    
    if not check_requirements():
        return False
    
    print("\n可用的构建选项:")
    print("1. 单exe文件 + 显示命令行窗口 (推荐调试)")
    print("2. 单exe文件 + 隐藏命令行窗口 (推荐发布)")
    print("3. 目录模式 + 显示命令行窗口 (最稳定)")
    print("4. 构建所有选项")
    
    choice = input("\n请选择构建选项 (1-4): ").strip()
    
    clean_build_dirs()
    
    success_count = 0
    
    if choice == "1":
        if build_option_1():
            success_count = 1
    elif choice == "2":
        if build_option_2():
            success_count = 1
    elif choice == "3":
        if build_option_3():
            success_count = 1
    elif choice == "4":
        print("\n构建所有选项...")
        if build_option_1():
            success_count += 1
        clean_build_dirs()
        if build_option_2():
            success_count += 1
        clean_build_dirs()
        if build_option_3():
            success_count += 1
    else:
        print("× 无效选择")
        return False
    
    print("\n" + "=" * 60)
    print("构建结果总结:")
    print("=" * 60)
    
    if success_count > 0:
        print(f"✓ 成功构建了 {success_count} 个版本")
        print("\n生成的文件:")
        
        files_to_check = [
            "dist/线缆拓扑图生成器.exe",
            "dist/线缆拓扑图生成器_无窗口.exe", 
            "dist/线缆拓扑图生成器/线缆拓扑图生成器.exe"
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path) / (1024 * 1024)
                print(f"  - {file_path} ({file_size:.1f} MB)")
        
        return True
    else:
        print("× 所有构建都失败了")
        return False

if __name__ == "__main__":
    success = main()
    input("\n按回车键退出...")
    sys.exit(0 if success else 1)