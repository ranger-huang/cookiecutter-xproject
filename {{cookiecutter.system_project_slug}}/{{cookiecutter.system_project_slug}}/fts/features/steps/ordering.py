import os
import json
from unittest import skip, SkipTest, mock
import time
from datetime import timedelta

from behave import *
from behave import register_type
from datetime import datetime
import parse

from django.utils.timezone import get_default_timezone, get_current_timezone
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import resolve
from rest_framework import status

from xlock_conf import constants
from xlock_xpay.xpay_bike.models import BikeModel
from xlock_xpay.xpay_order.models import RentProduct, WXOrder
from xlock_xpay.utils.views import oauth_authorized, get_oauth_userinfo
import logging
logger = logging.getLogger(__name__)

use_step_matcher("re")


@step('我已经注册和登陆了')
@given('我已经注册和登陆了')
def step_impl(context):
    weixin_access_token_res = os.environ.get('FETCH_ACCESS_TOKEN_DATA', None)
    if not weixin_access_token_res:
        raise SkipTest('请提供微信客户端获取到的AccessToken数据')
    res = json.loads(weixin_access_token_res)

    UserModel = get_user_model()
    user = UserModel.objects.get(username="consumer")
    backend = "xlock_xpay.xpay_account.auth_backends.PhoneSmsBackend"
    context.test.client.force_login(user, backend=backend)

    # force oauth authorized user openid
    request = RequestFactory().get('/')
    request.session = context.test.client.session
    oauth_authorized(request, dict(openid=res['openid']))
    request.session.save()

    user.username = "wx_{}".format(res['openid'])
    user.save()
    context.user = user


PRODUCT_TYPE_MAP = {
    "景区": {
        "价格类型": "market",
        "市场价": "market",
        "计费单位": "hours",
        "小时": "hours",
        "1 hours": timedelta(hours=1)
    },
    "酒店": {
        "价格类型": "group",
        "团队价": "group",
        "计费单位": "guys",
        "人次": "guys",
        "4 hours": timedelta(hours=4)
    },
}


@step('有"(?P<product_label>.+)"的产品计费如下')
@given('有"(?P<product_label>.+)"的产品计费如下')
def step_impl(context, product_label):
    vendor_name, bike_label = product_label.split(":")

    bike = BikeModel.objects.create(seq=1, status=BikeModel.STATUS.active,
                                    label=bike_label)
    product = RentProduct(bike_model=bike,
                          label="{}:{}".format(vendor_name, bike.label),
                          seq=1,
                          guiding_price=0,
                          status=RentProduct.STATUS.active,
                          )

    for row in context.table:
        if row["出租地点"] in PRODUCT_TYPE_MAP:
            tmap = PRODUCT_TYPE_MAP[row["出租地点"]]
            setattr(product,
                    "{}_price".format(tmap[row['价格类型']]),
                    float(row['单价元'])
            )
    product.save()
    context.product = product


@step('我以"(?P<tour_type>.*)"方式游览园区')
@given('我以"(?P<tour_type>.*)"方式游览园区')
def step_impl(context, tour_type):
    context.tour_type = tour_type
    context.test.assertIn(tour_type, PRODUCT_TYPE_MAP)


from xlock_xpay.views.order import OrderingView, OrderingRequestSerializer


@step('我租用"(?P<product_label>[^"]+)",租用(?P<step>\d+)小时')
@step('我租用"(?P<product_label>[^"]+)",租用(?P<step>\d+)量')
def step_impl(context, product_label: str, step: int):
    """
    :type context: behave.runner.Context
    :param product_label:
    :param step:
    """
    if not os.path.exists(constants.XPAY_WEIXIN_MCH_CERT) or \
            not os.path.exists(constants.XPAY_WEIXIN_MCH_KEY):
        raise SkipTest('Ensure mch_cert and mch_key file is present. paths: {}, {}'
                       .format(constants.XPAY_WEIXIN_MCH_CERT,
                               constants.XPAY_WEIXIN_MCH_KEY))

    userinfo = get_oauth_userinfo(context.test.client)
    assert userinfo
    logger.info(userinfo)

    product = context.product
    context.test.assertEqual(product.label, product_label)

    request_path = '/xpay/ordering/'
    resolver = resolve(request_path)
    context.test.assertIs(resolver.func.view_class, OrderingView)

    ctype = PRODUCT_TYPE_MAP[context.tour_type]["价格类型"]

    dt = datetime.fromtimestamp(time.time(), tz=get_default_timezone())
    dt = datetime.combine(dt, context.NOW.time())
    with mock.patch.object(WXOrder,
                           "datetimer", return_value=dt) as mock_method:
        response = context.test.client.post(request_path, data=dict(
            productseq=product.seq,
            ctype=ctype,
            step=int(step)
        ))
        context.test.assertEqual(response.status_code, status.HTTP_200_OK)

    order_trade_no = response.data['data']['order']['trade_no']
    wxorder = WXOrder.objects.get(out_trade_no=order_trade_no)

    context.test.assertEqual(wxorder.product_id, product.id)
    wxorder.expired_at = wxorder.expired_at.astimezone(get_current_timezone())
    context.order = wxorder


@step('这个订单合计金额是(?P<amount_price>\d+)')
@then('这个订单合计金额是(?P<amount_price>\d+)')
def step_impl(context, amount_price):
    context.test.assertEqual(
        float(context.order.amount_price),
        float(amount_price)
    )

@parse.with_pattern(r"((1|0?)[0-9]|2[0-3]):([0-5][0-9])")
def parse_time(text):
    return datetime.strptime(text, "%H:%M")

register_type(Time=parse_time)


use_step_matcher("cfparse")


@step("这个订单租用至{expired_at:Time}结束")
@then('这个订单租用至{expired_at:Time}结束')
def step_impl(context, expired_at: datetime):
    """
    :type context: behave.runner.Context
    """
    context.test.assertEqual(
        expired_at.time(),
        context.order.expired_at.time()
    )


@step("现在时间是{now:Time}")
@given("现在时间是{now:Time}")
def step_impl(context, now: datetime):
    """
    :type context: behave.runner.Context
    """
    context.NOW = now


@step("从租车入口成功登陆尚骑注册系统")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass