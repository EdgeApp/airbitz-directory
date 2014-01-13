from rest_framework import serializers

from directory.models import Business, BusinessImage, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name','description')

class MiniBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('name',
                  'description',
                  'city',
                  'state', 
                  'postalcode')

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('name',
                  'description',
                  'city',
                  'state', 
                  'postalcode')

class BusinessImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessImage
        fields = ('image', 'height', 'width')

class AutoCompleteSerializer(serializers.Serializer):
    pk = serializers.Field()
    name = serializers.CharField(required=False, max_length=100)

    def restore_object(self, attrs, instance=None):
        if instance:
            # Update existing instance
            instance.name = attrs.get('name', instance.title)
            instance.distance = attrs.get('distance', instance.title)
            return instance
        # Create new instance
        return AutoCompleteSerializer(**attrs)

class CitySuggestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('name',
                  'description',
                  )
