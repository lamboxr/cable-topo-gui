#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试双目录配置功能
"""

import sys
import os
import tempfile
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

# 模拟新的topo生成API
def mock_generate_topology_files(sro_config, box_config, cable_config, output_dir):
    """模拟新的generate_topology_files函数"""
    print("开始模拟新的拓扑生成...")
    
    import time
    time.sleep(1)  # 模拟处理时间
    
    # 创建一个模拟的结果文件
    result_file = os.path.join(output_dir, "topology_result.zip")
    with open(result_file, 'w') as f:
        f.write("模拟的新API拓扑文件内容")
    
    print("模拟新API拓扑生成成功完成")
    return {
        "code": 200,
        "file_path": result_file,
        "msg": "拓扑生成成功",
        "error_message": None
    }

# 替换新的API函数进行测试
try:
    import topo_generator
    topo_generator.generate_topology_files = mock_generate_topology_files
    print("已替换generate_topology_files函数为测试版本")
except ImportError:
    print("无法导入topo_generator，将创建模拟模块")
    
    # 创建模拟模块
    class MockTopoGenerator:
        @staticmethod
        def generate_topology_files(sro_config, box_config, cable_config, output_dir):
            return mock_generate_topology_files(sro_config, box_config, cable_config, output_dir)
    
    sys.modules['topo_generator'] = MockTopoGenerator()

def create_test_gpkg_directory():
    """创建测试用的gpkg目录"""
    test_dir = os.path.join(tempfile.gettempdir(), "test_gpkg")
    os.makedirs(test_dir, exist_ok=True)
    
    # 创建模拟的gpkg文件
    for filename in ["SRO.gpkg", "BOX.gpkg", "CABLE.gpkg"]:
        filepath = os.path.join(test_dir, filename)
        with open(filepath, 'w') as f:
            f.write("模拟的gpkg文件内容")
    
    print(f"创建测试gpkg目录: {test_dir}")
    return test_dir

def show_current_config():
    """显示当前配置"""
    settings = QSettings("CableTopoGenerator", "Settings")
    
    print("=" * 40)
    print("当前配置状态:")
    
    gpkg_dir = settings.value("last_gpkg_directory", "未设置")
    save_dir = settings.value("last_save_directory", "未设置")
    
    print(f"gpkg目录: {gpkg_dir}")
    print(f"保存目录: {save_dir}")
    print("=" * 40)

try:
    from cable_topo import TopologyGenerator
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        
        print("双目录配置功能测试启动！")
        print("=" * 50)
        
        # 显示当前配置
        show_current_config()
        
        # 创建测试目录
        test_gpkg_dir = create_test_gpkg_directory()
        
        print("=" * 50)
        print("新功能:")
        print("✓ 独立保存gpkg目录和文件保存目录")
        print("✓ 选择gpkg目录时记住位置")
        print("✓ 保存文件时记住位置")
        print("✓ 程序启动时自动恢复上次的gpkg目录")
        print("=" * 50)
        print("测试步骤:")
        print("1. 程序启动时会尝试恢复上次的gpkg目录")
        print("2. 点击'选择gpkg目录'，选择不同的目录")
        print("3. 生成拓扑文件，选择不同的保存目录")
        print("4. 关闭程序，重新打开验证目录记忆")
        print("=" * 50)
        print("配置管理命令:")
        print("python config_manager.py show")
        print("python config_manager.py set-gpkg <目录>")
        print("python config_manager.py set-save <目录>")
        print("=" * 50)
        
        window = TopologyGenerator()
        window.show()
        
        sys.exit(app.exec_())
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖都已安装")
except Exception as e:
    print(f"启动错误: {e}")