# 大学生消费管理系统开发指南：基于 Python Tkinter 与 Excel

## 一、项目概述

在大学生活中，合理管理个人消费是培养财商的重要一环。开发一个适合自己的消费管理系统，不仅能帮助记录日常开支，还能通过数据分析形成良好的消费习惯。本指南将详细介绍如何使用 Python 的 Tkinter 库和 Excel 构建一个功能完备的大学生消费管理系统，满足记录消费、预算管理、分类统计、可视化分析和生成月度报告等核心需求。

### 1.1 系统目标与功能需求

本系统的主要目标是帮助大学生有效管理生活费开支，具体功能需求包括：



1.  **预算管理**：设置月度预算并实时跟踪支出情况

2.  **消费分类统计**：按自定义类别记录和统计消费

3.  **提醒功能**：预算接近或超出时的预警提示

4.  **可视化分析**：用图表直观展示消费分布

5.  **自动同步**：系统与 Excel 数据保持实时一致

6.  **月度报告**：每月生成详细的消费分析报告

7.  **简洁美观的 GUI 界面**：操作便捷，功能导向明确

### 1.2 技术选型与架构设计

本系统采用以下技术栈实现：



*   **前端界面**：使用 Tkinter 库构建图形用户界面，轻量且无需额外安装

*   **数据存储**：使用 Excel 文件作为数据库，便于查看和编辑

*   **数据处理**：使用 openpyxl 库操作 Excel 文件，实现数据的读写和更新

*   **可视化**：使用 matplotlib 库生成消费统计图表

*   **报告生成**：使用 fpdf 库从 Excel 数据生成 PDF 格式的月度报告

系统架构采用分层设计，分为用户界面层、业务逻辑层和数据存储层，各层之间通过清晰的接口交互，确保系统的可维护性和可扩展性。

## 二、开发环境搭建

### 2.1 安装必要的 Python 库

在开始编码前，需要安装几个关键的 Python 库：



1.  **Tkinter**：Python 的标准 GUI 库，通常无需额外安装

2.  **openpyxl**：用于操作 Excel 文件的强大库

3.  **matplotlib**：用于创建可视化图表

4.  **fpdf**：用于生成 PDF 格式的月度报告

使用以下命令安装所需库：



```
pip install openpyxl matplotlib fpdf
```

### 2.2 设置 Excel 文件结构

在开发前，需要预先设计好 Excel 文件的数据结构，以满足系统的数据存储需求。创建一个名为`expenses.xlsx`的 Excel 文件，包含以下工作表：



1.  **消费记录**工作表：

*   日期（Date）

*   金额（Amount）

*   类别（Category）

*   说明（Description）

1.  **预算设置**工作表：

*   月份（Month）

*   预算金额（Budget）

*   已用金额（Spent）

*   剩余金额（Remaining）

1.  **分类统计**工作表（自动生成）：

*   类别（Category）

*   总消费（Total Spending）

*   占比（Percentage）

确保 Excel 文件与 Python 脚本位于同一目录下，以便系统能够正确读取和写入数据。

## 三、核心功能开发

### 3.1 数据模型与 Excel 操作

#### 3.1.1 数据模型设计

首先定义系统所需的数据模型，包括消费记录和预算信息：



```
class Expense:

&#x20;   def \_\_init\_\_(self, date, amount, category, description):

&#x20;       self.date = date

&#x20;       self.amount = amount

&#x20;       self.category = category

&#x20;       self.description = description

class Budget:

&#x20;   def \_\_init\_\_(self, month, budget\_amount):

&#x20;       self.month = month

&#x20;       self.budget\_amount = budget\_amount

&#x20;       self.spent = 0.0

&#x20;       self.remaining = budget\_amount

&#x20;   def update\_spent(self, amount):

&#x20;       self.spent += amount

&#x20;       self.remaining = self.budget\_amount - self.spent
```

#### 3.1.2 Excel 文件操作类

创建一个 Excel 操作类，封装对 Excel 文件的读写和更新操作：



```
import openpyxl

from openpyxl.utils import get\_column\_letter

from datetime import datetime

class ExcelHandler:

&#x20;   def \_\_init\_\_(self, filename):

&#x20;       self.filename = filename

&#x20;       self.workbook = None

&#x20;       self.ensure\_worksheets\_exist()

&#x20;   def ensure\_worksheets\_exist(self):

&#x20;       try:

&#x20;           self.workbook = openpyxl.load\_workbook(self.filename)

&#x20;       except FileNotFoundError:

&#x20;           self.workbook = openpyxl.Workbook()

&#x20;           self.workbook.remove(self.workbook.active)

&#x20;           self.create\_new\_worksheets()

&#x20;           self.save()

&#x20;   def create\_new\_worksheets(self):

&#x20;       # 创建消费记录工作表

&#x20;       expense\_sheet = self.workbook.create\_sheet("消费记录")

&#x20;       expense\_sheet.append(\["日期", "金额", "类别", "说明"])

&#x20;      &#x20;

&#x20;       # 创建预算设置工作表

&#x20;       budget\_sheet = self.workbook.create\_sheet("预算设置")

&#x20;       budget\_sheet.append(\["月份", "预算金额", "已用金额", "剩余金额"])

&#x20;      &#x20;

&#x20;       # 创建分类统计工作表

&#x20;       category\_sheet = self.workbook.create\_sheet("分类统计")

&#x20;       category\_sheet.append(\["类别", "总消费", "占比"])

&#x20;   def save(self):

&#x20;       self.workbook.save(self.filename)

&#x20;   def add\_expense(self, expense):

&#x20;       expense\_sheet = self.workbook\["消费记录"]

&#x20;       expense\_sheet.append(\[

&#x20;           expense.date.strftime("%Y-%m-%d"),

&#x20;           expense.amount,

&#x20;           expense.category,

&#x20;           expense.description

&#x20;       ])

&#x20;       self.save()

&#x20;   def get\_all\_expenses(self):

&#x20;       expense\_sheet = self.workbook\["消费记录"]

&#x20;       expenses = \[]

&#x20;       for row in expense\_sheet.iter\_rows(min\_row=2, values\_only=True):

&#x20;           date = datetime.strptime(row\[0], "%Y-%m-%d")

&#x20;           amount = row\[1]

&#x20;           category = row\[2]

&#x20;           description = row\[3]

&#x20;           expenses.append(Expense(date, amount, category, description))

&#x20;       return expenses

&#x20;   def set\_budget(self, month, budget\_amount):

&#x20;       budget\_sheet = self.workbook\["预算设置"]

&#x20;       # 检查是否已有该月份的预算记录

&#x20;       for row in budget\_sheet.iter\_rows(min\_row=2, values\_only=True):

&#x20;           if row\[0] == month:

&#x20;               # 更新现有预算

&#x20;               row\_index = budget\_sheet.max\_row - (budget\_sheet.max\_row - row\[0].row)

&#x20;               budget\_sheet.cell(row=row\_index, column=2, value=budget\_amount)

&#x20;               budget\_sheet.cell(row=row\_index, column=3, value=0.0)

&#x20;               budget\_sheet.cell(row=row\_index, column=4, value=budget\_amount)

&#x20;               self.save()

&#x20;               return

&#x20;       # 如果没有，则添加新预算记录

&#x20;       budget\_sheet.append(\[month, budget\_amount, 0.0, budget\_amount])

&#x20;       self.save()

&#x20;   def get\_budget(self, month):

&#x20;       budget\_sheet = self.workbook\["预算设置"]

&#x20;       for row in budget\_sheet.iter\_rows(min\_row=2, values\_only=True):

&#x20;           if row\[0] == month:

&#x20;               return Budget(month, row\[1])

&#x20;       return None

&#x20;   def update\_budget\_spent(self, month, amount):

&#x20;       budget\_sheet = self.workbook\["预算设置"]

&#x20;       for row in budget\_sheet.iter\_rows(min\_row=2, values\_only=True):

&#x20;           if row\[0] == month:

&#x20;               row\_index = budget\_sheet.max\_row - (budget\_sheet.max\_row - row\[0].row)

&#x20;               new\_spent = row\[2] + amount

&#x20;               new\_remaining = row\[3] - amount

&#x20;               budget\_sheet.cell(row=row\_index, column=3, value=new\_spent)

&#x20;               budget\_sheet.cell(row=row\_index, column=4, value=new\_remaining)

&#x20;               self.save()

&#x20;               return

&#x20;   def generate\_category\_statistics(self):

&#x20;       expense\_sheet = self.workbook\["消费记录"]

&#x20;       category\_sheet = self.workbook\["分类统计"]

&#x20;      &#x20;

&#x20;       # 清空现有统计数据

&#x20;       category\_sheet.delete\_rows(2, category\_sheet.max\_row -1)

&#x20;      &#x20;

&#x20;       # 计算各类别总消费

&#x20;       categories = {}

&#x20;       for row in expense\_sheet.iter\_rows(min\_row=2, values\_only=True):

&#x20;           category = row\[2]

&#x20;           amount = row\[1]

&#x20;           if category in categories:

&#x20;               categories\[category] += amount

&#x20;           else:

&#x20;               categories\[category] = amount

&#x20;      &#x20;

&#x20;       # 计算总消费和占比

&#x20;       total\_spent = sum(categories.values())

&#x20;       for category, total in categories.items():

&#x20;           percentage = (total / total\_spent) \* 100 if total\_spent != 0 else 0

&#x20;           category\_sheet.append(\[category, total, f"{percentage:.1f}%"])

&#x20;      &#x20;

&#x20;       self.save()

&#x20;   def get\_category\_statistics(self):

&#x20;       category\_sheet = self.workbook\["分类统计"]

&#x20;       statistics = \[]

&#x20;       for row in category\_sheet.iter\_rows(min\_row=2, values\_only=True):

&#x20;           category = row\[0]

&#x20;           total = row\[1]

&#x20;           percentage = row\[2]

&#x20;           statistics.append((category, total, percentage))

&#x20;       return statistics
```

### 3.2 主窗口界面设计

使用 Tkinter 创建系统的主窗口，实现基本的界面布局和组件：



```
import tkinter as tk

from tkinter import ttk, messagebox

from datetime import datetime

class ExpenseManagerGUI:

&#x20;   def \_\_init\_\_(self, master, excel\_handler):

&#x20;       self.master = master

&#x20;       self.master.title("大学生消费管理系统")

&#x20;      &#x20;

&#x20;       self.excel\_handler = excel\_handler

&#x20;      &#x20;

&#x20;       # 设置窗口大小和位置

&#x20;       window\_width = 800

&#x20;       window\_height = 600

&#x20;       screen\_width = self.master.winfo\_screenwidth()

&#x20;       screen\_height = self.master.winfo\_screenheight()

&#x20;       x\_position = (screen\_width - window\_width) // 2

&#x20;       y\_position = (screen\_height - window\_height) // 2

&#x20;       self.master.geometry(f"{window\_width}x{window\_height}+{x\_position}+{y\_position}")

&#x20;      &#x20;

&#x20;       # 创建主框架

&#x20;       self.main\_frame = ttk.Frame(self.master, padding="10")

&#x20;       self.main\_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

&#x20;       self.master.columnconfigure(0, weight=1)

&#x20;       self.master.rowconfigure(0, weight=1)

&#x20;      &#x20;

&#x20;       # 创建界面组件

&#x20;       self.create\_widgets()

&#x20;      &#x20;

&#x20;       # 初始化预算提醒定时器

&#x20;       self.check\_budget\_alert()

&#x20;      &#x20;

&#x20;       # 加载消费记录

&#x20;       self.load\_expenses()

&#x20;      &#x20;

&#x20;   def create\_widgets(self):

&#x20;       # 创建顶部预算信息区域

&#x20;       self.create\_budget\_section()

&#x20;      &#x20;

&#x20;       # 创建左侧消费记录区域

&#x20;       self.create\_expense\_list\_section()

&#x20;      &#x20;

&#x20;       # 创建右侧图表区域

&#x20;       self.create\_chart\_section()

&#x20;      &#x20;

&#x20;       # 创建底部操作按钮

&#x20;       self.create\_action\_buttons()

&#x20;      &#x20;

&#x20;   def create\_budget\_section(self):

&#x20;       # 预算设置框架

&#x20;       budget\_frame = ttk.LabelFrame(self.main\_frame, text="月度预算设置")

&#x20;       budget\_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 月份选择

&#x20;       self.month\_combobox = ttk.Combobox(budget\_frame, values=\[

&#x20;           "一月", "二月", "三月", "四月", "五月", "六月",

&#x20;           "七月", "八月", "九月", "十月", "十一月", "十二月"

&#x20;       ], state="readonly")

&#x20;       self.month\_combobox.set(datetime.now().strftime("%B"))  # 默认显示当前月份

&#x20;       self.month\_combobox.grid(row=0, column=0, padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 预算金额输入

&#x20;       self.budget\_entry = ttk.Entry(budget\_frame)

&#x20;       self.budget\_entry.grid(row=0, column=1, padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 设置预算按钮

&#x20;       self.set\_budget\_button = ttk.Button(budget\_frame, text="设置预算", command=self.set\_budget)

&#x20;       self.set\_budget\_button.grid(row=0, column=2, padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 预算状态显示

&#x20;       self.budget\_status\_label = ttk.Label(budget\_frame, text="")

&#x20;       self.budget\_status\_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 加载当前月份预算

&#x20;       current\_month = datetime.now().strftime("%B")

&#x20;       self.load\_budget(current\_month)

&#x20;      &#x20;

&#x20;   def create\_expense\_list\_section(self):

&#x20;       # 消费记录框架

&#x20;       expense\_list\_frame = ttk.LabelFrame(self.main\_frame, text="消费记录")

&#x20;       expense\_list\_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 消费记录表格

&#x20;       self.expense\_tree = ttk.Treeview(expense\_list\_frame, columns=("金额", "类别", "说明", "日期"), show="headings")

&#x20;       self.expense\_tree.heading("金额", text="金额")

&#x20;       self.expense\_tree.heading("类别", text="类别")

&#x20;       self.expense\_tree.heading("说明", text="说明")

&#x20;       self.expense\_tree.heading("日期", text="日期")

&#x20;       self.expense\_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E), padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 添加垂直滚动条

&#x20;       scrollbar = ttk.Scrollbar(expense\_list\_frame, orient=tk.VERTICAL, command=self.expense\_tree.yview)

&#x20;       scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

&#x20;       self.expense\_tree.configure(yscrollcommand=scrollbar.set)

&#x20;      &#x20;

&#x20;       # 使表格随窗口大小调整

&#x20;       expense\_list\_frame.grid\_rowconfigure(0, weight=1)

&#x20;       expense\_list\_frame.grid\_columnconfigure(0, weight=1)

&#x20;      &#x20;

&#x20;   def create\_chart\_section(self):

&#x20;       # 图表框架

&#x20;       chart\_frame = ttk.LabelFrame(self.main\_frame, text="消费分类统计")

&#x20;       chart\_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.N, tk.S, tk.W, tk.E), padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 预留图表显示区域

&#x20;       self.chart\_canvas = tk.Canvas(chart\_frame, width=400, height=300)

&#x20;       self.chart\_canvas.grid(row=0, column=0, padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 初始化图表

&#x20;       self.update\_chart()

&#x20;      &#x20;

&#x20;   def create\_action\_buttons(self):

&#x20;       # 操作按钮框架

&#x20;       button\_frame = ttk.Frame(self.main\_frame)

&#x20;       button\_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 添加消费按钮

&#x20;       self.add\_expense\_button = ttk.Button(button\_frame, text="添加消费", command=self.open\_add\_expense\_window)

&#x20;       self.add\_expense\_button.grid(row=0, column=0, padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 生成月度报告按钮

&#x20;       self.generate\_report\_button = ttk.Button(button\_frame, text="生成月度报告", command=self.generate\_monthly\_report)

&#x20;       self.generate\_report\_button.grid(row=0, column=1, padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 刷新数据按钮

&#x20;       self.refresh\_button = ttk.Button(button\_frame, text="刷新数据", command=self.refresh\_data)

&#x20;       self.refresh\_button.grid(row=0, column=2, padx=5, pady=5)

&#x20;      &#x20;

&#x20;       # 退出系统按钮

&#x20;       self.quit\_button = ttk.Button(button\_frame, text="退出系统", command=self.master.destroy)

&#x20;       self.quit\_button.grid(row=0, column=3, padx=5, pady=5)

&#x20;      &#x20;

&#x20;   def load\_budget(self, month):

&#x20;       budget = self.excel\_handler.get\_budget(month)

&#x20;       if budget:

&#x20;           self.budget\_entry.delete(0, tk.END)

&#x20;           self.budget\_entry.insert(0, budget.budget\_amount)

&#x20;           self.budget\_status\_label.config(text=f"已用: {budget.spent:.1f} 元, 剩余: {budget.remaining:.1f} 元")

&#x20;       else:

&#x20;           self.budget\_entry.delete(0, tk.END)

&#x20;           self.budget\_status\_label.config(text="")

&#x20;   def set\_budget(self):

&#x20;       month = self.month\_combobox.get()

&#x20;       try:

&#x20;           budget\_amount = float(self.budget\_entry.get())

&#x20;           self.excel\_handler.set\_budget(month, budget\_amount)

&#x20;           self.load\_budget(month)

&#x20;           messagebox.showinfo("预算设置", "预算设置成功！")

&#x20;       except ValueError:

&#x20;           messagebox.showerror("错误", "请输入有效的预算金额！")

&#x20;   def open\_add\_expense\_window(self):

&#x20;       add\_window = tk.Toplevel(self.master)

&#x20;       AddExpenseWindow(add\_window, self.excel\_handler, self)

&#x20;   def add\_new\_expense(self, expense):

&#x20;       self.excel\_handler.add\_expense(expense)

&#x20;       self.excel\_handler.update\_budget\_spent(expense.date.strftime("%B"), expense.amount)

&#x20;       self.load\_expenses()

&#x20;       self.update\_chart()

&#x20;       self.check\_budget\_alert()

&#x20;   def load\_expenses(self):

&#x20;       # 清空现有数据

&#x20;       for item in self.expense\_tree.get\_children():

&#x20;           self.expense\_tree.delete(item)

&#x20;      &#x20;

&#x20;       # 加载新数据

&#x20;       expenses = self.excel\_handler.get\_all\_expenses()

&#x20;       for expense in expenses:

&#x20;           self.expense\_tree.insert(

&#x20;               "",

&#x20;               tk.END,

&#x20;               values=(

&#x20;                   f"{expense.amount:.1f} 元",

&#x20;                   expense.category,

&#x20;                   expense.description,

&#x20;                   expense.date.strftime("%Y-%m-%d")

&#x20;               )

&#x20;           )

&#x20;   def update\_chart(self):

&#x20;       # 生成消费分类统计

&#x20;       self.excel\_handler.generate\_category\_statistics()

&#x20;       statistics = self.excel\_handler.get\_category\_statistics()

&#x20;      &#x20;

&#x20;       # 准备图表数据

&#x20;       categories = \[stat\[0] for stat in statistics]

&#x20;       amounts = \[stat\[1] for stat in statistics]

&#x20;      &#x20;

&#x20;       # 清除现有图表

&#x20;       self.chart\_canvas.delete("all")

&#x20;      &#x20;

&#x20;       # 创建新图表

&#x20;       if categories:

&#x20;           import matplotlib

&#x20;           matplotlib.use('TkAgg')

&#x20;           from matplotlib.backends.backend\_tkagg import FigureCanvasTkAgg

&#x20;           from matplotlib.figure import Figure

&#x20;          &#x20;

&#x20;           fig = Figure(figsize=(3, 2), dpi=100)

&#x20;           ax = fig.add\_subplot(111)

&#x20;           ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)

&#x20;           ax.axis('equal')  # 保证饼图为正圆形

&#x20;          &#x20;

&#x20;           canvas = FigureCanvasTkAgg(fig, master=self.chart\_canvas)

&#x20;           canvas.draw()

&#x20;           canvas.get\_tk\_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

&#x20;          &#x20;

&#x20;           # 将图表嵌入到Tkinter窗口中

&#x20;           self.chart\_canvas.create\_window((0,0), window=canvas.get\_tk\_widget(), anchor=tk.NW)

&#x20;       else:

&#x20;           self.chart\_canvas.create\_text(

&#x20;               200, 150,

&#x20;               text="无消费记录，无法生成图表",

&#x20;               fill="gray",

&#x20;               font=("Arial", 12)

&#x20;           )

&#x20;   def check\_budget\_alert(self):

&#x20;       current\_month = datetime.now().strftime("%B")

&#x20;       budget = self.excel\_handler.get\_budget(current\_month)

&#x20;       if budget:

&#x20;           threshold = budget.budget\_amount \* 0.9  # 90%的预算阈值

&#x20;           if budget.remaining < threshold and not hasattr(self, 'alert\_shown'):

&#x20;               messagebox.showwarning("预算提醒", "已接近月度预算限额！")

&#x20;               self.alert\_shown = True  # 确保只提醒一次

&#x20;           elif budget.remaining >= threshold:

&#x20;               self.alert\_shown = False  # 重置提醒状态

&#x20;      &#x20;

&#x20;       # 每小时检查一次预算状态

&#x20;       self.master.after(3600000, self.check\_budget\_alert)

&#x20;   def refresh\_data(self):

&#x20;       self.load\_expenses()

&#x20;       self.update\_chart()

&#x20;       self.load\_budget(self.month\_combobox.get())

&#x20;   def generate\_monthly\_report(self):

&#x20;       from report\_generator import generate\_monthly\_report

&#x20;       current\_month = datetime.now().strftime("%B")

&#x20;       generate\_monthly\_report(current\_month, self.excel\_handler)

&#x20;       messagebox.showinfo("报告生成", "月度报告已生成！")
```

### 3.3 添加消费记录窗口

创建一个用于添加新消费记录的子窗口：



```
class AddExpenseWindow:

&#x20;   def \_\_init\_\_(self, master, excel\_handler, main\_gui):

&#x20;       self.master = master

&#x20;       self.master.title("添加消费记录")

&#x20;       self.excel\_handler = excel\_handler

&#x20;       self.main\_gui = main\_gui

&#x20;      &#x20;

&#x20;       \# 设置窗口大小和位置

&#x20;       window\_width = 300

&#x20;       window\_height = 200

&#x20;       screen\_width = self.master.winfo\_screenwidth()

&#x20;       screen\_height = self.master.winfo\_screenheight()

&#x20;       x\_position = (screen\_width - window\_width) // 2

&#x20;       y\_position = (screen\_height - window\_height) // 2

&#x20;       self.master.geometry(f"{window\_width}x{window\_height}+{x\_position}+{y\_position}")

&#x20;      &#x20;

&#x20;       \# 创建输入组件

&#x20;       self.create\_widgets()

&#x20;      &#x20;

&#x20;   def create\_widgets(self):

&#x20;       \# 金额输入

&#x20;       ttk.Label(self.master, text="金额:").grid(row=0, column=0, padx=5, pady=5)

&#x20;       self.amount\_entry = ttk.Entry(self.master)

&#x20;       self.amount\_entry.grid(row=0, column=1, padx=5, pady=5)

&#x20;      &#x20;

&#x20;       \# 类别选择

&#x20;       ttk.Label(self.master, text="类别:").grid(row=1, column=0, padx=5, pady=5)

&#x20;       self.category\_combobox = ttk.Combobox(self.master, values=\[

&#x20;           "餐饮", "交通", "学习", "娱乐", "日用品", "其他"

&#x20;       ], state="readonly")

&#x20;       self.category\_combobox.set("餐饮")

&#x20;       self.category\_combobox.grid(row=1, column=1, padx=5, pady=5)

&#x20;      &#x20;

&#x20;       \# 说明输入

&#x20;       ttk.Label(self.master, text="说明:").grid(row=2, column=0, padx=5, pady=5)

&#x20;       self.description\_entry = ttk.Entry(self.master)

&#x20;       self.description\_entry.grid(row=2, column=1, padx=5, pady=5)

&#x20;      &#x20;

&#x20;       \# 确定按钮

&#x20;       ttk.Button(self.master, text="确定", command=self.save\_expense).grid(

&#x20;           row=3,

&#x20;           column=0,

&#x20;           columnspan=2,

&#x20;           pady=5

&#x20;       )

&#x20;      &#x20;

&#x20;   def save\_expense(self):

&#x20;       try:

&#x20;           amount = float(self.amount\_entry.get())

&#x20;           category = self.category\_combobox.get()

&#x20;           description = self.description\_entry.get()

&#x20;           date = datetime.now()

&#x20;          &#x20;

&#x20;           if amount <= 0:

&#x20;               raise ValueError("金额必须大于0！")

&#x20;              &#x20;

&#x20;           expense = Expense(date, amount, category, description)

&#x20;           self.main\_gui.add\_new\_expense(expense)

&#x20;           self.master.destroy()

&#x20;       except ValueError as e:

&#x20;           messagebox.showerror("错误", str(e))
```

### 3.4 月度报告生成模块

创建一个独立的报告生成模块，用于生成 PDF 格式的月度报告：



```
from fpdf import FPDF

from datetime import datetime

from openpyxl import load\_workbook

def generate\_monthly\_report(month, excel\_handler):

&#x20;   \# 创建PDF对象

&#x20;   pdf = FPDF()

&#x20;   pdf.add\_page()

&#x20;  &#x20;

&#x20;   \# 设置字体

&#x20;   pdf.set\_font("Arial", size=12)

&#x20;  &#x20;

&#x20;   \# 报告标题

&#x20;   pdf.cell(200, 10, txt=f"{month}月消费报告", ln=1, align="C")

&#x20;  &#x20;

&#x20;   \# 生成时间

&#x20;   pdf.cell(200, 10, txt=f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1, align="R")

&#x20;  &#x20;

&#x20;   \# 消费记录标题

&#x20;   pdf.set\_font("Arial", "B", size=12)

&#x20;   pdf.cell(200, 10, txt="本月消费记录", ln=1, align="L")

&#x20;   pdf.set\_font("Arial", size=10)

&#x20;  &#x20;

&#x20;   \# 获取本月消费记录

&#x20;   expenses = excel\_handler.get\_all\_expenses()

&#x20;   monthly\_expenses = \[expense for expense in expenses if expense.date.strftime("%B") == month]

&#x20;  &#x20;

&#x20;   \# 显示消费记录表格

&#x20;   if monthly\_expenses:

&#x20;       pdf.ln(5)

&#x20;       pdf.set\_font("Arial", "B", size=10)

&#x20;       pdf.cell(40, 10, "日期", border=1)

&#x20;       pdf.cell(50, 10, "类别", border=1)

&#x20;       pdf.cell(80, 10, "说明", border=1)

&#x20;       pdf.cell(30, 10, "金额", border=1, ln=1)

&#x20;      &#x20;

&#x20;       pdf.set\_font("Arial", size=10)

&#x20;       for expense in monthly\_expenses:

&#x20;           pdf.cell(40, 10, expense.date.strftime("%Y-%m-%d"), border=1)

&#x20;           pdf.cell(50, 10, expense.category, border=1)

&#x20;           pdf.cell(80, 10, expense.description, border=1)

&#x20;           pdf.cell(30, 10, f"{expense.amount:.1f} 元", border=1, ln=1)

&#x20;   else:

&#x20;       pdf.cell(200, 10, "本月无消费记录", ln=1)

&#x20;  &#x20;

&#x20;   \# 预算信息

&#x20;   pdf.ln(10)

&#x20;   pdf.set\_font("Arial", "B", size=12)

&#x20;   pdf.cell(200, 10, txt="本月预算情况", ln=1, align="L")

&#x20;   pdf.set\_font("Arial", size=10)

&#x20;  &#x20;

&#x20;   budget = excel\_handler.get\_budget(month)

&#x20;   if budget:

&#x20;       pdf.cell(200, 10, f"预算总额: {budget.budget\_amount:.1f} 元", ln=1)

&#x20;       pdf.cell(200, 10, f"已用金额: {budget.spent:.1f} 元", ln=1)

&#x20;       pdf.cell(200, 10, f"剩余金额: {budget.remaining:.1f} 元", ln=1)

&#x20;   else:

&#x20;       pdf.cell(200, 10, "本月未设置预算", ln=1)

&#x20;  &#x20;

&#x20;   \# 消费分类统计

&#x20;   pdf.ln(10)

&#x20;   pdf.set\_font("Arial", "B", size=12)

&#x20;   pdf.cell(200, 10, txt="消费分类统计", ln=1, align="L")

&#x20;   pdf.set\_font("Arial", size=10)

&#x20;  &#x20;

&#x20;   statistics = excel\_handler.get\_category\_statistics()

&#x20;   if statistics:

&#x20;       pdf.ln(5)

&#x20;       pdf.set\_font("Arial", "B", size=10)

&#x20;       pdf.cell(80, 10, "类别", border=1)

&#x20;       pdf.cell(80, 10, "总消费", border=1)

&#x20;       pdf.cell(40, 10, "占比", border=1, ln=1)

&#x20;      &#x20;

&#x20;       pdf.set\_font("Arial", size=10)

&#x20;       for stat in statistics:

&#x20;           pdf.cell(80, 10, stat\[0], border=1)

&#x20;           pdf.cell(80, 10, f"{stat\[1]:.1f} 元", border=1)

&#x20;           pdf.cell(40, 10, stat\[2], border=1, ln=1)

&#x20;   else:

&#x20;       pdf.cell(200, 10, "无消费记录，无法生成分类统计", ln=1)

&#x20;  &#x20;

&#x20;   \# 保存PDF文件

&#x20;   report\_filename = f"{month}月消费报告.pdf"

&#x20;   pdf.output(report\_filename, "F")
```

## 四、系统功能增强与优化

### 4.1 预算提醒功能优化

当前系统已经实现了基本的预算提醒功能，但可以进一步优化：



1.  **多种提醒方式**：除了弹出窗口，还可以添加系统通知或声音提醒

2.  **自定义提醒阈值**：允许用户设置不同的提醒阈值（如 80%、90%、100%）

3.  **历史提醒记录**：记录所有预算提醒事件，方便查看



```
\# 在ExpenseManagerGUI类中添加提醒设置功能

def create\_budget\_alert\_settings(self):

&#x20;   alert\_frame = ttk.LabelFrame(self.main\_frame, text="预算提醒设置")

&#x20;   alert\_frame.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

&#x20;  &#x20;

&#x20;   ttk.Label(alert\_frame, text="提醒阈值:").grid(row=0, column=0, padx=5, pady=5)

&#x20;   self.alert\_threshold = ttk.Entry(alert\_frame)

&#x20;   self.alert\_threshold.grid(row=0, column=1, padx=5, pady=5)

&#x20;   self.alert\_threshold.insert(0, "90")  # 默认90%

&#x20;  &#x20;

&#x20;   ttk.Button(alert\_frame, text="保存设置", command=self.save\_alert\_settings).grid(

&#x20;       row=0,

&#x20;       column=2,

&#x20;       padx=5,

&#x20;       pady=5

&#x20;   )

&#x20;  &#x20;

&#x20;   \# 加载现有设置（如果有）

&#x20;   self.load\_alert\_settings()

&#x20;  &#x20;

def load\_alert\_settings(self):

&#x20;   try:

&#x20;       with open("alert\_settings.txt", "r") as f:

&#x20;           threshold = f.read().strip()

&#x20;           if threshold:

&#x20;               self.alert\_threshold.delete(0, tk.END)

&#x20;               self.alert\_threshold.insert(0, threshold)

&#x20;   except FileNotFoundError:

&#x20;       pass

def save\_alert\_settings(self):

&#x20;   try:

&#x20;       threshold = int(self.alert\_threshold.get())

&#x20;       if 0 <= threshold <= 100:

&#x20;           with open("alert\_settings.txt", "w") as f:

&#x20;               f.write(str(threshold))

&#x20;           messagebox.showinfo("设置保存", "提醒阈值设置成功！")

&#x20;       else:

&#x20;           raise ValueError("阈值必须在0到100之间！")

&#x20;   except ValueError as e:

&#x20;       messagebox.showerror("错误", str(e))

def check\_budget\_alert(self):

&#x20;   try:

&#x20;       with open("alert\_settings.txt", "r") as f:

&#x20;           threshold = int(f.read().strip())

&#x20;   except (FileNotFoundError, ValueError):

&#x20;       threshold = 90  # 默认值

&#x20;  &#x20;

&#x20;   current\_month = datetime.now().strftime("%B")

&#x20;   budget = self.excel\_handler.get\_budget(current\_month)

&#x20;   if budget:

&#x20;       threshold\_amount = budget.budget\_amount \* threshold / 100

&#x20;       if budget.remaining < threshold\_amount and not hasattr(self, 'alert\_shown'):

&#x20;           messagebox.showwarning("预算提醒", f"已接近月度预算限额（剩余{budget.remaining:.1f}元）！")

&#x20;           self.alert\_shown = True

&#x20;       elif budget.remaining >= threshold\_amount:

&#x20;           self.alert\_shown = False

&#x20;  &#x20;

&#x20;   \# 每小时检查一次预算状态

&#x20;   self.master.after(3600000, self.check\_budget\_alert)
```

### 4.2 消费记录查询与过滤

为了方便用户查找特定消费记录，可以添加查询和过滤功能：



```
\# 在ExpenseManagerGUI类中添加查询功能

def create\_search\_section(self):

&#x20;   search\_frame = ttk.LabelFrame(self.main\_frame, text="消费记录查询")

&#x20;   search\_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

&#x20;  &#x20;

&#x20;   self.search\_entry = ttk.Entry(search\_frame)

&#x20;   self.search\_entry.grid(row=0, column=0, padx=5, pady=5)

&#x20;  &#x20;

&#x20;   self.search\_button = ttk.Button(search\_frame, text="搜索", command=self.search\_expenses)

&#x20;   self.search\_button.grid(row=0, column=1, padx=5, pady=5)

&#x20;  &#x20;

&#x20;   self.search\_type = ttk.Combobox(search\_frame, values=\["全部", "日期", "类别", "说明"], state="readonly")

&#x20;   self.search\_type.set("全部")

&#x20;   self.search\_type.grid(row=0, column=2, padx=5, pady=5)

def search\_expenses(self):

&#x20;   query = self.search\_entry.get().strip()

&#x20;   search\_type = self.search\_type.get()

&#x20;  &#x20;

&#x20;   \# 清空现有数据

&#x20;   for item in self.expense\_tree.get\_children():

&#x20;       self.expense\_tree.delete(item)

&#x20;  &#x20;

&#x20;   \# 加载匹配数据

&#x20;   expenses = self.excel\_handler.get\_all\_expenses()

&#x20;   for expense in expenses:

&#x20;       match = False

&#x20;       if search\_type == "全部":

&#x20;           if query.lower() in str(expense.amount).lower() or \\

&#x20;              query.lower() in expense.category.lower() or \\

&#x20;              query.lower() in expense.description.lower() or \\

&#x20;              query.lower() in expense.date.strftime("%Y-%m-%d").lower():

&#x20;               match = True

&#x20;       elif search\_type == "日期":

&#x20;           if query.lower() in expense.date.strftime("%Y-%m-%d").lower():

&#x20;               match = True

&#x20;       elif search\_type == "类别":

&#x20;           if query.lower() in expense.category.lower():

&#x20;               match = True

&#x20;       elif search\_type == "说明":

&#x20;           if query.lower() in expense.description.lower():

&#x20;               match = True

&#x20;      &#x20;

&#x20;       if match:

&#x20;           self.expense\_tree.insert(

&#x20;               "",

&#x20;               tk.END,

&#x20;               values=(

&#x20;                   f"{expense.amount:.1f} 元",

&#x20;                   expense.category,

&#x20;                   expense.description,

&#x20;                   expense.date.strftime("%Y-%m-%d")

&#x20;               )

&#x20;           )
```

### 4.3 数据备份与恢复功能

为了防止数据丢失，可以添加数据备份和恢复功能：



```
import shutil

import os

\# 在ExpenseManagerGUI类中添加备份和恢复功能

def create\_backup\_section(self):

&#x20;   backup\_frame = ttk.LabelFrame(self.main\_frame, text="数据备份与恢复")

&#x20;   backup\_frame.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

&#x20;  &#x20;

&#x20;   ttk.Button(backup\_frame, text="创建备份", command=self.create\_backup).grid(

&#x20;       row=0,

&#x20;       column=0,

&#x20;       padx=5,

&#x20;       pady=5

&#x20;   )

&#x20;  &#x20;

&#x20;   ttk.Button(backup\_frame, text="恢复备份", command=self.restore\_backup).grid(

&#x20;       row=0,

&#x20;       column=1,

&#x20;       padx=5,

&#x20;       pady=5

&#x20;   )

def create\_backup(self):

&#x20;   backup\_dir = "expenses\_backup"

&#x20;   os.makedirs(backup\_dir, exist\_ok=True)

&#x20;  &#x20;

&#x20;   timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

&#x20;   backup\_filename = f"expenses\_{timestamp}.xlsx"

&#x20;   backup\_path = os.path.join(backup\_dir, backup\_filename)

&#x20;  &#x20;

&#x20;   shutil.copyfile("expenses.xlsx", backup\_path)

&#x20;   messagebox.showinfo("备份成功", f"备份文件已保存至：{backup\_path}")

def restore\_backup(self):

&#x20;   backup\_dir = "expenses\_backup"

&#x20;   if not os.path.exists(backup\_dir) or not os.listdir(backup\_dir):

&#x20;       messagebox.showerror("无备份", "没有可用的备份文件！")

&#x20;       return

&#x20;  &#x20;

&#x20;   \# 创建选择备份文件的窗口

&#x20;   restore\_window = tk.Toplevel(self.master)

&#x20;   RestoreBackupWindow(restore\_window, backup\_dir, self)
```

### 4.4 界面美化与用户体验优化

为了提升系统的可用性和美观度，可以进行以下界面优化：



1.  **使用主题**：应用 ttk 主题，改善界面外观

2.  **响应式布局**：使界面在不同窗口大小下保持良好布局

3.  **键盘快捷键**：为常用功能添加快捷键

4.  **工具提示**：为按钮和输入框添加提示信息

5.  **数据验证**：在输入时进行数据验证和格式检查



```
\# 设置应用主题

ttk.Style().theme\_use('clam')  # 可选主题包括 'winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'

\# 添加工具提示

def create\_tooltips(self):

&#x20;   from tkinter import messagebox

&#x20;  &#x20;

&#x20;   \# 为预算设置按钮添加工具提示

&#x20;   self.set\_budget\_button.bind(

&#x20;       "\<Enter>",

&#x20;       lambda e: messagebox.showinfo("提示", "设置本月预算金额")

&#x20;   )

&#x20;  &#x20;

&#x20;   \# 为添加消费按钮添加工具提示

&#x20;   self.add\_expense\_button.bind(

&#x20;       "\<Enter>",

&#x20;       lambda e: messagebox.showinfo("提示", "添加新的消费记录")

&#x20;   )

&#x20;  &#x20;

&#x20;   \# 为生成报告按钮添加工具提示

&#x20;   self.generate\_report\_button.bind(

&#x20;       "\<Enter>",

&#x20;       lambda e: messagebox.showinfo("提示", "生成本月消费报告")

&#x20;   )
```

## 五、系统测试与部署

### 5.1 系统测试方案

在完成系统开发后，需要进行全面的测试以确保其稳定性和正确性：



1.  **功能测试**：

*   测试预算设置和更新功能

*   测试消费记录的添加、编辑和删除

*   测试分类统计和图表生成

*   测试预算提醒功能

*   测试月度报告生成

1.  **边界测试**：

*   输入极端值（如 0 或极大的预算金额）

*   不输入必填项

*   输入特殊字符和符号

1.  **性能测试**：

*   大量消费记录的加载和显示性能

*   长时间运行后的内存使用情况

*   大数据量下的图表生成速度

1.  **兼容性测试**：

*   在不同操作系统上的运行情况

*   不同 Python 版本的兼容性

### 5.2 系统部署与发布

完成测试后，可以将系统部署到目标环境中：



1.  **打包成可执行文件**：

    使用 PyInstaller 将 Python 脚本打包成独立的可执行文件，方便在没有 Python 环境的电脑上运行：



```
pip install pyinstaller

pyinstaller --onefile --windowed main.py
```



1.  **创建安装包**：

    为系统创建安装程序，包含必要的说明文档和快捷方式：



```
\# 使用Inno Setup或其他安装工具创建安装包
```



1.  **系统配置**：

*   确保 Excel 文件路径正确

*   设置合适的文件权限

*   配置系统环境变量（如有需要）

1.  **用户文档**：

    创建用户手册，包含：

*   系统安装与配置指南

*   基本操作流程

*   常见问题解答

*   数据备份与恢复说明

## 六、系统扩展与未来发展

### 6.1 系统功能扩展方向

基于当前系统，可以考虑以下扩展方向：



1.  **多用户支持**：添加用户认证系统，支持多个用户使用同一系统

2.  **云同步功能**：将数据同步到云存储，实现多设备访问

3.  **消费预测**：基于历史数据预测未来消费趋势

4.  **目标设定**：添加储蓄目标和消费计划功能

5.  **第三方服务集成**：

*   与银行账户或支付平台连接，自动导入交易记录

*   与记账应用或财务软件进行数据交换

### 6.2 技术升级路径

随着技术的发展，可以考虑以下技术升级：



1.  **迁移到更现代的 GUI 框架**：

*   使用 PyQt5 或 PySide6 替代 Tkinter，获得更丰富的界面组件

*   使用 Web 技术（如 Electron）构建跨平台应用

1.  **数据库升级**：

*   从 Excel 文件存储迁移到 SQLite 或 MySQL 数据库

*   使用 ORM（对象关系映射）工具简化数据操作

1.  **增强数据分析能力**：

*   使用 Pandas 库进行更复杂的数据分析

*   集成机器学习模型进行消费行为分析

1.  **自动化报表生成**：

*   使用更专业的报告生成工具

*   添加图表自定义和导出功能

## 七、总结与收获

通过本指南，你已经学会了如何使用 Python 的 Tkinter 库和 Excel 构建一个功能完备的大学生消费管理系统。这个系统不仅满足了基本的消费记录和预算管理需求，还提供了分类统计、可视化分析和月度报告等高级功能。

在开发过程中，你掌握了以下关键技能：



1.  使用 Tkinter 创建图形用户界面

2.  使用 openpyxl 库操作 Excel 文件

3.  在 Tkinter 中嵌入 matplotlib 图表

4.  实现数据持久化和自动同步

5.  开发自定义报告生成功能

6.  系统测试与部署方法

这个项目不仅可以帮助你管理个人消费，还可以作为进一步学习 Python GUI 开发和数据处理的基础。通过不断优化和扩展，可以将其发展成为一个专业的财务管理工具。

希望本指南能为你提供有价值的参考，帮助你在编程学习和个人财务管理方面都取得进步！

## 八、附录：完整代码结构



```
大学生消费管理系统/

├── expenses.xlsx          # 数据存储文件

├── main.py                # 主程序

├── excel\_handler.py       # Excel操作模块

├── gui.py                 # GUI模块

├── report\_generator.py    # 报告生成模块

├── backup\_restore.py      # 备份恢复模块

└── requirements.txt       # 依赖库列表
```



```
\# requirements.txt文件内容

openpyxl==3.1.2

matplotlib==3.7.2

fpdf==1.7.2

pyinstaller==5.13.0
```

**参考资料 **

\[1] Building a Money Manager with Python and Tkinter[ https://codepal.ai/code-generator/query/Q2pmIWhJ/python-money-manager-application-tkinter-csv-import](https://codepal.ai/code-generator/query/Q2pmIWhJ/python-money-manager-application-tkinter-csv-import)

\[2] Building a Money Manager with Python and Tkinter[ https://codepal.ai/code-generator/query/U7JvmUxl/python-code-money-manager-application-tkinter](https://codepal.ai/code-generator/query/U7JvmUxl/python-code-money-manager-application-tkinter)

\[3] nureddinhaji/expenses-tracker[ https://github.com/nureddinhaji/expenses-tracker](https://github.com/nureddinhaji/expenses-tracker)

\[4] finance-tracker[ https://github.com/topics/finance-tracker?l=python](https://github.com/topics/finance-tracker?l=python)

\[5] Expense Tracker[ https://github.com/InfectedDuck/Expense-tracker-with-tkinter/](https://github.com/InfectedDuck/Expense-tracker-with-tkinter/)

\[6] budget[ https://github.com/topics/budget?l=python\&o=desc\&s=updated](https://github.com/topics/budget?l=python\&o=desc\&s=updated)

\[7] adarshsonkusre/Automated-Python-Budget-Tracker-Application[ https://github.com/adarshsonkusre/Automated-Python-Budget-Tracker-Application](https://github.com/adarshsonkusre/Automated-Python-Budget-Tracker-Application)

\[8] 使用tkinter制作一款商品选择器持续创作，加速成长!这是我参与「掘金日新计划 · 6 月更文挑战」的第25天， 需求 - 掘金[ https://juejin.cn/post/7110864885398913054](https://juejin.cn/post/7110864885398913054)

\[9] 用python写了一个简易的记账软件，后期有可能更新!记账程序由来曾经在iOS14的快截指令中写了一个快捷指令用来记账， - 掘金[ https://juejin.cn/post/6889685014222094349](https://juejin.cn/post/6889685014222094349)

\[10] Excel表格数据同步:提升办公效率的必备技巧\_工作\_功能\_用户[ https://m.sohu.com/a/830374431\_121798711/](https://m.sohu.com/a/830374431_121798711/)

\[11] 学生成绩管理系统-python+Tkinter淘宝店铺搜索:点创微科 学生成绩管理系统-python+Tkinter 一 - 掘金[ https://juejin.cn/post/7430866198290710567](https://juejin.cn/post/7430866198290710567)

\[12] 基于python的学生信息管理系统 用的文件存储，tkinter库-抖音[ https://www.iesdouyin.com/share/video/7543899553687260466/?did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&from\_aid=1128\&from\_ssr=1\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&mid=7543899593709194026\&region=\&scene\_from=dy\_open\_search\_video\&share\_sign=YKP0BrztgnVA2VSiDkkqGQ5Esgvx150JNrFad1T5QMA-\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D\&share\_version=280700\&titleType=title\&ts=1756913117\&u\_code=0\&video\_share\_track\_ver=\&with\_sec\_did=1](https://www.iesdouyin.com/share/video/7543899553687260466/?did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&from_aid=1128\&from_ssr=1\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&mid=7543899593709194026\&region=\&scene_from=dy_open_search_video\&share_sign=YKP0BrztgnVA2VSiDkkqGQ5Esgvx150JNrFad1T5QMA-\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D\&share_version=280700\&titleType=title\&ts=1756913117\&u_code=0\&video_share_track_ver=\&with_sec_did=1)

\[13] #python教程：用Tkinter制作#学生信息管理系统-02登陆页制作 #python#编程#程序员 #计算机#电脑知识#互联网 #学习 -抖音[ https://www.iesdouyin.com/share/video/7087929863906037022/?did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&from\_aid=1128\&from\_ssr=1\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&mid=7087930042714262280\&region=\&scene\_from=dy\_open\_search\_video\&share\_sign=2jT9XH7n0r.Za\_lqbvti5kn5pGyQc6dXBu2KqAcYgu8-\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D\&share\_version=280700\&titleType=title\&ts=1756913117\&u\_code=0\&video\_share\_track\_ver=\&with\_sec\_did=1](https://www.iesdouyin.com/share/video/7087929863906037022/?did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&from_aid=1128\&from_ssr=1\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&mid=7087930042714262280\&region=\&scene_from=dy_open_search_video\&share_sign=2jT9XH7n0r.Za_lqbvti5kn5pGyQc6dXBu2KqAcYgu8-\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D\&share_version=280700\&titleType=title\&ts=1756913117\&u_code=0\&video_share_track_ver=\&with_sec_did=1)

\[14] Python课设-学生成绩管理系统tkinter 该项目使用到了Python内置模块tkinter ，导出数据使用到了openpyxl，该项目，实现了教师注册，教师登录，教师退出，在教师登录成绩之后，实现了学生成绩信息的查询、修改、删除、清空、保存，成绩排序等功能。-抖音[ https://www.iesdouyin.com/share/video/7478539595664084263/?did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&from\_aid=1128\&from\_ssr=1\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&mid=7478539180079991591\&region=\&scene\_from=dy\_open\_search\_video\&share\_sign=ZshqIdVRrST67YDsnTrtyEKO1ec1FKNm4CGd3GQdZUc-\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D\&share\_version=280700\&titleType=title\&ts=1756913117\&u\_code=0\&video\_share\_track\_ver=\&with\_sec\_did=1](https://www.iesdouyin.com/share/video/7478539595664084263/?did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&from_aid=1128\&from_ssr=1\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&mid=7478539180079991591\&region=\&scene_from=dy_open_search_video\&share_sign=ZshqIdVRrST67YDsnTrtyEKO1ec1FKNm4CGd3GQdZUc-\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D\&share_version=280700\&titleType=title\&ts=1756913117\&u_code=0\&video_share_track_ver=\&with_sec_did=1)

\[15] Personal Finance Management with Python[ https://codepal.ai/code-generator/query/Vd7AwsQk/personal-finance-manager-python-tkinter](https://codepal.ai/code-generator/query/Vd7AwsQk/personal-finance-manager-python-tkinter)

\[16] Excel Budget Tracker in Python[ https://codepal.ai/code-generator/query/VF78zJAr/python-budget-tracker-excel-app](https://codepal.ai/code-generator/query/VF78zJAr/python-budget-tracker-excel-app)

\[17] Financial-planner[ https://github.com/EremiteWolf/Financial-planner/blob/main/README.md](https://github.com/EremiteWolf/Financial-planner/blob/main/README.md)

\[18] Tkinter Excel Automation GUI[ https://github.com/zarnabkh/tkinter-excel-automation](https://github.com/zarnabkh/tkinter-excel-automation)

\[19] Financial Tracker App using tkinter[ https://codepal.ai/code-generator/query/eMZ4YQRc/financial-tracker-app](https://codepal.ai/code-generator/query/eMZ4YQRc/financial-tracker-app)

\[20] Expense Tracking Application Using Python Tkinter[ https://pythonguides.com/expense-tracking-application-using-python-tkinter/](https://pythonguides.com/expense-tracking-application-using-python-tkinter/)

\[21] python\_exel\_app[ https://github.com/marybadalyan/python\_excel\_app](https://github.com/marybadalyan/python_excel_app)

\[22] Basic pie chart[ https://matplotlib.org/3.0.3/gallery/pie\_and\_polar\_charts/pie\_features.html](https://matplotlib.org/3.0.3/gallery/pie_and_polar_charts/pie_features.html)

\[23] Pie Demo2[ https://matplotlib.org/3.3.2/gallery/pie\_and\_polar\_charts/pie\_demo2.html](https://matplotlib.org/3.3.2/gallery/pie_and_polar_charts/pie_demo2.html)

\[24] pie(x)[ https://matplotlib.org/stable/plot\_types/stats/pie.html](https://matplotlib.org/stable/plot_types/stats/pie.html)

\[25] Pie Demo2[ https://matplotlib.org/2.2.4/gallery/pie\_and\_polar\_charts/pie\_demo2.html](https://matplotlib.org/2.2.4/gallery/pie_and_polar_charts/pie_demo2.html)

\[26] 用 Python 让数据自己‘涨’起来！ 手把手教你用 Matplotlib 实现数据动态增长效果！-抖音[ https://www.iesdouyin.com/share/video/7519121669848403234/?did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&from\_aid=1128\&from\_ssr=1\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&mid=7519121869358844735\&region=\&scene\_from=dy\_open\_search\_video\&share\_sign=wG6UqS5CinWRLBeLw\_Dw\_ZLiCAg2km9k4DXG71qWJvs-\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D\&share\_version=280700\&titleType=title\&ts=1756913155\&u\_code=0\&video\_share\_track\_ver=\&with\_sec\_did=1](https://www.iesdouyin.com/share/video/7519121669848403234/?did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&from_aid=1128\&from_ssr=1\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&mid=7519121869358844735\&region=\&scene_from=dy_open_search_video\&share_sign=wG6UqS5CinWRLBeLw_Dw_ZLiCAg2km9k4DXG71qWJvs-\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D\&share_version=280700\&titleType=title\&ts=1756913155\&u_code=0\&video_share_track_ver=\&with_sec_did=1)

\[27] 在PyQT窗体上显示matplotlib折线图示例-抖音[ https://www.iesdouyin.com/share/video/7368042461588933898/?did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&from\_aid=1128\&from\_ssr=1\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&mid=7368042565293132563\&region=\&scene\_from=dy\_open\_search\_video\&share\_sign=vQdrgAWA.nnRCZ11w6a6k.W1uL0cRQELxAigWY48i98-\&share\_track\_info=%7B%22link\_description\_type%22%3A%22%22%7D\&share\_version=280700\&titleType=title\&ts=1756913155\&u\_code=0\&video\_share\_track\_ver=\&with\_sec\_did=1](https://www.iesdouyin.com/share/video/7368042461588933898/?did=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&from_aid=1128\&from_ssr=1\&iid=MS4wLjABAAAANwkJuWIRFOzg5uCpDRpMj4OX-QryoDgn-yYlXQnRwQQ\&mid=7368042565293132563\&region=\&scene_from=dy_open_search_video\&share_sign=vQdrgAWA.nnRCZ11w6a6k.W1uL0cRQELxAigWY48i98-\&share_track_info=%7B%22link_description_type%22%3A%22%22%7D\&share_version=280700\&titleType=title\&ts=1756913155\&u_code=0\&video_share_track_ver=\&with_sec_did=1)

\[28] Python Reminder Window with Countdown using tkinter[ https://codepal.ai/code-generator/query/P65UnMf7/python-reminder-window](https://codepal.ai/code-generator/query/P65UnMf7/python-reminder-window)

\[29] \[Tkinter] Reminder[ https://python-forum.io/thread-25252.html](https://python-forum.io/thread-25252.html)

\[30] Python | after method in Tkinter[ https://www.geeksforgeeks.org/python-after-method-in-tkinter/](https://www.geeksforgeeks.org/python-after-method-in-tkinter/)

\[31] Python Reminder Function with GUI[ https://codepal.ai/code-generator/query/ubbVMR8n/python-reminder-function-gui](https://codepal.ai/code-generator/query/ubbVMR8n/python-reminder-function-gui)

\[32] xl-reports 0.1.3[ https://pypi.org/project/xl-reports/](https://pypi.org/project/xl-reports/)

\[33] komanaki/earg[ https://github.com/komanaki/earg](https://github.com/komanaki/earg)

\[34] nevenjer/revenue-report-extractor[ https://github.com/nevenjer/revenue-report-extractor](https://github.com/nevenjer/revenue-report-extractor)

\[35] The Best Python Libraries for Excel in 2025[ https://www.sheetflash.com/blog/the-best-python-libraries-for-excel-in-2024](https://www.sheetflash.com/blog/the-best-python-libraries-for-excel-in-2024)

\[36] Plot & Button using Grid in tkinter[ https://discuss.python.org/t/plot-button-using-grid-in-tkinter/103322](https://discuss.python.org/t/plot-button-using-grid-in-tkinter/103322)

\[37] Embedding in Tk Canvas[ https://matplotlib.org/2.2.3/gallery/user\_interfaces/embedding\_in\_tk\_canvas\_sgskip.html](https://matplotlib.org/2.2.3/gallery/user_interfaces/embedding_in_tk_canvas_sgskip.html)

\[38] user\_interfaces example code: embedding\_in\_tk.py[ https://omz-software.com/pythonista2/docs/matplotlib/examples/user\_interfaces/embedding\_in\_tk.html](https://omz-software.com/pythonista2/docs/matplotlib/examples/user_interfaces/embedding_in_tk.html)

\[39] Unable to view networkx graph plot while embedding matplotlib[ https://github.com/TomSchimansky/CustomTkinter/issues/971](https://github.com/TomSchimansky/CustomTkinter/issues/971)

\[40] Plotting data using tkinter-based libraries (matplotlib, seaborn)[ https://noobtomaster.com/python-gui-tkinter/plotting-data-using-tkinter-based-libraries-matplotlib-seaborn/](https://noobtomaster.com/python-gui-tkinter/plotting-data-using-tkinter-based-libraries-matplotlib-seaborn/)

\[41] PySimpleGUI/Demo\_Matplotlib\_Embedded\_Toolbar.py at master · PySimpleGUI/PySimpleGUI · GitHub[ https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo\_Matplotlib\_Embedded\_Toolbar.py](https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Matplotlib_Embedded_Toolbar.py)

\[42] Excel Automation with Python (project)[ https://codefinity.com/courses/projects/812d70bd-8fd5-4d01-ae09-22f6da6cbdea/b0ef5b4c-df73-4ce9-886a-ea0945daf587/46d4b453-f415-4d39-9857-1d52aa3f33eb](https://codefinity.com/courses/projects/812d70bd-8fd5-4d01-ae09-22f6da6cbdea/b0ef5b4c-df73-4ce9-886a-ea0945daf587/46d4b453-f415-4d39-9857-1d52aa3f33eb)

\[43] openpyxl.workbook.workbook module[ https://openpyxl.readthedocs.io/en/3.0/api/openpyxl.workbook.workbook.html](https://openpyxl.readthedocs.io/en/3.0/api/openpyxl.workbook.workbook.html)

\[44] TUR14CUS/Invoices-Generator[ https://github.com/TUR14CUS/Invoices-Generator](https://github.com/TUR14CUS/Invoices-Generator)

\[45] avinesh-masih/employee-report-generator[ https://github.com/avinesh-masih/employee-report-generator](https://github.com/avinesh-masih/employee-report-generator)

\[46] Charanvir/Invoice-PDF[ https://github.com/Charanvir/Invoice-PDF](https://github.com/Charanvir/Invoice-PDF)

\[47] Converting Excel to PDF Files in Python[ https://docs.aspose.com/cells/java/converting-excel-to-pdf-files-in-python/](https://docs.aspose.com/cells/java/converting-excel-to-pdf-files-in-python/)

\[48] Create PDF File in Python[ https://products.aspose.com/cells/python-java/create/pdf/](https://products.aspose.com/cells/python-java/create/pdf/)

\[49] Export WORKBOOK to PDF from Excel[ https://products.aspose.cloud/cells/python/export/workbook-to-pdf/](https://products.aspose.cloud/cells/python/export/workbook-to-pdf/)

\[50] Pie charts[ https://matplotlib.org/3.8.1/gallery/pie\_and\_polar\_charts/pie\_features.html](https://matplotlib.org/3.8.1/gallery/pie_and_polar_charts/pie_features.html)

\[51] Pie Demo2[ https://matplotlib.org/2.1.2/gallery/pie\_and\_polar\_charts/pie\_demo2.html](https://matplotlib.org/2.1.2/gallery/pie_and_polar_charts/pie_demo2.html)

\[52] Bar of pie[ https://matplotlib.org/3.2.1/gallery/pie\_and\_polar\_charts/bar\_of\_pie.html](https://matplotlib.org/3.2.1/gallery/pie_and_polar_charts/bar_of_pie.html)

\[53] Basic pie chart[ https://matplotlib.org/2.2.3/gallery/pie\_and\_polar\_charts/pie\_features.html](https://matplotlib.org/2.2.3/gallery/pie_and_polar_charts/pie_features.html)

\[54] Generating pie charts[ https://www.oreilly.com/library/view/hands-on-data-science/9781787280748/3874e44c-bdb3-4f82-b7f8-d947e0cec469.xhtml](https://www.oreilly.com/library/view/hands-on-data-science/9781787280748/3874e44c-bdb3-4f82-b7f8-d947e0cec469.xhtml)

\[55] openpyxl and saving xlsm files[ https://python-forum.io/thread-8966.html](https://python-forum.io/thread-8966.html)

\[56] Write/Append Data to Excel Using openpyxl[ https://www.jquery-az.com/append-data-openpyxl/](https://www.jquery-az.com/append-data-openpyxl/)

\[57] Python - Writing to an excel file using openpyxl module[ https://www.tutorialspoint.com/python-writing-to-an-excel-file-using-openpyxl-module](https://www.tutorialspoint.com/python-writing-to-an-excel-file-using-openpyxl-module)

\[58] reportbro-fpdf2 2.7.9[ https://pypi.org/project/reportbro-fpdf2/](https://pypi.org/project/reportbro-fpdf2/)

\[59] Smruthi3/Generating-PDF-report-using-Python[ https://github.com/Smruthi3/Generating-PDF-report-using-Python](https://github.com/Smruthi3/Generating-PDF-report-using-Python)

\[60] jobsta/reportbro-lib[ https://github.com/jobsta/reportbro-lib](https://github.com/jobsta/reportbro-lib)

\[61] Sven-Bo/PDF-Report-Generator-Using-Python-and-SQL[ https://github.com/Sven-Bo/PDF-Report-Generator-Using-Python-and-SQL](https://github.com/Sven-Bo/PDF-Report-Generator-Using-Python-and-SQL)

> （注：文档部分内容可能由 AI 生成）