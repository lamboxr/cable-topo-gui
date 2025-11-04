#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
断开信号连接修复测试脚本
"""

import sys
import os
import time
from PyQt5.QtWidgets import QApplication

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

# 模拟成功的gen_topos函数
def mock_gen_topos_success(gpkg_params, temp_dir):
    """模拟成功的拓扑生成函数"""
    print("开始模拟拓扑生成...")
    
    # 模拟处理时间
    time.sleep(2)
    
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

# 替换gen_topos函数进行测试
try:
    import topo_creator.topo_generator
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
    
    class TestTopologyGenerator(TopologyGenerator):
        def handle_result(self, result):
            print("=== handle_result 开始 ===")
            print(f"user_canceled = {getattr(self, 'user_canceled', 'undefined')}")
            super().handle_result(result)
            print("=== handle_result 结束 ===")
        
        def cancel_generation(self):
            print("=== cancel_generation 开始 ===")
            super().cancel_generation()
            print("=== cancel_generation 结束 ===")
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = TestTopologyGenerator()
        window.show()
        
        print("断开信号连接修复测试启动成功！")
        print("修复内容:")
        print("1. 在关闭进度对话框前先断开canceled信号连接")
        print("2. 防止progress.close()触发canceled信号")
        print("3. 在取消方法中也断开信号连接")
        print("\n测试步骤:")
        print("1. 选择包含gpkg文件的目录")
        print("2. 点击'生成拓扑'按钮")
        print("3. 等待生成完成")
        print("4. 观察控制台输出，应该不会出现'用户请求取消生成...'")
        print("5. 应该显示成功消息而不是取消消息")
        
        sys.exit(app.exec_())
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖都已安装")
except Exception as e:
    print(f"启动错误: {e}")