"""
File Toolbox - Desktop GUI
A beautiful desktop app for file sorting and Excel merging.
"""

import customtkinter as ctk
import os
import shutil
import threading
import zipfile
from io import BytesIO
import tkinter as tk
from tkinter import filedialog, messagebox


# ---------- 设置外观 ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FileToolboxApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("File Toolbox")
        self.geometry("700x550")
        self.minsize(600, 450)

        # 文件类型分类
        self.FILE_TYPES = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json", ".xml"],
            "Programs": [".exe", ".msi", ".dmg", ".app"],
        }

        self.sorter_files = []  # 文件分类器选择的文件
        self._build_ui()

    def _build_ui(self):
        # 标题
        title = ctk.CTkLabel(self, text="File Toolbox", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(self, text="by Yison Periona", font=ctk.CTkFont(size=13), text_color="gray")
        subtitle.pack(pady=(0, 15))

        # Tab 切换
        self.tabview = ctk.CTkTabview(self, width=640, height=400)
        self.tabview.pack(padx=20, pady=10, fill="both", expand=True)

        # Tab 1: 文件分类
        self.tab_sort = self.tabview.add("File Sorter")
        self._build_sorter_tab()

        # Tab 2: Excel 合并
        self.tab_merge = self.tabview.add("Excel Merger")
        self._build_merger_tab()

    # ========== 文件分类器 ==========
    def _build_sorter_tab(self):
        # 说明
        ctk.CTkLabel(
            self.tab_sort,
            text="Select files to sort by type",
            font=ctk.CTkFont(size=16)
        ).pack(pady=(15, 10))

        # 选择文件按钮
        ctk.CTkButton(
            self.tab_sort, text="Choose Files",
            command=self._pick_sort_files,
            width=200, height=40, font=ctk.CTkFont(size=14)
        ).pack(pady=5)

        # 已选文件列表
        self.sorter_listbox = tk.Listbox(
            self.tab_sort, height=10, width=70,
            bg="#1a1a2e", fg="#e0e0e0", selectbackground="#3b82f6",
            font=("Consolas", 11), relief="flat", bd=0
        )
        self.sorter_listbox.pack(padx=20, pady=10, fill="both", expand=True)

        # 底部按钮
        bottom = ctk.CTkFrame(self.tab_sort, fg_color="transparent")
        bottom.pack(pady=10, fill="x", padx=20)

        self.sorter_status = ctk.CTkLabel(bottom, text="", font=ctk.CTkFont(size=12), text_color="gray")
        self.sorter_status.pack(side="left")

        ctk.CTkButton(
            bottom, text="Sort & Download",
            command=self._run_sorter,
            width=180, height=38, font=ctk.CTkFont(size=14),
            fg_color="#16a34a", hover_color="#15803d"
        ).pack(side="right")

    def _pick_sort_files(self):
        files = filedialog.askopenfilenames(title="Choose files to sort")
        for f in files:
            name = os.path.basename(f)
            self.sorter_files.append(f)
            self.sorter_listbox.insert("end", f"  {name}")
        self.sorter_status.configure(text=f"{len(self.sorter_files)} files selected")

    def _get_category(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        for category, extensions in self.FILE_TYPES.items():
            if ext in extensions:
                return category
        return "Others"

    def _run_sorter(self):
        if not self.sorter_files:
            messagebox.showinfo("Info", "Please select files first!")
            return

        # 选择保存位置
        save_dir = filedialog.askdirectory(title="Choose output folder")
        if not save_dir:
            return

        result = {}
        for filepath in self.sorter_files:
            filename = os.path.basename(filepath)
            category = self._get_category(filename)
            folder = os.path.join(save_dir, category)
            os.makedirs(folder, exist_ok=True)
            shutil.copy2(filepath, os.path.join(folder, filename))
            result.setdefault(category, []).append(filename)

        # 打包 zip
        zip_path = os.path.join(save_dir, "sorted_files.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            for category, files in result.items():
                for fname in files:
                    zf.write(os.path.join(save_dir, category, fname), f"sorted/{category}/{fname}")

        # 显示结果
        msg = "Done!\n\n"
        for cat, files in sorted(result.items()):
            msg += f"  {cat}: {len(files)} files\n"
        msg += f"\nSaved to: {save_dir}\nZIP: sorted_files.zip"
        self.sorter_status.configure(text=f"Sorted {sum(len(v) for v in result.values())} files")
        messagebox.showinfo("Sort Complete", msg)

    # ========== Excel 合并器 ==========
    def _build_merger_tab(self):
        ctk.CTkLabel(
            self.tab_merge,
            text="Select Excel files to merge",
            font=ctk.CTkFont(size=16)
        ).pack(pady=(15, 10))

        ctk.CTkButton(
            self.tab_merge, text="Choose Excel Files",
            command=self._pick_merge_files,
            width=200, height=40, font=ctk.CTkFont(size=14)
        ).pack(pady=5)

        self.merger_listbox = tk.Listbox(
            self.tab_merge, height=10, width=70,
            bg="#1a1a2e", fg="#e0e0e0", selectbackground="#3b82f6",
            font=("Consolas", 11), relief="flat", bd=0
        )
        self.merger_listbox.pack(padx=20, pady=10, fill="both", expand=True)

        bottom = ctk.CTkFrame(self.tab_merge, fg_color="transparent")
        bottom.pack(pady=10, fill="x", padx=20)

        self.merger_status = ctk.CTkLabel(bottom, text="", font=ctk.CTkFont(size=12), text_color="gray")
        self.merger_status.pack(side="left")

        ctk.CTkButton(
            bottom, text="Merge & Download",
            command=self._run_merger,
            width=180, height=38, font=ctk.CTkFont(size=14),
            fg_color="#7c3aed", hover_color="#6d28d9"
        ).pack(side="right")

        self.merge_files = []

    def _pick_merge_files(self):
        files = filedialog.askopenfilenames(
            title="Choose Excel files",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        for f in files:
            self.merge_files.append(f)
            self.merger_listbox.insert("end", f"  {os.path.basename(f)}")
        self.merger_status.configure(text=f"{len(self.merge_files)} Excel files selected")

    def _run_merger(self):
        if not self.merge_files:
            messagebox.showinfo("Info", "Please select Excel files first!")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save merged file",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not save_path:
            return

        try:
            import pandas as pd
        except ImportError:
            messagebox.showerror("Error", "pandas is not installed!\nRun: pip install pandas openpyxl")
            return

        all_data = pd.DataFrame()
        success = 0
        skip = 0

        for f in self.merge_files:
            try:
                df = pd.read_excel(f)
                df["source_file"] = os.path.basename(f)
                all_data = pd.concat([all_data, df], ignore_index=True)
                success += 1
            except Exception as e:
                skip += 1

        if all_data.empty:
            messagebox.showerror("Error", "No data to merge!")
            return

        all_data.to_excel(save_path, index=False)
        self.merger_status.configure(text=f"Merged {success} files, {len(all_data)} rows")
        messagebox.showinfo("Merge Complete", f"Merged {success} files ({skip} skipped)\n{len(all_data)} rows total\n\nSaved to:\n{save_path}")


if __name__ == "__main__":
    app = FileToolboxApp()
    app.mainloop()
