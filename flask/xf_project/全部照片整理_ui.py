import os
import re
import shutil

import pandas as pd
from PyQt6.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QPushButton, QTextEdit, QWidget


from FileInputRow import FileInputRow


def organize_baichuan_photos_ALl(excel_file_path, photo_dir_path, output_dir_path,log_func=print):
    matched_excel_path = os.path.join(output_dir_path, "已匹配订单.xlsx")
    unmatched_excel_path = os.path.join(output_dir_path, "未匹配订单.xlsx")

    # 读取 Excel 并处理空值、去掉列首尾空格
    df = pd.read_excel(excel_file_path, dtype=str)
    df = df.fillna("")
    df.columns = df.columns.str.strip()

    df["货运单号"] = df["货运单号"].astype(str).str.strip()
    df["客户名称"] = df["客户名称"].astype(str).str.strip()
    df["承运人"] = df["承运人"].astype(str).str.strip()

    # 所有承运人都参与分类，不再限制百川开头
    order_to_customer = {k.lower(): v for k, v in zip(df["货运单号"], df["客户名称"])}
    order_to_carrier = {k.lower(): v for k, v in zip(df["货运单号"], df["承运人"])}
    all_orders = set(order_to_customer.keys())
    matched_orders = set()

    os.makedirs(output_dir_path, exist_ok=True)
    log_func("📂 开始扫描照片目录...")

    # 遍历照片目录
    for root, _, files in os.walk(photo_dir_path):
        for file_name in files:
            if not (file_name.lower().endswith(".jpg") or file_name.lower().endswith(".png")):
                continue
            file_base = os.path.splitext(file_name)[0].strip().lower()
            match = re.match(r'([a-zA-Z0-9]+)', file_base)
            order_id = match.group(1) if match else file_base

            customer_name = order_to_customer.get(order_id, "未匹配")
            carrier_name = order_to_carrier.get(order_id, "")
            if order_id in all_orders:
                matched_orders.add(order_id)

            folder_name = f"{customer_name}{carrier_name}" if carrier_name else customer_name
            customer_dir = os.path.join(output_dir_path, folder_name)
            os.makedirs(customer_dir, exist_ok=True)
            shutil.copy2(os.path.join(root, file_name), os.path.join(customer_dir, file_name))

    # 输出未匹配和已匹配 Excel
    unmatched_orders = all_orders - matched_orders
    if unmatched_orders:
        unmatched_df = df[df["货运单号"].str.lower().isin(unmatched_orders)]
        unmatched_df.to_excel(unmatched_excel_path, index=False)
    if matched_orders:
        matched_df = df[df["货运单号"].str.lower().isin(matched_orders)]
        matched_df.to_excel(matched_excel_path, index=False)

    log_func("🧩 分类完成")
    return output_dir_path


class PhotoOrganize_All_Tab(QWidget):
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
            organize_baichuan_photos_ALl(excel, photos, outdir,log_func=self.log_msg)
            QMessageBox.information(self, "完成", f"照片已整理完成，结果保存在：\n{outdir}")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
            self.log_msg(str(e))