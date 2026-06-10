from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch
import json
import re


# -----------------------
# Load model
# -----------------------
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-2B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto"
)

processor = AutoProcessor.from_pretrained(
    "Qwen/Qwen2-VL-2B-Instruct"
)


# -----------------------
# JSON cleaner
# -----------------------
def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None
    return None


# -----------------------
# VLM FUNCTION
# -----------------------
def run_vlm(image_path):

    prompt = """
You are an oil palm agriculture expert.

Return ONLY valid JSON. No markdown, no explanation.

{
  "tree_characteristics": {
    "leaf_color": "",
    "fruit_visibility": "",
    "crown_condition": "",
    "trunk_condition": ""
  },
  "visible_symptoms": [],
  "health_status": "",
  "possible_condition": "",
  "production_status": "",
  "search_keywords": [],
  "overall_assessment": ""
}

Generate highly specific agricultural search keywords based on visible symptoms.

Bad example:
- oil palm agriculture

Good example:
- oil palm yellow leaves nutrient deficiency
- low fruit bunch density oil palm yield
- oil palm crown sparse symptoms
"""

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image_path},
                {"type": "text", "text": prompt}
            ]
        }
    ]

    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    image_inputs, video_inputs = process_vision_info(messages)

    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt"
    )

    inputs = inputs.to(model.device)

    generated_ids = model.generate(
        **inputs,
        max_new_tokens=512
    )

    # ✅ FIX: remove prompt tokens
    generated_ids_trimmed = [
        out_ids[len(in_ids):]
        for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]

    output = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True
    )[0]

    # convert JSON safely
    return extract_json(output)