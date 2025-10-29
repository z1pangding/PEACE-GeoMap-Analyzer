"""
PEACE项目GUI界面 - 优化打包版
保留完整功能但移除不必要的依赖以减小EXE文件大小
"""
import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QTextEdit, QComboBox, 
                            QProgressBar, QGroupBox, QSplitter, QMessageBox, QScrollArea,
                            QMenuBar, QDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt6.QtGui import QPixmap, QFont, QTextCursor
import re
import os

def detect_question_type(question):
    """智能检测问题类型"""
    question_lower = question.lower()
    
    # 提取类问题关键词
    extracting_keywords = {
        'extracting-sheet_name': ['标题', '图幅', '名称', 'title', 'name', 'sheet'],
        'extracting-scale': ['比例尺', 'scale', '比例'],
        'extracting-lonlat': ['经纬度', '坐标', 'longitude', 'latitude', 'lon', 'lat'],
        'extracting-index_map': ['索引', 'index', '位置图']
    }
    
    # 分析类问题关键词
    analyzing_keywords = {
        'analyzing-formation': ['地层', '构造', '岩层', 'formation', 'stratum', '地质'],
        'analyzing-earthquake_risk': ['地震', 'earthquake', '风险', 'risk', '活动']
    }
    
    # 推理类问题关键词
    reasoning_keywords = {
        'reasoning-area_comparison': ['比较', '对比', '差异', 'compare', 'difference'],
        'reasoning-fault_existence': ['断层', 'fault', '断裂', '存在'],
        'reasoning-lithology_composition': ['岩性', '岩石', 'lithology', '成分']
    }
    
    # 指代类问题关键词
    referring_keywords = {
        'referring-rock_by_color': ['颜色', 'colour', '什么颜色', '哪种颜色', '岩石颜色']
    }
    
    # 定位类问题关键词
    grounding_keywords = {
        'grounding-title_by_name': ['标题位置', 'title location', '标题在哪'],
        'grounding-main_map_by_name': ['主图', 'main map', '主体地图'],
        'grounding-scale_by_name': ['比例尺位置', 'scale location'],
        'grounding-legend_by_name': ['图例', 'legend', '图例位置']
    }
    
    # 检测逻辑
    all_keywords = {
        **extracting_keywords,
        **analyzing_keywords, 
        **reasoning_keywords,
        **referring_keywords,
        **grounding_keywords
    }
    
    scores = {}
    for q_type, keywords in all_keywords.items():
        score = 0
        for keyword in keywords:
            if keyword in question_lower:
                score += 1
        scores[q_type] = score
    
    # 返回得分最高的问题类型
    if max(scores.values()) == 0:
        # 如果没有匹配到任何关键词，返回通用分析类型
        return "analyzing-formation"
    
    return max(scores, key=scores.get)

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
    
    def run(self):
        try:
            self.progress_signal.emit("🚀 开始处理地质图分析...")
            
            # 延迟导入copilot以避免启动时的依赖问题
            try:
                from copilot import copilot
                
                # 定义进度回调函数
                def progress_callback(message):
                    self.progress_signal.emit(message)
                
                self.progress_signal.emit("🎯 正在调用分析引擎...")
                answer = copilot(
                    self.image_path, 
                    self.question, 
                    self.question_type, 
                    self.copilot_modes,
                    progress_callback
                )
                self.progress_signal.emit("🎉 分析完成！结果已生成")
                self.result_signal.emit(str(answer))
            except Exception as e:
                self.error_signal.emit(f"处理错误: {str(e)}")
            
        except Exception as e:
            self.error_signal.emit(f"处理错误: {str(e)}")

class APIConfigDialog(QDialog):
    """API配置对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔑 API配置")
        self.setModal(True)
        self.setFixedSize(450, 250)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("🔑 阿里通义千问API配置")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # API密钥输入
        key_layout = QVBoxLayout()
        key_layout.addWidget(QLabel("API密钥:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        key_layout.addWidget(self.api_key_input)
        layout.addLayout(key_layout)
        
        # 模型选择
        model_layout = QVBoxLayout()
        model_layout.addWidget(QLabel("模型:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "qwen-vl-max",
            "qwen3-vl-plus", 
            "qwen-vl-plus"
        ])
        model_layout.addWidget(self.model_combo)
        layout.addLayout(model_layout)
        
        # 说明
        info_label = QLabel("获取API密钥：阿里云控制台 → 通义千问 → API-KEY管理")
        info_label.setStyleSheet("color: #6c757d; font-size: 10px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 按钮
        button_layout = QHBoxLayout()
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(self.save_config)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # 加载配置
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        settings = QSettings("PEACE", "APIConfig")
        api_key = settings.value("api_key", "")
        model = settings.value("model", "qwen3-vl-plus")
        
        self.api_key_input.setText(api_key)
        index = self.model_combo.findText(model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
    
    def save_config(self):
        """保存配置"""
        api_key = self.api_key_input.text().strip()
        model = self.model_combo.currentText()
        
        if not api_key:
            QMessageBox.warning(self, "警告", "请输入API密钥！")
            return
        
        if not api_key.startswith("sk-"):
            QMessageBox.warning(self, "警告", "API密钥格式不正确！")
            return
        
        # 保存到设置
        settings = QSettings("PEACE", "APIConfig")
        settings.setValue("api_key", api_key)
        settings.setValue("model", model)
        
        # 更新文件
        try:
            api_file = os.path.join(os.path.dirname(__file__), "utils", "api.py")
            with open(api_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            content = re.sub(r'api_key = ".*?"', f'api_key = "{api_key}"', content)
            content = re.sub(r'model_name = ".*?"', f'model_name = "{model}"', content)
            
            with open(api_file, "w", encoding="utf-8") as f:
                f.write(content)
            
            QMessageBox.information(self, "成功", "API配置已保存！")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败：{str(e)}")

class GeoMapAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PEACE 地质图分析")
        self.setGeometry(100, 100, 1200, 700)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: #e0e0e0;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                font-size: 12px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
            }
            QLabel {
                font-size: 11px;
            }
            QProgressBar {
                border: 1px solid #007ACC;
                border-radius: 5px;
                text-align: center;
                font-size: 10px;
            }
            QProgressBar::chunk {
                background-color: #007ACC;
                border-radius: 5px;
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
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建水平分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(5)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #bdc3c7;
                border: 1px solid #95a5a6;
            }
        """)
        main_layout.addWidget(splitter)
        
        # 左侧：控制面板
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        control_layout.setSpacing(10)
        
        # 图像选择组
        image_group = QGroupBox("地质图上传")
        image_group.setStyleSheet("QGroupBox { font-size: 12px; }")
        image_layout = QVBoxLayout(image_group)
        
        # 图像选择行
        image_row = QHBoxLayout()
        self.image_path_label = QLabel("请选择地质图文件...")
        self.image_path_label.setWordWrap(True)
        self.image_path_label.setStyleSheet("background-color: white; border: 1px solid #cccccc; padding: 8px; border-radius: 4px;")
        self.image_path_label.setMinimumHeight(40)
        image_row.addWidget(self.image_path_label, 70)
        
        self.select_image_btn = QPushButton("📁 选择图片")
        self.select_image_btn.setFixedWidth(120)
        self.select_image_btn.clicked.connect(self.select_image)
        image_row.addWidget(self.select_image_btn, 30)
        
        image_layout.addLayout(image_row)
        
        # 图像预览
        self.image_preview_label = QLabel()
        self.image_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview_label.setMinimumSize(300, 200)
        self.image_preview_label.setMaximumHeight(250)
        self.image_preview_label.setStyleSheet("background-color: white; border: 1px solid #cccccc; padding: 8px; border-radius: 4px;")
        self.image_preview_label.setText("图像预览")
        image_layout.addWidget(self.image_preview_label)
        
        control_layout.addWidget(image_group)
        
        # API配置组
        api_config_group = QGroupBox("API配置")
        api_config_layout = QVBoxLayout(api_config_group)
        
        # API状态显示
        api_status_row = QHBoxLayout()
        self.api_status_label = QLabel("🔑 API状态: 未配置")
        self.api_status_label.setStyleSheet("QLabel { font-size: 11px; color: #dc3545; }")
        api_status_row.addWidget(self.api_status_label, 70)
        
        self.api_config_btn = QPushButton("⚙️ 配置API")
        self.api_config_btn.setFixedWidth(100)
        self.api_config_btn.clicked.connect(self.show_api_config_dialog)
        api_status_row.addWidget(self.api_config_btn, 30)
        
        api_config_layout.addLayout(api_status_row)
        control_layout.addWidget(api_config_group)
        
        # 更新API状态显示
        self.update_api_status()
        
        # 问题设置组
        question_group = QGroupBox("问题配置")
        question_group.setStyleSheet("QGroupBox { font-size: 12px; }")
        question_layout = QVBoxLayout(question_group)
        
        # 问题类型选择
        type_row = QHBoxLayout()
        type_label = QLabel("问题类型:")
        type_label.setStyleSheet("QLabel { font-size: 11px; }")
        type_row.addWidget(type_label, 20)
        self.question_type_combo = QComboBox()
        self.question_type_combo.addItems([
            "auto-detect (🤖 自动检测问题类型)",
            "analyzing-formation (地层分析)",
            "extracting-sheet_name (提取图幅名称)",
            "extracting-scale (提取比例尺)",
            "extracting-lonlat (提取经纬度)",
            "analyzing-earthquake_risk (地震风险评估)",
            "reasoning-area_comparison (区域对比推理)",
            "reasoning-fault_existence (断层存在性推理)",
            "referring-rock_by_color (根据颜色指代岩石)",
            "grounding-title_by_name (定位标题)",
            "grounding-main_map_by_name (定位主图)"
        ])
        self.question_type_combo.setMinimumHeight(30)
        self.question_type_combo.currentTextChanged.connect(self.on_question_type_changed)
        type_row.addWidget(self.question_type_combo, 80)
        question_layout.addLayout(type_row)
        
        # 智能提示标签
        self.type_hint_label = QLabel("💡 选择'自动检测'让系统智能识别您的问题类型")
        self.type_hint_label.setStyleSheet("QLabel { font-size: 10px; color: #6c757d; font-style: italic; }")
        self.type_hint_label.setWordWrap(True)
        question_layout.addWidget(self.type_hint_label)
        
        # 问题输入区域
        question_layout.addWidget(QLabel("问题描述:"))
        self.question_input = QTextEdit()
        self.question_input.setMaximumHeight(100)
        self.question_input.setMinimumHeight(80)
        self.question_input.setPlaceholderText(
            "请输入您想了解的关于地质图的问题...\n\n"
            "💡 提示：选择'自动检测问题类型'可以让系统自动识别您的问题类型，无需手动选择！"
        )
        self.question_input.textChanged.connect(self.on_question_changed)  # 连接文本变化信号
        question_layout.addWidget(self.question_input)
        
        control_layout.addWidget(question_group)
        
        # 控制按钮区域
        button_group = QGroupBox("操作控制")
        button_layout = QVBoxLayout(button_group)
        
        # 按钮行
        btn_row = QHBoxLayout()
        self.analyze_btn = QPushButton("🔍 开始分析")
        self.analyze_btn.setStyleSheet("QPushButton { font-size: 14px; padding: 12px; }")
        self.analyze_btn.clicked.connect(self.start_analysis)
        btn_row.addWidget(self.analyze_btn)
        
        self.clear_btn = QPushButton("🗑️ 清空")
        self.clear_btn.clicked.connect(self.clear_all)
        btn_row.addWidget(self.clear_btn)
        
        button_layout.addLayout(btn_row)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # 未确定模式
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #007ACC;
                border-radius: 8px;
                background-color: #f0f0f0;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #007ACC;
                border-radius: 6px;
            }
        """)
        button_layout.addWidget(self.progress_bar)
        
        control_layout.addWidget(button_group)
        
        # 添加控制面板到分割器
        control_scroll = QScrollArea()
        control_scroll.setWidget(control_widget)
        control_scroll.setWidgetResizable(True)
        control_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        splitter.addWidget(control_scroll)
        
        # 右侧：结果展示
        result_widget = QWidget()
        result_layout = QVBoxLayout(result_widget)
        result_layout.setSpacing(10)
        
        # 结果组
        result_group = QGroupBox("分析结果")
        result_group.setStyleSheet("QGroupBox { font-size: 12px; }")
        result_group_layout = QVBoxLayout(result_group)
        
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFont(QFont("Microsoft YaHei", 10))
        self.result_display.setStyleSheet("background-color: white; font-family: Consolas, 'Courier New', monospace; padding: 10px;")
        self.result_display.setPlaceholderText("分析结果将显示在此处...")
        result_group_layout.addWidget(self.result_display)
        
        result_layout.addWidget(result_group)
        
        # 模块状态指示器
        status_group = QGroupBox("模块状态")
        status_group.setStyleSheet("QGroupBox { font-size: 12px; }")
        status_layout = QHBoxLayout(status_group)
        
        # HIE状态
        hie_widget = QWidget()
        hie_layout = QVBoxLayout(hie_widget)
        hie_layout.setContentsMargins(5, 5, 5, 5)
        self.hie_status = QLabel("📊 HIE")
        self.hie_status.setStyleSheet("QLabel { font-size: 10px; font-weight: bold; color: #6c757d; }")
        self.hie_progress = QProgressBar()
        self.hie_progress.setRange(0, 100)
        self.hie_progress.setValue(0)
        self.hie_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ced4da;
                border-radius: 3px;
                text-align: center;
                font-size: 8px;
                height: 12px;
            }
            QProgressBar::chunk {
                background-color: #6c757d;
                border-radius: 2px;
            }
        """)
        hie_layout.addWidget(self.hie_status)
        hie_layout.addWidget(self.hie_progress)
        status_layout.addWidget(hie_widget)
        
        # DKI状态
        dki_widget = QWidget()
        dki_layout = QVBoxLayout(dki_widget)
        dki_layout.setContentsMargins(5, 5, 5, 5)
        self.dki_status = QLabel("🧠 DKI")
        self.dki_status.setStyleSheet("QLabel { font-size: 10px; font-weight: bold; color: #6c757d; }")
        self.dki_progress = QProgressBar()
        self.dki_progress.setRange(0, 100)
        self.dki_progress.setValue(0)
        self.dki_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ced4da;
                border-radius: 3px;
                text-align: center;
                font-size: 8px;
                height: 12px;
            }
            QProgressBar::chunk {
                background-color: #6c757d;
                border-radius: 2px;
            }
        """)
        dki_layout.addWidget(self.dki_status)
        dki_layout.addWidget(self.dki_progress)
        status_layout.addWidget(dki_widget)
        
        # PEQA状态
        peqa_widget = QWidget()
        peqa_layout = QVBoxLayout(peqa_widget)
        peqa_layout.setContentsMargins(5, 5, 5, 5)
        self.peqa_status = QLabel("🤖 PEQA")
        self.peqa_status.setStyleSheet("QLabel { font-size: 10px; font-weight: bold; color: #6c757d; }")
        self.peqa_progress = QProgressBar()
        self.peqa_progress.setRange(0, 100)
        self.peqa_progress.setValue(0)
        self.peqa_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ced4da;
                border-radius: 3px;
                text-align: center;
                font-size: 8px;
                height: 12px;
            }
            QProgressBar::chunk {
                background-color: #6c757d;
                border-radius: 2px;
            }
        """)
        peqa_layout.addWidget(self.peqa_status)
        peqa_layout.addWidget(self.peqa_progress)
        status_layout.addWidget(peqa_widget)
        
        result_layout.addWidget(status_group)
        
        # 进度日志组
        progress_group = QGroupBox("详细日志")
        progress_group.setStyleSheet("QGroupBox { font-size: 12px; }")
        progress_group_layout = QVBoxLayout(progress_group)
        
        self.progress_display = QTextEdit()
        self.progress_display.setReadOnly(True)
        self.progress_display.setMaximumHeight(180)
        self.progress_display.setMinimumHeight(120)
        self.progress_display.setFont(QFont("Microsoft YaHei", 11))
        self.progress_display.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Microsoft YaHei', sans-serif;
                font-size: 11px;
                color: #495057;
                line-height: 1.4;
            }
        """)
        self.progress_display.setPlaceholderText("详细处理日志将在此显示...")
        progress_group_layout.addWidget(self.progress_display)
        
        result_layout.addWidget(progress_group)
        
        # 添加结果区域到分割器
        result_scroll = QScrollArea()
        result_scroll.setWidget(result_widget)
        result_scroll.setWidgetResizable(True)
        result_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        splitter.addWidget(result_scroll)
        
        # 设置分割器比例 (左侧45%，右侧55%)
        splitter.setSizes([540, 660])
        
        # 初始化状态
        self.update_controls_state(False)
        
    def on_question_changed(self):
        """当问题文本改变时更新按钮状态"""
        self.update_controls_state(
            bool(self.current_image_path) and 
            bool(self.question_input.toPlainText().strip())
        )
    
    def on_question_type_changed(self, text):
        """当问题类型改变时更新提示"""
        if "auto-detect" in text:
            self.type_hint_label.setText("🤖 系统将根据您的问题内容自动选择最合适的分析类型")
            self.type_hint_label.setStyleSheet("QLabel { font-size: 10px; color: #007bff; font-style: italic; }")
        else:
            self.type_hint_label.setText("💡 您已手动指定问题类型，系统将按此类型进行分析")
            self.type_hint_label.setStyleSheet("QLabel { font-size: 10px; color: #6c757d; font-style: italic; }")
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 设置菜单
        settings_menu = menubar.addMenu('设置')
        
        # API配置动作
        api_config_action = settings_menu.addAction('API配置')
        api_config_action.triggered.connect(self.show_api_config_dialog)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        # 关于动作
        about_action = help_menu.addAction('关于')
        about_action.triggered.connect(self.show_about)
    
    def show_api_config_dialog(self):
        """显示API配置对话框"""
        dialog = APIConfigDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.update_api_status()
            QMessageBox.information(self, "成功", "API配置已更新！")
    
    def show_about(self):
        """显示关于信息"""
        about_text = """PEACE - 地质图智能分析系统

项目基于微软研究院PEACE项目二次开发
原项目地址: https://github.com/microsoft/PEACE

二次开发单位: 浙江省水文地质工程地质大队（浙江省宁波地质院）
二次开发人: 基础地质调查研究中心-丁正鹏
邮箱: zhengpengding@outlook.com

@article{huang2025peace,
  title={PEACE: Empowering Geologic Map Holistic Understanding with MLLMs},
  author={Huang, Yangyu and Gao, Tianyi and Xu, Haoran and Zhao, Qihao and Song, Yang and Gui, Zhipeng and Lv, Tengchao and Chen, Hao and Cui, Lei and Li, Scarlett and others},
  journal={arXiv preprint arXiv:2501.06184},
  year={2025}
}

基于多模态大语言模型的地质图理解工具
支持图片上传、问题分析、结果展示等功能

版本: 1.0
技术支持: 阿里通义千问"""
        QMessageBox.about(self, "关于 PEACE", about_text)
    
    def update_api_status(self):
        """更新API状态显示"""
        settings = QSettings("PEACE", "APIConfig")
        api_key = settings.value("api_key", "")
        model = settings.value("model", "")
        
        if api_key:
            # 显示API密钥的前几位和后几位
            masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else api_key
            self.api_status_label.setText(f"🔑 API状态: 已配置 ({masked_key})")
            self.api_status_label.setStyleSheet("QLabel { font-size: 11px; color: #28a745; }")
        else:
            self.api_status_label.setText("🔑 API状态: 未配置")
            self.api_status_label.setStyleSheet("QLabel { font-size: 11px; color: #dc3545; }")
    
    def check_api_config(self):
        """检查API配置"""
        settings = QSettings("PEACE", "APIConfig")
        api_key = settings.value("api_key", "")
        
        if not api_key:
            # 如果没有API配置，显示配置对话框
            QMessageBox.information(self, "首次使用", 
                                   "欢迎使用PEACE地质图分析系统！\n\n"
                                   "首次使用需要配置阿里通义千问API密钥。")
            self.show_api_config_dialog()
    
    def select_image(self):
        """选择地质图文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择地质图文件",
            "",
            "图像文件 (*.jpg *.jpeg *.png *.bmp *.tiff *.tif);;所有文件 (*)"
        )
        
        if file_path:
            # 检查文件大小
            file_size = os.path.getsize(file_path)
            max_size = 50 * 1024 * 1024  # 50MB limit (增加到50MB以支持更大的地质图文件)
            
            if file_size > max_size:
                QMessageBox.warning(
                    self, 
                    "文件过大", 
                    f"选择的图像文件太大 ({file_size/1024/1024:.1f}MB)。\n"
                    f"请使用小于50MB的图像文件。\n\n"
                    "建议：\n"
                    "• 使用图像编辑软件压缩文件\n"
                    "• 选择分辨率较低的图像\n"
                    "• 裁剪图像到主要区域"
                )
                return
            
            self.current_image_path = file_path
            self.image_path_label.setText(f"已选择: {os.path.basename(file_path)} ({file_size/1024/1024:.1f}MB)")
            
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
                self.image_preview_label.setText("无法加载图像")
            
            self.update_controls_state(
                bool(self.current_image_path) and 
                bool(self.question_input.toPlainText().strip())
            )
    
    def update_controls_state(self, has_image_and_question):
        """更新控件状态"""
        self.analyze_btn.setEnabled(has_image_and_question)
        if has_image_and_question:
            self.analyze_btn.setStyleSheet("QPushButton { background-color: #4CAF50; font-size: 14px; padding: 12px; }")
        else:
            self.analyze_btn.setStyleSheet("QPushButton { background-color: #cccccc; font-size: 14px; padding: 12px; }")
    
    def start_analysis(self):
        """开始分析地质图"""
        if not self.current_image_path:
            QMessageBox.warning(self, "警告", "请先选择地质图文件！")
            return
            
        question = self.question_input.toPlainText().strip()
        if not question:
            QMessageBox.warning(self, "警告", "请输入问题！")
            return
        
        # 获取问题类型（去掉显示文本中的描述）
        question_type_text = self.question_type_combo.currentText()
        question_type = question_type_text.split(' ')[0]  # 取第一个部分
        if question_type == "auto-detect":
            # 智能检测问题类型
            self.update_progress("🤖 [智能检测] 正在分析问题类型...")
            question_type = detect_question_type(question)
            type_mapping = {
                'extracting-sheet_name': '提取图幅名称',
                'extracting-scale': '提取比例尺', 
                'extracting-lonlat': '提取经纬度',
                'analyzing-formation': '地层分析',
                'analyzing-earthquake_risk': '地震风险评估',
                'reasoning-area_comparison': '区域对比推理',
                'reasoning-fault_existence': '断层存在性推理',
                'referring-rock_by_color': '根据颜色指代岩石',
                'grounding-title_by_name': '定位标题',
                'grounding-main_map_by_name': '定位主图'
            }
            detected_type_name = type_mapping.get(question_type, '通用分析')
            self.update_progress(f"🤖 [智能检测] 检测到问题类型: {detected_type_name}")
        
        # 重置模块状态
        self.reset_module_status()
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 设置为不确定模式
        
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
        self.processing_thread.start()
        self.analyze_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
    
    def update_progress(self, message):
        """更新进度信息"""
        # 添加时间戳
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        # 更新模块状态
        if "[HIE]" in message:
            if "开始" in message or "加载图像" in message:
                self.hie_status.setText("📊 HIE (运行中)")
                self.hie_status.setStyleSheet("QLabel { font-size: 10px; font-weight: bold; color: #007bff; }")
                self.hie_progress.setValue(10)
            elif "检查缓存" in message:
                self.hie_progress.setValue(20)
            elif "初始化" in message:
                self.hie_progress.setValue(30)
            elif "分析地图布局" in message:
                self.hie_progress.setValue(40)
            elif "裁剪和保存" in message:
                self.hie_progress.setValue(50)
            elif "提取图例" in message:
                self.hie_progress.setValue(60)
            elif "匹配岩石" in message:
                self.hie_progress.setValue(70)
            elif "提取基本信息" in message:
                self.hie_progress.setValue(80)
            elif "岩石区域" in message or "保存数字化" in message:
                self.hie_progress.setValue(90)
            elif "提取完成" in message:
                self.hie_status.setText("✅ HIE (完成)")
                self.hie_status.setStyleSheet("QLabel { font-size: 10px; font-weight: bold; color: #28a745; }")
                self.hie_progress.setValue(100)
                self.hie_progress.setStyleSheet("""
                    QProgressBar::chunk {
                        background-color: #28a745;
                        border-radius: 2px;
                    }
                """)
                    
        elif "[DKI]" in message:
            if "检查知识库" in message:
                self.dki_status.setText("🧠 DKI (运行中)")
                self.dki_status.setStyleSheet("QLabel { font-size: 10px; font-weight: bold; color: #007bff; }")
                self.dki_progress.setValue(10)
            elif "解析经纬度" in message:
                self.dki_progress.setValue(25)
            elif "获取地震学" in message:
                self.dki_progress.setValue(45)
            elif "获取地理学" in message:
                self.dki_progress.setValue(60)
            elif "整合知识库" in message:
                self.dki_progress.setValue(75)
            elif "保存知识库" in message:
                self.dki_progress.setValue(85)
            elif "选择相关知识" in message:
                self.dki_progress.setValue(90)
            elif "注入完成" in message:
                self.dki_status.setText("✅ DKI (完成)")
                self.dki_status.setStyleSheet("QLabel { font-size: 10px; font-weight: bold; color: #28a745; }")
                self.dki_progress.setValue(100)
                self.dki_progress.setStyleSheet("""
                    QProgressBar::chunk {
                        background-color: #28a745;
                        border-radius: 2px;
                    }
                """)
                    
        elif "[PEQA]" in message:
            if "开始构建" in message:
                self.peqa_status.setText("🤖 PEQA (运行中)")
                self.peqa_status.setStyleSheet("QLabel { font-size: 10px; font-weight: bold; color: #007bff; }")
                self.peqa_progress.setValue(10)
            elif "处理地图信息" in message:
                self.peqa_progress.setValue(20)
            elif "注入领域知识" in message:
                self.peqa_progress.setValue(35)
            elif "选择相关组件" in message:
                self.peqa_progress.setValue(45)
            elif "准备图像组件" in message:
                self.peqa_progress.setValue(60)
            elif "构建提示词" in message:
                self.peqa_progress.setValue(75)
            elif "调用大语言模型" in message:
                self.peqa_progress.setValue(85)
            elif "问答处理完成" in message:
                self.peqa_status.setText("✅ PEQA (完成)")
                self.peqa_status.setStyleSheet("QLabel { font-size: 10px; font-weight: bold; color: #28a745; }")
                self.peqa_progress.setValue(100)
                self.peqa_progress.setStyleSheet("""
                    QProgressBar::chunk {
                        background-color: #28a745;
                        border-radius: 2px;
                    }
                """)
        
        # 获取当前文本
        current_text = self.progress_display.toPlainText()
        if current_text:
            new_text = current_text + "\n" + formatted_message
        else:
            new_text = formatted_message
        
        self.progress_display.setPlainText(new_text)
        
        # 滚动到底部
        cursor = self.progress_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.progress_display.setTextCursor(cursor)
        
        # 强制更新界面
        QApplication.processEvents()
    
    def reset_module_status(self):
        """重置所有模块状态"""
        # 重置HIE
        self.hie_status.setText("📊 HIE")
        self.hie_status.setStyleSheet("QLabel { font-size: 10px; font-weight: bold; color: #6c757d; }")
        self.hie_progress.setValue(0)
        self.hie_progress.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #6c757d;
                border-radius: 2px;
            }
        """)
        
        # 重置DKI
        self.dki_status.setText("🧠 DKI")
        self.dki_status.setStyleSheet("QLabel { font-size: 10px; font-weight: bold; color: #6c757d; }")
        self.dki_progress.setValue(0)
        self.dki_progress.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #6c757d;
                border-radius: 2px;
            }
        """)
        
        # 重置PEQA
        self.peqa_status.setText("🤖 PEQA")
        self.peqa_status.setStyleSheet("QLabel { font-size: 10px; font-weight: bold; color: #6c757d; }")
        self.peqa_progress.setValue(0)
        self.peqa_progress.setStyleSheet("""
            QProgressBar::chunk {
                background-color: #6c757d;
                border-radius: 2px;
            }
        """)
    
    def show_result(self, result):
        """显示分析结果"""
        formatted_result = self.format_result_display(result)
        self.result_display.setHtml(formatted_result)
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        
        # 添加完成信息到进度日志
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        completion_message = f"[{timestamp}] ✅ 所有处理已完成"
        current_text = self.progress_display.toPlainText()
        if current_text:
            new_text = current_text + "\n" + completion_message
        else:
            new_text = completion_message
        self.progress_display.setPlainText(new_text)
    
    def format_result_display(self, result):
        """格式化分析结果显示，使用Markdown风格"""
        if not result:
            return "<p style='color: #6c757d; font-style: italic;'>暂无分析结果</p>"
        
        # 尝试解析JSON格式
        try:
            import json
            if result.strip().startswith('{') and result.strip().endswith('}'):
                data = json.loads(result)
                return self.format_json_result(data)
        except:
            pass
        
        # 如果不是JSON，使用文本格式化
        return self.format_text_result(result)
    
    def format_json_result(self, data):
        """格式化JSON结果"""
        html = "<div style='font-family: Microsoft YaHei; line-height: 1.6;'>"
        
        # 处理answer字段
        if 'answer' in data:
            html += "<div style='margin-bottom: 15px;'>"
            html += "<h3 style='color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px;'>🎯 分析结果</h3>"
            answer = data['answer']
            if isinstance(answer, list):
                html += "<ul style='margin: 10px 0; padding-left: 20px;'>"
                for item in answer:
                    html += f"<li style='margin: 5px 0; color: #2c3e50;'>• {item}</li>"
                html += "</ul>"
            else:
                html += f"<p style='background-color: #e8f4f8; padding: 12px; border-radius: 5px; border-left: 4px solid #3498db; margin: 10px 0; font-size: 14px; color: #2c3e50;'>{answer}</p>"
            html += "</div>"
        
        # 处理reason字段
        if 'reason' in data:
            html += "<div style='margin-bottom: 15px;'>"
            html += "<h3 style='color: #27ae60; border-bottom: 2px solid #27ae60; padding-bottom: 5px;'>📋 分析过程</h3>"
            reason = data['reason']
            # 将reason按分号或句号分段
            sentences = [s.strip() for s in reason.replace(';', '。').split('。') if s.strip()]
            html += "<ol style='margin: 10px 0; padding-left: 20px;'>"
            for i, sentence in enumerate(sentences, 1):
                html += f"<li style='margin: 8px 0; color: #34495e;'><strong>步骤 {i}:</strong> {sentence}</li>"
            html += "</ol>"
            html += "</div>"
        
        # 处理其他字段
        for key, value in data.items():
            if key not in ['answer', 'reason']:
                html += "<div style='margin: 10px 0;'>"
                html += f"<h4 style='color: #8e44ad; margin: 8px 0;'>📊 {key.replace('_', ' ').title()}</h4>"
                html += f"<p style='background-color: #f8f9fa; padding: 8px; border-radius: 4px; margin: 5px 0; color: #495057;'>{value}</p>"
                html += "</div>"
        
        html += "</div>"
        return html
    
    def format_text_result(self, text):
        """格式化文本结果"""
        html = "<div style='font-family: Microsoft YaHei; line-height: 1.6;'>"
        html += "<h3 style='color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px;'>🎯 分析结果</h3>"
        
        # 将文本按段落分割
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        for paragraph in paragraphs:
            if paragraph.strip():
                # 检查是否是列表项（以数字、-、*开头）
                lines = paragraph.split('\n')
                if any(line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '-', '•', '*')) for line in lines):
                    html += "<ul style='margin: 10px 0; padding-left: 20px;'>"
                    for line in lines:
                        line = line.strip()
                        if line:
                            # 移除列表标记
                            clean_line = line.replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').replace('5.', '')
                            clean_line = clean_line.replace('- ', '').replace('• ', '').replace('* ', '').strip()
                            if clean_line:
                                html += f"<li style='margin: 5px 0; color: #2c3e50;'>• {clean_line}</li>"
                    html += "</ul>"
                else:
                    html += f"<p style='background-color: #e8f4f8; padding: 12px; border-radius: 5px; border-left: 4px solid #3498db; margin: 10px 0; font-size: 14px; color: #2c3e50;'>{paragraph}</p>"
        
        html += "</div>"
        return html
        
        # 添加完成信息到进度日志
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        completion_message = f"[{timestamp}] ✅ 所有处理已完成"
        current_text = self.progress_display.toPlainText()
        if current_text:
            new_text = current_text + "\n" + completion_message
        else:
            new_text = completion_message
        self.progress_display.setPlainText(new_text)
    
    def show_error(self, error_msg):
        """显示错误信息"""
        QMessageBox.critical(self, "错误", error_msg)
        
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.analyze_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        
        # 添加错误信息到进度日志
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        error_message = f"[{timestamp}] ❌ 错误: {error_msg}"
        current_text = self.progress_display.toPlainText()
        if current_text:
            new_text = current_text + "\n" + error_message
        else:
            new_text = error_message
        self.progress_display.setPlainText(new_text)
    
    def clear_all(self):
        """清空所有内容"""
        self.current_image_path = ""
        self.image_path_label.setText("请选择地质图文件...")
        self.image_preview_label.clear()
        self.image_preview_label.setText("图像预览区域\n(支持 JPG, PNG, BMP, TIF 等格式)")
        self.question_input.clear()
        self.result_display.clear()
        self.progress_bar.setVisible(False)
        self.update_controls_state(False)
        
        # 清空进度日志
        self.progress_display.clear()
        
        # 重置模块状态
        self.reset_module_status()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PEACE 地质图理解系统")
    
    # 设置应用图标和样式
    app.setStyle('Fusion')
    
    # 设置应用支持中文
    app.setFont(QFont("Microsoft YaHei", 9))
    
    window = GeoMapAnalyzerGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()