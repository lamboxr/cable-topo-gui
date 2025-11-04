#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的topo生成API集成
"""

import sys
import os
import tempfile
from PyQt5.QtWidgets import QApplication

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

# 模拟新的topo生成API
def mock_generate_topology_files(sro_config, box_config, cable_config, output_dir):
    """模拟新的generate_topology_files函数"""
    print("开始模拟新的拓扑生成...")
    print(f"SRO配置: {sro_config}")
    print(f"BOX配置: {box_config}")
    print(f"CABLE配置: {cable_config}")
    print(f"输出目录: {output_dir}")
    
    import time
    time.sleep(2)  # 模拟处理时间
    
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

try:
    from cable_topo import TopologyGenerator
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = TopologyGenerator()
        window.show()
        
        print("新API集成测试启动成功！")
        print("=" * 50)
        print("新API变化:")
        print("✓ 导入: from topo_generator import generate_topology_files")
        print("✓ 参数格式: (gpkg_path, layer_name) 元组")
        print("✓ 返回格式: {'code': 200, 'file_path': '...', 'msg': '...'}")
        print("✓ 错误处理: code 400/500 + error_message")
        print("=" * 50)
        print("测试步骤:")
        print("1. 选择包含gpkg文件的目录")
        print("2. 点击'生成拓扑'按钮")
        print("3. 观察控制台输出，应显示新的API调用格式")
        print("4. 验证成功消息显示")
        print("=" * 50)
        
        sys.exit(app.exec_())
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖都已安装")
    print("可能需要先安装新的topo-generator包:")
    print("pip install topo-generator")
except Exception as e:
    print(f"启动错误: {e}")