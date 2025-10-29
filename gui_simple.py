"""
PEACE项目GUI界面 - 简洁版 (支持中文地质图)
"""
import sys
import os
import json
import logging
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QTextEdit, QComboBox, 
                            QProgressBar, QGroupBox, QSplitter, QMessageBox, QScrollArea,
                            QSizePolicy, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMutex
from PyQt6.QtGui import QPixmap, QFont, QTextCursor

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
logger = logging.getLogger(__name__)

class ProcessingThread(QThread):
    """处理线程，用于在后台执行地质图分析"""
    progress_signal = pyqtSignal(str)
    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, image_path, question, question_type, copilot_modes):
        super().__init__()
        self.image_path = image_path
        self.question = question
        self.question_type = question_type
        self.copilot_modes = copilot_modes
        self.mutex = QMutex()
    
    def run(self):
        try:
            self.progress_signal.emit("开始处理地质图...")
            
            # 延迟导入copilot以避免启动时的依赖问题
            try:
                from copilot import copilot
                self.progress_signal.emit("正在调用HIE模块进行信息提取...")
                answer = copilot(
                    self.image_path, 
                    self.question, 
                    self.question_type, 
                    self.copilot_modes
                )
                self.progress_signal.emit("处理完成！")
                self.result_signal.emit(str(answer))
            except Exception as e:
                self.error_signal.emit(f"导入copilot时出现错误: {str(e)}")
                logger.error(f"导入copilot时出现错误: {e}")
            
        except Exception as e:
            self.error_signal.emit(f"处理过程中出现错误: {str(e)}")
            logger.error(f"处理地质图时出现错误: {e}")

class GeoMapAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PEACE - 地质图智能分析系统")
        self.setGeometry(100, 100, 1400, 900)
        
        self.current_image_path = ""
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面 - 简洁布局：左侧功能，右侧结果"""
        # 主中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局 - 水平分割
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 左侧：图像和控制功能
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(10)
        
        # 标题
        title_label = QLabel("PEACE - 地质图智能分析系统")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; padding: 10px; border-bottom: 2px solid #3498db;")
        left_layout.addWidget(title_label)
        
        # 图像选择区域
        image_group = QGroupBox("图像选择")
        image_layout = QVBoxLayout(image_group)
        
        # 选择按钮
        self.select_image_btn = QPushButton("📁 选择地质图")
        self.select_image_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                font-size: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.select_image_btn.clicked.connect(self.select_image)
        image_layout.addWidget(self.select_image_btn)
        
        # 文件路径显示
        self.image_path_label = QLabel("请选择地质图文件...")
        self.image_path_label.setWordWrap(True)
        self.image_path_label.setStyleSheet("""
            QLabel {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                padding: 8px;
                font-size: 11px;
            }
        """)
        image_layout.addWidget(self.image_path_label)
        
        # 图像预览
        self.image_preview_label = QLabel()
        self.image_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview_label.setMinimumSize(400, 300)
        self.image_preview_label.setMaximumHeight(300)
        self.image_preview_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        self.image_preview_label.setText("图像预览区域\n(支持 JPG, PNG, BMP, TIF 等格式)")
        image_layout.addWidget(self.image_preview_label)
        
        left_layout.addWidget(image_group)
        
        # 问题配置区域
        question_group = QGroupBox("问题配置")
        question_layout = QVBoxLayout(question_group)
        
        # 问题类型
        question_type_layout = QHBoxLayout()
        question_type_layout.addWidget(QLabel("问题类型:"))
        self.question_type_combo = QComboBox()
        self.question_type_combo.addItems([
            "analyzing-formation (地层分析)",
            "extracting-sheet_name (提取图幅名称)",
            "extracting-scale (提取比例尺)",
            "extracting-lonlat (提取经纬度)",
            "analyzing-earthquake_risk (地震风险评估)",
            "reasoning-area_comparison (区域对比推理)",
            "reasoning-fault_existence (断层存在性推理)",
            "referring-rock_by_color (根据颜色指代岩石)",
            "grounding-title_by_name (定位标题)",
            "grounding-main_map_by_name (定位主图)",
            "custom (自定义)"
        ])
        question_type_layout.addWidget(self.question_type_combo)
        question_layout.addLayout(question_type_layout)
        
        # 问题输入
        question_layout.addWidget(QLabel("问题:"))
        self.question_input = QTextEdit()
        self.question_input.setMaximumHeight(80)
        self.question_input.setPlaceholderText("请输入您想了解的关于地质图的问题...")
        self.question_input.textChanged.connect(self.on_question_changed)
        question_layout.addWidget(self.question_input)
        
        left_layout.addWidget(question_group)
        
        # 控制按钮区域
        control_group = QGroupBox("控制")
        control_layout = QVBoxLayout(control_group)
        
        # 按钮行
        btn_row = QHBoxLayout()
        self.analyze_btn = QPushButton("🔍 开始分析")
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.analyze_btn.clicked.connect(self.start_analysis)
        btn_row.addWidget(self.analyze_btn)
        
        self.clear_btn = QPushButton("🗑️ 清空")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 5px;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_all)
        btn_row.addWidget(self.clear_btn)
        
        control_layout.addLayout(btn_row)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3498db;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 4px;
            }
        """)
        control_layout.addWidget(self.progress_bar)
        
        left_layout.addWidget(control_group)
        
        # 日志区域
        log_group = QGroupBox("处理日志")
        log_layout = QVBoxLayout(log_group)
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(150)
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 3px;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        log_layout.addWidget(self.log_display)
        
        left_layout.addWidget(log_group)
        
        # 添加左侧到主布局
        left_scroll = QScrollArea()
        left_scroll.setWidget(left_widget)
        left_scroll.setWidgetResizable(True)
        main_layout.addWidget(left_scroll, 40)  # 占40%宽度
        
        # 右侧：结果展示
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(10)
        
        # 右侧标题
        right_title = QLabel("分析结果")
        right_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_title.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        right_title.setStyleSheet("color: #2c3e50; padding: 10px; border-bottom: 2px solid #3498db;")
        right_layout.addWidget(right_title)
        
        # 结果显示区域
        result_group = QGroupBox("结果")
        result_layout = QVBoxLayout(result_group)
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFont(QFont("Microsoft YaHei", 11))
        self.result_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 11px;
            }
        """)
        self.result_display.setPlaceholderText("分析结果将显示在此处...")
        result_layout.addWidget(self.result_display)
        
        right_layout.addWidget(result_group)
        
        # 使用说明
        info_group = QGroupBox("使用说明")
        info_layout = QVBoxLayout(info_group)
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(150)
        info_text.setHtml("""
        <p><b>使用步骤:</b></p>
        <ol>
            <li>点击"选择地质图"按钮上传图像</li>
            <li>选择问题类型或输入自定义问题</li>
            <li>点击"开始分析"执行AI推理</li>
            <li>查看右侧分析结果</li>
        </ol>
        <p><b>注意:</b> 首次运行可能需要几分钟加载模型</p>
        """)
        info_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 3px;
                font-size: 10px;
            }
        """)
        info_layout.addWidget(info_text)
        
        right_layout.addWidget(info_group)
        
        # 添加右侧到主布局
        right_scroll = QScrollArea()
        right_scroll.setWidget(right_widget)
        right_scroll.setWidgetResizable(True)
        main_layout.addWidget(right_scroll, 60)  # 占60%宽度
        
        # 初始化状态
        self.update_controls_state(False)
        self.log_message("系统已就绪。请选择地质图文件开始分析。")
    
    def on_question_changed(self):
        """当问题文本改变时更新按钮状态"""
        self.update_controls_state(
            bool(self.current_image_path) and 
            bool(self.question_input.toPlainText().strip())
        )
    
    def select_image(self):
        """选择地质图文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择地质图文件",
            "",
            "图像文件 (*.jpg *.jpeg *.png *.bmp *.tiff *.tif);;所有文件 (*)"
        )
        
        if file_path:
            self.current_image_path = file_path
            self.image_path_label.setText(f"已选择: {os.path.basename(file_path)}")
            
            # 显示图像预览
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.image_preview_label.width() - 20,
                    self.image_preview_label.height() - 20,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_preview_label.setPixmap(scaled_pixmap)
            else:
                self.image_preview_label.setText("无法加载图像")
            
            self.log_message(f"选择文件: {os.path.basename(file_path)}")
            self.update_controls_state(
                bool(self.current_image_path) and 
                bool(self.question_input.toPlainText().strip())
            )
    
    def update_controls_state(self, has_image_and_question):
        """更新控件状态"""
        self.analyze_btn.setEnabled(has_image_and_question)
        
        if has_image_and_question:
            self.analyze_btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    padding: 10px;
                    font-size: 12px;
                    font-weight: bold;
                    border-radius: 5px;
                }
            """)
        else:
            self.analyze_btn.setStyleSheet("""
                QPushButton {
                    background-color: #95a5a6;
                    color: white;
                    border: none;
                    padding: 10px;
                    font-size: 12px;
                    font-weight: bold;
                    border-radius: 5px;
                }
            """)
    
    def start_analysis(self):
        """开始分析地质图"""
        if not self.current_image_path:
            QMessageBox.warning(self, "警告", "请先选择地质图文件！")
            return
            
        question = self.question_input.toPlainText().strip()
        if not question:
            QMessageBox.warning(self, "警告", "请输入问题！")
            return
        
        # 获取问题类型
        question_type_text = self.question_type_combo.currentText()
        question_type = question_type_text.split(' ')[0]  # 取第一个部分
        if question_type == "custom":
            question_type = "analyzing-formation"  # 默认类型
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        
        # 创建处理线程
        self.processing_thread = ProcessingThread(
            self.current_image_path,
            question,
            question_type,
            ["HIE", "DKI", "PEQA"]
        )
        
        # 连接信号
        self.processing_thread.progress_signal.connect(self.update_progress)
        self.processing_thread.result_signal.connect(self.show_result)
        self.processing_thread.error_signal.connect(self.show_error)
        
        # 开始处理
        self.log_message(f"开始分析地质图: {os.path.basename(self.current_image_path)}")
        self.log_message(f"问题: {question}")
        self.log_message(f"问题类型: {question_type}")
        
        self.processing_thread.start()
        self.analyze_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
    
    def update_progress(self, message):
        """更新进度信息"""
        self.log_message(message)
    
    def show_result(self, result):
        """显示分析结果"""
        self.result_display.setPlainText(result)
        self.log_message("分析完成！")
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self.log_message("处理完成，结果已显示。")
    
    def show_error(self, error_msg):
        """显示错误信息"""
        QMessageBox.critical(self, "错误", error_msg)
        self.log_message(f"错误: {error_msg}")
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
    
    def log_message(self, message):
        """记录日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        current_text = self.log_display.toPlainText()
        if current_text:
            self.log_display.setPlainText(current_text + "\n" + log_entry)
        else:
            self.log_display.setPlainText(log_entry)
        # 滚动到底部
        cursor = self.log_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_display.setTextCursor(cursor)
    
    def clear_all(self):
        """清空所有内容"""
        self.current_image_path = ""
        self.image_path_label.setText("请选择地质图文件...")
        self.image_preview_label.clear()
        self.image_preview_label.setText("图像预览区域\n(支持 JPG, PNG, BMP, TIF 等格式)")
        self.question_input.clear()
        self.result_display.clear()
        self.log_display.clear()
        self.progress_bar.setVisible(False)
        self.update_controls_state(False)
        
        self.log_message("已清空所有内容")

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PEACE 地质图理解系统")
    
    # 设置应用支持中文
    app.setFont(QFont("Microsoft YaHei", 9))
    
    window = GeoMapAnalyzerGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()