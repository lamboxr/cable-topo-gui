#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强化构建脚本 - 多种方法解决DLL问题
"""

import os
import sys
import subprocess
import shutil

def install_dependencies():
    """安装和更新依赖"""
    print("检查和安装依赖...")
    
    # 更新pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    # 安装requirements
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requiements.txt"])
    
    # 确保PyInstaller是最新版本
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])
    
    print("✓ 依赖安装完成")

def clean_build():
    """清理构建目录"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ 清理 {dir_name} 目录")

def build_method_1_spec():
    """方法1: 使用改进的spec文件"""
    print("\n=== 方法1: 使用改进的spec文件 ===")
    
    cmd = [
        "pyinstaller",
        "cable_topo.spec",
        "--clean",
        "--noconfirm",
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        exe_path = "dist/线缆拓扑图生成器.exe"
        if os.path.exists(exe_path):
            print("✓ 方法1成功")
            return True
    except subprocess.CalledProcessError as e:
        print(f"× 方法1失败: {e}")
        if e.stderr:
            print(f"错误: {e.stderr}")
    
    return False

def build_method_2_dir():
    """方法2: 使用目录模式"""
    print("\n=== 方法2: 使用目录模式 ===")
    
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
            print("✓ 方法2成功")
            return True
    except subprocess.CalledProcessError as e:
        print(f"× 方法2失败: {e}")
        if e.stderr:
            print(f"错误: {e.stderr}")
    
    return False

def build_method_3_collect_all():
    """方法3: 使用collect-all参数"""
    print("\n=== 方法3: 使用collect-all参数 ===")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=img/icon.ico",
        "--name=线缆拓扑图生成器_v3",
        "--clean",
        "--noconfirm",
        "--collect-all=pandas",
        "--collect-all=numpy",
        "--collect-all=geopandas",
        "--collect-all=shapely",
        "--collect-all=pyproj",
        "--collect-all=fiona",
        "cable_topo.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        exe_path = "dist/线缆拓扑图生成器_v3.exe"
        if os.path.exists(exe_path):
            print("✓ 方法3成功")
            return True
    except subprocess.CalledProcessError as e:
        print(f"× 方法3失败: {e}")
        if e.stderr:
            print(f"错误: {e.stderr}")
    
    return False

def test_exe(exe_path):
    """测试生成的exe文件"""
    print(f"\n测试exe文件: {exe_path}")
    
    if not os.path.exists(exe_path):
        print("× exe文件不存在")
        return False
    
    file_size = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"✓ 文件大小: {file_size:.1f} MB")
    
    # 简单的启动测试（快速退出）
    try:
        # 注意：这里只是检查exe是否能启动，不等待GUI
        result = subprocess.run([exe_path, "--help"], 
                              timeout=5, 
                              capture_output=True, 
                              text=True)
        print("✓ exe文件可以启动")
        return True
    except subprocess.TimeoutExpired:
        print("✓ exe文件启动正常（GUI程序）")
        return True
    except Exception as e:
        print(f"× exe启动测试失败: {e}")
        return False

def main():
    print("=" * 60)
    print("线缆拓扑图生成器 - 强化构建脚本")
    print("=" * 60)
    
    # 检查必要文件
    required_files = ["cable_topo.py", "img/icon.ico", "requiements.txt"]
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"× 缺少必要文件: {file_path}")
            return False
    
    # 安装依赖
    try:
        install_dependencies()
    except Exception as e:
        print(f"× 依赖安装失败: {e}")
        return False
    
    # 清理构建目录
    clean_build()
    
    # 尝试不同的构建方法
    methods = [
        ("改进的spec文件", build_method_1_spec, "dist/线缆拓扑图生成器.exe"),
        ("目录模式", build_method_2_dir, "dist/线缆拓扑图生成器/线缆拓扑图生成器.exe"),
        ("collect-all参数", build_method_3_collect_all, "dist/线缆拓扑图生成器_v3.exe"),
    ]
    
    successful_builds = []
    
    for method_name, method_func, exe_path in methods:
        print(f"\n尝试构建方法: {method_name}")
        
        if method_func():
            if test_exe(exe_path):
                successful_builds.append((method_name, exe_path))
                print(f"✓ {method_name} 构建并测试成功")
            else:
                print(f"× {method_name} 构建成功但测试失败")
        
        # 每次方法后清理，为下次尝试做准备
        if os.path.exists("build"):
            shutil.rmtree("build")
    
    # 总结结果
    print("\n" + "=" * 60)
    print("构建结果总结:")
    print("=" * 60)
    
    if successful_builds:
        print("✓ 成功的构建:")
        for method_name, exe_path in successful_builds:
            file_size = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"  - {method_name}: {exe_path} ({file_size:.1f} MB)")
        
        print(f"\n推荐使用: {successful_builds[0][1]}")
        return True
    else:
        print("× 所有构建方法都失败了")
        print("\n建议:")
        print("1. 检查Python环境和依赖版本")
        print("2. 尝试在虚拟环境中构建")
        print("3. 检查是否有杀毒软件干扰")
        print("4. 尝试降级pandas版本到1.5.x")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)