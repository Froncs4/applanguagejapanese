import io
from gtts import gTTS

def generate_japanese_voice(text: str) -> bytes:
    """
    Генерирует голосовое сообщение (японский язык) из текста с помощью Google TTS.
    Возвращает байты аудиофайла.
    """
    tts = gTTS(text=text, lang='ja')
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return buffer.getvalue()