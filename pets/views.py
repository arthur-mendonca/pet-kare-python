from rest_framework.views import APIView, status, Request
from rest_framework.response import Response
from pet_kare.pagination import CustomPageNumberPagination
from pets.serializers import PetsSerializer
from groups.serializers import GroupSerializer
from django.shortcuts import get_object_or_404

from .models import Pet
from traits.models import Trait
from groups.models import Group
from django.db.models import Q


class PetsView(APIView, CustomPageNumberPagination):
    def get(self, request):
        pets = Pet.objects.all()
        trait_name = request.query_params.get("trait")

        if trait_name is not None:
            pets = pets.filter(traits__name__iexact=trait_name)

            result_page = self.paginate_queryset(pets, request, view=self)
            serializer = PetsSerializer(result_page, many=True)

            return self.get_paginated_response(serializer.data)

        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetsSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        traits = serializer.validated_data.pop("traits")
        group_data = serializer.validated_data.pop("group")
        group, created = Group.objects.get_or_create(
            scientific_name__iexact=group_data["scientific_name"], defaults=group_data
        )
        pet = Pet.objects.create(group=group, **serializer.validated_data)

        for trait in traits:
            trait_obj, created = Trait.objects.get_or_create(
                name__iexact=trait["name"], defaults=trait
            )
            pet.traits.add(trait_obj)

        serializer = PetsSerializer(instance=pet)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PetsDetailsView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, pk=pet_id)

        serializer = PetsSerializer(instance=pet)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, pk=pet_id)
        serializer = PetsSerializer(instance=pet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        traits_data = serializer.validated_data.get("traits")
        group_data = serializer.validated_data.pop("group", None)

        for key, value in serializer.validated_data.items():
            if key != "traits" and key != "group":
                setattr(pet, key, value)

        if group_data is not None:
            try:
                group = Group.objects.get(
                    scientific_name__iexact=group_data["scientific_name"]
                )
            except Group.DoesNotExist:
                group = Group.objects.create(**group_data)
            pet.group = group

        if traits_data is not None:
            pet.traits.clear()
            for trait_data in traits_data:
                trait_name = trait_data.get("name")
                trait, _ = Trait.objects.get_or_create(name__iexact=trait_name)
                pet.traits.add(trait)

        pet.save()
        serializer = PetsSerializer(instance=pet)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, pk=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
