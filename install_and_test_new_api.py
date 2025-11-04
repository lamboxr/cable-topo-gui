#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装新依赖并测试API集成
"""

import sys
import subprocess
import os

def install_new_dependencies():
    """安装新的依赖包"""
    print("安装新的topo-generator依赖...")
    
    try:
        # 安装新的依赖
        subprocess.check_call([sys.executable, "-m", "pip", "install", "topo-generator"])
        print("✓ topo-generator 安装成功")
        
        # 安装其他依赖
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requiements.txt"])
        print("✓ 所有依赖安装完成")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"× 依赖安装失败: {e}")
        return False

def test_import():
    """测试新API导入"""
    try:
        from topo_generator import generate_topology_files
        print("✓ 新API导入成功")
        return True
    except ImportError as e:
        print(f"× 新API导入失败: {e}")
        return False

def main():
    print("=" * 60)
    print("新API集成 - 安装和测试脚本")
    print("=" * 60)
    
    # 安装依赖
    if not install_new_dependencies():
        print("依赖安装失败，请手动安装:")
        print("pip install topo-generator")
        return False
    
    # 测试导入
    if not test_import():
        print("API导入失败，请检查安装")
        return False
    
    print("\n" + "=" * 60)
    print("✓ 新API集成准备完成！")
    print("=" * 60)
    print("API变化总结:")
    print("1. 导入变更:")
    print("   旧: from topo_creator.topo_generator import gen_topos")
    print("   新: from topo_generator import generate_topology_files")
    print()
    print("2. 参数格式变更:")
    print("   旧: gpkg_params = {'SRO': {'gpkg_path': '...', 'layer_name': '...'}}")
    print("   新: sro_config = (gpkg_path, layer_name)")
    print()
    print("3. 返回格式变更:")
    print("   新: {'code': 200, 'file_path': '...', 'msg': '...'}")
    print()
    print("现在可以运行:")
    print("- python test_new_topo_api.py  # 测试新API")
    print("- python cable_topo.py         # 运行主程序")
    print("- python build_single_exe.py   # 重新打包")
    
    return True

if __name__ == "__main__":
    success = main()
    input("\n按回车键退出...")
    sys.exit(0 if success else 1)