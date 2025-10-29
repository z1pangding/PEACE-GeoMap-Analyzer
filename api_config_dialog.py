"""
API配置对话框模块
"""
import os
import re
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QComboBox, QMessageBox, QPushButton)
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QFont

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