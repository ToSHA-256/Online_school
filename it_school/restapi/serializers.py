from rest_framework import serializers

from mainpage.models import Course, DAYS_OF_WEEK_CHOICES, Lesson, CustomUser


class WeekdaysField(serializers.Field):
    def to_representation(self, value):
        return ', '.join([dict(DAYS_OF_WEEK_CHOICES).get(item) for item in value])

    def to_internal_value(self, data):
        return [key for key, value in DAYS_OF_WEEK_CHOICES if value in data]


class CourseSerializer(serializers.ModelSerializer):
    days_of_week = serializers.MultipleChoiceField(choices=DAYS_OF_WEEK_CHOICES, allow_blank=False)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'short_des', 'difficulty', 'rating', 'price', 'start_date',
                  'start_time', 'days_of_week', 'technologies', 'lessons_count', 'mentor']

    def create(self, validated_data):
        days_of_week = validated_data.get('days_of_week', [])
        print(days_of_week)
        instance = Course.objects.create(**validated_data)
        print(instance)
        instance.days_of_week = days_of_week

        print(instance)
        print(instance.days_of_week)
        instance.save()
        return instance


class CustomUserSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'courses')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'start_date', 'start_time')


class LessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'start_date', 'start_time', 'material')
