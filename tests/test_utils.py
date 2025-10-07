from shortly.utils import create_shortcode

def test_shortcode_helper():
    #first 10 digits hsould be the same
    assert create_shortcode(0) == "0"
    assert create_shortcode(9) == "9"
    #digits past 10 should correspend to alpha chars
    assert create_shortcode(10) == "A"
    assert create_shortcode(61) == "z"
    #check that string encoding is wokring corrctly on larger numbers
    assert create_shortcode(62) == "10"
    assert create_shortcode(4567) == "1Bf"
