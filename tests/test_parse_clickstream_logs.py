from unittest.mock import mock_open, patch

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

import parse_clickstream_logs

EXAMPLE = "https://dis.fun.com/wiki/Madam_Mim|" \
          "en-us|" \
          "<134>2021-02-09T23:59:53Z|" \
          "2f2fedc8dfc17d81|" \
          "/__track/special/tracking?a=6081&n=5b2&rollout=21c6a&action=45aef&" \
          "category=46ee&label=8ad49&ga_value=6e0cd&is_Interactive=ced1&" \
          "unique_id=b58e0&c=374&x=4d2e7&lc=28a19&u=0b1b0"


class TestParseClickstreamLogs:

    @patch('parse_clickstream_logs.open', new_callable=mock_open, read_data=EXAMPLE)
    def test_read_input_file(self, mock_file):
        input_path = 'test_path'
        result = parse_clickstream_logs.read_input_file(input_path)
        expected = pd.DataFrame({"url_orig": [EXAMPLE]})
        assert assert_frame_equal(result, expected, check_like=True) is None
        mock_file.assert_called_with(input_path, 'r')

    def test_parse_input_data(self):
        df_test = pd.DataFrame({"url_orig": [EXAMPLE]})
        df_result = parse_clickstream_logs.parse_input_data(df_test)
        df_expected = pd.DataFrame({
            "timestamp": [pd.Timestamp("2021-02-09T23:59:53Z")],
            "user_id": ["2f2fedc8dfc17d81"],
            "article_id": ["6081"],
            "wiki_id": ["374"]
        })
        assert assert_frame_equal(df_expected, df_result, check_like=True) is None

    @pytest.mark.parametrize(
        "test_data, expected",
        [
            (
                    {"user_id": "name", "wiki_id_last": 1, "wiki_id_first": 1, "article_id_last": 2,
                     "article_id_first": 2},
                    {"user_id": "name", "is_same_wiki": True, "is_same_article": True}
            ),
            (
                    {"user_id": "name", "wiki_id_last": 1, "wiki_id_first": 1, "article_id_last": 2,
                     "article_id_first": 100},
                    {"user_id": "name", "is_same_wiki": True, "is_same_article": False}
            ),
            (
                    {"user_id": "name", "wiki_id_last": 1, "wiki_id_first": 100, "article_id_last": 2,
                     "article_id_first": 2},
                    {"user_id": "name", "is_same_wiki": False, "is_same_article": False, }
            ),
            (
                    {"user_id": "name", "wiki_id_last": 1, "wiki_id_first": 100, "article_id_last": 2,
                     "article_id_first": 100},
                    {"user_id": "name", "is_same_wiki": False, "is_same_article": False}
            )
        ]
    )
    def test_is_same_wiki_and_article(self, test_data, expected):
        assert parse_clickstream_logs.is_same_wiki_and_article(test_data) == expected

    def test_process_data(self):
        df_test = pd.DataFrame({
            "timestamp": [
                pd.Timestamp("2021-02-09T23:59:53Z"),
                pd.Timestamp("2021-02-09T23:00:53Z"),
                pd.Timestamp("2021-02-09T23:59:53Z"),
                pd.Timestamp("2021-02-09T23:30:53Z"),
            ],
            "user_id": [
                "2f2fedc8dfc17d8x",
                "2f2fedc8dfc17d81",
                "2f2fedc8dfc17d81",
                "2f2fedc8dfc17d81",
            ],
            "article_id": ["6081", "6081", "1", "6081"],
            "wiki_id": ["374", "374", "374", "374"]
        })
        expected = pd.DataFrame({
            "user_id": ["2f2fedc8dfc17d81"],
            "is_same_article": [False],
            "is_same_wiki": [True],
        })
        assert assert_frame_equal(parse_clickstream_logs.process_data(df_test), expected, check_like=True) is None
