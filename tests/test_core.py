"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_paylocity.tap import TapPaylocity

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    # TODO: Initialize minimal tap config
    "client_id": "",
    "client_secret": "",
    "company_id": ""
}


# Run standard built-in tap tests from the SDK:
TestTapPaylocity = get_tap_test_class(
    tap_class=TapPaylocity,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
