from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Reviews



########################## Model serializer class #############################
class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Reviews
        exclude = ('watchlist',)
        # fields = "__all__"
      
class WatchListSerializer(serializers.ModelSerializer):

    ## this is for making calculations and to add new field I need define a new method call get_fieldName
    # len_name = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True, read_only=True)# read_only when I send post I can modifie it -- review comes from related name 
    #overwriting platfomr field because is only showing id platform
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = "__all__"
        # fields = ['id', 'name', 'description']
        # exclude = ['active']

#     def get_len_name(self, object): #object has acces to all my elements (is, name, description, active)
#           length = len(object.name)
#           return length
#         ###### Object level validation #########
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and descript can't be same")
#             #{
# #     "non_field_errors": [
# #         "Name and descript can't be same"
# #     ]
# # }
#         else:
#             return data

#     #######field_level_validation#######
#     def validate_name(self, value): #validate_fieldIWhangtoValidate so value parametter here is name
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short!")
#             #{name: ["Name is too short!"]}
#         else:
#             return value

# class StreamPlatformSerializer(serializers.ModelSerializer):
class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer): #HyperlinkModel is for showing link(endpoint) instead of id

    #one streamplatform can have many watchlist
    watchlist = WatchListSerializer(many=True, read_only=True) # watchlist comes from name_related in forein key, this is for showing whatchlist all fields in borwser api
    # watchlist = serializers.StringRelatedField(many=True) # to show all the __str__ that comes from my model in this case "title"
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True) # show only primary key for watchlist
    # watchlist = serializers.HyperlinkedRelatedField(many=True,read_only=True, view_name='movie-detail') # this for pas a link(endpoint) for every movie or tvserie, movie-detail comes from my url name in urls.py need to add context serializer

    class Meta:
        model = StreamPlatform
        fields = "__all__"










########################## serializer class #############################
#funtion to validor parametor in classes (There are 3 kinds of validations)
# def desc_length(value):
#     if len(value) < 3:
#         raise serializers.ValidationError("description is too short")

# # two classes from serializer: 1. serializer and 2. Model
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)# read_only prevents update it or change it
#     name = serializers.CharField()
#     description = serializers.CharField(validators=[desc_length]) #{description: ["description is too short"]}
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data): #instance is my old data
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#     ###### Object level validation #########
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and descript can't be same")
#             #{
# #     "non_field_errors": [
# #         "Name and descript can't be same"
# #     ]
# # }
#         else:
#             return data

#     #######field_level_validation#######
#     def validate_name(self, value): #validate_fieldIWhangtoValidate so value parametter here is name
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short!")
#             #{name: ["Name is too short!"]}
#         else:
#             return value
