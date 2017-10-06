from rest_framework.test import APIClient
from splinter.browser import Browser

def before_all(context):
    context.browser = Browser()
    context.test.client = APIClient()
    pass

def after_all(context):
    context.browser.quit()
    pass


def before_scenario(context, scenario):
    context.fixtures = []
