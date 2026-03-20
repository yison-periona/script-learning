"""
Excel 合并器
功能：把一个文件夹里的多个 Excel 文件合并成一个
用法：python excel_merger.py <Excel所在文件夹> <输出文件名>
举例：python excel_merger.py C:/my-excels 合并结果.xlsx
"""

import os
import sys
import pandas as pd


def merge_excels(folder_path, output_name="合并结果.xlsx"):
    """扫描文件夹，把所有 Excel 合并成一个文件"""
    # 支持的 Excel 格式
    excel_extensions = [".xlsx", ".xls"]

    # 找出文件夹里所有 Excel 文件
    excel_files = []
    for filename in os.listdir(folder_path):
        ext = os.path.splitext(filename)[1].lower()
        if ext in excel_extensions:
            excel_files.append(filename)

    if not excel_files:
        print("没有找到 Excel 文件！")
        return

    print(f"找到 {len(excel_files)} 个 Excel 文件：")
    for f in excel_files:
        print(f"  - {f}")
    print()

    # 逐个读取并合并
    all_data = pd.DataFrame()
    success_count = 0
    skip_count = 0

    for filename in excel_files:
        file_path = os.path.join(folder_path, filename)

        try:
            # 读取 Excel 文件（取第一个工作表）
            df = pd.read_excel(file_path)

            # 添加一列"来源文件"，方便知道数据来自哪个文件
            df["来源文件"] = filename

            # 合并到总数据里
            all_data = pd.concat([all_data, df], ignore_index=True)
            success_count += 1
            print(f"  已合并：{filename}（{len(df)} 行）")

        except Exception as e:
            skip_count += 1
            print(f"  跳过：{filename}（原因：{e}）")

    if all_data.empty:
        print("\n没有可合并的数据")
        return

    # 保存合并结果
    output_path = os.path.join(folder_path, output_name)
    all_data.to_excel(output_path, index=False)

    print(f"\n合并完成！")
    print(f"  成功：{success_count} 个文件")
    print(f"  跳过：{skip_count} 个文件")
    print(f"  总行数：{len(all_data)} 行")
    print(f"  保存到：{output_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = "."

    output = sys.argv[2] if len(sys.argv) > 2 else "合并结果.xlsx"

    if not os.path.isdir(folder):
        print(f"错误：'{folder}' 不是一个有效的文件夹")
        sys.exit(1)

    merge_excels(folder, output)
