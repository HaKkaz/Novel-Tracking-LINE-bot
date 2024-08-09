import pytest
from unittest.mock import patch, Mock
from src.extractors.xyi6_com_extractor import xyi6_com_extractor
from src.models.classes import Chapter, Novel
from requests.exceptions import RequestException

@pytest.fixture
def extractor():
    return xyi6_com_extractor()

@pytest.fixture
def mock_html_1():
    with open('src/test/test_samples/xyi6_com_1.html', 'r') as f:
        return f.read()

@pytest.fixture
def mock_html_2():
    with open('src/test/test_samples/xyi6_com_2.html', 'r') as f:
        return f.read()

@patch('requests.post')
def test_extract_chapters_success(
    mock_post, 
    extractor: xyi6_com_extractor, 
    mock_html_1: str, 
    mock_html_2: str
):
    # Mock the response for the initial request
    mock_response_1 = Mock()
    mock_response_1.status_code = 200
    mock_response_1.text = mock_html_1
    mock_response_2 = Mock()
    mock_response_2.status_code = 200
    mock_response_2.text = mock_html_2
    mock_post.side_effect = [mock_response_1, mock_response_2]

    novel = Novel(
        name='Test Novel',
        id='5502',
        url='https://xyi6.com/Book/Indexd3/bookshow/bookId/5502.html',
        website='xyi6.com',
        lastest_chapter=830,
    )

    chapters = extractor.extract_chapters(novel)

    assert chapters[0] == Chapter('/bkshow/0/5502/801/1/0/mb/1', '教訓王錚', 801)
    assert chapters[-1] == Chapter('/bkshow/0/5502/900/1/0/mb/1', '確定不知',900)
    assert len(chapters) == 100
    assert str(chapters[0]) == "第801章 教訓王錚 /bkshow/0/5502/801/1/0/mb/1"

@patch('requests.post')
def test_request_failure(mock_post, extractor: xyi6_com_extractor):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_post.return_value = mock_response

    novel = Novel(
        name='Test Novel',
        id='5502',
        url='https://xyi6.com/Book/Indexd3/bookshow/bookId/5502.html',
        website='xyi6.com',
        lastest_chapter=830,
    )

    chapters = extractor.extract_chapters(novel)

    assert chapters == []

def test_wrong_novel_website(extractor: xyi6_com_extractor):
    novel = Novel(
        name='Test Novel',
        id='5502',
        url='https://xyi6.com/Book/Indexd3/bookshow/bookId/5502.html',
        website='www.novels.com.tw',
        lastest_chapter=830,
    )

    chapters = extractor.extract_chapters(novel)

    assert chapters == []

def test_wrong_novel_type(extractor: xyi6_com_extractor):
    novel = 'Test Novel'

    chapters = extractor.extract_chapters(novel)

    assert chapters == []

@patch('requests.post')
def test_no_option_html(mock_test, extractor: xyi6_com_extractor):
    no_option_html = """
    <!DOCTYPE html><html lang="zh">
        <head>
            AAA BBB CCC
        </head>
    </html>
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = no_option_html
    mock_test.return_value = mock_response
    
    novel = Novel(
        name='Test Novel',
        id='5502',
        url='https://xyi6.com/Book/Indexd3/bookshow/bookId/5502.html',
        website='xyi6.com',
        lastest_chapter=830,
    )

    chapters = extractor.extract_chapters(novel)

    assert chapters == []

@patch('requests.post')
def test_extract_chapters_network_error(mock_post, extractor: xyi6_com_extractor):
    # Mock the post request to raise a RequestException
    mock_post.side_effect = RequestException("Network error")

    # Create a sample Novel instance
    novel = Novel(
        name='Test Novel',
        id='5502',
        url='https://xyi6.com/Book/Indexd3/bookshow/bookId/5502.html',
        website='xyi6.com',
        lastest_chapter=830,
    )

    # Call the method under test
    chapters = extractor.extract_chapters(novel)

    # Assert that the result is an empty list as expected
    assert chapters == []