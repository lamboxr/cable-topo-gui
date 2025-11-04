#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终验证测试脚本 - 测试成功和取消两种场景
"""

import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

# 模拟成功的gen_topos函数
def mock_gen_topos_success(gpkg_params, temp_dir):
    """模拟成功的拓扑生成函数"""
    print("开始模拟拓扑生成...")
    
    # 模拟处理时间
    time.sleep(3)  # 3秒，足够用户测试取消功能
    
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
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = TopologyGenerator()
        window.show()
        
        print("最终验证测试启动成功！")
        print("=" * 50)
        print("修复总结:")
        print("✓ 在关闭进度对话框前断开canceled信号连接")
        print("✓ 防止progress.close()触发canceled信号")
        print("✓ 使用user_canceled标志区分用户取消和正常完成")
        print("✓ 简化了信号处理逻辑")
        print("=" * 50)
        print("测试场景:")
        print("1. 成功场景：等待3秒完成，应显示'文件已保存至：xxx'")
        print("2. 取消场景：在3秒内点击取消，应显示'拓扑生成已被取消'")
        print("3. 按钮状态：无论成功还是取消，生成按钮都应重新启用")
        print("=" * 50)
        print("现在可以:")
        print("- 测试正常生成流程")
        print("- 测试取消功能")
        print("- 验证按钮状态恢复")
        print("- 验证保存目录功能")
        
        sys.exit(app.exec_())
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖都已安装")
except Exception as e:
    print(f"启动错误: {e}")