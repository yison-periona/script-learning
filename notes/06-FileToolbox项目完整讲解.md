# FileToolbox 试水项目完整讲解

## 你做了什么

今天你从一个"基本不会编程"的状态，用 Claude Code 完成了一个完整的桌面软件产品：

**FileToolbox** — 一个文件工具箱，包含两个功能：
1. **File Sorter**：把一堆文件按类型自动分类
2. **Excel Merger**：把多个 Excel 文件合并成一个

而且这个软件已经打包成了 .exe，任何人双击就能用。

---

## 一、项目文件结构

整理后的目录结构是这样的：

```
script-learning/
├── notes/                          # 学习笔记文件夹
│   ├── 01-什么是脚本.md
│   ├── 02-脚本用什么语言写.md
│   ├── 03-脚本怎么运行的.md
│   ├── 04-脚本变现的思路.md
│   └── 05-学习路线图.md
│
├── scripts/                        # 项目代码文件夹
│   ├── file_sorter.py              # 脚本1：文件分类器（命令行版）
│   ├── excel_merger.py             # 脚本2：Excel合并器（命令行版）
│   ├── toolbox_app.py              # WebUI 版（Streamlit 网页界面）
│   └── toolbox_desktop.py          # 桌面 GUI 版（CustomTkinter 窗口）
│
├── toolbox_launcher.py             # exe 启动入口
├── .gitignore                      # Git 忽略配置
└── dist/FileToolbox/               # 打包后的 exe 文件夹
```

### 为什么要分开？

- `notes/`：只放学习笔记，和代码无关
- `scripts/`：放所有代码文件
- `dist/`：打包生成的文件，不上传到 GitHub

---

## 二、第一个脚本：file_sorter.py 逐行讲解

这个脚本的核心逻辑只有 40 行左右。我把关键部分拆开讲。

### 2.1 导入库

```python
import os        # 操作文件和文件夹（Python 自带）
import shutil    # 移动/复制文件（Python 自带）
import sys       # 获取命令行参数（Python 自带）
```

**什么是"库"？**

库就是别人已经写好的工具包，你直接拿来用。

`os`、`shutil`、`sys` 都是 Python 自带的，不需要安装任何东西。

### 2.2 文件类型定义

```python
FILE_TYPES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ...],
    "文档": [".pdf", ".doc", ".docx", ".txt", ...],
    "视频": [".mp4", ".avi", ".mkv", ...],
    ...
}
```

这是一个**字典**（Python 的数据结构），格式是：

```
键 : 值
"图片" : [".jpg", ".png", ...]
```

意思是：后缀是 .jpg 或 .png 的文件，属于"图片"分类。

### 2.3 判断文件属于哪个分类

```python
def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return DEFAULT_FOLDER
```

逐行解释：

| 代码 | 作用 |
|------|------|
| `os.path.splitext(filename)[1]` | 从文件名中提取后缀，比如 `"照片.jpg"` → `".jpg"` |
| `.lower()` | 把后缀转成小写，`.JPG` 和 `.jpg` 统一处理 |
| `for ... in FILE_TYPES.items():` | 遍历字典里的每一对"分类名: 后缀列表" |
| `if ext in extensions:` | 如果文件后缀在这个列表里 |
| `return category` | 返回对应的分类名 |
| `return DEFAULT_FOLDER` | 都不匹配就归为"其他" |

### 2.4 主函数

```python
def sort_files(folder_path):
    for filename in os.listdir(folder_path):      # 列出文件夹里所有文件
        file_path = os.path.join(folder_path, filename)  # 拼出完整路径

        if os.path.isdir(file_path):              # 如果是子文件夹，跳过
            continue

        category = get_category(filename)          # 判断分类
        category_folder = os.path.join(folder_path, category)
        os.makedirs(category_folder, exist_ok=True)  # 创建分类文件夹
        shutil.move(file_path, destination)        # 移动文件
```

核心就是：**遍历 → 判断类型 → 创建文件夹 → 移动文件**。

### 2.5 程序入口

```python
if __name__ == "__main__":
    if len(sys.argv) > 1:       # 如果用户传了参数
        folder = sys.argv[1]     # 用参数作为文件夹路径
    else:
        folder = "."             # 否则用当前目录
```

`sys.argv` 就是命令行参数：
- `python file_sorter.py C:/my-folder` → `sys.argv[1]` 是 `C:/my-folder`
- `python file_sorter.py` → 没有参数，用当前目录

---

## 三、第二个脚本：excel_merger.py 逐行讲解

### 3.1 用到了新库

```python
import pandas as pd
```

**pandas** 是 Python 最常用的数据处理库。

你需要安装它：`pip install pandas openpyxl`

### 3.2 读取 Excel

```python
df = pd.read_excel(file_path)
```

一行代码就能读取 Excel 文件，返回一个 DataFrame（表格数据结构）。

比如你的 Excel 是：
```
| 姓名 | 科目 | 成绩 |
| 张三 | 语文 | 85  |
```

读取后 `df` 就是这个表格。

### 3.3 合并数据

```python
df["source_file"] = filename          # 添加一列标记来源
all_data = pd.concat([all_data, df])  # 合并到总表
```

`pd.concat()` 把多个表格按行拼接在一起。

### 3.4 保存结果

```python
all_data.to_excel(output_path, index=False)
```

把合并后的数据保存为 Excel 文件。`index=False` 表示不保存行号。

---

## 四、WebUI 版：toolbox_app.py 讲解

### 4.1 什么是 Streamlit

Streamlit 是一个 Python 库，让你**只用 Python 代码就能写网页**。

不需要写 HTML、CSS、JavaScript，全用 Python 就行。

### 4.2 核心概念

```python
import streamlit as st

st.title("页面标题")          # 大标题
st.write("一段文字")          # 普通文字
st.button("点击按钮")         # 按钮
st.file_uploader("选择文件")   # 文件上传
st.dataframe(df)              # 显示表格
st.download_button(...)       # 下载按钮
```

每一行代码就会在网页上显示一个组件。

### 4.3 标签页

```python
tab1, tab2 = st.tabs(["File Sorter", "Excel Merger"])
```

一行代码创建标签页切换。

### 4.4 交互逻辑

```python
if st.button("Sort Files"):
    # 用户点了按钮后执行的代码
    with st.spinner("Sorting..."):  # 显示加载动画
        # 实际处理逻辑
    st.success("Done!")  # 显示成功提示
```

### 4.5 为什么最后没用 WebUI 方案打包 exe

因为 Streamlit 依赖太多（pandas、numpy、matplotlib 等），打包出来几百 MB。

而 CustomTkinter 只依赖 Python 自带的 tkinter，打包出来 30MB 左右。

---

## 五、桌面 GUI 版：toolbox_desktop.py 讲解

### 5.1 什么是 CustomTkinter

**tkinter** 是 Python 自带的图形界面库。

**CustomTkinter** 是 tkinter 的美化版，提供现代化的深色主题外观。

### 5.2 核心概念

```python
import customtkinter as ctk

app = ctk.CTk()           # 创建窗口
app.title("窗口标题")       # 设置标题
app.geometry("700x550")    # 设置大小

ctk.CTkLabel(app, text="文字")           # 文字标签
ctk.CTkButton(app, text="按钮", command=函数名)  # 按钮
ctk.CTkTabview(app)                       # 标签页
```

### 5.3 按钮事件

```python
ctk.CTkButton(app, text="Sort", command=self._run_sorter)
```

当用户点击按钮时，会自动调用 `self._run_sorter` 这个函数。

### 5.4 文件选择对话框

```python
from tkinter import filedialog

files = filedialog.askopenfilenames(title="选择文件")          # 选择多个文件
save_dir = filedialog.askdirectory(title="选择保存位置")         # 选择文件夹
save_path = filedialog.asksaveasfilename(defaultextension=".xlsx")  # 保存文件
```

这些都是 tkinter 自带的弹窗，不需要额外安装。

### 5.5 类（Class）的概念

你可能注意到了代码里有 `class FileToolboxApp(ctk.CTk):`。

**什么是类？**

类就是把相关的数据和功能打包在一起。

```python
class FileToolboxApp(ctk.CTk):
    def __init__(self):       # 初始化（创建窗口时自动执行）
        self.title("...")     # self 代表这个窗口自己
        self._build_ui()      # 构建界面

    def _build_sorter_tab(self):   # 方法（属于这个类的函数）
        ...

    def _run_sorter(self):         # 方法
        ...
```

你不需要完全理解类，只需要知道：
- `self.xxx` 表示"这个窗口自己的 xxx"
- `self.xxx()` 表示"调用这个窗口自己的某个功能"

---

## 六、打包成 exe 讲解

### 6.1 PyInstaller 是什么

PyInstaller 把 Python 程序打包成一个独立的 .exe 文件。

用户不需要安装 Python，双击就能运行。

### 6.2 打包命令解析

```bash
pyinstaller --noconfirm --onedir -w --name "FileToolbox" \
  --exclude-module numpy \
  --exclude-module torch \
  --hidden-import customtkinter \
  scripts/toolbox_desktop.py
```

| 参数 | 作用 |
|------|------|
| `--noconfirm` | 不询问，直接覆盖旧文件 |
| `--onedir` | 打包成一个文件夹（包含 exe 和依赖文件） |
| `-w` | 不显示命令行黑窗口（windowed 模式） |
| `--name "FileToolbox"` | exe 文件名 |
| `--exclude-module xxx` | 排除不需要的大库，减小体积 |
| `--hidden-import xxx` | 强制包含某个库 |
| 最后的 `.py` 文件 | 程序入口文件 |

### 6.3 --onedir vs --onefile

| | --onedir | --onefile |
|--|----------|-----------|
| 输出 | 一个文件夹 | 单个 .exe 文件 |
| 启动速度 | 快 | 慢（每次要解压） |
| 大小 | 文件夹整体较大 | 差不多 |
| 分发 | 需要压缩成 zip 发送 | 直接发一个文件 |
| 适合 | 内部使用 | 发给客户 |

如果你想发单个 exe 文件，把 `--onedir` 换成 `--onefile` 就行。

---

## 七、今天的完整流程回顾

### 你经历了什么

```
不会编程
  ↓
Claude Code 帮你写了第一个脚本（file_sorter.py）
  ↓
用假数据测试，看到效果
  ↓
做了第二个脚本（excel_merger.py）
  ↓
用 Streamlit 做了 WebUI 版（浏览器界面）
  ↓
用 PyInstaller 打包成 exe
  ↓
发现 exe 太大，换了 CustomTkinter 方案
  ↓
重新打包成 31MB 的桌面应用
  ↓
推送到 GitHub
```

### 你学到了什么

| 概念 | 你用到了 |
|------|---------|
| Python 脚本 | file_sorter.py, excel_merger.py |
| 文件操作 | os, shutil 库 |
| 数据处理 | pandas 库 |
| Web 界面 | Streamlit 框架 |
| 桌面 GUI | CustomTkinter 框架 |
| 打包分发 | PyInstaller 工具 |
| 版本控制 | Git + GitHub |

---

## 八、下一步建议

### 你现在可以做的

1. **试用 exe**：双击桌面的 FileToolbox.exe，用真实文件测试两个功能
2. **修改界面文字**：打开 `toolbox_desktop.py`，把英文改成中文，重新打包
3. **展示给别人看**：把 exe 文件夹压缩成 zip 发给同学，让他们试试

### 你可以继续学的内容

1. **tkinter 布局**：怎么让界面更好看、排列更整齐
2. **pandas 进阶**：数据筛选、分组、统计
3. **更多脚本类型**：PDF 处理、图片批量处理、网页抓取
4. **接单实践**：在闲鱼发布第一个接单信息

### 接单文案参考

> 专业定制 Python 脚本 / 小工具
> - 文件批量处理（分类、重命名、整理）
> - Excel 数据处理（合并、清洗、统计）
> - 自动化脚本（定时任务、批量操作）
> - 可打包成 exe，双击直接使用
> 欢迎私聊具体需求
> 作品展示：github.com/yison-periona
