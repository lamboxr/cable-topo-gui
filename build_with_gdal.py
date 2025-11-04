#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
带GDAL支持的构建脚本
"""

import os
import sys
import subprocess
import shutil

def install_gdal_dependencies():
    """安装GDAL相关依赖"""
    print("安装GDAL相关依赖...")
    
    # 更新pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # 安装GDAL相关包
    gdal_packages = [
        "fiona>=1.8.0",
        "pyogrio>=0.5.0", 
        "GDAL>=3.4.0",
        "rasterio>=1.3.0"
    ]
    
    for package in gdal_packages:
        try:
            print(f"安装 {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"× {package} 安装失败: {e}")
            print("尝试使用conda-forge安装...")
            try:
                subprocess.check_call(["conda", "install", "-c", "conda-forge", package.split(">=")[0], "-y"])
                print(f"✓ {package} 通过conda安装成功")
            except:
                print(f"× {package} conda安装也失败")
    
    # 安装其他依赖
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requiements.txt"])
    print("✓ 所有依赖安装完成")

def build_with_collect_all():
    """使用collect-all方式构建"""
    print("\n开始构建...")
    
    # 清理构建目录
    if os.path.exists("build"):
        try:
            shutil.rmtree("build")
            print("✓ 清理 build 目录")
        except PermissionError:
            print("! build 目录清理失败，继续构建...")
    
    if os.path.exists("dist"):
        try:
            shutil.rmtree("dist")
            print("✓ 清理 dist 目录")
        except PermissionError:
            print("! dist 目录清理失败，继续构建...")
    
    # PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",  # 显示命令行窗口
        "--icon=img/icon.ico",
        "--name=线缆拓扑图生成器",
        "--clean",
        "--noconfirm",
        # 收集所有相关包
        "--collect-all=pandas",
        "--collect-all=numpy", 
        "--collect-all=geopandas",
        "--collect-all=shapely",
        "--collect-all=fiona",
        "--collect-all=pyogrio",
        "--collect-all=rasterio",
        "--collect-all=pyproj",
        # 添加隐藏导入
        "--hidden-import=fiona.crs",
        "--hidden-import=fiona.drvsupport", 
        "--hidden-import=fiona.env",
        "--hidden-import=fiona._env",
        "--hidden-import=pyogrio.raw",
        "--hidden-import=pyogrio._io",
        "--hidden-import=pyogrio._ogr",
        # 包含数据文件
        "--add-data=img/icon.ico;img",
        "cable_topo.py"
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        print("✓ 打包成功！")
        
        exe_path = "dist/线缆拓扑图生成器.exe"
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"✓ 生成的exe文件: {exe_path}")
            print(f"✓ 文件大小: {file_size:.1f} MB")
            return True
        else:
            print("× 未找到生成的exe文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"× 打包失败: {e}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("线缆拓扑图生成器 - 带GDAL支持的构建脚本")
    print("=" * 60)
    
    # 检查必要文件
    required_files = ["cable_topo.py", "img/icon.ico", "requiements.txt"]
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"× 缺少必要文件: {file_path}")
            return False
    
    # 安装依赖
    try:
        install_gdal_dependencies()
    except Exception as e:
        print(f"× 依赖安装失败: {e}")
        print("请手动安装GDAL相关依赖")
        return False
    
    # 构建
    success = build_with_collect_all()
    
    if success:
        print("\n" + "=" * 60)
        print("✓ 构建完成！")
        print("✓ 可执行文件位置: dist/线缆拓扑图生成器.exe")
        print("✓ 该版本包含完整的GDAL支持")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("× 构建失败")
        print("建议:")
        print("1. 手动安装GDAL: conda install -c conda-forge gdal")
        print("2. 或使用OSGeo4W安装GDAL")
        print("3. 确保GDAL在系统PATH中")
        print("=" * 60)
    
    return success

if __name__ == "__main__":
    success = main()
    input("\n按回车键退出...")
    sys.exit(0 if success else 1)