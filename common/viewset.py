from rest_framework import viewsets

class BaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def perform_create(self, serializer):
        if hasattr(serializer.Meta.model, "created_by"):
            # Only set created_by if user is authenticated
            if self.request.user.is_authenticated:
                serializer.save(
                    created_by=self.request.user,
                    updated_by=self.request.user
                )
            else:
                # For anonymous users, don't set created_by/updated_by
                serializer.save()
        else:
            serializer.save()

    def perform_update(self, serializer):
        if hasattr(serializer.Meta.model, "updated_by"):
            # Only set updated_by if user is authenticated
            if self.request.user.is_authenticated:
                serializer.save(updated_by=self.request.user)
            else:
                serializer.save()
        else:
            serializer.save()