"""
文件分类器
功能：把一个文件夹里的所有文件，按类型自动分类到不同子文件夹
用法：python file_sorter.py <文件夹路径>
举例：python file_sorter.py C:/my-messy-folder
"""

import os
import shutil
import sys

# 文件类型 → 对应的文件夹名字
FILE_TYPES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
    "文档": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "视频": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "音频": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "代码": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json", ".xml"],
    "程序": [".exe", ".msi", ".dmg", ".app"],
}

# 如果文件后缀不在上面的分类里，就放到这个文件夹
DEFAULT_FOLDER = "其他"


def get_category(filename):
    """根据文件后缀，判断它属于哪个分类"""
    # 取出文件后缀（小写），比如 ".jpg"
    ext = os.path.splitext(filename)[1].lower()

    # 在 FILE_TYPES 里找到匹配的分类
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category

    # 没找到就归为"其他"
    return DEFAULT_FOLDER


def sort_files(folder_path):
    """主函数：扫描文件夹，把文件分类移动"""
    # 统计信息
    moved = 0
    skipped = 0

    # 遍历文件夹里的每一个文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 跳过子文件夹，只处理文件
        if os.path.isdir(file_path):
            skipped += 1
            continue

        # 判断这个文件属于哪个分类
        category = get_category(filename)

        # 创建对应的子文件夹（如果还不存在）
        category_folder = os.path.join(folder_path, category)
        os.makedirs(category_folder, exist_ok=True)

        # 移动文件到子文件夹
        destination = os.path.join(category_folder, filename)
        shutil.move(file_path, destination)
        moved += 1

        print(f"  {filename} → {category}/")

    # 打印统计结果
    print(f"\n完成！移动了 {moved} 个文件，跳过了 {skipped} 个文件夹")


if __name__ == "__main__":
    # 如果用户没有传入文件夹路径，就使用当前目录
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = "."

    # 检查路径是否存在
    if not os.path.isdir(folder):
        print(f"错误：'{folder}' 不是一个有效的文件夹")
        sys.exit(1)

    print(f"开始整理文件夹：{folder}\n")
    sort_files(folder)
