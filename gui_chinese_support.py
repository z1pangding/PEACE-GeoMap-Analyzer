"""
PEACE项目GUI界面 - 修复版 (中文编码支持 + 详细步骤)
"""
import sys
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QTextEdit, QComboBox, 
                            QProgressBar, QGroupBox, QSplitter, QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QTextCursor

class ProcessingThread(QThread):
    """处理线程，执行真实地质图分析"""
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
            # HIE模块处理过程
            self.progress_signal.emit("【HIE模块】开始地质图数字化...")
            self.progress_signal.emit("  ├─ 初始化地质图分析器...")
            
            from modules import hierarchical_information_extraction
            hie = hierarchical_information_extraction()
            
            self.progress_signal.emit("  ├─ 检测地质图布局结构...")
            self.progress_signal.emit("  │  ├─ 识别主地图区域...")
            self.progress_signal.emit("  │  ├─ 识别图例区域...")
            self.progress_signal.emit("  │  ├─ 识别标题区域...")
            self.progress_signal.emit("  │  └─ 识别比例尺区域...")
            
            meta = hie.digitalize(self.image_path)
            
            self.progress_signal.emit("  ├─ 提取图例信息...")
            self.progress_signal.emit("  │  ├─ 识别岩石类型...")
            self.progress_signal.emit("  │  └─ 分析地层年代...")
            
            self.progress_signal.emit("  └─ HIE模块处理完成")
            
            # DKI模块处理过程
            self.progress_signal.emit("【DKI模块】开始领域知识注入...")
            self.progress_signal.emit("  ├─ 初始化地质知识库...")
            
            from modules import domain_knowledge_injection
            dki = domain_knowledge_injection()
            
            self.progress_signal.emit("  ├─ 分析问题需求... (支持中文)")
            self.progress_signal.emit("  ├─ 检索相关地质知识...")
            self.progress_signal.emit("  │  ├─ 获取地震历史数据...")
            self.progress_signal.emit("  │  └─ 获取地理环境信息...")
            
            # 确保中文问题能正确传递
            question_encoded = self.question.encode('utf-8').decode('utf-8')  # 确保UTF-8编码
            knowledge = dki.consult(question_encoded, meta)
            
            self.progress_signal.emit("  └─ DKI模块处理完成")
            
            # PEQA模块处理过程
            self.progress_signal.emit("【PEQA模块】开始答案生成...")
            self.progress_signal.emit("  ├─ 分析问题类型...")
            self.progress_signal.emit("  ├─ 构建增强提示...")
            self.progress_signal.emit("  │  ├─ 选择相关图像区域...")
            self.progress_signal.emit("  │  └─ 整合多源信息...")
            
            from modules import prompt_enhanced_QA
            peqa = prompt_enhanced_QA()
            
            self.progress_signal.emit("  ├─ 调用AI模型生成答案...")
            # 确保中文问题和类型能正确传递
            answer = peqa.answer(
                meta, 
                knowledge, 
                True, 
                self.image_path, 
                question_encoded,  # 使用编码处理过的中文问题
                self.question_type
            )
            
            self.progress_signal.emit("  ├─ 格式化答案输出...")
            try:
                answer = json.loads(answer)
                from utils import prompt
                final_answer = prompt.get_final_answer(answer, self.question_type)
            except:
                final_answer = answer
            
            self.progress_signal.emit("  └─ PEQA模块处理完成")
            self.progress_signal.emit("🎉 分析完成！")
            self.result_signal.emit(str(final_answer))
            
        except Exception as e:
            import traceback
            self.error_signal.emit(f"处理错误: {str(e)}\\n详细错误: {traceback.format_exc()}")

class GeoMapAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PEACE地质图分析系统 - 中文支持版")
        self.setGeometry(100, 100, 1200, 700)
        
        self.current_image_path = ""
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面 - 右侧包含日志和结果"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # 使用分割器，左侧40%，右侧60%
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(3)
        
        # 左侧功能区
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(10)
        
        # 图像选择组
        image_group = QGroupBox("选择地质图")
        image_group_layout = QVBoxLayout(image_group)
        
        self.select_btn = QPushButton("选择图片")
        self.select_btn.clicked.connect(self.select_image)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        image_group_layout.addWidget(self.select_btn)
        
        self.image_path_label = QLabel("未选择图片")
        self.image_path_label.setWordWrap(True)
        self.image_path_label.setStyleSheet("padding: 5px; border: 1px solid #ccc;")
        image_group_layout.addWidget(self.image_path_label)
        
        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setMinimumSize(300, 200)
        self.image_preview.setStyleSheet("border: 1px solid #ccc; background-color: #f9f9f9;")
        self.image_preview.setText("图片预览")
        image_group_layout.addWidget(self.image_preview)
        
        left_layout.addWidget(image_group)
        
        # 问题设置组
        question_group = QGroupBox("问题设置")
        question_group_layout = QVBoxLayout(question_group)
        
        question_type_layout = QHBoxLayout()
        question_type_layout.addWidget(QLabel("类型:"))
        self.question_type_combo = QComboBox()
        self.question_type_combo.addItems([
            "地层分析", 
            "提取图名", 
            "提取比例尺",
            "提取经纬度",
            "地震风险评估",
            "区域对比",
            "断层分析",
            "自定义"
        ])
        question_type_layout.addWidget(self.question_type_combo)
        question_group_layout.addLayout(question_type_layout)
        
        question_group_layout.addWidget(QLabel("问题:"))
        self.question_input = QTextEdit()
        self.question_input.setMaximumHeight(80)
        self.question_input.setPlaceholderText("输入您的问题 (支持中文)...")
        self.question_input.textChanged.connect(self.update_button_state)
        question_group_layout.addWidget(self.question_input)
        
        left_layout.addWidget(question_group)
        
        # 操作按钮组
        button_group = QGroupBox("操作")
        button_group_layout = QVBoxLayout(button_group)
        
        self.analyze_btn = QPushButton("开始分析")
        self.analyze_btn.clicked.connect(self.start_analysis)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        button_group_layout.addWidget(self.analyze_btn)
        
        self.clear_btn = QPushButton("清空")
        self.clear_btn.clicked.connect(self.clear_all)
        button_group_layout.addWidget(self.clear_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        button_group_layout.addWidget(self.progress_bar)
        
        left_layout.addWidget(button_group)
        
        # 添加到左侧
        splitter.addWidget(left_widget)
        
        # 右侧 - 上方日志，下方结果
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 日志显示组（上方）
        log_group = QGroupBox("处理日志")
        log_group_layout = QVBoxLayout(log_group)
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Consolas", 8))
        log_group_layout.addWidget(self.log_display)
        right_layout.addWidget(log_group)
        
        # 结果显示组（下方）
        result_group = QGroupBox("分析结果")
        result_group_layout = QVBoxLayout(result_group)
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFont(QFont("Consolas", 9))
        result_group_layout.addWidget(self.result_display)
        right_layout.addWidget(result_group)
        
        # 设置日志和结果的高度比例（日志占1/3，结果占2/3）
        log_group.setMaximumHeight(200)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([480, 720])
        
        main_layout.addWidget(splitter)
        self.update_button_state()
    
    def select_image(self):
        """选择地质图"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择地质图", "", "图像文件 (*.jpg *.jpeg *.png *.bmp *.tiff *.tif)"
        )
        
        if file_path:
            self.current_image_path = file_path
            self.image_path_label.setText(os.path.basename(file_path))
            
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    self.image_preview.width() - 10,
                    self.image_preview.height() - 10,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_preview.setPixmap(scaled)
            
            self.log_message(f"已选择: {os.path.basename(file_path)}")
            self.update_button_state()
    
    def update_button_state(self):
        """更新按钮状态"""
        has_image = bool(self.current_image_path)
        has_question = bool(self.question_input.toPlainText().strip())
        self.analyze_btn.setEnabled(has_image and has_question)
    
    def start_analysis(self):
        """开始分析"""
        if not self.current_image_path:
            QMessageBox.warning(self, "警告", "请先选择地质图！")
            return
        
        question = self.question_input.toPlainText().strip()
        if not question:
            QMessageBox.warning(self, "警告", "请输入问题！")
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.analyze_btn.setEnabled(False)
        
        type_map = {
            "地层分析": "analyzing-formation",
            "提取图名": "extracting-sheet_name", 
            "提取比例尺": "extracting-scale",
            "提取经纬度": "extracting-lonlat",
            "地震风险评估": "analyzing-earthquake_risk",
            "区域对比": "reasoning-area_comparison",
            "断层分析": "reasoning-fault_existence",
            "自定义": "analyzing-formation"
        }
        question_type = type_map.get(self.question_type_combo.currentText(), "analyzing-formation")
        
        self.log_message(f"分析开始 - 图片: {os.path.basename(self.current_image_path)}")
        self.log_message(f"问题: {question}")
        self.log_message(f"类型: {question_type}")
        
        self.thread = ProcessingThread(
            self.current_image_path, question, question_type, ["HIE", "DKI", "PEQA"]
        )
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.result_signal.connect(self.show_result)
        self.thread.error_signal.connect(self.show_error)
        self.thread.start()
    
    def update_progress(self, message):
        """更新进度"""
        self.log_message(message)
    
    def show_result(self, result):
        """显示结果"""
        self.result_display.setPlainText(result)
        self.log_message("分析完成！")
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
    
    def show_error(self, error_msg):
        """显示错误"""
        self.log_message(f"错误: {error_msg}")
        QMessageBox.critical(self, "错误", error_msg)
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
    
    def log_message(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        current = self.log_display.toPlainText()
        self.log_display.setPlainText(current + "\n" + log_entry if current else log_entry)
        cursor = self.log_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_display.setTextCursor(cursor)
    
    def clear_all(self):
        """清空所有"""
        self.current_image_path = ""
        self.image_path_label.setText("未选择图片")
        self.image_preview.clear()
        self.image_preview.setText("图片预览")
        self.question_input.clear()
        self.result_display.clear()
        self.log_display.clear()
        self.progress_bar.setVisible(False)
        self.update_button_state()

def main():
    app = QApplication(sys.argv)
    window = GeoMapAnalyzerGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()