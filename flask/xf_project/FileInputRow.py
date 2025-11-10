from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFileDialog


class FileInputRow(QWidget):
    def __init__(self, label, folder_mode=False):
        super().__init__()
        self.label = QLabel(label)
        self.input = QLineEdit()
        self.btn = QPushButton("选择")

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn)
        self.setLayout(layout)

        self.folder_mode = folder_mode
        self.btn.clicked.connect(self.choose)

    def choose(self):
        if self.folder_mode:
            path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        else:
            path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if path:
            self.input.setText(path)

    def text(self):
        return self.input.text()