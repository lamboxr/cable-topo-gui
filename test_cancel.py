#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
取消功能测试脚本
"""

import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

# 模拟一个长时间运行的gen_topos函数
def mock_gen_topos(gpkg_params, temp_dir):
    """模拟长时间运行的拓扑生成函数"""
    print("开始模拟拓扑生成...")
    
    # 模拟长时间处理
    for i in range(10):
        time.sleep(1)  # 每秒检查一次
        print(f"处理进度: {(i+1)*10}%")
        
        # 在实际应用中，这里应该检查线程的中断状态
        # 但由于我们无法修改gen_topos函数，所以这只是演示
    
    print("模拟拓扑生成完成")
    return {
        "code": 200,
        "file_path": os.path.join(temp_dir, "test_topo.zip"),
        "error_message": None
    }

# 临时替换gen_topos函数进行测试
try:
    import topo_creator.topo_generator
    topo_creator.topo_generator.gen_topos = mock_gen_topos
    print("已替换gen_topos函数为测试版本")
except ImportError:
    print("无法导入topo_creator，将创建模拟模块")
    
    # 创建模拟模块
    class MockTopoCreator:
        class topo_generator:
            @staticmethod
            def gen_topos(gpkg_params, temp_dir):
                return mock_gen_topos(gpkg_params, temp_dir)
    
    sys.modules['topo_creator'] = MockTopoCreator()
    sys.modules['topo_creator.topo_generator'] = MockTopoCreator.topo_generator()

try:
    from cable_topo import TopologyGenerator
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = TopologyGenerator()
        window.show()
        
        print("取消功能测试启动成功！")
        print("测试步骤:")
        print("1. 选择一个包含gpkg文件的目录")
        print("2. 点击'生成拓扑'按钮（按钮会变为禁用状态）")
        print("3. 在进度对话框中点击'取消'按钮")
        print("4. 观察按钮是否重新变为可用状态")
        print("\n改进的取消功能:")
        print("- 立即设置取消标志并发出信号")
        print("- 3秒后强制终止线程")
        print("- 显示取消确认消息")
        print("- 检查条件后重新启用生成按钮")
        print("- 添加调试输出显示按钮状态")
        
        sys.exit(app.exec_())
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖都已安装")
except Exception as e:
    print(f"启动错误: {e}")