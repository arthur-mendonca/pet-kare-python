from rest_framework.views import APIView, Request, Response
from pet_kare.pagination import CustomPageNumberPagination
from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework import status


class GroupView(APIView, CustomPageNumberPagination):
    def get(self, request: Request) -> Response:
        groups = Group.objects.all()

        result_page = self.paginate_queryset(groups, request)

        serializer = GroupSerializer(instance=result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = GroupSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data

        if Group.objects.filter(
            scientific_name__iexact=group_data["scientific_name"]
        ).exists():
            return Response(
                status=400, data={"message": "Group with this name already exists"}
            )
        else:
            group = Group.objects.create(**group_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
