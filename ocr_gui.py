import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import numpy as np
from PIL import ImageGrab, Image
from ocr_core import process_ocr
from ocr_translate import translate_text  # 번역 함수 임포트
from ocr_help import show_help

PASSWORD = "1234"
THEME = {"mode": "light"}
LANG = {"code": "ko"}

THEMES = {
    "light": {"bg": "#F0F0F0", "fg": "#222222", "btn_bg": "#E0E0E0", "btn_fg": "#111111", "list_bg": "#FFFFFF", "list_fg": "#222222"},
    "dark": {"bg": "#222222", "fg": "#F0F0F0", "btn_bg": "#333333", "btn_fg": "#F0F0F0", "list_bg": "#292929", "list_fg": "#F0F0F0"}
}
ocr_history = []

TRANSLATIONS = {
    "ko": {
        "title": "EasyOCR 기록형",
        "start": "스타트",
        "ocr_history": "OCR 결과 히스토리",
        "new_ocr": "새로운 영역 OCR",
        "open_file": "파일 불러오기",
        "copy": "복사",
        "delete": "삭제",
        "translate": "번역",
        "dark_mode": "🌙 다크모드 전환",
        "light_mode": "☀️ 라이트모드 전환",
        "exit_confirm": "정말 종료하시겠습니까?",
        "lang_mode": "🌐 언어 변경",
        "file_done": "이미지 파일의 OCR 분석이 완료되었습니다!",
        "file_error": "이미지를 불러오는데 실패했습니다.",
        "copy_done": "OCR 결과가 클립보드에 복사되었습니다.",
        "delete_warn": "먼저 삭제할 항목을 선택하세요.",
        "translate_lang": "결과 언어 코드를 입력하세요(예: ko, en, ja, zh)",
        "translate_result": "번역 결과",
        "detail": "OCR 기록 상세",
        "password_prompt": "프로그램을 실행하려면 비밀번호를 입력하세요.",
        "password_error": "비밀번호가 틀렸습니다!",
        "start_title": "EasyOCR 시작",
        "start_text": "EasyOCR 프로그램"
    },
    "en": {
        "title": "EasyOCR Log",
        "start": "Start",
        "ocr_history": "OCR Result History",
        "new_ocr": "New Area OCR",
        "open_file": "Open Image File",
        "copy": "Copy",
        "delete": "Delete",
        "translate": "Translate",
        "dark_mode": "🌙 Switch to Dark Mode",
        "light_mode": "☀️ Switch to Light Mode",
        "exit_confirm": "Are you sure you want to exit?",
        "lang_mode": "🌐 Change Language",
        "file_done": "Image OCR analysis is complete!",
        "file_error": "Failed to load image.",
        "copy_done": "OCR result copied to clipboard.",
        "delete_warn": "Please select an item to delete.",
        "translate_lang": "Enter result language code (e.g., ko, en, ja, zh)",
        "translate_result": "Translation Result",
        "detail": "OCR Detail",
        "password_prompt": "Enter password to launch the program.",
        "password_error": "Incorrect password!",
        "start_title": "EasyOCR Start",
        "start_text": "EasyOCR Program"
    },
    "ja": {
        "title": "EasyOCR 履歴",
        "start": "スタート",
        "ocr_history": "OCR結果の履歴",
        "new_ocr": "新しい領域OCR",
        "open_file": "画像ファイルを開く",
        "copy": "コピー",
        "delete": "削除",
        "translate": "翻訳",
        "dark_mode": "🌙 ダークモードに切替",
        "light_mode": "☀️ ライトモードに切替",
        "exit_confirm": "本当に終了しますか？",
        "lang_mode": "🌐 言語を変更",
        "file_done": "画像OCR分析が完了しました！",
        "file_error": "画像の読み込みに失敗しました。",
        "copy_done": "OCR結果をクリップボードにコピーしました。",
        "delete_warn": "削除する項目を選択してください。",
        "translate_lang": "結果の言語コードを入力してください（例：ko, en, ja, zh）",
        "translate_result": "翻訳結果",
        "detail": "OCR記録の詳細",
        "password_prompt": "プログラムを実行するにはパスワードを入力してください。",
        "password_error": "パスワードが間違っています！",
        "start_title": "EasyOCR 起動",
        "start_text": "EasyOCR プログラム"
    },
    "zh": {
        "title": "EasyOCR 记录",
        "start": "开始",
        "ocr_history": "OCR结果历史",
        "new_ocr": "新的区域OCR",
        "open_file": "打开图片文件",
        "copy": "复制",
        "delete": "删除",
        "translate": "翻译",
        "dark_mode": "🌙 切换到深色模式",
        "light_mode": "☀️ 切换到浅色模式",
        "exit_confirm": "您确定要退出吗？",
        "lang_mode": "🌐 更改语言",
        "file_done": "图像OCR分析已完成！",
        "file_error": "加载图像失败。",
        "copy_done": "OCR结果已复制到剪贴板。",
        "delete_warn": "请选择要删除的项目。",
        "translate_lang": "请输入语言代码（如：ko, en, ja, zh）",
        "translate_result": "翻译结果",
        "detail": "OCR记录详情",
        "password_prompt": "请输入密码以启动程序。",
        "password_error": "密码错误！",
        "start_title": "EasyOCR 启动",
        "start_text": "EasyOCR 程序"
    }
}


def get_text(key):
    return TRANSLATIONS[LANG["code"]].get(key, key)

def apply_theme(widgets):
    theme = THEMES[THEME["mode"]]
    widgets["root"].configure(bg=theme["bg"])
    widgets["label"].configure(bg=theme["bg"], fg=theme["fg"])
    widgets["listbox"].configure(bg=theme["list_bg"], fg=theme["list_fg"])
    for btn in widgets["buttons"]:
        btn.configure(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground=theme["btn_bg"], activeforeground=theme["btn_fg"])

def toggle_theme(widgets, theme_btn):
    THEME["mode"] = "dark" if THEME["mode"] == "light" else "light"
    tr = TRANSLATIONS[LANG["code"]]
    theme_btn.config(text=tr["light_mode"] if THEME["mode"] == "dark" else tr["dark_mode"])
    apply_theme(widgets)

def update_labels(widgets):
    tr = TRANSLATIONS[LANG["code"]]
    widgets["root"].title(tr["title"])
    widgets["label"].config(text=tr["ocr_history"])
    btns = widgets["buttons"]
    btns[0].config(text=tr["new_ocr"])
    btns[1].config(text=tr["open_file"])
    btns[2].config(text=tr["copy"])
    btns[3].config(text=tr["delete"])
    btns[4].config(text=tr["translate"])
    btns[5].config(text=tr["dark_mode"] if THEME["mode"] == "light" else tr["light_mode"])
    btns[6].config(text=tr["lang_mode"])
    btns[7].config(text="도움말" if LANG["code"] == "ko" else "Help" if LANG["code"] == "en" else "ヘルプ" if LANG["code"] == "ja" else "帮助")

def toggle_language(widgets):
    codes = list(TRANSLATIONS.keys())
    idx = codes.index(LANG["code"])
    LANG["code"] = codes[(idx + 1) % len(codes)]
    update_labels(widgets)

def add_to_history(result, listbox):
    ocr_history.append(result)
    listbox.insert(tk.END, result)

def select_area_and_add(listbox, widgets):
    global start_x, start_y, end_x, end_y
    start_x = start_y = end_x = end_y = 0
    def on_mouse_down(event):
        global start_x, start_y
        start_x, start_y = event.x, event.y
    def on_mouse_up(event):
        global end_x, end_y
        end_x, end_y = event.x, event.y
        area_root.destroy()
        x1, y1 = min(start_x, end_x), min(start_y, end_y)
        x2, y2 = max(start_x, end_x), max(start_y, end_y)
        img = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))
        ocr_result = process_ocr(img)
        add_to_history(ocr_result, listbox)
    area_root = tk.Tk()
    area_root.attributes("-fullscreen", True)
    area_root.attributes("-alpha", 0.3)
    area_root.config(bg='gray')
    area_root.bind("<ButtonPress-1>", on_mouse_down)
    area_root.bind("<ButtonRelease-1>", on_mouse_up)
    area_root.mainloop()

def open_file_and_ocr(listbox, widgets):
    filetypes = [("이미지 파일", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"), ("모든 파일", "*.*")]
    file_path = filedialog.askopenfilename(title=get_text("open_file"), filetypes=filetypes)
    if not file_path:
        return
    try:
        img = np.array(Image.open(file_path))
        ocr_result = process_ocr(img)
        add_to_history(f"[파일: {file_path.split('/')[-1]}] {ocr_result}", listbox)
        messagebox.showinfo(get_text("open_file"), get_text("file_done"))
    except Exception as e:
        messagebox.showerror(get_text("open_file"), f"{get_text('file_error')}\n{e}")

def copy_selected(listbox, widgets):
    sel = listbox.curselection()
    if sel:
        text = listbox.get(sel[0])
        listbox.clipboard_clear()
        listbox.clipboard_append(text)
        messagebox.showinfo(get_text("copy"), get_text("copy_done"))

def delete_selected(listbox, widgets):
    sel = listbox.curselection()
    if sel:
        idx = sel[0]
        listbox.delete(idx)
        del ocr_history[idx]
    else:
        messagebox.showwarning(get_text("delete"), get_text("delete_warn"))

def translate_selected(listbox, widgets):
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning(get_text("translate"), get_text("translate_lang"))
        return
    text = listbox.get(sel[0])
    lang = simpledialog.askstring(get_text("translate"), get_text("translate_lang"), initialvalue="ko")
    if not lang:
        return
    result = translate_text(text, src='auto', dest=lang)
    messagebox.showinfo(get_text("translate_result"), result)

def show_main_gui():
    root = tk.Tk()
    root.title(get_text("title"))
    root.geometry("700x560")
    def on_closing():
        if messagebox.askokcancel(get_text("title"), get_text("exit_confirm")):
            root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    label = tk.Label(root, text=get_text("ocr_history"), font=("맑은 고딕", 16))
    label.pack(pady=10)
    listbox = tk.Listbox(root, width=100, height=20)
    listbox.pack(padx=10, pady=10)

    ocr_btn = tk.Button(root)
    file_btn = tk.Button(root)
    copy_btn = tk.Button(root)
    delete_btn = tk.Button(root)
    translate_btn = tk.Button(root)
    theme_btn = tk.Button(root)
    lang_btn = tk.Button(root)
    help_btn = tk.Button(root, text="도움말", font=("맑은 고딕", 12), command=lambda: show_help(LANG["code"]))

    widgets = {
        "root": root,
        "label": label,
        "listbox": listbox,
        "buttons": [ocr_btn, file_btn, copy_btn, delete_btn, translate_btn, theme_btn, lang_btn, help_btn]
    }

    # 버튼 기능 연결
    ocr_btn.config(command=lambda: select_area_and_add(listbox, widgets))
    file_btn.config(command=lambda: open_file_and_ocr(listbox, widgets))
    copy_btn.config(command=lambda: copy_selected(listbox, widgets))
    delete_btn.config(command=lambda: delete_selected(listbox, widgets))
    translate_btn.config(command=lambda: translate_selected(listbox, widgets))
    theme_btn.config(command=lambda: toggle_theme(widgets, theme_btn))
    lang_btn.config(command=lambda: toggle_language(widgets))
    help_btn.config(command=lambda: show_help(LANG["code"]))

    # 버튼 배치 (한 줄에 정렬)
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    for btn in [ocr_btn, file_btn, copy_btn, delete_btn, translate_btn, theme_btn, lang_btn, help_btn]:
        btn.pack(side=tk.LEFT, padx=5)

    apply_theme(widgets)
    update_labels(widgets)

    def show_detail(event):
        sel = listbox.curselection()
        if sel:
            msg = listbox.get(sel[0])
            messagebox.showinfo(get_text("detail"), msg)
    listbox.bind("<Double-Button-1>", show_detail)
    root.mainloop()

def ask_password(on_success, root):
    pw = simpledialog.askstring(get_text("password"), get_text("password_prompt"), show="*", parent=root)
    if pw is None:
        root.deiconify()
        return
    if pw == PASSWORD:
        root.destroy()
        on_success()
    else:
        messagebox.showerror(get_text("password"), get_text("password_error"), parent=root)
        ask_password(on_success, root)

def show_start_gui():
    start_root = tk.Tk()
    start_root.title(get_text("start_title"))
    start_root.geometry("300x150")
    label = tk.Label(start_root, text=get_text("start_text"), font=("맑은 고딕", 16))
    label.pack(pady=15)
    def on_start():
        start_root.withdraw()
        def run_main():
            show_main_gui()
        ask_password(run_main, start_root)
    start_btn = tk.Button(
        start_root, text=get_text("start"), font=("맑은 고딕", 14), width=15, height=2,
        command=on_start
    )
    start_btn.pack(pady=10)
    start_root.mainloop()
