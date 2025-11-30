#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始配置设置脚本
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QSettings

def setup_gpkg_directory():
    """设置gpkg目录"""
    app = QApplication(sys.argv)
    
    msg = QMessageBox()
    msg.setWindowTitle("设置gpkg目录")
    msg.setText("请选择包含gpkg文件的目录")
    msg.setInformativeText("这个目录应该包含SRO.gpkg、BOX.gpkg、CABLE.gpkg文件")
    msg.exec_()
    
    directory = QFileDialog.getExistingDirectory(None, "选择gpkg目录")
    
    if directory:
        # 检查目录中是否有gpkg文件
        gpkg_files = [f for f in os.listdir(directory) if f.lower().endswith('.gpkg')]
        
        if gpkg_files:
            settings = QSettings("CableTopoGenerator", "Settings")
            settings.setValue("last_gpkg_directory", directory)
            
            print(f"✓ gpkg目录已设置为: {directory}")
            print(f"  发现的gpkg文件: {', '.join(gpkg_files)}")
            return directory
        else:
            print(f"× 选择的目录中没有gpkg文件: {directory}")
            return None
    else:
        print("× 未选择目录")
        return None

def setup_save_directory():
    """设置保存目录"""
    app = QApplication(sys.argv)
    
    msg = QMessageBox()
    msg.setWindowTitle("设置保存目录")
    msg.setText("请选择生成文件的默认保存目录")
    msg.setInformativeText("生成的拓扑文件将默认保存到这个目录")
    msg.exec_()
    
    directory = QFileDialog.getExistingDirectory(None, "选择保存目录")
    
    if directory:
        settings = QSettings("CableTopoGenerator", "Settings")
        settings.setValue("last_save_directory", directory)
        
        print(f"✓ 保存目录已设置为: {directory}")
        return directory
    else:
        print("× 未选择目录")
        return None

def main():
    print("线缆拓扑图生成器 - 初始配置设置")
    print("=" * 50)
    
    settings = QSettings("CableTopoGenerator", "Settings")
    
    # 检查当前配置
    current_gpkg = settings.value("last_gpkg_directory")
    current_save = settings.value("last_save_directory")
    
    print("当前配置:")
    print(f"  gpkg目录: {current_gpkg if current_gpkg else '未设置'}")
    print(f"  保存目录: {current_save if current_save else '未设置'}")
    print()
    
    # 设置gpkg目录
    print("1. 设置gpkg目录...")
    gpkg_dir = setup_gpkg_directory()
    
    if gpkg_dir:
        print()
        # 设置保存目录
        print("2. 设置保存目录...")
        save_dir = setup_save_directory()
        
        if save_dir:
            print()
            print("=" * 50)
            print("✓ 配置设置完成！")
            print("=" * 50)
            print("最终配置:")
            print(f"  gpkg目录: {gpkg_dir}")
            print(f"  保存目录: {save_dir}")
            print()
            print("现在可以运行主程序:")
            print("  python cable_topo.py")
        else:
            print("× 保存目录设置失败")
    else:
        print("× gpkg目录设置失败")

if __name__ == "__main__":
    main()