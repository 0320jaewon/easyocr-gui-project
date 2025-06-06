# easyocr-gui-project
EasyOCR과 tkinter 기반의 텍스트 추출 및 번역 프로그램
주요기능
- 화면 드래그로 영역 지정 후 OCR 실행
- 이미지 파일 불러오기 및 OCR 처리
- Google Translate API 기반 자동 번역
- 다국어 UI 지원 (한/영/일/중)
- 다크모드 전환 및 히스토리 관리

  사용된 기술 스택
- - Python
- EasyOCR
- googletrans
- tkinter
- Pillow, OpenCV

  파일 구성
- `main.py`: 실행 진입점
- `ocr_core.py`: 이미지 전처리 및 OCR 처리
- `ocr_gui.py`: 전체 GUI 구성
- `ocr_translate.py`: 번역 기능
- `ocr_help.py`: 도움말 UI
