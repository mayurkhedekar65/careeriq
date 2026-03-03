from rest_framework import serializers
from .models import AptitudeTest, AptitudeQuestions


#Start Test Serializer
class StartTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = AptitudeTest
        fields = [
            "id",
            "test_mode",
            "category",
            "difficulty_level",
            "no_of_questions",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


#For Showing questions to user
class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AptitudeQuestions
        fields = [
            "id",
            "question_text",
            "difficulty_level",
            "user_answer",
        ]
        many = True
        


#For Submitting answer of a question
class SubmitAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = AptitudeQuestions
        fields = [
            "id",
            "user_answer",
        ]


#Test Result Serializer
class TestResultSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = AptitudeTest
        fields = [
            "id",
            "test_mode",
            "category",
            "difficulty_level",
            "no_of_correct_answers",
            "score",
            "created_at",
            "questions",
        ]