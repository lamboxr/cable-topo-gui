import sys
import os
import sqlite3
import tempfile
import shutil
import subprocess
import platform
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,
                             QMessageBox, QProgressDialog, QLineEdit,
                             QGroupBox, QComboBox)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
from topo_creator.topo_generator import gen_topos
# 在文件顶部确保正确导入
from PyQt5.QtWidgets import QMessageBox


class TopologyGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.last_save_path = None  # 记录最后保存的文件路径
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle("线缆拓扑图生成器 v0.1.0 @xurui FiberHome 2025. All Rights Reserved")
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
        layer_layout.addLayout(sro_layout)

        # BOX图层行
        box_layout = QHBoxLayout()
        box_layout.addWidget(QLabel("BOX.gpkg 图层："))
        self.box_combo = QComboBox()
        box_layout.addWidget(self.box_combo, 1)
        layer_layout.addLayout(box_layout)

        # CABLE图层行
        cable_layout = QHBoxLayout()
        cable_layout.addWidget(QLabel("CABLE.gpkg 图层："))
        self.cable_combo = QComboBox()
        cable_layout.addWidget(self.cable_combo, 1)
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

    def select_directory(self):
        """选择gpkg文件所在目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择gpkg目录")
        if dir_path:
            self.dir_edit.setText(dir_path)

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
                subprocess.run(['explorer', self.last_save_path])
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
            return

        # 检查并加载各个文件的图层
        sro_path = os.path.join(dir_path, "SRO.gpkg")
        box_path = os.path.join(dir_path, "BOX.gpkg")
        cable_path = os.path.join(dir_path, "CABLE.gpkg")

        sro_layers = self.get_all_layers(sro_path)
        box_layers = self.get_all_layers(box_path)
        cable_layers = self.get_all_layers(cable_path)

        # 填充下拉框
        self.sro_combo.addItems(sro_layers)
        self.box_combo.addItems(box_layers)
        self.cable_combo.addItems(cable_layers)

        # 只有当三个文件都有可用图层时才启用生成按钮
        if sro_layers and box_layers and cable_layers:
            self.generate_btn.setEnabled(True)
        else:
            self.generate_btn.setEnabled(False)

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
        dir_path = self.dir_edit.text()

        # 1. 校验目录是否存在
        if not dir_path:
            QMessageBox.warning(self, "输入错误", "请指定gpkg目录")
            return

        if not os.path.exists(dir_path):
            QMessageBox.warning(self, "目录不存在", f"指定的目录不存在：{dir_path}")
            return

        if not os.path.isdir(dir_path):
            QMessageBox.warning(self, "不是目录", f"指定的路径不是一个目录：{dir_path}")
            return

        # 2. 校验三个gpkg文件是否存在
        required_files = [
            ("SRO.gpkg", self.sro_combo),
            ("BOX.gpkg", self.box_combo),
            ("CABLE.gpkg", self.cable_combo)
        ]

        missing_files = []
        for file_name, combo in required_files:
            file_path = os.path.join(dir_path, file_name)
            if not os.path.exists(file_path):
                missing_files.append(file_name)
            elif combo.count() == 0:
                QMessageBox.warning(self, "图层错误", f"{file_name}中未找到可用图层")
                return

        if missing_files:
            QMessageBox.warning(self, "文件缺失",
                                f"目录下缺少必要的文件：{', '.join(missing_files)}")
            return

        # 3. 校验是否选择了图层
        if self.sro_combo.currentText() == "":
            QMessageBox.warning(self, "未选择图层", "请选择SRO.gpkg的图层")
            return

        if self.box_combo.currentText() == "":
            QMessageBox.warning(self, "未选择图层", "请选择BOX.gpkg的图层")
            return

        if self.cable_combo.currentText() == "":
            QMessageBox.warning(self, "未选择图层", "请选择CABLE.gpkg的图层")
            return

        # 4. 准备gpkg参数
        gpkg_params = {
            "SRO": {
                "gpkg_path": os.path.join(dir_path, "SRO.gpkg"),
                "layer_name": self.sro_combo.currentText()
            },
            "BOX": {
                "gpkg_path": os.path.join(dir_path, "BOX.gpkg"),
                "layer_name": self.box_combo.currentText()
            },
            "CABLE": {
                "gpkg_path": os.path.join(dir_path, "CABLE.gpkg"),
                "layer_name": self.cable_combo.currentText()
            }
        }

        sro_config = (os.path.join(dir_path, "SRO.gpkg"), self.sro_combo.currentText())
        box_config = (os.path.join(dir_path, "BOX.gpkg"), self.box_combo.currentText())
        cable_config = (os.path.join(dir_path, "CABLE.gpkg"), self.cable_combo.currentText())


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
        # 检查是否满足启用条件
        dir_path = self.dir_edit.text()
        if (dir_path and os.path.exists(dir_path) and 
            self.sro_combo.count() > 0 and 
            self.box_combo.count() > 0 and 
            self.cable_combo.count() > 0):
            self.generate_btn.setEnabled(True)
            print("生成按钮已重新启用")
        else:
            print("生成按钮未启用，条件不满足")

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
            # 询问保存路径
            save_path, _ = QFileDialog.getSaveFileName(
                self, "保存拓扑图", os.path.join(os.path.expanduser("~"), default_filename), "ZIP文件 (*.zip)"
            )

            if save_path:
                try:
                    # 确保保存路径有.zip扩展名
                    if not save_path.endswith('.zip'):
                        save_path += '.zip'
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

    def run(self):
        """线程执行函数"""
        try:
            # 更新进度：开始处理
            self.progress_updated.emit(20)

            if self.is_canceled:
                return

            # 调用第三方函数处理
            self.progress_updated.emit(40)
            
            # 在这里我们无法直接中断gen_topos函数，但可以检查取消状态
            if self.is_canceled:
                return
            
            # 由于gen_topos可能是一个长时间运行的函数，我们需要在调用前后检查取消状态
            print("开始调用gen_topos函数...")
            self.third_party_result = gen_topos(self.gpkg_params, self.temp_dir)
            print("gen_topos函数调用完成")

            if self.is_canceled:
                return

            # 处理完成
            self.progress_updated.emit(100)
            self.finished.emit(self.third_party_result)

        except Exception as e:
            if not self.is_canceled:
                self.finished.emit({
                    "code": 500,
                    "file_path": None,
                    "error_message": f"发生未知错误：{str(e)}"
                })

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TopologyGenerator()
    window.show()
    sys.exit(app.exec_())