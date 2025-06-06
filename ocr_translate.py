# ocr_translate.py

from googletrans import Translator
import time
import datetime
import os

translator = Translator()
LOG_FILE = "translate_error.log"

def translate_text(text, src='auto', dest='ko', log_error=True):
    try:
        result = translator.translate(text, src=src, dest=dest)
        return result.text
    except Exception as e:
        if log_error:
            log_translate_error(text, src, dest, e)
        return f"[번역 실패] {e}"

def batch_translate(texts, src='auto', dest='ko'):
    results = []
    for t in texts:
        results.append(translate_text(t, src, dest))
    return results

def detect_language(text):
    try:
        result = translator.detect(text)
        return result.lang
    except Exception as e:
        log_translate_error(text, "auto", "detect", e)
        return None

def save_translations(texts, translations, filename=None):
    if not filename:
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"translations_{now}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for i, (orig, trans) in enumerate(zip(texts, translations)):
                f.write(f"[{i+1}] 원문: {orig}\n")
                f.write(f"[{i+1}] 번역: {trans}\n\n")
        return filename
    except Exception as e:
        log_translate_error("[SAVE]", "auto", "file", e)
        return None

def log_translate_error(text, src, dest, error):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] SRC:{src} DEST:{dest} TEXT:{text}\n")
            f.write(f"ERROR: {error}\n\n")
    except:
        pass

def summary_report(texts, translations, src, dest, exec_time):
    n = len(texts)
    diff_count = sum([o != t for o, t in zip(texts, translations)])
    stat = (
        f"총 {n}개 문장 번역 ({src} → {dest})\n"
        f"실패/불일치 번역 {diff_count}개\n"
        f"수행 시간: {exec_time:.2f}초\n"
    )
    return stat

def split_paragraphs(text):
    import re
    sents = re.split(r'(?<=[.?!])\s+', text.strip())
    return [s for s in sents if s]

def pretty_print(orig, trans, sep_len=40):
    print("-" * sep_len)
    print(f"원문: {orig}\n번역: {trans}")
    print("-" * sep_len)

def test_all():
    print("=== ocr_translate.py 테스트 ===")
    samples = [
        "Hello, how are you?",
        "배고파요. 밥 먹었니?",
        "これは日本語の文章です。",
        "OCR 결과를 바로 번역할 수 있습니다!"
    ]
    langs = [detect_language(t) for t in samples]
    print("자동 언어 감지 결과:", langs)
    start = time.time()
    translations = batch_translate(samples, src='auto', dest='ko')
    exec_time = time.time() - start
    for orig, trans in zip(samples, translations):
        pretty_print(orig, trans)
    stat = summary_report(samples, translations, "auto", "ko", exec_time)
    print(stat)
    fn = save_translations(samples, translations)
    print("번역 결과가 저장된 파일:", fn)

if __name__ == "__main__":
    test_all()
