from unittest import TestCase
from unittest.mock import mock_open, patch

import pandas as pd
from pandas.testing import assert_frame_equal

import parse_clickstream_logs

EXAMPLE = "https://dis.fun.com/wiki/Madam_Mim|" \
          "en-us|" \
          "<134>2021-02-09T23:59:53Z|" \
          "2f2fee88f2e665659dbe7dc8dfc17d81|" \
          "/__track/special/tracking?a=6081&n=5b2&rollout=21c6a&action=45aef&" \
          "category=46ee&label=8ad49&ga_value=6e0cd&is_Interactive=ced1&" \
          "unique_id=b58e0&c=374&x=4d2e7&lc=28a19&u=0b1b0"


class TestParseClickstreamLogs(TestCase):

    @patch('parse_clickstream_logs.open', mock_open(read_data=EXAMPLE))
    def test_read_input_file(self):
        input_path = 'test_path'
        result = parse_clickstream_logs.read_input_file(input_path)
        expected = pd.DataFrame({"url_orig": [EXAMPLE]})
        self.assertEqual(assert_frame_equal(result, expected), None)

    def test_parse_input_data(self):
        test_df = pd.DataFrame({"url_orig": [EXAMPLE]})
        df_result = parse_clickstream_logs.parse_input_data(test_df)
        df_expected = pd.DataFrame({
            "url_orig": [EXAMPLE],
            "url": ["https://dis.fun.com/wiki/Madam_Mim"],
            "lang": ["en-us"],
            "timestamp": [pd.Timestamp("2021-02-09T23:59:53Z")],
            "user_id": ["2f2fee88f2e665659dbe7dc8dfc17d81"],
            "article_id": ["6081"],
            "wiki_id": ["374"]
        })
        self.assertEqual(assert_frame_equal(df_expected, df_result), None)
