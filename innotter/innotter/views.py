from rest_framework.viewsets import ModelViewSet


class SerializersPermissionsBaseViewSet(ModelViewSet):
    queryset = None
    default_serializer_class = None
    serializer_classes_by_action = {}
    permission_classes_by_action = {}

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action.get(self.action, self.permission_classes)]
