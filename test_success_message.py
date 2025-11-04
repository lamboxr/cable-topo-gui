#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试成功消息的脚本
"""

import sys
import os
import time
from PyQt5.QtWidgets import QApplication

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

# 模拟一个成功的gen_topos函数
def mock_gen_topos_success(gpkg_params, temp_dir):
    """模拟成功的拓扑生成函数"""
    print("开始模拟拓扑生成...")
    
    # 模拟处理时间
    for i in range(3):
        time.sleep(1)
        print(f"处理进度: {(i+1)*33}%")
    
    # 创建一个模拟的结果文件
    result_file = os.path.join(temp_dir, "test_topo_success.zip")
    with open(result_file, 'w') as f:
        f.write("模拟的拓扑文件内容")
    
    print("模拟拓扑生成成功完成")
    return {
        "code": 200,
        "file_path": result_file,
        "error_message": None
    }

# 模拟一个失败的gen_topos函数
def mock_gen_topos_failure(gpkg_params, temp_dir):
    """模拟失败的拓扑生成函数"""
    print("开始模拟拓扑生成...")
    
    # 模拟处理时间
    time.sleep(2)
    
    print("模拟拓扑生成失败")
    return {
        "code": 500,
        "file_path": None,
        "error_message": "模拟的生成失败错误"
    }

# 替换gen_topos函数进行测试
try:
    import topo_creator.topo_generator
    # 可以选择成功或失败的模拟
    topo_creator.topo_generator.gen_topos = mock_gen_topos_success
    print("已替换gen_topos函数为成功测试版本")
except ImportError:
    print("无法导入topo_creator，将创建模拟模块")
    
    # 创建模拟模块
    class MockTopoCreator:
        class topo_generator:
            @staticmethod
            def gen_topos(gpkg_params, temp_dir):
                return mock_gen_topos_success(gpkg_params, temp_dir)
    
    sys.modules['topo_creator'] = MockTopoCreator()
    sys.modules['topo_creator.topo_generator'] = MockTopoCreator.topo_generator()

try:
    from cable_topo import TopologyGenerator
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = TopologyGenerator()
        window.show()
        
        print("成功消息测试启动成功！")
        print("测试步骤:")
        print("1. 选择一个包含gpkg文件的目录")
        print("2. 点击'生成拓扑'按钮")
        print("3. 等待生成完成")
        print("4. 观察是否显示正确的成功消息")
        print("\n修复内容:")
        print("- 移除了cancel()方法中立即发出的canceled信号")
        print("- 分离了UI取消处理和线程取消信号处理")
        print("- 确保只有真正取消时才显示取消消息")
        
        sys.exit(app.exec_())
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖都已安装")
except Exception as e:
    print(f"启动错误: {e}")