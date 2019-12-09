from rest_framework import serializers
from .models import Student


class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('student_id', 'first_name', 'last_name', 'tutor_group_id', 'house_id', 'EAL_status', 'SEN_status')
