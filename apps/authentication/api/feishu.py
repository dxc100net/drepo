from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from users.permissions import IsAuthPasswdTimeValid
from users.models import User
from common.utils import get_logger
from common.permissions import IsOrgAdmin
from common.mixins.api import RoleUserMixin, RoleAdminMixin
from authentication import errors

logger = get_logger(__file__)


class FeiShuQRUnBindBase(APIView):
    user: User

    def post(self, request: Request, **kwargs):
        user = self.user

        if not user.feishu_id:
            raise errors.FeiShuNotBound

        user.feishu_id = None
        user.save()
        return Response()


class FeiShuQRUnBindForUserApi(RoleUserMixin, FeiShuQRUnBindBase):
    permission_classes = (IsAuthPasswdTimeValid,)


class FeiShuQRUnBindForAdminApi(RoleAdminMixin, FeiShuQRUnBindBase):
    user_id_url_kwarg = 'user_id'
    permission_classes = (IsOrgAdmin,)


class FeiShuEventSubscriptionCallback(APIView):
    """
    # https://open.feishu.cn/document/ukTMukTMukTM/uUTNz4SN1MjL1UzM
    """
    permission_classes = ()

    def post(self, request: Request, *args, **kwargs):
        return Response(data=request.data)
