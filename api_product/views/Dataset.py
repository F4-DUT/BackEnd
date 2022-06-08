from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
import tensorflow as tf


from api_account.permission import ManagerPermission, UserPermission
from api_base.pagination import CustomPagePagination
from api_base.views import BaseViewSet
from api_product.models import Dataset, Category
from api_product.serializers import DatasetSerializer
from api_product.services import DatasetService, CategoryService


class DatasetViewSet(BaseViewSet):
    queryset = Dataset.objects.all()
    permission_classes = [UserPermission]
    pagination_class = CustomPagePagination

    @action(detail=False, methods=['post'])
    def change_model(self, request):
        print(request.FILES.get('new_model'))
        new_model_file = request.FILES.get('new_model')
        if new_model_file:
            new_model = tf.keras.models.load_model(new_model_file.temporary_file_path())
            if new_model:
                new_model.save("api_product/constants/classify_model.h5")
                return Response({"detail": "Completed change file model!!"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error_message": "New model is conflict!!"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error_message": "File model is null!"})

    @action(detail=True, methods=['delete'])
    def delete_dataset(self, request, pk):
        dataset = self.get_object()
        category = dataset.category
        if dataset:
            dataset.delete()
            rs = Dataset.objects.filter(category=category)
            page = self.paginate_queryset(rs)
            if page is not None:
                res = DatasetSerializer(page, many=True)
                return self.get_paginated_response(res.data)
            res = DatasetSerializer(page, many=True)
            return Response({'detail': res.data}, status=status.HTTP_200_OK)
        return Response({"error_message": "dataset is not define!"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def train_mode(self, request, pk):
        try:
            if DatasetService.train_mode():
                return Response({'success': "Model is trained!"}, status=status.HTTP_200_OK)
            return Response({"error_message": "Model is train fail!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error_message": str(e)}, status=status.HTTP_400_BAD_REQUEST)