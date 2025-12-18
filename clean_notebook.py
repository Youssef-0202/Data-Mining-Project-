import os

file_path = r'c:\Users\HP\OneDrive\Bureau\DM Project\notebooks\3_baseline_vs_xgboost.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

markers = ['<<<<<<< HEAD\n', '=======\n', '>>>>>>> b48df8eb891df0c07b6cd35f323e63d7e4a4889f\n']

new_lines = [line for line in lines if line not in markers]

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Cleaned {file_path}")
