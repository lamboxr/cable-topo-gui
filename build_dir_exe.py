#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建脚本 - 将 cable_topo.py 打包成目录形式的 exe (更稳定)
"""

import os
import sys
import subprocess
import shutil

def build_dir_exe():
    """构建目录形式的 exe (更稳定，避免DLL问题)"""
    
    # 检查 PyInstaller 是否安装
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
    except ImportError:
        print("× PyInstaller 未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller 安装完成")
    
    # 检查图标文件是否存在
    icon_path = "img/icon.ico"
    if not os.path.exists(icon_path):
        print(f"× 图标文件不存在: {icon_path}")
        return False
    
    # 检查入口文件是否存在
    entry_file = "cable_topo.py"
    if not os.path.exists(entry_file):
        print(f"× 入口文件不存在: {entry_file}")
        return False
    
    # 清理之前的构建文件
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("✓ 清理 build 目录")
    
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        print("✓ 清理 dist 目录")
    
    # PyInstaller 命令参数 - 使用目录模式
    cmd = [
        "pyinstaller",
        "--onedir",                     # 打包成目录形式
        "--windowed",                   # 不显示控制台窗口
        f"--icon={icon_path}",          # 设置图标
        "--name=线缆拓扑图生成器",        # 设置exe文件名
        "--clean",                      # 清理临时文件
        "--noconfirm",                  # 不询问覆盖
        "--collect-all=pandas",         # 收集pandas所有文件
        "--collect-all=numpy",          # 收集numpy所有文件
        "--collect-all=geopandas",      # 收集geopandas所有文件
        "--collect-all=shapely",        # 收集shapely所有文件
        entry_file
    ]
    
    print("开始打包...")
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        print("✓ 打包成功！")
        
        # 检查生成的文件
        exe_path = "dist/线缆拓扑图生成器/线缆拓扑图生成器.exe"
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"✓ 生成的exe文件: {exe_path}")
            print(f"✓ 文件大小: {file_size:.1f} MB")
            
            # 计算整个目录大小
            total_size = 0
            dist_dir = "dist/线缆拓扑图生成器"
            for dirpath, dirnames, filenames in os.walk(dist_dir):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
            
            total_size_mb = total_size / (1024 * 1024)
            print(f"✓ 总目录大小: {total_size_mb:.1f} MB")
            return True
        else:
            print("× 未找到生成的exe文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"× 打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("线缆拓扑图生成器 - 目录打包脚本")
    print("=" * 50)
    
    success = build_dir_exe()
    
    if success:
        print("\n" + "=" * 50)
        print("✓ 打包完成！")
        print("✓ 可执行文件位置: dist/线缆拓扑图生成器/线缆拓扑图生成器.exe")
        print("✓ 整个目录可以复制到其他机器运行")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("× 打包失败，请检查错误信息")
        print("=" * 50)
        sys.exit(1)