#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试保存目录记忆功能
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

def check_saved_settings():
    """检查已保存的设置"""
    settings = QSettings("CableTopoGenerator", "Settings")
    last_dir = settings.value("last_save_directory", "未设置")
    print(f"当前保存的目录: {last_dir}")
    
    geometry = settings.value("geometry")
    window_state = settings.value("windowState")
    print(f"窗口几何信息: {'已保存' if geometry else '未保存'}")
    print(f"窗口状态信息: {'已保存' if window_state else '未保存'}")

try:
    from cable_topo import TopologyGenerator
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        
        print("保存目录记忆功能测试启动！")
        print("=" * 50)
        
        # 检查当前设置
        check_saved_settings()
        
        print("=" * 50)
        print("新功能:")
        print("✓ 记住上次保存的目录")
        print("✓ 下次打开时默认使用上次的目录")
        print("✓ 保存窗口位置和大小")
        print("✓ 使用QSettings持久化配置")
        print("=" * 50)
        print("测试步骤:")
        print("1. 选择包含gpkg文件的目录")
        print("2. 点击'生成拓扑'按钮")
        print("3. 在保存对话框中选择一个目录保存文件")
        print("4. 关闭程序")
        print("5. 重新运行程序，再次生成时应默认到上次的目录")
        print("=" * 50)
        
        window = TopologyGenerator()
        window.show()
        
        sys.exit(app.exec_())
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖都已安装")
except Exception as e:
    print(f"启动错误: {e}")