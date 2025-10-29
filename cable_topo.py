import sys
import os
import sqlite3
import tempfile
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,
                             QMessageBox, QProgressDialog)
from PyQt5.QtCore import QThread, pyqtSignal
from topo_creator.topo_generator import gen_topos


class TopologyGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle("线缆拓扑图生成器")
        self.setGeometry(100, 100, 600, 200)

        # 创建主布局
        main_layout = QVBoxLayout()

        # 目录选择区域
        dir_layout = QHBoxLayout()
        self.dir_label = QLabel("未选择目录")
        self.select_btn = QPushButton("选择gpkg目录")
        self.select_btn.clicked.connect(self.select_directory)

        dir_layout.addWidget(QLabel("gpkg目录："))
        dir_layout.addWidget(self.dir_label, 1)
        dir_layout.addWidget(self.select_btn)

        # 生成按钮
        self.generate_btn = QPushButton("生成拓扑")
        self.generate_btn.clicked.connect(self.start_generation)
        self.generate_btn.setEnabled(False)  # 初始禁用

        # 添加到主布局
        main_layout.addLayout(dir_layout)
        main_layout.addWidget(self.generate_btn)
        main_layout.addStretch()

        # 设置中心部件
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def select_directory(self):
        """选择gpkg文件所在目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择gpkg目录")
        if dir_path:
            self.dir_label.setText(dir_path)
            self.generate_btn.setEnabled(True)

    def start_generation(self):
        """开始生成拓扑图（使用子线程）"""
        dir_path = self.dir_label.text()

        # 检查三个必要文件是否存在
        required_files = ["SRO.gpkg", "BOX.gpkg", "CABLE.gpkg"]
        missing_files = []

        for file in required_files:
            file_path = os.path.join(dir_path, file)
            if not os.path.exists(file_path):
                missing_files.append(file)

        if missing_files:
            QMessageBox.warning(self, "文件缺失",
                                f"缺少必要的文件：{', '.join(missing_files)}")
            return

        # 准备gpkg参数
        gpkg_params = {
            "SRO": {
                "gpkg_path": os.path.join(dir_path, "SRO.gpkg"),
                "layer_name": self.get_layer_name(os.path.join(dir_path, "SRO.gpkg"))
            },
            "BOX": {
                "gpkg_path": os.path.join(dir_path, "BOX.gpkg"),
                "layer_name": self.get_layer_name(os.path.join(dir_path, "BOX.gpkg"))
            },
            "CABLE": {
                "gpkg_path": os.path.join(dir_path, "CABLE.gpkg"),
                "layer_name": self.get_layer_name(os.path.join(dir_path, "CABLE.gpkg"))
            }
        }

        # 获取Windows临时目录
        temp_dir = tempfile.gettempdir()

        # 创建进度对话框
        self.progress = QProgressDialog("正在生成拓扑图...", "取消", 0, 100, self)
        self.progress.setWindowTitle("处理中")
        self.progress.setWindowModality(2)  # 模态窗口，阻止其他操作
        self.progress.setValue(10)

        # 创建并启动子线程
        self.worker = ProcessingThread(gpkg_params, temp_dir)
        self.worker.finished.connect(self.handle_result)
        self.worker.progress_updated.connect(self.update_progress)
        self.progress.canceled.connect(self.worker.cancel)
        self.worker.start()

        self.progress.setValue(20)

    def get_layer_name(self, gpkg_path):
        """从gpkg文件中获取图层名称"""
        try:
            conn = sqlite3.connect(gpkg_path)
            cursor = conn.cursor()

            # 查询图层名称（GeoPackage规范中的gpkg_contents表）
            cursor.execute("SELECT table_name FROM gpkg_contents")
            result = cursor.fetchone()

            conn.close()

            return result[0] if result else ""
        except Exception as e:
            QMessageBox.warning(self, "数据库错误", f"获取图层名称失败：{str(e)}")
            return ""

    def update_progress(self, value):
        """更新进度条"""
        self.progress.setValue(value)

    def handle_result(self, result):
        """处理线程返回的结果"""
        self.progress.close()

        if result["code"] == 200 and result["file_path"]:
            # 询问保存路径
            save_path, _ = QFileDialog.getSaveFileName(
                self, "保存拓扑图", result["file_path"], "*.zip"
            )

            if save_path:
                try:
                    # 复制文件到目标路径
                    import shutil
                    shutil.copy2(result["file_path"], save_path)
                    QMessageBox.information(self, "成功", f"文件已保存至：{save_path}")
                except Exception as e:
                    QMessageBox.error(self, "保存失败", f"无法保存文件：{str(e)}")
        elif result["code"] in [400, 500]:
            QMessageBox.error(self, "处理失败", result.get("error_message", "未知错误"))
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

    def run(self):
        """线程执行函数"""
        try:
            # 模拟进度更新
            self.progress_updated.emit(30)

            # 这里调用第三方函数（示例中使用模拟返回）
            # 实际使用时替换为真实的第三方函数调用
            self.progress_updated.emit(60)

            # 模拟处理时间
            import time
            time.sleep(2)

            if self.is_canceled:
                return

            self.progress_updated.emit(90)

            # 模拟第三方函数返回结果（200成功示例）
            # 可以根据测试需要修改返回的code
            temp_file = os.path.join(self.temp_dir, "topology_result.png")
            with open(temp_file, 'w') as f:
                f.write("模拟生成的拓扑图内容")

            result = gen_topos(self.gpkg_params, self.temp_dir)

            # 其他测试用例：
            # result = {"code": 400, "file_path": None, "error_message": "没有找到SRO信息"}
            # result = {"code": 500, "file_path": None, "error_message": "发生未知错误：测试错误"}

            self.finished.emit(result)

        except Exception as e:
            self.finished.emit({
                "code": 500,
                "file_path": None,
                "error_message": f"发生未知错误：{str(e)}"
            })

    def cancel(self):
        """取消处理"""
        self.is_canceled = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TopologyGenerator()
    window.show()
    sys.exit(app.exec_())