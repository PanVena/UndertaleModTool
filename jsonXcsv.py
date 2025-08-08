import json
import csv
import tkinter as tk
from tkinter import filedialog, messagebox


def json_to_csv():
    try:
        json_file = filedialog.askopenfilename(
            title="Виберіть JSON файл",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not json_file:
            return

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "Strings" not in data or not isinstance(data["Strings"], list):
            messagebox.showerror("Помилка", "JSON має містити ключ 'Strings' зі списком.")
            return

        csv_file = filedialog.asksaveasfilename(
            title="Збережіть CSV файл",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not csv_file:
            return

        with open(csv_file, "w", encoding="utf-8-sig", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "STRINGS", "TRANSLATION"])
            for i, val in enumerate(data["Strings"], start=1):
                writer.writerow([i, val if val is not None else ""])

        messagebox.showinfo("Готово", f"CSV збережено:\n{csv_file}")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))


def csv_to_json():
    try:
        csv_file = filedialog.askopenfilename(
            title="Виберіть CSV файл",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not csv_file:
            return

        json_file = filedialog.asksaveasfilename(
            title="Збережіть JSON файл",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if not json_file:
            return

        strings_list = []

        with open(csv_file, "r", encoding="utf-8", newline='') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            next(reader, None)  # пропустити заголовок

            for row in reader:
                if len(row) >= 3:  # беремо третю колонку
                    text = row[2]
                    # замінюємо реальні переноси рядків на символи \n
                    text = text.replace("\r\n", "\n").replace("\n", "\n").replace("\t", "")
                    strings_list.append(text)

        data = {"Strings": strings_list}

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Готово", f"JSON збережено:\n{json_file}\nЗаписів: {len(strings_list)}")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))



# ==== Головне вікно ====
root = tk.Tk()
root.title("JSON ↔ CSV Конвертер")
root.geometry("300x150")
root.resizable(False, False)

btn1 = tk.Button(root, text="JSON → CSV", font=("Arial", 14), command=json_to_csv)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="CSV → JSON", font=("Arial", 14), command=csv_to_json)
btn2.pack(pady=10)

root.mainloop()
