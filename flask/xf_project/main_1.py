import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget,
)

from excel对比高亮显示_ui import ExcelCompareTab
from 全部照片整理_ui import PhotoOrganize_All_Tab
from 百川照片整理_ui import PhotoOrganizeTab
from 部门匹配_ui import DeptMatchTab
from 基地内部组织分摊分类_ui import Jidi_neibuzuzhi_fentanfenlei
from 每日跟踪_ui import sync_excel_incremental_ui
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("app_icon.ico"))
        self.setWindowTitle("Excel 工具箱 - PyQt6 版")

        self.resize(700, 500)
        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.addTab(ExcelCompareTab(), "① Excel 对比")
        tabs.addTab(DeptMatchTab(), "② 部门匹配")
        tabs.addTab(PhotoOrganizeTab(), "③ 百川照片整理")
        tabs.addTab(PhotoOrganize_All_Tab(), "④ 全部照片整理")
        tabs.addTab(Jidi_neibuzuzhi_fentanfenlei(), "⑤ 基地内部分摊")
        tabs.addTab(sync_excel_incremental_ui(), "⑥ 每日跟踪")

        layout.addWidget(tabs)
        self.setLayout(layout)


# =========================================================
# 启动程序
# =========================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
