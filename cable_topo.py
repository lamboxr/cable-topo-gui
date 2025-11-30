import sys
import os
import sqlite3
import tempfile
import shutil
import subprocess
import platform
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,
                             QMessageBox, QProgressDialog, QLineEdit,
                             QGroupBox, QComboBox)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QSettings
from PyQt5.QtGui import QIcon
from topo_generator import generate_topology_files
# 在文件顶部确保正确导入
from PyQt5.QtWidgets import QMessageBox


class TopologyGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 初始化配置管理
        self.settings = QSettings("CableTopoGenerator", "Settings")
        
        # 记录最后保存的文件路径
        self.last_save_path = None
        
        # 从配置中读取两个独立的目录配置
        self.last_gpkg_directory = self.settings.value("last_gpkg_directory", os.path.expanduser("~"))
        self.last_save_directory = self.settings.value("last_save_directory", os.path.expanduser("~"))
        
        # 记录三个gpkg文件的实际路径
        self.sro_gpkg_path = None
        self.box_gpkg_path = None
        self.cable_gpkg_path = None
        
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle("线缆拓扑图生成器 v1.0.0 @xurui FiberHome 2025. All Rights Reserved")
        self.setGeometry(100, 100, 800, 280)
        
        # 设置窗口图标
        icon_path = os.path.join(os.path.dirname(__file__), "img", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # 创建主布局
        main_layout = QVBoxLayout()

        # 目录选择区域
        dir_layout = QHBoxLayout()
        self.dir_edit = QLineEdit()
        self.dir_edit.setPlaceholderText("请选择或输入gpkg目录路径")
        self.select_btn = QPushButton("选择gpkg目录")
        self.select_btn.clicked.connect(self.select_directory)

        dir_layout.addWidget(QLabel("gpkg目录："))
        dir_layout.addWidget(self.dir_edit, 1)
        dir_layout.addWidget(self.select_btn)

        # 图层明细分组
        self.layer_group = QGroupBox("图层明细")
        layer_layout = QVBoxLayout()

        # SRO图层行
        sro_layout = QHBoxLayout()
        sro_layout.addWidget(QLabel("SRO.gpkg 图层："))
        self.sro_combo = QComboBox()
        sro_layout.addWidget(self.sro_combo, 1)
        self.sro_file_btn = QPushButton("选择SRO文件")
        self.sro_file_btn.setMaximumWidth(120)
        self.sro_file_btn.clicked.connect(self.select_sro_file)
        sro_layout.addWidget(self.sro_file_btn)
        layer_layout.addLayout(sro_layout)

        # BOX图层行
        box_layout = QHBoxLayout()
        box_layout.addWidget(QLabel("BOX.gpkg 图层："))
        self.box_combo = QComboBox()
        box_layout.addWidget(self.box_combo, 1)
        self.box_file_btn = QPushButton("选择BOX文件")
        self.box_file_btn.setMaximumWidth(120)
        self.box_file_btn.clicked.connect(self.select_box_file)
        box_layout.addWidget(self.box_file_btn)
        layer_layout.addLayout(box_layout)

        # CABLE图层行
        cable_layout = QHBoxLayout()
        cable_layout.addWidget(QLabel("CABLE.gpkg 图层："))
        self.cable_combo = QComboBox()
        cable_layout.addWidget(self.cable_combo, 1)
        self.cable_file_btn = QPushButton("选择CABLE文件")
        self.cable_file_btn.setMaximumWidth(120)
        self.cable_file_btn.clicked.connect(self.select_cable_file)
        cable_layout.addWidget(self.cable_file_btn)
        layer_layout.addLayout(cable_layout)

        self.layer_group.setLayout(layer_layout)

        # 生成按钮
        self.generate_btn = QPushButton("生成拓扑")
        self.generate_btn.clicked.connect(self.start_generation)
        self.generate_btn.setEnabled(False)  # 初始禁用

        # 保存目录显示区域
        self.save_info_group = QGroupBox("保存信息")
        save_info_layout = QVBoxLayout()
        
        # 保存路径显示
        save_path_layout = QHBoxLayout()
        self.save_path_label = QLabel("保存目录：尚未保存文件")
        self.save_path_label.setStyleSheet("color: gray; font-size: 10pt;")
        self.open_dir_btn = QPushButton("打开保存的文件")
        self.open_dir_btn.clicked.connect(self.open_save_directory)
        self.open_dir_btn.setEnabled(False)  # 初始禁用
        self.open_dir_btn.setMaximumWidth(120)
        
        save_path_layout.addWidget(self.save_path_label, 1)
        save_path_layout.addWidget(self.open_dir_btn)
        save_info_layout.addLayout(save_path_layout)
        
        self.save_info_group.setLayout(save_info_layout)
        self.save_info_group.setVisible(False)  # 初始隐藏

        # 绑定目录编辑框变化事件
        self.dir_edit.textChanged.connect(self.on_dir_changed)
        
        # 恢复上次的gpkg目录
        self.restore_last_gpkg_directory()

        # 添加到主布局
        main_layout.addLayout(dir_layout)
        main_layout.addWidget(self.layer_group)
        main_layout.addWidget(self.generate_btn)
        main_layout.addWidget(self.save_info_group)
        main_layout.addStretch()

        # 设置中心部件
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # 设置窗口最小尺寸
        self.setMinimumSize(800, 280)
        
        # 恢复窗口位置和大小
        self.restore_window_state()

    def select_directory(self):
        """选择gpkg文件所在目录"""
        # 使用记住的gpkg目录作为起始位置
        dir_path = QFileDialog.getExistingDirectory(
            self, 
            "选择gpkg目录", 
            self.last_gpkg_directory
        )
        if dir_path:
            self.dir_edit.setText(dir_path)
            # 保存选择的gpkg目录到配置
            self.last_gpkg_directory = dir_path
            self.settings.setValue("last_gpkg_directory", dir_path)

    def open_save_directory(self):
        """打开保存文件的目录"""
        if not self.last_save_path or not os.path.exists(self.last_save_path):
            QMessageBox.warning(self, "文件不存在", "保存的文件不存在或已被删除")
            return
        
        # 获取文件所在目录
        save_dir = os.path.dirname(self.last_save_path)
        
        try:
            # 根据操作系统打开文件管理器
            system = platform.system()
            if system == "Windows":
                # Windows: 打开文件管理器并选中文件
                abs_path = os.path.abspath(save_dir)
                os.startfile(abs_path)
                # subprocess.run(['explorer', self.last_save_path])
            elif system == "Darwin":  # macOS
                subprocess.run(['open', '-R', self.last_save_path], check=True)
            else:  # Linux
                subprocess.run(['xdg-open', save_dir], check=True)
        except Exception as e:
            QMessageBox.warning(self, "打开失败", f"无法打开目录：{str(e)}")

    def update_save_info(self, save_path):
        """更新保存信息显示"""
        if save_path and os.path.exists(save_path):
            self.last_save_path = save_path
            # 显示保存路径（截断过长的路径）
            display_path = save_path
            if len(display_path) > 60:
                display_path = "..." + display_path[-57:]
            
            self.save_path_label.setText(f"保存目录：{display_path}")
            self.save_path_label.setStyleSheet("color: green; font-size: 10pt;")
            self.open_dir_btn.setEnabled(True)
            self.save_info_group.setVisible(True)
        else:
            self.save_path_label.setText("保存目录：尚未保存文件")
            self.save_path_label.setStyleSheet("color: gray; font-size: 10pt;")
            self.open_dir_btn.setEnabled(False)
            self.save_info_group.setVisible(False)

    def on_dir_changed(self):
        """目录路径变化时触发，更新图层信息"""
        dir_path = self.dir_edit.text()
        self.generate_btn.setEnabled(False)

        # 清空所有下拉框
        self.sro_combo.clear()
        self.box_combo.clear()
        self.cable_combo.clear()

        # 检查目录是否存在
        if not dir_path or not os.path.exists(dir_path):
            self.sro_gpkg_path = None
            self.box_gpkg_path = None
            self.cable_gpkg_path = None
            return

        # 检查并加载各个文件的图层（按固有规则自动读取）
        sro_path = os.path.join(dir_path, "SRO.gpkg")
        box_path = os.path.join(dir_path, "BOX.gpkg")
        cable_path = os.path.join(dir_path, "CABLE.gpkg")

        # 尝试加载SRO
        if os.path.exists(sro_path):
            self.sro_gpkg_path = sro_path
            sro_layers = self.get_all_layers(sro_path)
            self.sro_combo.addItems(sro_layers)
        else:
            self.sro_gpkg_path = None

        # 尝试加载BOX
        if os.path.exists(box_path):
            self.box_gpkg_path = box_path
            box_layers = self.get_all_layers(box_path)
            self.box_combo.addItems(box_layers)
        else:
            self.box_gpkg_path = None

        # 尝试加载CABLE
        if os.path.exists(cable_path):
            self.cable_gpkg_path = cable_path
            cable_layers = self.get_all_layers(cable_path)
            self.cable_combo.addItems(cable_layers)
        else:
            self.cable_gpkg_path = None

        # 检查是否可以启用生成按钮
        self.check_and_enable_generate_button()

    def select_sro_file(self):
        """选择SRO.gpkg文件"""
        start_dir = self.last_gpkg_directory if self.last_gpkg_directory else os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择SRO.gpkg文件", start_dir, "GeoPackage文件 (*.gpkg)"
        )
        if file_path:
            self.sro_gpkg_path = file_path
            self.sro_combo.clear()
            layers = self.get_all_layers(file_path)
            self.sro_combo.addItems(layers)
            self.check_and_enable_generate_button()

    def select_box_file(self):
        """选择BOX.gpkg文件"""
        start_dir = self.last_gpkg_directory if self.last_gpkg_directory else os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择BOX.gpkg文件", start_dir, "GeoPackage文件 (*.gpkg)"
        )
        if file_path:
            self.box_gpkg_path = file_path
            self.box_combo.clear()
            layers = self.get_all_layers(file_path)
            self.box_combo.addItems(layers)
            self.check_and_enable_generate_button()

    def select_cable_file(self):
        """选择CABLE.gpkg文件"""
        start_dir = self.last_gpkg_directory if self.last_gpkg_directory else os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择CABLE.gpkg文件", start_dir, "GeoPackage文件 (*.gpkg)"
        )
        if file_path:
            self.cable_gpkg_path = file_path
            self.cable_combo.clear()
            layers = self.get_all_layers(file_path)
            self.cable_combo.addItems(layers)
            self.check_and_enable_generate_button()

    def get_all_layers(self, gpkg_path):
        """从gpkg文件中获取所有图层名称"""
        layers = []
        if not os.path.exists(gpkg_path):
            return layers

        try:
            conn = sqlite3.connect(gpkg_path)
            cursor = conn.cursor()

            # 查询所有图层名称
            cursor.execute("SELECT table_name FROM gpkg_contents")
            results = cursor.fetchall()

            conn.close()

            # 提取图层名称
            layers = [result[0] for result in results if result[0]]
            return layers
        except Exception as e:
            QMessageBox.warning(self, "数据库错误",
                                f"读取{os.path.basename(gpkg_path)}图层失败：{str(e)}")
            return layers

    def start_generation(self):
        """开始生成拓扑图（使用子线程）"""
        # 1. 校验三个gpkg文件是否都已选择
        if not self.sro_gpkg_path or not os.path.exists(self.sro_gpkg_path):
            QMessageBox.warning(self, "文件缺失", "请选择SRO.gpkg文件")
            return

        if not self.box_gpkg_path or not os.path.exists(self.box_gpkg_path):
            QMessageBox.warning(self, "文件缺失", "请选择BOX.gpkg文件")
            return

        if not self.cable_gpkg_path or not os.path.exists(self.cable_gpkg_path):
            QMessageBox.warning(self, "文件缺失", "请选择CABLE.gpkg文件")
            return

        # 2. 校验是否选择了图层
        if self.sro_combo.currentText() == "":
            QMessageBox.warning(self, "未选择图层", "请选择SRO.gpkg的图层")
            return

        if self.box_combo.currentText() == "":
            QMessageBox.warning(self, "未选择图层", "请选择BOX.gpkg的图层")
            return

        if self.cable_combo.currentText() == "":
            QMessageBox.warning(self, "未选择图层", "请选择CABLE.gpkg的图层")
            return

        # 3. 准备gpkg参数
        gpkg_params = {
            "SRO": {
                "gpkg_path": self.sro_gpkg_path,
                "layer_name": self.sro_combo.currentText()
            },
            "BOX": {
                "gpkg_path": self.box_gpkg_path,
                "layer_name": self.box_combo.currentText()
            },
            "CABLE": {
                "gpkg_path": self.cable_gpkg_path,
                "layer_name": self.cable_combo.currentText()
            }
        }

        sro_config = (self.sro_gpkg_path, self.sro_combo.currentText())
        box_config = (self.box_gpkg_path, self.box_combo.currentText())
        cable_config = (self.cable_gpkg_path, self.cable_combo.currentText())


        # 5. 获取Windows临时目录
        temp_dir = tempfile.gettempdir()

        # 6. 禁用生成按钮，防止重复点击
        self.generate_btn.setEnabled(False)
        
        # 7. 创建进度对话框
        self.progress = QProgressDialog("正在生成拓扑图...", "取消", 0, 100, self)
        self.progress.setWindowTitle("处理中")
        self.progress.setWindowModality(2)  # 模态窗口，阻止其他操作
        self.progress.setValue(10)

        # 8. 创建并启动子线程
        self.worker = ProcessingThread(gpkg_params, temp_dir)
        self.worker.finished.connect(self.handle_result)
        self.worker.progress_updated.connect(self.update_progress)
        
        # 只连接进度对话框的取消信号，不连接线程的取消信号
        self.progress.canceled.connect(self.cancel_generation)
        
        # 添加标志来跟踪是否被用户取消
        self.user_canceled = False
        
        self.worker.start()

    def update_progress(self, value):
        """更新进度条"""
        if 0 <= value <= 100:  # 确保进度值在有效范围内
            self.progress.setValue(value)

    def cancel_generation(self):
        """取消生成操作"""
        print("用户请求取消生成...")
        
        # 设置用户取消标志
        self.user_canceled = True
        
        # 先断开进度对话框的信号连接，再关闭
        if hasattr(self, 'progress') and self.progress:
            try:
                self.progress.canceled.disconnect()  # 断开信号连接
            except:
                pass  # 如果已经断开或没有连接，忽略错误
            self.progress.close()
        
        # 取消线程
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.cancel()
            # 设置超时强制终止
            QTimer.singleShot(3000, self.force_terminate_worker)  # 3秒后强制终止
        
        # 重新启用生成按钮
        self.check_and_enable_generate_button()
        
        # 显示取消消息
        QMessageBox.information(self, "已取消", "拓扑生成已被取消")
        print("取消处理完成，按钮状态:", self.generate_btn.isEnabled())

    def force_terminate_worker(self):
        """强制终止工作线程"""
        if hasattr(self, 'worker') and self.worker.isRunning():
            print("强制终止工作线程...")
            self.worker.terminate()
            self.worker.wait(1000)  # 等待1秒
            if self.worker.isRunning():
                print("线程仍在运行，强制结束...")
                self.worker.quit()
            print("强制终止完成")

    def check_and_enable_generate_button(self):
        """检查并启用生成按钮"""
        # 检查是否满足启用条件：三个文件都已选择且都有可用图层
        if (self.sro_gpkg_path and os.path.exists(self.sro_gpkg_path) and self.sro_combo.count() > 0 and
            self.box_gpkg_path and os.path.exists(self.box_gpkg_path) and self.box_combo.count() > 0 and
            self.cable_gpkg_path and os.path.exists(self.cable_gpkg_path) and self.cable_combo.count() > 0):
            self.generate_btn.setEnabled(True)
            print("生成按钮已启用")
        else:
            self.generate_btn.setEnabled(False)
            print("生成按钮未启用，条件不满足")

    def save_window_state(self):
        """保存窗口状态"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        
    def restore_window_state(self):
        """恢复窗口状态"""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        window_state = self.settings.value("windowState")
        if window_state:
            self.restoreState(window_state)

    def restore_last_gpkg_directory(self):
        """恢复上次的gpkg目录"""
        if self.last_gpkg_directory and os.path.exists(self.last_gpkg_directory):
            # 检查目录中是否有gpkg文件
            gpkg_files = [f for f in os.listdir(self.last_gpkg_directory) 
                         if f.lower().endswith('.gpkg')]
            if gpkg_files:
                # 如果有gpkg文件，自动填入目录
                self.dir_edit.setText(self.last_gpkg_directory)
                print(f"恢复上次gpkg目录: {self.last_gpkg_directory}")
            else:
                print(f"上次gpkg目录中无gpkg文件: {self.last_gpkg_directory}")
        else:
            print("上次gpkg目录不存在或未设置")

    def closeEvent(self, event):
        """程序关闭时保存状态"""
        self.save_window_state()
        event.accept()

    def handle_result(self, result):
        """处理线程返回的结果"""
        print("处理线程结果...")
        
        # 如果用户已经取消，不处理结果
        if getattr(self, 'user_canceled', False):
            print("用户已取消，忽略结果")
            return
        
        # 先断开进度对话框的信号连接，再关闭
        if hasattr(self, 'progress') and self.progress:
            self.progress.canceled.disconnect()  # 断开信号连接
            self.progress.close()
        
        # 重新启用生成按钮
        self.check_and_enable_generate_button()

        if result["code"] == 200 and result["file_path"] and os.path.exists(result["file_path"]):
            # 获取默认文件名
            default_filename = os.path.basename(result["file_path"])
            
            # 使用记住的目录作为默认保存位置
            default_save_path = os.path.join(self.last_save_directory, default_filename)
            
            # 询问保存路径
            save_path, _ = QFileDialog.getSaveFileName(
                self, "保存拓扑图", default_save_path, "ZIP文件 (*.zip)"
            )

            if save_path:
                try:
                    # 确保保存路径有.zip扩展名
                    if not save_path.endswith('.zip'):
                        save_path += '.zip'
                    
                    # 保存当前选择的目录到配置
                    save_directory = os.path.dirname(save_path)
                    self.last_save_directory = save_directory
                    self.settings.setValue("last_save_directory", save_directory)
                    
                    # 复制文件到目标路径
                    shutil.copy2(result["file_path"], save_path)
                    
                    # 显示成功消息
                    QMessageBox.information(self, "成功", f"文件已保存至：{save_path}")
                    
                    # 更新保存信息显示
                    self.update_save_info(save_path)
                    
                    # 立即打开保存目录
                    self.open_save_directory()
                    
                except Exception as e:
                    QMessageBox.error(self, "保存失败", f"无法保存文件：{str(e)}")
        elif result["code"] in [400, 500]:
            QMessageBox.critical(self, "处理失败", result.get("error_message", "未知错误"))
        else:
            QMessageBox.warning(self, "未知结果", "处理返回了未知结果")


class ProcessingThread(QThread):
    """处理拓扑生成的子线程"""
    finished = pyqtSignal(dict)
    progress_updated = pyqtSignal(int)

    def __init__(self, gpkg_params, temp_dir):
        super().__init__()
        self.gpkg_params = gpkg_params
        self.temp_dir = temp_dir
        self.is_canceled = False
        self.third_party_result = None
        self.backup_dir = None  # 记录备份目录，用于清理

    def run(self):
        """线程执行函数"""
        backup_dir = None
        try:
            # 更新进度：开始处理
            self.progress_updated.emit(10)

            if self.is_canceled:
                return

            # 1. 创建带时间戳的备份目录
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            workspace_dir = os.getcwd()  # 获取工作目录
            tmp_base_dir = os.path.join(workspace_dir, "tmp")
            
            # 确保tmp目录存在
            if not os.path.exists(tmp_base_dir):
                os.makedirs(tmp_base_dir)
                print(f"创建tmp目录: {tmp_base_dir}")
            
            # 创建带时间戳的备份目录
            backup_dir = os.path.join(tmp_base_dir, f"backup_{timestamp}")
            os.makedirs(backup_dir)
            self.backup_dir = backup_dir
            print(f"创建备份目录: {backup_dir}")
            
            self.progress_updated.emit(15)
            
            if self.is_canceled:
                return

            # 2. 复制三个gpkg文件到备份目录
            print("开始复制gpkg文件到备份目录...")
            
            sro_original = self.gpkg_params["SRO"]["gpkg_path"]
            box_original = self.gpkg_params["BOX"]["gpkg_path"]
            cable_original = self.gpkg_params["CABLE"]["gpkg_path"]
            
            # 复制SRO文件
            sro_backup = os.path.join(backup_dir, "SRO.gpkg")
            shutil.copy2(sro_original, sro_backup)
            print(f"已备份: {sro_original} -> {sro_backup}")
            
            self.progress_updated.emit(20)
            
            if self.is_canceled:
                return
            
            # 复制BOX文件
            box_backup = os.path.join(backup_dir, "BOX.gpkg")
            shutil.copy2(box_original, box_backup)
            print(f"已备份: {box_original} -> {box_backup}")
            
            self.progress_updated.emit(25)
            
            if self.is_canceled:
                return
            
            # 复制CABLE文件
            cable_backup = os.path.join(backup_dir, "CABLE.gpkg")
            shutil.copy2(cable_original, cable_backup)
            print(f"已备份: {cable_original} -> {cable_backup}")
            
            self.progress_updated.emit(30)
            
            if self.is_canceled:
                return

            # 3. 准备使用备份文件的配置
            sro_config = (
                sro_backup, 
                self.gpkg_params["SRO"]["layer_name"]
            )
            box_config = (
                box_backup, 
                self.gpkg_params["BOX"]["layer_name"]
            )
            cable_config = (
                cable_backup, 
                self.gpkg_params["CABLE"]["layer_name"]
            )
            
            self.progress_updated.emit(40)
            
            if self.is_canceled:
                return
            
            print(f"开始调用generate_topology_files函数...")
            print(f"使用备份文件:")
            print(f"  SRO: {sro_backup}")
            print(f"  BOX: {box_backup}")
            print(f"  CABLE: {cable_backup}")
            
            # 4. 调用生成器API（使用备份文件）
            result = generate_topology_files(
                sro_config=sro_config,
                box_config=box_config,
                cable_config=cable_config,
                output_dir=self.temp_dir
            )
            
            print("generate_topology_files函数调用完成")

            if self.is_canceled:
                return

            # 5. 处理结果
            if result:
                if result.get('code') == 200:
                    self.third_party_result = {
                        "code": 200,
                        "file_path": result.get('file_path'),
                        "error_message": None,
                        "msg": result.get('msg', '生成成功'),
                        "backup_dir": backup_dir  # 传递备份目录信息
                    }
                elif result.get('code') in [400, 500]:
                    self.third_party_result = {
                        "code": result.get('code'),
                        "file_path": None,
                        "error_message": result.get('error_message', '生成失败'),
                        "backup_dir": backup_dir
                    }
                else:
                    self.third_party_result = {
                        "code": 500,
                        "file_path": None,
                        "error_message": "未知的返回结果",
                        "backup_dir": backup_dir
                    }
            else:
                self.third_party_result = {
                    "code": 500,
                    "file_path": None,
                    "error_message": "生成器返回空结果",
                    "backup_dir": backup_dir
                }

            # 处理完成
            self.progress_updated.emit(100)
            self.finished.emit(self.third_party_result)

        except Exception as e:
            if not self.is_canceled:
                self.finished.emit({
                    "code": 500,
                    "file_path": None,
                    "error_message": f"发生未知错误：{str(e)}",
                    "backup_dir": backup_dir
                })
        finally:
            # 6. 清理备份目录（可选：如果想保留备份用于调试，可以注释掉这部分）
            if backup_dir and os.path.exists(backup_dir):
                try:
                    shutil.rmtree(backup_dir)
                    print(f"已清理备份目录: {backup_dir}")
                except Exception as e:
                    print(f"清理备份目录失败: {str(e)}")

    def cancel(self):
        """取消处理"""
        print("设置取消标志...")
        self.is_canceled = True
        
        # 尝试优雅地退出线程
        if self.isRunning():
            print("请求线程退出...")
            self.requestInterruption()
            
            # 等待一小段时间让线程自然结束
            if not self.wait(1000):  # 等待1秒
                print("线程未能自然结束，将被强制终止")
                self.terminate()
                self.wait(1000)  # 等待终止完成
        
        # 清理备份目录
        if self.backup_dir and os.path.exists(self.backup_dir):
            try:
                shutil.rmtree(self.backup_dir)
                print(f"已清理备份目录: {self.backup_dir}")
            except Exception as e:
                print(f"清理备份目录失败: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TopologyGenerator()
    window.show()
    sys.exit(app.exec_())