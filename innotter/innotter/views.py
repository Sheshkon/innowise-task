from rest_framework.viewsets import ModelViewSet


class SerializersPermissionsBaseViewSet(ModelViewSet):
    queryset = None
    default_serializer_class = None
    serializer_classes_by_action = {}
    permission_classes_by_action = {}

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
