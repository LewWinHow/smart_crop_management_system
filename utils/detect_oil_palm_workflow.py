import os
from django.conf import settings

from utils.llm import build_llm_prompt, llm, llm_for_user, build_structured_prompt, llm_classify
from utils.rag import run_rag
from utils.vlm import run_vlm


def resolve_image_path(image_path: str) -> str:
    """
    统一处理路径：
    - 如果是绝对路径 → 直接用
    - 如果是 media 相对路径 → 拼接 MEDIA_ROOT
    """

    # 1. 已经是绝对路径
    if os.path.isabs(image_path):
        return image_path

    # 2. Django media 相对路径
    full_path = os.path.join(settings.MEDIA_ROOT, image_path)

    return full_path


def pipeline(image_path):
    # -------------------
    # 0. 路径统一处理
    # -------------------
    full_image_path = resolve_image_path(image_path)

    # 安全检查
    if not os.path.exists(full_image_path):
        raise FileNotFoundError(f"Image not found: {full_image_path}")

    # -------------------
    # 1. VLM
    # -------------------
    vlm_result = run_vlm(full_image_path)

    if vlm_result is None:
        vlm_result = {
            "visible_symptoms": [],
            "search_keywords": ["oil palm health"]
        }

    # -------------------
    # 2. RAG
    # -------------------
    search_keywords = vlm_result.get("search_keywords", [])
    web_context = run_rag(search_keywords)

    # -------------------
    # 3. LLM Prompt
    # -------------------
    prompt = build_llm_prompt(vlm_result, web_context)
    json_result = llm_classify(vlm_result, web_context)

    # -------------------
    # 4. LLM Output
    # -------------------
    result = llm(prompt)
    response = llm_for_user(result)

    return response, json_result