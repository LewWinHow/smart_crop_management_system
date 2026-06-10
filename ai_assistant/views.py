from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from markdown_it.rules_inline import newline
from rest_framework.views import APIView

import ai_assistant
from ai_assistant.models import Chat
from utils.audio_to_text import audio_to_text
from utils.llm import *
from utils.rag import run_rag
import re


# Create your views here.
class GetChat(LoginRequiredMixin, APIView):
    def get(self, request):
        employee = request.user
        permission = employee.permission
        if Chat.objects.filter(employee=employee).exists() is False:
            message = Chat.objects.create(
                message="Hi, I'm your Smart Crop Management System AI Assistant. How can I help you?\n"
                        "你好， 我是你的智能农物管理系统AI助手。有什么我可以帮到你的呢？", employee=employee, sender=2)
            message.save()
        
        chat_list = Chat.objects.filter(employee=employee).all()
        return render(request, 'ai_assistant/chat.html', {'chat_list': chat_list, 'permission': permission})

    def post(self, request):
        employee = request.user
        message = (request.data.get('message','') or '').strip() or None

        if message is None:
            return JsonResponse({'error': 'Empty message'}, status=400)

        # 保存用户消息
        Chat.objects.create(message=message, employee=employee, sender=1).save()

        # 使用 RAG 检索相关农业知识
        search_keywords = self.extract_keywords(message)
        rag_context = run_rag(search_keywords) if search_keywords else ""
        
        # 构建增强的 prompt，包含 RAG 检索的知识
        enhanced_prompt = self.build_enhanced_prompt(message, rag_context)
        
        # 调用 LLM 生成回复
        response = llm(enhanced_prompt)
        
        # 保存 LLM 回复
        Chat.objects.create(message=response, employee=employee, sender=2).save()

        # 返回完整的聊天记录
        chat_list = Chat.objects.filter(employee=employee).all()
        data = {
            'chat_list': [
                {
                    'message': chat.message,
                    'sender': chat.sender
                } for chat in chat_list
            ]
        }
        return JsonResponse(data)
    
    def extract_keywords(self, message):
        """
        从用户消息中提取关键词用于 RAG 检索
        """
        # 定义农业相关关键词模式
        keywords = []
        
        # 疾病相关
        disease_patterns = [
            r'灵芝病', r'ganoderma', r'basal stem rot',
            r'叶斑病', r'leaf spot',
            r'炭疽病', r'anthracnose',
            r'病害', r'disease',
        ]
        
        # 营养相关
        nutrient_patterns = [
            r'营养', r'nutrient',
            r'氮肥', r'nitrogen',
            r'钾肥', r'potassium',
            r'镁', r'magnesium',
            r'硼', r'boron',
            r'施肥', r'fertilizer',
        ]
        
        # 管理相关
        management_patterns = [
            r'灌溉', r'irrigation', r'浇水', r'water',
            r'采收', r'harvest', r'fruit',
            r'土壤', r'soil', r'pH',
            r'害虫', r'pest', r'insect',
        ]
        
        # 检查消息中包含哪些关键词
        message_lower = message.lower()
        
        for pattern in disease_patterns + nutrient_patterns + management_patterns:
            if re.search(pattern, message_lower):
                keywords.append(pattern)
        
        return keywords
    
    def build_enhanced_prompt(self, user_message, rag_context):
        """
        构建增强的 prompt，结合用户问题和 RAG 检索的知识
        强调使用白话文回答
        """
        if rag_context:
            return f"""
你是一个专业的油棕树农业助手。

## 相关农业知识（供参考）：
{rag_context}

## 用户问题：
{user_message}

## 回答要求：
1. 使用简单易懂的白话文
2. 不要用表格（如 | 项目 | 正常 | 异常 |）
3. 不要用特殊图标（如 ✅ ❌ 🔸 等）
4. 用普通段落和编号（1. 2. 3.）来组织内容
5. 像跟农民聊天一样，口语化、亲切
6. 根据用户使用的语言（中文/英文）回答

请基于农业知识，用简单易懂的语言回答用户的问题。
"""
        else:
            return user_message


class ClearChat(LoginRequiredMixin, View):
    def get(self, request):
        employee = request.user
        chat_list = Chat.objects.filter(employee=employee).all()
        chat_list.delete()

        return redirect('ai_assistant:get_chat')



