#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI测试脚本 - 测试新增的保存目录功能
"""

import sys
import os
from PyQt5.QtWidgets import QApplication

# 添加当前目录到路径，以便导入cable_topo
sys.path.insert(0, os.path.dirname(__file__))

try:
    from cable_topo import TopologyGenerator
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = TopologyGenerator()
        window.show()
        
        print("GUI测试启动成功！")
        print("新功能:")
        print("1. 生成完成后会自动打开保存目录")
        print("2. 在界面底部显示保存路径信息")
        print("3. 提供'打开保存目录'按钮")
        
        sys.exit(app.exec_())
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖都已安装")
except Exception as e:
    print(f"启动错误: {e}")