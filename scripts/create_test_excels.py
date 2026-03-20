import pandas as pd
import os

scripts_dir = os.path.dirname(os.path.abspath(__file__))
test_folder = os.path.join(scripts_dir, "test-excels")
os.makedirs(test_folder, exist_ok=True)

df1 = pd.DataFrame({
    "name": ["A", "B", "C"],
    "subject": ["chinese", "chinese", "chinese"],
    "score": [85, 92, 78]
})
df1.to_excel(os.path.join(test_folder, "chinese.xlsx"), index=False)

df2 = pd.DataFrame({
    "name": ["A", "B", "D"],
    "subject": ["math", "math", "math"],
    "score": [90, 76, 88]
})
df2.to_excel(os.path.join(test_folder, "math.xlsx"), index=False)

df3 = pd.DataFrame({
    "name": ["C", "D", "A"],
    "subject": ["english", "english", "english"],
    "score": [95, 82, 70]
})
df3.to_excel(os.path.join(test_folder, "english.xlsx"), index=False)

print("Done: 3 test Excel files created")
