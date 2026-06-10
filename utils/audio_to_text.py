# import os
# import uuid
#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.conf import settings
#
# from funasr import AutoModel
#
# # ✅ 加载模型（中文优化）
# # model="paraformer-zh", vad_model="fsmn-vad", punc_model="ct-punc-c"
# model = AutoModel(
#     model="paraformer-en-small",
#     vad_model="fsmn-vad",
#     punc_model="ct-punc-c"
# )
#
# def audio_to_text(audio):
#     tmp_dir = os.path.join(settings.MEDIA_ROOT, "tmp")
#     os.makedirs(tmp_dir, exist_ok=True)
#
#     filename = f"{uuid.uuid4()}.webm"
#     file_path = os.path.join(tmp_dir, filename)
#
#     # 保存上传音频
#     with open(file_path, "wb+") as f:
#         for chunk in audio.chunks():
#             f.write(chunk)
#
#     try:
#         # ✅ FunASR 识别
#         res = model.generate(input=file_path)
#
#         # ⚠️ FunASR 返回是 list
#         text = res[0]["text"]
#
#     finally:
#         # 删除临时文件
#         if os.path.exists(file_path):
#             os.remove(file_path)
#
#     return text
import os
import uuid

from django.conf import settings
import whisper

# ✅ 加载 Whisper 小模型（超小 & 快）
model = whisper.load_model("tiny")


def audio_to_text(audio):
    tmp_dir = os.path.join(settings.MEDIA_ROOT, "tmp")
    os.makedirs(tmp_dir, exist_ok=True)

    filename = f"{uuid.uuid4()}.webm"
    file_path = os.path.join(tmp_dir, filename)

    # 保存上传音频
    with open(file_path, "wb+") as f:
        for chunk in audio.chunks():
            f.write(chunk)

    try:
        # ✅ Whisper 识别（自动处理格式）
        result = model.transcribe(file_path)

        text = result["text"]

    finally:
        # 删除临时文件
        if os.path.exists(file_path):
            os.remove(file_path)

    return text