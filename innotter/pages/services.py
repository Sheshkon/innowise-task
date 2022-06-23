from datetime import datetime, timedelta
from innotter.settings import BLOCK_DAYS

from .models import Page


def block_page(page: Page, is_to_permanent=False):
    if is_to_permanent:
        page.is_permanent_blocked = True
    else:
        page.unblock_date = datetime.now() + timedelta(days=BLOCK_DAYS)

    page.save()

    return page
