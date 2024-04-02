from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

from .http import SeleniumRequest


class SeleniumMiddleware:
    """Scrapy middleware handling the requests using selenium"""

    def __init__(
        self,
        driver_executable_path,
        driver_arguments,
    ):

        service = Service(executable_path=driver_executable_path)
        options = webdriver.Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")

        for argument in driver_arguments:
            options.add_argument(argument)

        # locally installed driver
        self.driver = webdriver.ChromiumDriver(service=service, options=options)

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""

        driver_executable_path = crawler.settings.get("SELENIUM_DRIVER_EXECUTABLE_PATH")
        driver_arguments = crawler.settings.get("SELENIUM_DRIVER_ARGUMENTS")

        middleware = cls(
            driver_executable_path=driver_executable_path,
            driver_arguments=driver_arguments,
        )
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""

        if not isinstance(request, SeleniumRequest):
            return None

        self.driver.get(request.url)

        for cookie_name, cookie_value in request.cookies.items():
            self.driver.add_cookie({"name": cookie_name, "value": cookie_value})

        if request.wait_until:
            WebDriverWait(self.driver, request.wait_time).until(request.wait_until)

        if request.screenshot:
            request.meta["screenshot"] = self.driver.get_screenshot_as_png()

        if request.script:
            self.driver.execute_script(request.script)

        body = str.encode(self.driver.page_source)

        # Expose the driver via the "meta" attribute
        request.meta.update({"driver": self.driver})

        return HtmlResponse(
            self.driver.current_url, body=body, encoding="utf-8", request=request
        )

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""
        self.driver.quit()
