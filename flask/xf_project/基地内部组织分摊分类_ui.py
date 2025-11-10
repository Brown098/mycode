import os


from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,QLabel,  QMessageBox, QTextEdit
)

from FileInputRow import FileInputRow

import pandas as pd
import os

def main_1(file1, file2, save_path, log_func=print):
    """执行基地内部组织分摊分类（优化版）"""
    log_func("🚀 开始处理 Excel 数据...")

    # ============ 1. 读取数据 ============
    try:
        data = pd.read_excel(file1, sheet_name="账单明细")
        roster = pd.read_excel(file2)
    except Exception as e:
        log_func(f"❌ Excel 读取失败: {e}")
        return

    if data.empty or roster.empty:
        log_func("⚠️ 文件内容为空，终止执行。")
        return

    log_func(f"📂 已读取账单 {len(data)} 行，花名册 {len(roster)} 行")

    # ============ 2. 清洗电话号码 ============
    def clean_phone(s: str) -> str:
        return ''.join(filter(str.isdigit, str(s)))

    for col in ["寄件公司电话", "到方客户电话"]:
        if col in data.columns:
            data[col] = data[col].astype(str).map(clean_phone)

    for col in ["个人电话", "公司电话"]:
        if col in roster.columns:
            roster[col] = roster[col].astype(str).map(clean_phone)

    # ============ 3. 花名册索引与唯一标识 ============
    name_counts = roster["姓名"].value_counts()
    unique_names = set(name_counts[name_counts == 1].index)

    # 设置索引方便后续快速匹配
    roster_personal = roster.drop_duplicates(subset=["姓名", "个人电话"]).set_index(["姓名", "个人电话"])
    roster_company = roster.drop_duplicates(subset=["姓名", "公司电话"]).set_index(["姓名", "公司电话"])

    # ============ 4. 账单中提取匹配信息 ============
    def get_match_info(row):
        pay = str(row.get("付款方式", ""))
        if pay.startswith("寄"):
            return pd.Series([row.get("经手人", ""), row.get("寄件公司电话", "")])
        elif pay.startswith("到"):
            return pd.Series([row.get("收件人", ""), row.get("到方客户电话", "")])
        else:
            return pd.Series(["", ""])

    data[["匹配姓名", "匹配电话"]] = data.apply(get_match_info, axis=1)

    # ============ 5. 匹配函数 ============
    cols = ["一级组织", "二级组织", "三级组织"]

    def find_org_info(name, phone):
        if not name or pd.isna(name):
            return [None, None, None]

        # 唯一姓名匹配
        if name in unique_names:
            match_rows = roster.loc[roster["姓名"] == name, cols]
            if not match_rows.empty:
                return match_rows.iloc[0].tolist()

        # 电话匹配（个人 + 公司）
        for idx_table in [roster_personal, roster_company]:
            try:
                row = idx_table.loc[(name, phone), cols]
                if isinstance(row, pd.DataFrame):
                    row = row.iloc[0]
                return row.tolist()
            except KeyError:
                continue

        return [None, None, None]

    # 矢量化处理加速匹配
    log_func("⚙️ 正在匹配组织信息...")
    match_results = [find_org_info(n, p) for n, p in zip(data["匹配姓名"], data["匹配电话"])]
    data[cols] = pd.DataFrame(match_results, columns=cols)

    # ============ 6. 组织规则 ============
    rules = {
        "研发中心": ("一级组织", "一级组织", None),
        "生产运营中心": ("一级组织", "三级组织", "二级组织"),
        "计划与物流中心": ("三级组织", "三级组织", "三级组织"),
        "质量中心": ("一级组织", "三级组织", "二级组织"),
        "工程技术中心": ("一级组织", "三级组织", None),
        "海外销售部": ("一级组织", "三级组织", None),
        "商用车销售部": ("一级组织", "三级组织", None),
        "财务部": ("一级组织", "一级组织", None),
        "战略规划与投资部": ("一级组织", "一级组织", None),
        "乘用车销售部": ("一级组织", "一级组织", None),
        "电机事业部": ("一级组织", "一级组织", None),
        "售后服务运营部": ("一级组织", "一级组织", None),
        "商用车国内销售部": ("一级组织", "一级组织", None),
        "电控车空事业部": ("一级组织", "三级组织", None),
        "采购部": ("一级组织", "一级组织", None),
        "运营管理与精益数字化部": ("一级组织", "一级组织", None),
        "人力资源部": ("一级组织", "一级组织", None),
        "商用车事业部": ("一级组织", "一级组织", None),
        "乘用车国内销售部": ("一级组织", "一级组织", None),
        "行政外事与法务部": ("一级组织", "一级组织", None),
        "精益与数字化运营部": ("一级组织", "一级组织", None),
        "产品线管理中心": ("一级组织", "一级组织", None),
        "可持续发展办公室": ("一级组织", "一级组织", None),
        "APU事业部": ("一级组织", "一级组织", None),
        "智能底盘事业部": ("一级组织", "一级组织", None),
        "审计部": ("一级组织", "一级组织", None),
        "电源事业部": ("一级组织", "一级组织", None),
        "总成事业部": ("一级组织", "一级组织", None),
        "董秘办公室": ("一级组织", "一级组织", None),
    }

    # ============ 7. 生成分摊字段 ============
    def fill_fields(row):
        org = row["一级组织"]
        if org not in rules:
            return [None, None, None]
        inner_key, finance_key, base_key = rules[org]
        inner = row.get(inner_key)
        finance = row.get(finance_key)
        base = row.get(base_key) if base_key else None
        return [base, finance, inner]

    log_func("📊 正在生成分摊字段...")
    data[["基地", "财报分摊", "内部分摊"]] = data.apply(fill_fields, axis=1, result_type="expand")

    # ============ 8. 输出统计 ============
    matched = data["一级组织"].notna().sum()
    unmatched = len(data) - matched
    log_func(f"✅ 匹配成功: {matched} 行，未匹配: {unmatched} 行")
    log_func(f"📈 唯一姓名数量: {len(unique_names)}")

    # ============ 9. 保存文件 ============
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        data.to_excel(save_path, index=False)
        log_func(f"🎯 已保存结果到: {save_path}")
    except Exception as e:
        log_func(f"❌ 保存失败: {e}")





#ui显示

class Jidi_neibuzuzhi_fentanfenlei(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.file1 = FileInputRow("顺丰账单")
        self.file2 = FileInputRow("对账花名册（张小芳使用）")
        self.output_dir = FileInputRow("输出文件夹", folder_mode=True)
        self.run_btn = QPushButton("开始匹配")
        self.run_btn.setStyleSheet("font-weight:bold; background:#4CAF50; color:white; padding:6px;")
        self.run_btn.clicked.connect(self.run_task)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("background:#f8f8f8;")

        layout.addWidget(self.file1)
        layout.addWidget(self.file2)
        layout.addWidget(self.output_dir)
        layout.addWidget(self.run_btn)
        layout.addWidget(QLabel("日志输出:"))
        layout.addWidget(self.log)
        self.setLayout(layout)

    def log_msg(self, msg):
        self.log.append(msg)
        QApplication.processEvents()

    def run_task(self):
        f1, f2, outdir = self.file1.text(), self.file2.text(), self.output_dir.text()
        print(f1, f2, outdir)
        if not all([f1, f2, outdir]):
            QMessageBox.warning(self, "缺少文件", "请选择两个文件和输出目录。")
            return

        try:
            base_name = os.path.splitext(os.path.basename(f1))[0]
            out_path = os.path.join(outdir, f"{base_name}--匹配结果.xlsx")
            self.log.clear()
            self.log_msg("🧮 开始执行匹配任务...")
            main_1(f1, f2, save_path=out_path, log_func=self.log_msg)
            QMessageBox.information(self, "完成", f"结果已保存到:\n{out_path}")
        except Exception as e:
            self.log_msg(f"❌ 出现错误: {e}")
            QMessageBox.critical(self, "错误", f"运行出错: {e}")



