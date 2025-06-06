# ocr_help.py
import tkinter as tk

HELP_TEXTS = {
    "ko": """
■■■ EasyOCR 프로그램 도움말 ■■■

1. 새로운 영역 OCR
- 화면을 드래그하여 원하는 영역의 텍스트를 인식합니다.

2. 파일 불러오기
- PNG, JPG, BMP 등 이미지 파일을 불러와 텍스트를 추출합니다.

3. 복사/삭제/번역
- 리스트에서 결과를 클릭 후 복사, 삭제, 번역 버튼을 사용하세요.

4. 다크모드 전환
- 눈에 편한 어두운 화면으로 바꿀 수 있습니다.

5. 언어 변경
- 한글, 영어, 일본어, 중국어로 UI를 바꿀 수 있습니다.

6. 단축키(Hotkey)
- Ctrl+C: 복사, Del: 삭제, F1: 도움말 창 열기(추가예정)

7. 히스토리 검색/고정/내보내기(추가예정)
- 많은 결과를 검색, 즐겨찾기, 내보내기 기능은 추후 지원됩니다.

■ 자주 묻는 질문(FAQ)
- Q: OCR 결과가 이상하게 나와요!
  A: 이미지 해상도를 올리거나 글씨가 잘 보이게 전처리해보세요.
- Q: 번역이 잘 안 되는데?
  A: 인터넷 연결을 확인하고, 구글 번역 서비스 상태를 점검하세요.

■ 문의: 언제든 도움 필요하면 개발자에게 연락!

""",
    "en": """
■■■ EasyOCR Program Help ■■■

1. New Area OCR
- Drag to select any area on the screen and extract its text.

2. Open Image File
- Load image files (PNG, JPG, BMP, etc.) to extract text.

3. Copy/Delete/Translate
- Click a result in the list, then use Copy, Delete, or Translate.

4. Switch to Dark Mode
- Switch to a dark, eye-friendly theme.

5. Change Language
- UI supports Korean, English, Japanese, and Chinese.

6. Hotkeys
- Ctrl+C: Copy, Del: Delete, F1: Open help (Upcoming)

7. History Search/Favorite/Export (Upcoming)
- Will support searching, favorites, and export soon.

■ FAQ
- Q: OCR result is weird!
  A: Try higher-resolution images or clearer text.

- Q: Translation doesn't work well?
  A: Check your internet connection and Google Translate service.

■ Contact: Feel free to ask for help anytime!
""",
    "ja": """
■■■ EasyOCR プログラム ヘルプ ■■■

1. 新しい領域OCR
- 画面をドラッグして選択し、テキストを認識します。

2. ファイルを開く
- 画像ファイル(PNG, JPG, BMP等)からテキストを抽出します。

3. コピー/削除/翻訳
- リストの結果をクリックしてボタンで操作します。

4. ダークモード切替
- 目に優しいダークテーマに変更可能です。

5. 言語変更
- UIは韓国語、英語、日本語、中国語に対応します。

6. ホットキー
- Ctrl+C: コピー, Del: 削除, F1: ヘルプ(今後追加予定）

7. 履歴検索/お気に入り/エクスポート（今後追加予定）

■ FAQ
- Q: OCR結果がおかしい！
  A: 解像度を上げるか、文字をもっとはっきりさせてみてください。

- Q: 翻訳が上手くいかない？
  A: インターネット接続とGoogle翻訳の状態を確認してください。

■ お問い合わせ：ご質問があればお気軽にどうぞ！
""",
    "zh": """
■■■ EasyOCR 程序帮助 ■■■

1. 新区域OCR
- 拖拽选取屏幕区域，识别并提取文字。

2. 打开图片文件
- 支持PNG、JPG、BMP等图片格式提取文字。

3. 复制/删除/翻译
- 在列表中点击结果，再使用相应按钮。

4. 切换暗模式
- 可切换为护眼的深色主题。

5. 更改语言
- 支持中文、韩文、英文、日文界面。

6. 快捷键
- Ctrl+C: 复制, Del: 删除, F1: 打开帮助（即将上线）

7. 历史搜索/收藏/导出（即将上线）

■ 常见问题(FAQ)
- Q: OCR 结果不对？
  A: 请尝试更高清晰度的图片或让文字更清楚。

- Q: 翻译不正常？
  A: 请检查网络连接及Google翻译服务状态。

■ 联系：如需帮助，请随时联系我们！
"""
}

def show_help(lang_code="ko"):
    msg = HELP_TEXTS.get(lang_code, HELP_TEXTS["ko"])
    help_win = tk.Toplevel()
    help_win.title({"ko": "도움말", "en": "Help", "ja": "ヘルプ", "zh": "帮助"}.get(lang_code, "Help"))
    text = tk.Text(help_win, width=78, height=27, wrap='word')
    text.insert(tk.END, msg)
    text.config(state='disabled', font=("맑은 고딕", 11))
    text.pack(padx=16, pady=12)
    btn_close = tk.Button(help_win, text={"ko": "닫기", "en": "Close", "ja": "閉じる", "zh": "关闭"}.get(lang_code, "Close"), command=help_win.destroy)
    btn_close.pack(pady=10)
    # 도움말 창은 모달(항상 위)에 띄우기
    help_win.grab_set()
    help_win.transient()
