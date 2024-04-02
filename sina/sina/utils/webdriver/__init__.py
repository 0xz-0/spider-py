# ref: https://github.com/clemfromspace/scrapy-selenium/blob/develop/scrapy_selenium
import os

from ...settings import SELENIUM_DRIVER_EXECUTABLE_PATH
from .http import SeleniumRequest
from .middlewares import SeleniumMiddleware


driver_executable_path = os.path.join(
    os.path.dirname(__file__), SELENIUM_DRIVER_EXECUTABLE_PATH
)
_ = SeleniumRequest
_ = SeleniumMiddleware
