"""
PEACE项目GUI界面 - 优化版 (支持中文地质图)
"""
import sys
import os
import json
import logging
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QTextEdit, QComboBox, 
                            QProgressBar, QGroupBox, QSplitter, QMessageBox, QScrollArea,
                            QSizePolicy, QFrame, QGridLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMutex, QTimer
from PyQt6.QtGui import QPixmap, QFont, QTextCursor, QPalette, QColor, QLinearGradient, QBrush

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
        self.setWindowTitle("PEACE 地质图理解系统 - 专业版")
        self.setGeometry(100, 100, 1600, 1000)
        
        # 设置渐变背景
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, 
                                                 stop: 0 #e6f3ff, stop: 1 #ffffff);
            }
        """)
        
        self.current_image_path = ""
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 顶部标题区域
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, 
                                                 stop: 0 #4a90e2, stop: 1 #357abd);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        title_layout = QHBoxLayout(title_frame)
        
        # 标题
        title_label = QLabel("🔍 PEACE - 地质图智能分析系统")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white; font-weight: bold;")
        title_layout.addWidget(title_label)
        
        main_layout.addWidget(title_frame)
        
        # 副标题
        subtitle_label = QLabel("Empowering Geologic Map Holistic Understanding with MLLMs")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QFont("Microsoft YaHei", 11))
        subtitle_label.setStyleSheet("color: #555555; padding: 5px 0px;")
        main_layout.addWidget(subtitle_label)
        
        # 创建水平分割器 - 将界面分为左右两部分
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(10)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #4a90e2;
                border: 1px solid #357abd;
            }
        """)
        
        # 左侧：控制面板
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(15)
        
        # 1. 地质图上传区域
        upload_group = QGroupBox("📁 地质图上传")
        upload_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px 0 5px;
                background-color: #e6f3ff;
                color: #4a90e2;
                border-radius: 4px;
            }
        """)
        upload_layout = QVBoxLayout(upload_group)
        
        # 上传按钮和文件路径
        path_layout = QHBoxLayout()
        self.image_path_label = QLabel("请从下方选择地质图文件...")
        self.image_path_label.setWordWrap(True)
        self.image_path_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 11px;
                color: #666666;
            }
        """)
        path_layout.addWidget(self.image_path_label, 70)
        
        self.select_image_btn = QPushButton("📁 选择图片")
        self.select_image_btn.setFixedWidth(120)
        self.select_image_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 15px;
                text-align: center;
                font-size: 12px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.select_image_btn.clicked.connect(self.select_image)
        path_layout.addWidget(self.select_image_btn, 30)
        
        upload_layout.addLayout(path_layout)
        
        # 图像预览区域
        preview_frame = QFrame()
        preview_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: white;
            }
        """)
        preview_frame.setMinimumHeight(300)
        preview_layout = QVBoxLayout(preview_frame)
        
        self.image_preview_label = QLabel()
        self.image_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview_label.setMinimumSize(400, 280)
        self.image_preview_label.setMaximumHeight(280)
        self.image_preview_label.setStyleSheet("""
            QLabel {
                background-color: #f9f9f9;
                border: 1px dashed #cccccc;
                border-radius: 5px;
                color: #999999;
                font-size: 12px;
            }
        """)
        self.image_preview_label.setText("图像预览区域\n(支持 JPG, PNG, BMP, TIF 等格式)")
        preview_layout.addWidget(self.image_preview_label)
        
        upload_layout.addWidget(preview_frame)
        left_layout.addWidget(upload_group)
        
        # 2. 问题配置区域
        question_group = QGroupBox("❓ 问题配置")
        question_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px 0 5px;
                background-color: #e6f3ff;
                color: #4a90e2;
                border-radius: 4px;
            }
        """)
        question_layout = QVBoxLayout(question_group)
        
        # 问题类型选择
        type_label = QLabel("问题类型:")
        type_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #4a90e2;")
        question_layout.addWidget(type_label)
        
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
        self.question_type_combo.setMinimumHeight(35)
        self.question_type_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QComboBox:focus {
                border: 2px solid #4a90e2;
            }
        """)
        question_layout.addWidget(self.question_type_combo)
        
        # 问题输入区域
        question_text_label = QLabel("问题描述:")
        question_text_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #4a90e2; margin-top: 10px;")
        question_layout.addWidget(question_text_label)
        
        self.question_input = QTextEdit()
        self.question_input.setMaximumHeight(120)
        self.question_input.setMinimumHeight(80)
        self.question_input.setPlaceholderText("请输入您想了解的关于地质图的问题...")
        self.question_input.textChanged.connect(self.on_question_changed)  # 连接文本变化信号
        self.question_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
            QTextEdit:focus {
                border: 2px solid #4a90e2;
            }
        """)
        question_layout.addWidget(self.question_input)
        
        left_layout.addWidget(question_group)
        
        # 3. 操作控制区域
        control_group = QGroupBox("⚙️ 操作控制")
        control_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px 0 5px;
                background-color: #e6f3ff;
                color: #4a90e2;
                border-radius: 4px;
            }
        """)
        control_layout = QVBoxLayout(control_group)
        
        # 按钮布局
        btn_layout = QHBoxLayout()
        
        self.analyze_btn = QPushButton("🚀 开始分析")
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.analyze_btn.clicked.connect(self.start_analysis)
        btn_layout.addWidget(self.analyze_btn)
        
        self.clear_btn = QPushButton("🗑️ 清空")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                border: none;
                color: white;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_all)
        btn_layout.addWidget(self.clear_btn)
        
        control_layout.addLayout(btn_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # 未确定模式
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4a90e2;
                border-radius: 8px;
                background-color: #f0f8ff;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4a90e2;
                border-radius: 6px;
            }
        """)
        control_layout.addWidget(self.progress_bar)
        
        left_layout.addWidget(control_group)
        
        # 4. 处理日志区域
        log_group = QGroupBox("📋 处理日志")
        log_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px 0 5px;
                background-color: #e6f3ff;
                color: #4a90e2;
                border-radius: 4px;
            }
        """)
        log_layout = QVBoxLayout(log_group)
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(180)
        self.log_display.setMinimumHeight(150)
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 10px;
                padding: 8px;
            }
        """)
        log_layout.addWidget(self.log_display)
        
        left_layout.addWidget(log_group)
        
        # 添加左侧控制面板到分割器
        left_scroll = QScrollArea()
        left_scroll.setWidget(left_widget)
        left_scroll.setWidgetResizable(True)
        splitter.addWidget(left_scroll)
        
        # 右侧：结果展示和说明
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(15)
        
        # 1. 结果展示区域
        result_group = QGroupBox("📊 分析结果")
        result_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px 0 5px;
                background-color: #e6f3ff;
                color: #4a90e2;
                border-radius: 4px;
            }
        """)
        result_layout = QVBoxLayout(result_group)
        
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFont(QFont("Microsoft YaHei", 11))
        self.result_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 11px;
                padding: 10px;
            }
        """)
        self.result_display.setPlaceholderText("分析结果将显示在此处...")
        result_layout.addWidget(self.result_display)
        
        right_layout.addWidget(result_group)
        
        # 2. 使用说明区域
        info_group = QGroupBox("ℹ️ 使用说明")
        info_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px 0 5px;
                background-color: #e6f3ff;
                color: #4a90e2;
                border-radius: 4px;
            }
        """)
        info_layout = QVBoxLayout(info_group)
        
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(180)
        info_text.setMinimumHeight(150)
        info_text.setHtml("""
        <style>
            p { margin: 8px 0; line-height: 1.5; }
            ul { margin: 8px 0; padding-left: 20px; line-height: 1.6; }
            li { margin: 4px 0; }
            b { color: #4a90e2; }
        </style>
        <b>功能说明:</b>
        <ul>
            <li><b>选择地质图:</b> 点击"选择图片"按钮上传地质图文件</li>
            <li><b>问题类型:</b> 从下拉菜单选择适合的分析类型</li>
            <li><b>问题描述:</b> 输入您想了解的具体地质问题</li>
            <li><b>开始分析:</b> 点击"开始分析"执行AI推理</li>
            <li><b>查看结果:</b> 分析结果将在右侧结果区域显示</li>
        </ul>
        <b>注意事项:</b>
        <ul>
            <li>首次运行可能需要几分钟时间加载模型</li>
            <li>支持多种图像格式 (JPG, PNG, TIF, BMP等)</li>
            <li>处理过程中请耐心等待</li>
        </ul>
        """)
        info_text.setStyleSheet("""
            QTextEdit {
                background-color: #f9f9f9;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 11px;
            }
        """)
        info_layout.addWidget(info_text)
        
        right_layout.addWidget(info_group)
        
        # 3. 系统信息区域
        status_group = QGroupBox("📋 系统状态")
        status_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px 0 5px;
                background-color: #e6f3ff;
                color: #4a90e2;
                border-radius: 4px;
            }
        """)
        status_layout = QVBoxLayout(status_group)
        
        status_text = QTextEdit()
        status_text.setReadOnly(True)
        status_text.setMaximumHeight(100)
        status_text.setHtml("""
        <style>
            p { margin: 5px 0; line-height: 1.4; }
            span { color: #4CAF50; font-weight: bold; }
        </style>
        <p><b>API状态:</b> <span>已连接</span></p>
        <p><b>模型:</b> <span>qwen3-vl-plus</span></p>
        <p><b>模块:</b> <span>HIE, DKI, PEQA</span></p>
        <p><b>状态:</b> <span>就绪</span></p>
        """)
        status_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 11px;
            }
        """)
        status_layout.addWidget(status_text)
        
        right_layout.addWidget(status_group)
        
        # 添加右侧区域到分割器
        right_scroll = QScrollArea()
        right_scroll.setWidget(right_widget)
        right_scroll.setWidgetResizable(True)
        splitter.addWidget(right_scroll)
        
        # 设置分割器比例 (左侧40%，右侧60%)
        splitter.setSizes([640, 960])
        
        # 将分割器添加到主布局
        main_layout.addWidget(splitter)
        
        # 底部信息栏
        bottom_frame = QFrame()
        bottom_frame.setStyleSheet("""
            QFrame {
                background-color: #f0f8ff;
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        bottom_layout = QHBoxLayout(bottom_frame)
        
        info_label = QLabel("PEACE - 地质图智能分析系统 | 阿里云Qwen API | 专业地质分析工具")
        info_label.setStyleSheet("color: #555555; font-size: 10px;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        bottom_layout.addWidget(info_label)
        
        main_layout.addWidget(bottom_frame)
        
        # 初始化状态
        self.update_controls_state(False)
        
        self.log_message("✅ 系统已就绪。请选择地质图文件开始分析。")
    
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
            self.image_path_label.setText(f"📁 已选择: {os.path.basename(file_path)}")
            
            # 显示图像预览
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # 缩放图像以适应预览区域
                scaled_pixmap = pixmap.scaled(
                    self.image_preview_label.width() - 20,
                    self.image_preview_label.height() - 20,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_preview_label.setPixmap(scaled_pixmap)
            else:
                self.image_preview_label.setText("❌ 无法加载图像")
                self.image_preview_label.setStyleSheet("""
                    QLabel {
                        background-color: #fff5f5;
                        border: 1px dashed #ff6b6b;
                        border-radius: 5px;
                        color: #ff6b6b;
                        font-size: 12px;
                    }
                """)
            
            self.log_message(f"📁 选择地质图: {os.path.basename(file_path)}")
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
                    background-color: #4CAF50;
                    border: none;
                    color: white;
                    padding: 12px 20px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 8px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
        else:
            self.analyze_btn.setStyleSheet("""
                QPushButton {
                    background-color: #cccccc;
                    border: none;
                    color: white;
                    padding: 12px 20px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 8px;
                    min-height: 40px;
                }
            """)
    
    def start_analysis(self):
        """开始分析地质图"""
        if not self.current_image_path:
            QMessageBox.warning(self, "⚠️ 警告", "请先选择地质图文件！")
            return
            
        question = self.question_input.toPlainText().strip()
        if not question:
            QMessageBox.warning(self, "⚠️ 警告", "请输入问题！")
            return
        
        # 获取问题类型（去掉显示文本中的描述）
        question_type_text = self.question_type_combo.currentText()
        question_type = question_type_text.split(' ')[0]  # 取第一个部分
        if question_type == "custom":
            question_type = "analyzing-formation"  # 默认类型
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 设置为不确定模式
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #FF9800;
                border-radius: 8px;
                background-color: #fff8e1;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #FF9800;
                border-radius: 6px;
            }
        """)
        
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
        self.log_message(f"🚀 开始分析地质图: {os.path.basename(self.current_image_path)}")
        self.log_message(f"❓ 问题: {question}")
        self.log_message(f"🏷️ 问题类型: {question_type}")
        
        self.processing_thread.start()
        self.analyze_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
    
    def update_progress(self, message):
        """更新进度信息"""
        self.log_message(message)
    
    def show_result(self, result):
        """显示分析结果"""
        self.result_display.setPlainText(result)
        self.log_message("✅ 分析完成！")
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4a90e2;
                border-radius: 8px;
                background-color: #f0f8ff;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4a90e2;
                border-radius: 6px;
            }
        """)
        self.analyze_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        self.log_message("📋 处理完成，结果已显示。")
    
    def show_error(self, error_msg):
        """显示错误信息"""
        QMessageBox.critical(self, "❌ 错误", error_msg)
        self.log_message(f"❌ 错误: {error_msg}")
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4a90e2;
                border-radius: 8px;
                background-color: #f0f8ff;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4a90e2;
                border-radius: 6px;
            }
        """)
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
        self.image_path_label.setText("请从下方选择地质图文件...")
        self.image_preview_label.clear()
        self.image_preview_label.setText("图像预览区域\n(支持 JPG, PNG, BMP, TIF 等格式)")
        self.image_preview_label.setStyleSheet("""
            QLabel {
                background-color: #f9f9f9;
                border: 1px dashed #cccccc;
                border-radius: 5px;
                color: #999999;
                font-size: 12px;
            }
        """)
        self.question_input.clear()
        self.result_display.clear()
        self.log_display.clear()
        self.progress_bar.setVisible(False)
        self.update_controls_state(False)
        
        self.log_message("🗑️ 已清空所有内容")

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