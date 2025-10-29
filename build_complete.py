#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整构建脚本 - 将 cable_topo.py 打包成单文件 exe
包含依赖安装和打包过程
"""

import os
import sys
import subprocess
import shutil

def install_dependencies():
    """安装项目依赖"""
    print("正在安装项目依赖...")
    
    # 安装requirements.txt中的依赖
    if os.path.exists("requiements.txt"):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requiements.txt"])
            print("✓ 项目依赖安装完成")
        except subprocess.CalledProcessError as e:
            print(f"× 项目依赖安装失败: {e}")
            return False
    
    # 安装本地wheel包
    wheel_file = "topo_creator-0.0.1-py3-none-any.whl"
    if os.path.exists(wheel_file):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", wheel_file, "--force-reinstall"])
            print("✓ topo_creator模块安装完成")
        except subprocess.CalledProcessError as e:
            print(f"× topo_creator模块安装失败: {e}")
            return False
    else:
        print(f"× 未找到wheel文件: {wheel_file}")
        return False
    
    return True

def build_exe():
    """构建单文件 exe"""
    
    # 先安装依赖
    if not install_dependencies():
        return False
    
    # 检查 PyInstaller 是否安装
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
    except ImportError:
        print("× PyInstaller 未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller 安装完成")
        except subprocess.CalledProcessError as e:
            print(f"× PyInstaller 安装失败: {e}")
            return False
    
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
    
    # 使用spec文件打包（更好的控制）
    spec_file = "cable_topo.spec"
    if os.path.exists(spec_file):
        cmd = ["pyinstaller", spec_file]
        print(f"使用spec文件打包: {spec_file}")
    else:
        # 回退到命令行参数
        cmd = [
            "pyinstaller",
            "--onefile",                    # 打包成单文件
            # "--windowed",                   # 不显示控制台窗口
            f"--icon={icon_path}",          # 设置图标
            "--name=线缆拓扑图生成器",        # 设置exe文件名
            "--clean",                      # 清理临时文件
            "--noconfirm",                  # 不询问覆盖
            entry_file
        ]
    
    print("开始打包...")
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, check=True, text=True, encoding='utf-8')
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
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("线缆拓扑图生成器 - 完整构建脚本")
    print("=" * 60)
    
    success = build_exe()
    
    if success:
        print("\n" + "=" * 60)
        print("✓ 打包完成！")
        print("✓ 可执行文件位置: dist/线缆拓扑图生成器.exe")
        print("=" * 60)
        
        # 询问是否打开文件夹
        try:
            choice = input("\n是否打开dist文件夹？(y/n): ").lower().strip()
            if choice in ['y', 'yes', '是']:
                if os.name == 'nt':  # Windows
                    os.startfile('dist')
                else:
                    subprocess.run(['xdg-open', 'dist'])
        except KeyboardInterrupt:
            pass
    else:
        print("\n" + "=" * 60)
        print("× 打包失败，请检查错误信息")
        print("=" * 60)
        sys.exit(1)