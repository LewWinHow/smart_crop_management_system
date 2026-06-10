import requests
import json
import re


def detect_language(text):
    """
    检测文本使用的语言
    返回: 'chinese', 'english', 或 'mixed'
    """
    # 计算中文字符比例
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.strip())
    
    if total_chars == 0:
        return 'english'
    
    chinese_ratio = chinese_chars / total_chars
    
    # 如果中文占比超过30%，认为是中文
    if chinese_ratio > 0.3:
        return 'chinese'
    else:
        return 'english'


def llm(prompt, model='gpt-oss:120b-cloud', temperature=0.3):
    """
    通用 LLM 函数，用于 AI 助手对话
    增强了农业专业知识的上下文
    根据用户语言自动调整回答语言
    """
    
    # 检测用户使用的语言
    user_language = detect_language(prompt)
    
    # 根据语言设置系统提示词
    if user_language == 'chinese':
        system_prompt = """
你是一位经验丰富的油棕树农业专家助手，专门为油棕种植园农民提供技术支持。

## 重要回答规则：
1. 必须使用简单易懂的白话文回答
2. 不要用表格、图表或特殊图标格式（如 | 项目 | 正常 | 异常 | 这种）
3. 不要用 emoji 图标（如 ✅ ❌ 🔸 等）
4. 用普通文字段落和编号列表（1. 2. 3.）来组织内容
5. 像跟农民聊天一样，用口语化、亲切的语言
6. 避免专业术语，如必须使用要解释清楚

## 你的职责：
- 帮助农民识别和解决油棕树的健康问题
- 提供科学的种植管理建议
- 关注预防和监测
- 不要推荐农药或化学药剂

## 回答示例：

不好的回答（不要用）：
| 症状 | 正常 | 异常 |
| 叶片 | 绿色 | 黄色 |
✅ 灵芝病识别
❌ 不要这样做

好的回答（应该这样）：
灵芝病是油棕树常见的病害。你可以通过以下几个方法来判断：

第一，看树干基部有没有长出像灵芝一样的白色真菌，这是最明显的特征。

第二，观察叶片，如果发现从下往上的叶子开始变黄，就要注意。

第三，用手敲击树干，如果声音沉闷，可能内部已经腐烂。

预防措施很简单：保持排水通畅，及时清理病死树，定期检查。

请基于以上规则回答用户的问题。"""
    else:  # english
        system_prompt = """
You are an experienced oil palm agricultural expert assistant, providing technical support for oil palm plantation farmers.

## Important Answer Rules:
1. Use simple, plain language that farmers can easily understand
2. Do NOT use tables, charts, or special icon formats (like | Item | Normal | Abnormal |)
3. Do NOT use emoji icons (like ✅ ❌ 🔸 etc.)
4. Use regular text paragraphs and numbered lists (1. 2. 3.) to organize content
5. Speak like you're chatting with farmers - friendly and conversational
6. Avoid technical jargon, explain if necessary

## Your Responsibilities:
- Help farmers identify and solve oil palm tree health problems
- Provide scientific planting management advice
- Focus on prevention and monitoring
- Do NOT recommend pesticides or chemicals

## Answer Example:

Bad answer (DO NOT use):
| Symptom | Normal | Abnormal |
| Leaves | Green | Yellow |
✅ Ganoderma identification
❌ Don't do this

Good answer (USE this style):
Ganoderma disease is common in oil palm trees. You can identify it by these methods:

First, look at the trunk base for white mushroom-like fungus growth. This is the most obvious sign.

Second, check the leaves. If lower leaves start turning yellow upward, pay attention.

Third, knock on the trunk. A dull sound may indicate internal rot.

Prevention is simple: keep good drainage, remove diseased trees promptly, and inspect regularly.

Please answer based on these rules."""
    
    prompt1 = f'''{system_prompt}

User input: {prompt}

Please respond in {'Chinese' if user_language == 'chinese' else 'English'}, following all the rules above.

'''

    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': model,
            'prompt': prompt1,
            'temperature': temperature,
            'stream': True
        },
        stream=True
    )

    result = ""

    for line in response.iter_lines():
        if not line:
            continue

        try:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                result += data["response"]
        except:
            continue

    return result.strip()


def build_llm_prompt(vlm_json, web_context):
    return f"""
You are a senior oil palm agricultural AI consultant.

You receive:

1. VLM Analysis (image understanding)
{json.dumps(vlm_json, indent=2)}

2. Web Agricultural Knowledge (RAG)
{web_context}

----------------------------------------

TASK:
- Analyze tree condition
- Interpret health status
- Estimate production impact
- Provide farming management advice

IMPORTANT RULES:
- NO pesticide or chemical instructions
- Focus on monitoring and agricultural decision support
- Be factual and based on evidence

----------------------------------------

Return ONLY valid JSON:

{{
  "tree_health_summary": "",
  "production_analysis": "",
  "risk_level": "Low / Medium / High",
  "management_advice": [
    ""
  ],
  "supporting_evidence": "",
  "confidence_level": "Low / Medium / High"
}}
"""


def build_user_prompt(json_result):
    return f"""
You are an agricultural assistant for oil palm farmers.

Your task is to explain the analysis in simple, clear English.

Do NOT output JSON. Do NOT use technical format.

Explain in a friendly way that a farmer can understand.

Here is the analysis result:

{json_result}

Please explain:

1. Tree health condition
2. Production situation
3. Risk level meaning
4. What the farmer should understand (NO treatment instructions)
"""


def llm_for_user(json_result):
    prompt = build_user_prompt(json_result)

    result = llm(prompt)

    return result


import json
import requests


def llm_fixed_json(prompt, model='gpt-oss:120b-cloud', temperature=0.2):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': model,
            'prompt': prompt,
            'temperature': temperature,
            'stream': True
        },
        stream=True
    )

    result = ""

    for line in response.iter_lines():
        if not line:
            continue

        try:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                result += data["response"]
        except:
            continue

    return result.strip()


def build_structured_prompt(vlm_json, web_context):
    """
    构建结构化分类提示词，用于图像分析和疾病识别
    结合 VLM 分析和 RAG 知识库
    """
    return f"""
You are an expert oil palm agricultural classifier with deep knowledge of plantation management.

You MUST classify the tree into fixed integer labels based on visual evidence and agricultural knowledge.

You are given:

1. VLM Analysis (Visual Understanding from Image):
{json.dumps(vlm_json, indent=2)}

2. Web & Local Agricultural Knowledge (RAG Context):
{web_context}

-----------------------------------

OUTPUT RULES (STRICT):
Return ONLY valid JSON.
No explanation. No text. No markdown.

-----------------------------------

CLASSIFICATION RULES:

STATUS (Health Condition):
1 = Healthy (健康)
   - Deep green leaves, dense canopy
   - Normal growth rate
   - No visible symptoms

2 = Nutrient Deficiency (营养缺乏)
   - Yellowing leaves (especially older leaves)
   - Slow growth
   - Specific patterns: leaf tip burning, interveinal chlorosis

3 = Sick (患病)
   - Disease symptoms visible
   - Fungal growth, lesions, rot
   - Severe yellowing or wilting

DISEASE (Specific Disease Type):
1 = None (无病害)
2 = Ganoderma Disease / Basal Stem Rot (灵芝病/基腐病)
   - White fungal body at trunk base (mushroom-like)
   - Yellowing from bottom leaves upward
   - Trunk decay, soft wood
   - Sparse canopy

3 = Leaf Spot (叶斑病)
   - Circular or irregular spots on leaves
   - Gray-white centers with brown edges
   - Common in high humidity

4 = Anthracnose (炭疽病)
   - Water-soaked spots on leaves
   - Brown or black expanding lesions
   - Leaf tips and margins affected
   - Small black dots in wet conditions

PRODUCTIVITY (Fruit Production Status):
1 = Producing (有生产)
   - Visible fruit bunches
   - Orange-red colored fruits
   - Active flowering

2 = Not Producing (没有生产)
   - No fruit visible
   - Tree too young (< 2.5 years)
   - Post-harvest recovery period

3 = Unknown (未知)
   - Image unclear
   - Cannot determine from visual evidence

-----------------------------------

DECISION GUIDELINES:

Step 1 - Assess Overall Health:
- If tree looks vigorous with deep green leaves → status = 1
- If yellowing present, especially older leaves → status = 2
- If disease symptoms (fungus, lesions, rot) → status = 3

Step 2 - Identify Disease (if status = 3):
- Trunk base with mushroom-like fungus → disease = 2 (Ganoderma)
- Circular leaf spots → disease = 3 (Leaf Spot)
- Water-soaked lesions with black dots → disease = 4 (Anthracnose)
- No disease symptoms but unhealthy → disease = 1

Step 3 - Assess Productivity:
- Visible fruit bunches → productivity = 1
- No fruit but healthy mature tree → productivity = 2
- Cannot see clearly → productivity = 3

IMPORTANT:
- Ganoderma (灵芝病) is identified by fungal growth at trunk base
- Nutrient deficiency shows as yellowing without fungal symptoms
- Always base classification on visible evidence from image

-----------------------------------

OUTPUT FORMAT:

{{
  "status": 0,
  "disease": 0,
  "productivity": 0
}}
"""


import json


def llm_classify(vlm_json, web_context):
    """
    使用 LLM 进行分类，结合 VLM 图像分析和 RAG 知识库
    返回结构化的分类结果
    """
    prompt = build_structured_prompt(vlm_json, web_context)

    result = llm_fixed_json(prompt)

    # 安全解析
    try:
        return json.loads(result)
    except:
        # fallback（防止模型乱输出）
        return {
            "status": 1,
            "disease": 1,
            "productivity": 0
        }
