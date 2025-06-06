import easyocr
import cv2
import numpy as np
import re

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 히스토그램 평활화
    gray = cv2.equalizeHist(gray)
    # 샤프닝
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharp = cv2.filter2D(gray, -1, kernel)
    # 노이즈 제거
    blur = cv2.medianBlur(sharp, 3)
    # adaptive threshold
    binary = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # 크기 확대
    resized = cv2.resize(binary, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    return resized

def correct_text(text):
    # 가장 흔한 오타/오인식 자동 교정
    corrections = [
        (" l ", " I "), ("0", "O"), ("  ", " "), ("-", "-"), ("_", "-")
        # 추가로 자주 틀리는 패턴 직접 추가 가능
    ]
    for wrong, right in corrections:
        text = text.replace(wrong, right)
    return text

def postprocess_text(text):
    # 한글, 영어, 숫자, 일부 특수문자만 남기기
    text = re.sub(r'[^ㄱ-ㅎ가-힣a-zA-Z0-9 .,?!\-+\n]', '', text)
    # 오타 자동 보정
    text = correct_text(text)
    return text.strip()

def process_ocr(img):
    preprocessed = preprocess_image(img)
    reader = easyocr.Reader(['ko', 'en'], gpu=False)
    results = reader.readtext(preprocessed, detail=1)
    text_output = []
    for bbox, text, conf in results:
        if conf > 0.3:  # 신뢰도 필터
            text_output.append(text)
    if text_output:
        raw = " ".join(text_output)
        processed = postprocess_text(raw)
        return processed
    else:
        return "⚠️ 텍스트를 인식하지 못했습니다."
