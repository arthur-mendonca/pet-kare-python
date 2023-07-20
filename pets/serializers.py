from rest_framework import serializers

from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from pets.models import SexChoices


class PetsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexChoices.choices, default=SexChoices.NOT_INFORMED
    )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
