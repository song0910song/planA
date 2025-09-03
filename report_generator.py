from fpdf import FPDF
from datetime import datetime

# 定义中文字体支持的PDF类
class ChinesePDF(FPDF):
    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation=orientation, unit=unit, format=format)
        # 设置中文字体支持
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        # 页头可以添加公司logo或标题
        pass
    
    def footer(self):
        # 页脚显示页码
        self.set_y(-15)
        self.set_font('SimSun', '', 10)
        self.cell(0, 10, f'第 {self.page_no()} 页', 0, 0, 'C')

# 月度报告生成函数
def generate_monthly_report(month, excel_handler):
    # 创建PDF对象
    pdf = ChinesePDF()
    pdf.add_page()
    
    try:
        # 设置字体（尝试多种中文字体以确保兼容性）
        try:
            pdf.set_font("SimSun", size=12)
        except:
            try:
                pdf.set_font("Heiti TC", size=12)
            except:
                pdf.set_font("Arial Unicode MS", size=12)
    except:
        # 如果无法设置中文字体，使用默认字体
        pdf.set_font("Arial", size=12)
    
    # 报告标题
    pdf.set_font_size(16)
    pdf.cell(200, 15, txt=f"{month}月消费报告", ln=1, align="C")
    
    # 生成时间
    pdf.set_font_size(12)
    pdf.cell(200, 10, txt=f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1, align="R")
    
    # 消费记录标题
    pdf.ln(10)
    pdf.set_font(style="B")
    pdf.cell(200, 10, txt="本月消费记录", ln=1, align="L")
    pdf.set_font(style="")
    
    # 获取本月消费记录
    expenses = excel_handler.get_all_expenses()
    
    # 将英文月份转换为数字月份进行比较
    month_to_number = {
        "一月": 1, "二月": 2, "三月": 3, "四月": 4,
        "五月": 5, "六月": 6, "七月": 7, "八月": 8,
        "九月": 9, "十月": 10, "十一月": 11, "十二月": 12
    }
    
    current_month_number = month_to_number.get(month, datetime.now().month)
    monthly_expenses = [expense for expense in expenses if expense.date.month == current_month_number]
    
    # 显示消费记录表格
    if monthly_expenses:
        pdf.ln(5)
        pdf.set_font(style="B")
        # 设置表头宽度和内容
        pdf.cell(40, 10, "日期", border=1)
        pdf.cell(50, 10, "类别", border=1)
        pdf.cell(80, 10, "说明", border=1)
        pdf.cell(30, 10, "金额", border=1, ln=1)
        
        pdf.set_font(style="")
        
        # 计算总消费金额
        total_amount = 0
        
        # 按日期排序消费记录
        monthly_expenses.sort(key=lambda x: x.date)
        
        # 显示每条消费记录
        for expense in monthly_expenses:
            pdf.cell(40, 10, expense.date.strftime("%Y-%m-%d"), border=1)
            pdf.cell(50, 10, expense.category, border=1)
            
            # 处理说明内容过长的情况
            description = expense.description
            if len(description) > 30:
                # 截取部分说明
                pdf.cell(80, 10, description[:30] + "...", border=1)
            else:
                pdf.cell(80, 10, description, border=1)
                
            pdf.cell(30, 10, f"{expense.amount:.1f} 元", border=1, ln=1)
            total_amount += expense.amount
        
        # 显示总计行
        pdf.set_font(style="B")
        pdf.cell(170, 10, "本月总消费", border=1)
        pdf.cell(30, 10, f"{total_amount:.1f} 元", border=1, ln=1)
        pdf.set_font(style="")
    else:
        pdf.cell(200, 10, "本月无消费记录", ln=1)
    
    # 预算信息
    pdf.ln(10)
    pdf.set_font(style="B")
    pdf.cell(200, 10, txt="本月预算情况", ln=1, align="L")
    pdf.set_font(style="")
    
    budget = excel_handler.get_budget(month)
    if budget:
        pdf.cell(200, 10, f"预算总额: {budget.budget_amount:.1f} 元", ln=1)
        pdf.cell(200, 10, f"已用金额: {budget.spent:.1f} 元", ln=1)
        pdf.cell(200, 10, f"剩余金额: {budget.remaining:.1f} 元", ln=1)
        
        # 计算预算使用百分比
        if budget.budget_amount > 0:
            usage_percentage = (budget.spent / budget.budget_amount) * 100
            pdf.cell(200, 10, f"预算使用: {usage_percentage:.1f}%", ln=1)
    else:
        pdf.cell(200, 10, "本月未设置预算", ln=1)
    
    # 消费分类统计
    pdf.ln(10)
    pdf.set_font(style="B")
    pdf.cell(200, 10, txt="消费分类统计", ln=1, align="L")
    pdf.set_font(style="")
    
    # 重新生成最新的分类统计数据
    excel_handler.generate_category_statistics()
    statistics = excel_handler.get_category_statistics()
    
    # 筛选本月的分类统计
    monthly_statistics = []
    total_monthly_spent = sum([expense.amount for expense in monthly_expenses])
    
    if total_monthly_spent > 0:
        # 按类别统计本月消费
        category_amounts = {}
        for expense in monthly_expenses:
            if expense.category in category_amounts:
                category_amounts[expense.category] += expense.amount
            else:
                category_amounts[expense.category] = expense.amount
        
        # 生成本月的分类统计
        for category, amount in category_amounts.items():
            percentage = (amount / total_monthly_spent) * 100
            monthly_statistics.append((category, amount, f"{percentage:.1f}%"))
        
        # 按消费金额排序
        monthly_statistics.sort(key=lambda x: x[1], reverse=True)
    
    if monthly_statistics:
        pdf.ln(5)
        pdf.set_font(style="B")
        pdf.cell(80, 10, "类别", border=1)
        pdf.cell(80, 10, "总消费", border=1)
        pdf.cell(40, 10, "占比", border=1, ln=1)
        
        pdf.set_font(style="")
        for stat in monthly_statistics:
            pdf.cell(80, 10, stat[0], border=1)
            pdf.cell(80, 10, f"{stat[1]:.1f} 元", border=1)
            pdf.cell(40, 10, stat[2], border=1, ln=1)
    else:
        pdf.cell(200, 10, "无消费记录，无法生成分类统计", ln=1)
    
    # 消费建议（基于消费数据分析）
    pdf.ln(10)
    pdf.set_font(style="B")
    pdf.cell(200, 10, txt="消费建议", ln=1, align="L")
    pdf.set_font(style="")
    
    # 根据数据提供简单的消费建议
    if monthly_expenses and budget:
        # 计算各类别的平均消费
        category_counts = {}
        category_totals = {}
        
        for expense in monthly_expenses:
            if expense.category in category_counts:
                category_counts[expense.category] += 1
                category_totals[expense.category] += expense.amount
            else:
                category_counts[expense.category] = 1
                category_totals[expense.category] = expense.amount
        
        # 找出消费最高的类别
        if category_totals:
            max_category = max(category_totals, key=category_totals.get)
            max_amount = category_totals[max_category]
            
            suggestions = []
            
            # 如果预算超支
            if budget.remaining < 0:
                suggestions.append(f"本月预算已超支 {abs(budget.remaining):.1f} 元，建议控制支出。")
            # 如果预算使用超过80%
            elif budget.spent / budget.budget_amount > 0.8:
                suggestions.append(f"本月预算使用已超过80%，请注意控制后期支出。")
            
            # 针对消费最高的类别给出建议
            suggestions.append(f"{max_category}类消费占比较高（{max_amount:.1f}元），建议适当控制该类支出。")
            
            # 输出建议
            for suggestion in suggestions:
                pdf.multi_cell(0, 8, suggestion)
                pdf.ln(2)
    else:
        pdf.cell(200, 10, "继续保持良好的消费习惯！", ln=1)
    
    # 保存PDF文件
    report_filename = f"{month}月消费报告.pdf"
    pdf.output(report_filename, "F")

# 测试函数（用于单独测试报告生成功能）
if __name__ == "__main__":
    # 这里可以添加测试代码，实际使用时会被主程序导入并调用
    pass