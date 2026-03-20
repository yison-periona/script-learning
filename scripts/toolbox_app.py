"""
文件工具箱 - WebUI
把文件分类器和 Excel 合并器做成网页界面
运行方式：streamlit run toolbox_app.py
"""

import streamlit as st
import os
import shutil
import pandas as pd
import tempfile

# 页面配置
st.set_page_config(
    page_title="File Toolbox",
    page_icon="📦",
    layout="centered"
)

# 文件类型分类规则
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json", ".xml"],
    "Programs": [".exe", ".msi", ".dmg", ".app"],
}


def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return "Others"


# ---------- 页面内容 ----------

st.title("📦 File Toolbox")
st.write("Upload files, click a button, get results. Simple.")

tab1, tab2 = st.tabs(["📁 File Sorter", "📊 Excel Merger"])

# ========== Tab 1: 文件分类器 ==========
with tab1:
    st.header("File Sorter")
    st.write("Upload a bunch of files, and they will be sorted by type automatically.")

    uploaded_files = st.file_uploader(
        "Choose files to sort",
        accept_multiple_files=True,
        key="sorter"
    )

    if uploaded_files:
        st.write(f"You uploaded **{len(uploaded_files)}** files:")

        # 显示文件列表
        cols = st.columns(4)
        for i, f in enumerate(uploaded_files):
            with cols[i % 4]:
                st.caption(f"📄 {f.name}")

        if st.button("Sort Files", type="primary", key="sort_btn"):
            with st.spinner("Sorting..."):
                # 创建临时文件夹来操作
                temp_dir = tempfile.mkdtemp()

                # 保存上传的文件到临时文件夹
                for f in uploaded_files:
                    save_path = os.path.join(temp_dir, f.name)
                    with open(save_path, "wb") as out:
                        out.write(f.read())

                # 执行分类
                result = {}
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    if os.path.isdir(file_path):
                        continue
                    category = get_category(filename)
                    category_folder = os.path.join(temp_dir, category)
                    os.makedirs(category_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(category_folder, filename))
                    if category not in result:
                        result[category] = []
                    result[category].append(filename)

                # 显示结果
                st.success("Done!")
                for category, files in sorted(result.items()):
                    with st.expander(f"📂 {category} ({len(files)} files)"):
                        for fname in files:
                            st.text(f"  └─ {fname}")

                # 打包成 zip 供下载
                import zipfile
                zip_path = os.path.join(temp_dir, "sorted_files.zip")
                with zipfile.ZipFile(zip_path, "w") as zf:
                    for category, files in result.items():
                        for fname in files:
                            fpath = os.path.join(temp_dir, category, fname)
                            zf.write(fpath, f"sorted/{category}/{fname}")

                with open(zip_path, "rb") as zf:
                    st.download_button(
                        label="Download Sorted Files (.zip)",
                        data=zf.read(),
                        file_name="sorted_files.zip",
                        mime="application/zip",
                        key="sort_download"
                    )

# ========== Tab 2: Excel 合并器 ==========
with tab2:
    st.header("Excel Merger")
    st.write("Upload multiple Excel files, and they will be merged into one.")

    uploaded_excels = st.file_uploader(
        "Choose Excel files (.xlsx)",
        accept_multiple_files=True,
        type=["xlsx", "xls"],
        key="merger"
    )

    if uploaded_excels:
        st.write(f"You uploaded **{len(uploaded_excels)}** Excel files:")
        for f in uploaded_excels:
            st.caption(f"📊 {f.name} ({f.size} bytes)")

        if st.button("Merge Files", type="primary", key="merge_btn"):
            with st.spinner("Merging..."):
                all_data = pd.DataFrame()
                success_count = 0

                for f in uploaded_excels:
                    try:
                        df = pd.read_excel(f)
                        df["source_file"] = f.name
                        all_data = pd.concat([all_data, df], ignore_index=True)
                        success_count += 1
                    except Exception as e:
                        st.warning(f"Skipped {f.name}: {e}")

                if all_data.empty:
                    st.error("No data to merge.")
                else:
                    st.success(f"Merged! {success_count} files, {len(all_data)} rows total.")

                    st.dataframe(all_data, use_container_width=True)

                    # 提供下载
                    from io import BytesIO
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        all_data.to_excel(writer, index=False)
                    output.seek(0)

                    st.download_button(
                        label="Download Merged Excel (.xlsx)",
                        data=output,
                        file_name="merged_result.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="merge_download"
                    )

# 页脚
st.divider()
st.caption("Built with Claude Code • Yison Periona")
