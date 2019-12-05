from rest_framework import serializers
from .models import SIMSStudent


class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = SIMSStudent
        fields = ('student_id', 'first_name', 'last_name', 'tutor_group_id', 'house_id', 'EAL_status', 'SEN_status')
