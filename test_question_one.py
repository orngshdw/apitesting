"""
This file contains tests to answer question 1:

Given the API POST request and payload below come up with Python solutions
(or write a plan on how you would automate the task) to:

1) Validate all questions have four non null options.
2) Validate
["New York Bulls", "Los Angeles Kings", "Golden State Warriors", "Houston Rocket"]
are the options for sports q1.
"""
from .helpers import get_key_values, request_get_content

API_ENDPOINT = "https://validate.test.com/api/quiz-questions"
PAYLOAD = {
    "quizSubject": ["sports", "math"],
    "semester": "2"
}
EXPECTED_OPTIONS = ["New York Bulls", "Los Angeles Kings",
                    "Golden State Warriors", "Houston Rocket"]


def test_options_not_null():
    """
    1) Validate all questions have four non null options
    """
    # ----- Setup ----- #
    # get response and convert to dict format
    resp_dict = request_get_content(API_ENDPOINT, PAYLOAD)

    # ----- Validate all options are not null and have 4 options ----- #
    all_options = get_key_values(resp_dict, "options")
    for location, value in all_options.items():
        # not null
        assert value, "{} doesn't contain options".format(location)
        count = len(value)
        # correct length
        assert 4 == count, \
            "Expected 4 options, but got {}:\n" \
            "`{}: {}`".format(count, location, value)


def test_expected_sports_options():
    """
    2) Validate
    ["New York Bulls", "Los Angeles Kings", "Golden State Warriors", "Houston Rocket"]
    are the options for sports q1
    This test checks all the
    """
    # ----- Setup ----- #
    # get response and convert to dict format
    response = request_get_content(API_ENDPOINT, PAYLOAD)

    # get values for "sports"
    sports_content = get_key_values(response, "sports")
    # get all "q1" found in "sports"
    questions = {}
    for path, content in sports_content.items():
        # json will not contain same keys at the same location,
        # so .update() is safe
        questions.update(get_key_values(content, "q1", root=path))


    # ----- Validate all q1["options"] contain expected values ----- #
    for path, content in questions.items():
        # Skip q1 if there are no "options"
        if not content.get("options", None):
            continue

        # validate option values are expected
        if set(content["options"]) ^ set(EXPECTED_OPTIONS):
            extra_options = set(content["options"]) - set(EXPECTED_OPTIONS)
            if extra_options:
                raise Exception(
                    "Unexpected options {} found at {}, got\n"
                    "`{}`\nexpected\n`{}`".format(
                        extra_options, path,
                        set(content["options"]), set(EXPECTED_OPTIONS)))

            missing_options = set(EXPECTED_OPTIONS) - set(content["options"])
            if missing_options:
                raise Exception(
                    "Missing options {} at {}, got\n"
                    "`{}`\nexpected\n`{}`".format(
                        missing_options, path,
                        set(content["options"]), set(EXPECTED_OPTIONS)))

        # validate order of "options" is expected
        assert content["options"] == EXPECTED_OPTIONS,\
            "{} is not the same order as expected:\n`{}`\nvs\n`{}`".format(
                path, content["options"], EXPECTED_OPTIONS)
