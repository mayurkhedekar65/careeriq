from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AptitudeTest, AptitudeQuestions
from .serializers import StartTestSerializer, QuestionSerializer, SubmitAnswerSerializer, TestResultSerializer
from fastapi import requests
from django.http import JsonResponse
import json

# Create your views here.
class StartTestView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = StartTestSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            test_mode = serializer.validated_data.get('test_mode')
            category = serializer.validated_data.get('category')
            difficulty_level = serializer.validated_data.get('difficulty_level')
            no_of_questions = serializer.validated_data.get('no_of_questions')
            aptitude_test = AptitudeTest.objects.create(user_id=user_id, test_mode=test_mode, category=category, difficulty_level=difficulty_level, no_of_questions=no_of_questions)
            aptitude_test.save()
            if aptitude_test.category == "All Categories" or aptitude_test.test_mode == "Full Developer Mock":
                all_category = "Logical Reasoning, Programming Logic, CS Fundamentals, Core Concepts, Data Interpretation"
                response = requests.post("http://127.0.0.1:8001/generate_aptitude_test", json={
                "test_mode": test_mode, "category": all_category, "difficulty_level": difficulty_level , "no_of_questions": no_of_questions})
            else:
                response = requests.post("http://127.0.0.1:8001/generate_aptitude_test", json={
                "test_mode": test_mode, "category": category, "difficulty_level": difficulty_level, "no_of_questions": no_of_questions})
            aptitude_questions = AptitudeQuestions.objects.create(test=aptitude_test, category=category, question_text=response.json()["questions"], correct_answer=response.json()["answer"], difficulty_level=difficulty_level)
            aptitude_questions.save()
            return JsonResponse({
                "id": aptitude_test.id,
                "test_mode": test_mode,
                "category": category,
                "difficulty_level": difficulty_level,
                "question": response.json()["question"]
            }, safe=False)
        
class SubmitAnswerView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = SubmitAnswerSerializer(data=request.data)
        if serializer.is_valid():
            question_id = serializer.validated_data.get('id')
            user_answer = serializer.validated_data.get('user_answer')
            question = AptitudeQuestions.objects.get(id=question_id)
            question.user_answer = user_answer
            question.is_correct = (user_answer == question.correct_answer)
            question.save()
            return JsonResponse({
                "id": question.id,
                "user_answer": user_answer,
                "is_correct": question.is_correct
            }, safe=False)
        
class Test_History_View(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = TestResultSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            tests = AptitudeTest.objects.filter(user_id=user_id)
            category = serializer.validated_data.get('category')
            difficulty_level = serializer.validated_data.get('difficulty_level')
            no_of_correct_answers = serializer.validated_data.get('no_of_correct_answers')
            score = serializer.validated_data.get('score')
            return JsonResponse({
                "id": user_id,
                "test_mode": tests.test_mode,
                "category": category,
                "difficulty_level": difficulty_level,
                "no_of_correct_answers": no_of_correct_answers,
                "score": score
            }, safe=False)

class display_data(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            test_id = serializer.validated_data.get('test_id')
            llm_data = AptitudeQuestions.objects.filter(test_id=test_id).order_by('id').values()
            return Response({"llm_data": llm_data})