from rest_framework.views import APIView, Request, Response
from rest_framework import status
from pet_kare.pagination import CustomPageNumberPagination
from traits.models import Trait
from traits.serializers import TraitSerializer


class TraitView(APIView, CustomPageNumberPagination):
    def get(self, request):
        traits = Trait.objects.all()

        result_page = self.paginate_queryset(traits, request)

        serializer = TraitSerializer(instance=result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = TraitSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        trait_data = serializer.validated_data

        if Trait.objects.filter(trait_name__iexact=trait_data["name"]).exists():
            return Response(
                {"message": "Trait already exists"}, status=status.HTTP_409_CONFLICT
            )
        else:
            trait = Trait.objects.create(**trait_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
