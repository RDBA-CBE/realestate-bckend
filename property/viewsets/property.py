from rest_framework import viewsets
from common.viewset import BaseViewSet
from common.paginator import Pagination
from django.db.models import Max, Min
from rest_framework.response import Response
from rest_framework import status
from ..models import Property
from ..filters.property import PropertyFilter
from ..serializers.property import (
    PropertyListSerializer, 
    PropertyDetailSerializer,
    PropertyCreateSerializer,
    PropertyUpdateSerializer
)

class PropertyViewSet(BaseViewSet):
    queryset = Property.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = PropertyFilter
    pagination_class = Pagination
    order_by = ['-id']  

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # Only show approved properties to non-admin users
    #     if not self.request.user.groups.filter(name='Admin').exists():
    #         queryset = queryset.filter(is_approved=True)
    #     return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PropertyListSerializer
        elif self.action == "retrieve":
            return PropertyDetailSerializer
        elif self.action == "create":
            return PropertyCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return PropertyUpdateSerializer
        return PropertyDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Apply pagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page or queryset, many=True)

        # Get min & max price from full filtered queryset
        price_stats = queryset.aggregate(
            min_price=Min("minimum_price"),
            max_price=Max("maximum_price")
        )

        # If paginated, wrap response in pagination format
        if page is not None:
            response = self.get_paginated_response(serializer.data)
            response.data["min_price"] = price_stats["min_price"]
            response.data["max_price"] = price_stats["max_price"]
            return response

        # Otherwise, return simple response
        return Response({
            "min_price": price_stats["min_price"],
            "max_price": price_stats["max_price"],
            "results": serializer.data
        }, status=status.HTTP_200_OK)
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        # Check if the user has already made an inquiry for this property
        has_inquired = False
        if user.is_authenticated:
            from ..models import Lead
            has_inquired = Lead.objects.filter(interested_property=instance, created_by=user).exists()

        # Get the original response data
        response = super().retrieve(request, *args, **kwargs)
        response.data['has_inquired'] = has_inquired

        return response
