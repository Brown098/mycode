
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QMessageBox

from FileInputRow import FileInputRow

import os
import re
import shutil

import pandas as pd


def organize_baichuan_photos(excel_file_path, photo_dir_path, output_dir_path):
    df = pd.read_excel(excel_file_path, dtype=str).fillna("")
    df["货运单号"] = df["货运单号"].astype(str).str.strip()
    df["客户名称"] = df["客户名称"].astype(str).str.strip()
    df["承运人"] = df["承运人"].astype(str).str.strip()
    df = df[df["承运人"].str.startswith("百川")]

    order_to_customer = {k.lower(): v for k, v in zip(df["货运单号"], df["客户名称"])}
    matched_orders = set()
    os.makedirs(output_dir_path, exist_ok=True)

    for root, dirs, files in os.walk(photo_dir_path):
        for file_name in files:
            if not file_name.lower().endswith((".jpg", ".png")):
                continue
            order_id = re.match(r'([a-zA-Z0-9]+)', os.path.splitext(file_name)[0])
            order_id = order_id.group(1).lower() if order_id else ""
            customer_name = order_to_customer.get(order_id, "未匹配")
            if order_id in order_to_customer:
                matched_orders.add(order_id)
            customer_dir = os.path.join(output_dir_path, f"{customer_name}百川")
            os.makedirs(customer_dir, exist_ok=True)
            shutil.copy2(os.path.join(root, file_name), os.path.join(customer_dir, file_name))

    unmatched_orders = set(order_to_customer.keys()) - matched_orders
    if unmatched_orders:
        df[df["货运单号"].str.lower().isin(unmatched_orders)].to_excel(
            os.path.join(output_dir_path, "未匹配订单.xlsx"), index=False
        )
    if matched_orders:
        df[df["货运单号"].str.lower().isin(matched_orders)].to_excel(
            os.path.join(output_dir_path, "已匹配订单.xlsx"), index=False
        )
    return output_dir_path





class PhotoOrganizeTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.excel = FileInputRow("Excel 文件：")
        self.photos = FileInputRow("照片文件夹：", folder_mode=True)
        self.output_dir = FileInputRow("输出文件夹：", folder_mode=True)
        self.run_btn = QPushButton("开始整理")
        self.run_btn.clicked.connect(self.run_organize)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.excel)
        layout.addWidget(self.photos)
        layout.addWidget(self.output_dir)
        layout.addWidget(self.run_btn)
        layout.addWidget(QLabel("日志输出："))
        layout.addWidget(self.log)
        self.setLayout(layout)

    def log_msg(self, msg): self.log.append(msg)

    def run_organize(self):
        excel, photos, outdir = self.excel.text(), self.photos.text(), self.output_dir.text()
        if not all([excel, photos, outdir]):
            QMessageBox.warning(self, "缺少文件", "请选择 Excel 文件、照片文件夹和输出文件夹。")
            return
        try:
            organize_baichuan_photos(excel, photos, outdir)
            QMessageBox.information(self, "完成", f"照片已整理完成，结果保存在：\n{outdir}")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
            self.log_msg(str(e))