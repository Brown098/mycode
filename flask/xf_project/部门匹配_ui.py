from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QMessageBox

from FileInputRow import FileInputRow

import os

import pandas as pd


def match_departments(excel_path, share_path, output_dir,log_func=print):
    dept_df = pd.read_excel(excel_path, sheet_name="部门数据")
    dept_df.columns = ['部门名称', '部门代码', '费用性质', '上级部门名称']
    dept_df['部门名称'] = dept_df['部门名称'].astype(str).str.strip()
    dept_df['上级部门名称'] = dept_df['上级部门名称'].astype(str).str.strip()

    share_df = pd.read_excel(share_path, sheet_name='汇总', header=None)
    for i in range(len(share_df)):
        if share_df.iloc[i].notna().any():
            share_df.columns = share_df.iloc[i]
            share_df = share_df.iloc[i + 1:].reset_index(drop=True)
            break

    dept_col = next((c for c in ['行标签'] if c in share_df.columns), None)
    if dept_col is None:
        raise ValueError("未在分摊费用表中找到部门列")

    share_df[dept_col] = share_df[dept_col].astype(str).str.strip()
    dept_group = dept_df.groupby('部门名称').apply(lambda x: x.to_dict('records')).to_dict()

    results = []
    last_code = None
    for i, row in share_df.iterrows():
        dept_name = str(row[dept_col]).strip()
        candidates = dept_group.get(dept_name)
        if candidates is None:
            code = '无匹配'
        elif len(candidates) == 1:
            code = candidates[0]['部门代码']
            last_code = code
        else:
            matched = False
            look_index = i - 1
            while look_index >= 0:
                prev_name = str(share_df.iloc[look_index][dept_col]).strip()
                for c in candidates:
                    if c['上级部门名称'] == prev_name:
                        code = c['部门代码']
                        last_code = code
                        matched = True
                        break
                if matched:
                    break
                look_index -= 1
            if not matched:
                if last_code and any(c['部门代码'] == last_code for c in candidates):
                    code = last_code
                else:
                    code = '无匹配'

        results.append({'行号': i + 1, '部门名称': dept_name, '部门代码': code})

    result_df = pd.DataFrame(results)

    try:
        os.makedirs(os.path.dirname(output_dir), exist_ok=True)
        result_df.to_excel(output_dir, index=False)
        log_func(f"🎯 已保存结果到: {output_dir}")
    except Exception as e:
        log_func(f"❌ 保存失败: {e}")



class DeptMatchTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.dept = FileInputRow("预提费用业务参数导出：")
        self.share = FileInputRow("需要分摊/预提 Excel 文件：")
        self.output_dir = FileInputRow("输出文件夹：", folder_mode=True)
        self.run_btn = QPushButton("开始匹配")
        self.run_btn.clicked.connect(self.run_match)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.dept)
        layout.addWidget(self.share)
        layout.addWidget(self.output_dir)
        layout.addWidget(self.run_btn)
        layout.addWidget(QLabel("日志输出："))
        layout.addWidget(self.log)
        self.setLayout(layout)

    def log_msg(self, msg): self.log.append(msg)

    def run_match(self):
        dept, share, outdir = self.dept.text(), self.share.text(), self.output_dir.text()
        if not all([dept, share, outdir]):
            QMessageBox.warning(self, "缺少文件", "请选择两个 Excel 文件和输出文件夹。")
            return
        try:
            base_name = os.path.splitext(os.path.basename(share))[0]
            output_dir = os.path.join(outdir, f"{base_name}--匹配结果.xlsx")
            match_departments(dept, share, output_dir,log_func=self.log_msg)
            QMessageBox.information(self, "完成", f"匹配完成，结果：\n{output_dir}")
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
            self.log_msg(str(e))
