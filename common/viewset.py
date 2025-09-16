from rest_framework import viewsets

class BaseViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        if hasattr(serializer.Meta.model, "created_by"):
            serializer.save(
                created_by=self.request.user,
                updated_by=self.request.user
            )
        else:
            serializer.save()

    def perform_update(self, serializer):
        if hasattr(serializer.Meta.model, "updated_by"):
            serializer.save(updated_by=self.request.user)
        else:
            serializer.save()