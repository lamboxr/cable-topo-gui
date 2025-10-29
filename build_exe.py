#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建脚本 - 将 cable_topo.py 打包成单文件 exe
"""

import os
import sys
import subprocess
import shutil

def build_exe():
    """构建单文件 exe"""
    
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
    
    # PyInstaller 命令参数
    cmd = [
        "pyinstaller",
        "cable_topo.spec",              # 使用spec文件
        "--clean",                      # 清理临时文件
        "--noconfirm",                  # 不询问覆盖
    ]
    
    print("开始打包...")
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        print("✓ 打包成功！")
        
        # 检查生成的文件
        exe_path = "dist/线缆拓扑图生成器.exe"
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
            print(f"✓ 生成的exe文件: {exe_path}")
            print(f"✓ 文件大小: {file_size:.1f} MB")
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
    print("线缆拓扑图生成器 - 打包脚本")
    print("=" * 50)
    
    success = build_exe()
    
    if success:
        print("\n" + "=" * 50)
        print("✓ 打包完成！")
        print("✓ 可执行文件位置: dist/线缆拓扑图生成器.exe")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("× 打包失败，请检查错误信息")
        print("=" * 50)
        sys.exit(1)