from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import AllowAny
from .models import TeacherUsersStats, TeacherTopic
import pandas as pd
from django.utils.timezone import is_aware
from django.http import HttpResponse
import io

__all__ = [
    'TeacherUsersStatsView',
    'ExportToExcelView',
    'TeacherEditView',
    'TopicsView',
    'TopicedTeachersView'
]


class TopicsView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = TeacherTopic.objects.all()
    serializer_class = TopicsSerializer

class TeacherUsersStatsView(APIView):
    serializer_class = TeacherUsersStatsSerializer
    permission_classes = [AllowAny]
    def get(self, request):
        stats = TeacherUsersStats.objects.all()
        serializer = self.serializer_class(stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeacherEditView(APIView):
    serializer_class = TeacherEditSerializer
    permission_classes = [AllowAny]

    def get(self, request, id=None):
        try:
            stats = TeacherUsersStats.objects.get(id=id)
        except TeacherUsersStats.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(stats)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id=None):
        try:
            stats = TeacherUsersStats.objects.get(id=id)
        except TeacherUsersStats.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(stats, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExportToExcelView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = TeacherUsersStats.objects.all()
        data = []

        for obj in queryset:
            updated_at = obj.updated_at
            if is_aware(updated_at):
                updated_at = updated_at.replace(tzinfo=None)

            data.append({
                'full_name': obj.full_name,
                'juda_ham_qoniqaman': obj.juda_ham_qoniqaman,
                'ortacha_qoniqaman': obj.ortacha_qoniqaman,
                'asosan_qoniqaman': obj.asosan_qoniqaman,
                'qoniqmayman': obj.qoniqmayman,
                'umuman_qoniqaman': obj.umuman_qoniqaman,
                'updated_at': updated_at,
                'topic_name': obj.topic.topic_name if obj.topic else None
            })

        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='TeacherStats')

        output.seek(0)

        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=teacher_users_stats.xlsx'
        return response
    
class TopicedTeachersView(ListAPIView):
    queryset = TeacherUsersStats.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TopicedTeachersSerializer
