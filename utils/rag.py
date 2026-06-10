from ddgs import DDGS
from utils.agricultural_knowledge import AGRICULTURAL_KNOWLEDGE


def search_web(query, max_results=3):
    """
    搜索网络获取最新的农业知识
    """
    results_text = []

    enhanced_query = f"oil palm agriculture {query}"

    with DDGS() as ddgs:
        results = ddgs.text(enhanced_query, max_results=max_results)

        for r in results:
            title = r.get("title", "")
            body = r.get("body", "")
            href = r.get("href", "")

            results_text.append(f"""
Title: {title}
Content: {body}
Source: {href}
""")

    return "\n".join(results_text)


def get_local_knowledge(query):
    """
    从本地知识库中检索相关信息
    使用关键词匹配来查找相关的农业知识
    """
    query_lower = query.lower()
    
    # 关键词映射 - 将用户问题映射到知识库主题
    knowledge_mapping = {
        'ganoderma': '灵芝病',
        'basal stem rot': '灵芝病',
        '灵芝': '灵芝病',
        'fungus': '灵芝病',
        'fungal': '灵芝病',
        
        'nutrient': '营养缺乏症',
        'nitrogen': '氮素缺乏',
        'potassium': '钾素缺乏',
        'magnesium': '镁素缺乏',
        'boron': '硼素缺乏',
        'yellow': '营养缺乏症',
        'fertilizer': '土壤管理',
        '施肥': '土壤管理',
        
        'leaf spot': '叶斑病',
        'anthracnose': '炭疽病',
        'disease': '病害',
        '病害': '病害',
        
        'growth': '生长阶段',
        'age': '生长阶段',
        'year': '生长阶段',
        '种植': '生长阶段',
        
        'soil': '土壤管理',
        'ph': '土壤管理',
        '土壤': '土壤管理',
        
        'water': '灌溉管理',
        'irrigation': '灌溉管理',
        'rain': '灌溉管理',
        '灌溉': '灌溉管理',
        '浇水': '灌溉管理',
        
        'harvest': '采收管理',
        'fruit': '采收管理',
        'yield': '采收管理',
        '采收': '采收管理',
        '结果': '采收管理',
        
        'pest': '常见害虫',
        'insect': '常见害虫',
        'beetle': '常见害虫',
        '害虫': '常见害虫',
        
        'health': '环境监测指标',
        'healthy': '健康监测',
        'symptom': '症状识别',
        '症状': '症状识别',
        '判断': '判断方法',
        'how to identify': '判断方法',
    }
    
    # 查找匹配的主题
    matched_topics = []
    for keyword, topic in knowledge_mapping.items():
        if keyword in query_lower:
            if topic not in matched_topics:
                matched_topics.append(topic)
    
    # 如果没有匹配到特定主题，返回整个知识库
    if not matched_topics:
        return AGRICULTURAL_KNOWLEDGE
    
    # 提取匹配主题的相关内容
    relevant_sections = []
    for topic in matched_topics:
        # 简单实现：返回包含该主题的所有内容
        # 可以优化为更精确的段落提取
        relevant_sections.append(f"## 相关主题：{topic}")
    
    # 返回知识库中标题包含匹配主题的部分
    lines = AGRICULTURAL_KNOWLEDGE.split('\n')
    selected_lines = []
    current_section = None
    include_section = False
    
    for line in lines:
        if line.startswith('###'):
            current_section = line
            include_section = any(topic in line for topic in matched_topics)
        
        if include_section or line.startswith('## 油棕树'):
            selected_lines.append(line)
    
    if selected_lines:
        return '\n'.join(selected_lines)
    
    return AGRICULTURAL_KNOWLEDGE


def run_rag(search_keywords):
    """
    运行 RAG 系统，结合本地知识库和网络搜索
    """
    if not search_keywords:
        return ""

    # 首先从本地知识库获取信息
    query = ' '.join(search_keywords)
    local_knowledge = get_local_knowledge(query)
    
    # 然后从网络搜索补充信息
    all_docs = [local_knowledge]
    
    for kw in search_keywords:
        web_results = search_web(kw)
        if web_results:
            all_docs.append(web_results)

    return "\n\n".join(all_docs)