"""Tests standard tap features using the built-in SDK tests library."""
from typing import Any

import datetime
import os

from singer_sdk.testing import get_tap_test_class

from tap_paylocity.tap import TapPaylocity

SAMPLE_CONFIG: dict[str, Any] = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "client_id": os.getenv("TAP_PAYLOCITY_CLIENT_ID"),
    "client_secret": os.getenv("TAP_PAYLOCITY_CLIENT_SECRET"),
    "company_id": os.getenv("TAP_PAYLOCITY_COMPANY_ID"),
}


# Run standard built-in tap tests from the SDK:
TestTapPaylocity = get_tap_test_class(
    tap_class=TapPaylocity,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
