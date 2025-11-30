#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理工具 - 查看和管理应用配置
"""

import sys
import os
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication

def show_current_settings():
    """显示当前配置"""
    settings = QSettings("CableTopoGenerator", "Settings")
    
    print("=" * 50)
    print("当前应用配置:")
    print("=" * 50)
    
    # 显示gpkg目录
    last_gpkg_dir = settings.value("last_gpkg_directory")
    if last_gpkg_dir:
        print(f"上次gpkg目录: {last_gpkg_dir}")
        print(f"gpkg目录是否存在: {'是' if os.path.exists(last_gpkg_dir) else '否'}")
        if os.path.exists(last_gpkg_dir):
            gpkg_files = [f for f in os.listdir(last_gpkg_dir) if f.lower().endswith('.gpkg')]
            print(f"gpkg文件数量: {len(gpkg_files)}")
    else:
        print("上次gpkg目录: 未设置")
    
    print()
    
    # 显示保存目录
    last_save_dir = settings.value("last_save_directory")
    if last_save_dir:
        print(f"上次保存目录: {last_save_dir}")
        print(f"保存目录是否存在: {'是' if os.path.exists(last_save_dir) else '否'}")
    else:
        print("上次保存目录: 未设置")
    
    print()
    
    # 显示窗口信息
    geometry = settings.value("geometry")
    window_state = settings.value("windowState")
    
    print(f"窗口几何信息: {'已保存' if geometry else '未保存'}")
    print(f"窗口状态信息: {'已保存' if window_state else '未保存'}")
    
    # 显示所有键
    print("\n所有配置键:")
    for key in settings.allKeys():
        value = settings.value(key)
        if isinstance(value, bytes):
            print(f"  {key}: <二进制数据 {len(value)} 字节>")
        else:
            print(f"  {key}: {value}")

def clear_settings():
    """清除所有配置"""
    settings = QSettings("CableTopoGenerator", "Settings")
    settings.clear()
    print("✓ 所有配置已清除")

def set_default_save_directory(directory):
    """设置默认保存目录"""
    if not os.path.exists(directory):
        print(f"× 目录不存在: {directory}")
        return False
    
    settings = QSettings("CableTopoGenerator", "Settings")
    settings.setValue("last_save_directory", directory)
    print(f"✓ 默认保存目录已设置为: {directory}")
    return True

def set_default_gpkg_directory(directory):
    """设置默认gpkg目录"""
    if not os.path.exists(directory):
        print(f"× 目录不存在: {directory}")
        return False
    
    settings = QSettings("CableTopoGenerator", "Settings")
    settings.setValue("last_gpkg_directory", directory)
    print(f"✓ 默认gpkg目录已设置为: {directory}")
    return True

def main():
    # 需要QApplication来使用QSettings
    app = QApplication(sys.argv)
    
    print("线缆拓扑图生成器 - 配置管理工具")
    
    if len(sys.argv) < 2:
        print("\n使用方法:")
        print("  python config_manager.py show              # 显示当前配置")
        print("  python config_manager.py clear             # 清除所有配置")
        print("  python config_manager.py set-save <目录>    # 设置默认保存目录")
        print("  python config_manager.py set-gpkg <目录>    # 设置默认gpkg目录")
        print("\n示例:")
        print("  python config_manager.py show")
        print("  python config_manager.py set-save C:\\Users\\用户名\\Documents")
        print("  python config_manager.py set-gpkg C:\\Users\\用户名\\gpkg_files")
        return
    
    command = sys.argv[1].lower()
    
    if command == "show":
        show_current_settings()
    elif command == "clear":
        clear_settings()
        print("重新显示配置:")
        show_current_settings()
    elif command == "set-save" and len(sys.argv) > 2:
        directory = sys.argv[2]
        if set_default_save_directory(directory):
            print("重新显示配置:")
            show_current_settings()
    elif command == "set-gpkg" and len(sys.argv) > 2:
        directory = sys.argv[2]
        if set_default_gpkg_directory(directory):
            print("重新显示配置:")
            show_current_settings()
    else:
        print("× 无效的命令")

if __name__ == "__main__":
    main()