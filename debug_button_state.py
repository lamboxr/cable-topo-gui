#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试按钮状态的测试脚本
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import QTimer

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

try:
    from cable_topo import TopologyGenerator
    
    class DebugTopologyGenerator(TopologyGenerator):
        def __init__(self):
            super().__init__()
            # 添加调试按钮
            self.debug_btn = QPushButton("调试：检查按钮状态")
            self.debug_btn.clicked.connect(self.debug_button_state)
            
            # 将调试按钮添加到布局中
            layout = self.centralWidget().layout()
            layout.insertWidget(layout.count() - 1, self.debug_btn)  # 在stretch之前插入
            
            # 定时器检查按钮状态
            self.timer = QTimer()
            self.timer.timeout.connect(self.check_button_status)
            self.timer.start(1000)  # 每秒检查一次
        
        def debug_button_state(self):
            """调试按钮状态"""
            print("=== 按钮状态调试 ===")
            print(f"生成按钮启用状态: {self.generate_btn.isEnabled()}")
            print(f"目录路径: {self.dir_edit.text()}")
            print(f"SRO图层数量: {self.sro_combo.count()}")
            print(f"BOX图层数量: {self.box_combo.count()}")
            print(f"CABLE图层数量: {self.cable_combo.count()}")
            
            if hasattr(self, 'worker'):
                print(f"工作线程存在: True")
                print(f"工作线程运行中: {self.worker.isRunning()}")
            else:
                print(f"工作线程存在: False")
            
            print("==================")
        
        def check_button_status(self):
            """定时检查按钮状态"""
            if hasattr(self, '_last_button_state'):
                current_state = self.generate_btn.isEnabled()
                if current_state != self._last_button_state:
                    print(f"按钮状态变化: {self._last_button_state} -> {current_state}")
                    self._last_button_state = current_state
            else:
                self._last_button_state = self.generate_btn.isEnabled()
        
        def handle_cancel(self):
            """重写取消处理，添加调试信息"""
            print("=== 开始处理取消 ===")
            print(f"取消前按钮状态: {self.generate_btn.isEnabled()}")
            
            super().handle_cancel()
            
            print(f"取消后按钮状态: {self.generate_btn.isEnabled()}")
            print("=== 取消处理完成 ===")
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = DebugTopologyGenerator()
        window.show()
        
        print("调试版本启动成功！")
        print("功能:")
        print("1. 实时监控按钮状态变化")
        print("2. 点击'调试：检查按钮状态'查看详细信息")
        print("3. 测试取消功能时观察控制台输出")
        
        sys.exit(app.exec_())
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖都已安装")
except Exception as e:
    print(f"启动错误: {e}")