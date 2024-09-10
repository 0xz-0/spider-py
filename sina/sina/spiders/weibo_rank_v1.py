from enum import Enum
import scrapy
from typing import List
from scrapy.http import Response
import logging
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json

from ..utils.database import DBRequestTask
from ..utils.webdriver import driver_executable_path, SeleniumRequest
from ..items import (
    HotSearchRealTimeItem,
    HotSearchHotGovItem,
    EntertainmentItem,
    NewsItem,
)