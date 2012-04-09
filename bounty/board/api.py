from tastypie.resources import ModelResource
import bounty.board.models as models
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import Authentication, ApiKeyAuthentication

class HackResource(ModelResource):
    class Meta:
        queryset = models.Hack.objects.all()
        resource_name = 'Hack'
        # authentication = ApiKeyAuthentication()
        # authorization = DjangoAuthorization()
        authentication = Authentication()
        authorization = Authorization()