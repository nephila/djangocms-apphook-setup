#!/usr/bin/env python

import sys
from tempfile import mkdtemp


def gettext(s):
    return s


HELPER_SETTINGS = dict(
    ROOT_URLCONF="tests.test_utils.urls",
    INSTALLED_APPS=[
        "parler",
        "aldryn_apphooks_config",
        "tests.test_utils",
        "tests.sample_app_1",
        "tests.sample_app_2",
        "tests.sample_app_3",
        "tests.sample_app_4",
        "tests.sample_app_5",
        "tests.sample_app_6",
    ],
    LANGUAGE_CODE="en",
    LANGUAGES=(
        ("en", gettext("English")),
        ("fr", gettext("French")),
        ("it", gettext("Italiano")),
    ),
    CMS_LANGUAGES={
        1: [
            {
                "code": "en",
                "name": gettext("English"),
                "public": True,
            },
            {
                "code": "it",
                "name": gettext("Italiano"),
                "public": True,
            },
            {
                "code": "fr",
                "name": gettext("French"),
                "public": True,
            },
        ],
        2: [
            {
                "code": "en",
                "name": gettext("English"),
                "public": True,
            },
        ],
        "default": {
            "hide_untranslated": False,
        },
    },
    PARLER_LANGUAGES={
        1: (
            {"code": "en"},
            {"code": "it"},
            {"code": "fr"},
        ),
        2: ({"code": "en"},),
        "default": {
            "fallback": "en",
            "hide_untranslated": False,
        },
    },
    PARLER_ENABLE_CACHING=False,
    FILE_UPLOAD_TEMP_DIR=mkdtemp(),
    SITE_ID=1,
)


def run():
    from app_helper import runner

    runner.cms("djangocms_apphook_setup")


def setup():
    from app_helper import runner

    runner.setup("djangocms_apphook_setup", sys.modules[__name__], use_cms=True)


if __name__ == "__main__":
    run()

if __name__ == "cms_helper":
    # this is needed to run cms_helper in pycharm
    setup()
