import pytest
from unittest.mock import patch, Mock
from src.extractors.novels_com_extractor import novels_com_extractor
from src.models.classes import Chapter, Novel
from requests.exceptions import RequestException

@pytest.fixture
def extractor():
    return novels_com_extractor()

@pytest.fixture
def mock_html():
    with open('src/test/test_samples/novels_com.html', 'r') as f:
        return f.read()

@patch('requests.get')
def test_extract_chapters_success(
    mock_get, 
    extractor: novels_com_extractor, 
    mock_html: str
):
    # Mock the response for the initial request
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = mock_html
    mock_get.return_value = mock_response

    novel = Novel(
        name='夫人有新歡了，霍總全球追妻', 
        id='nod288593604df337cb749726f76484b107a165581c286f9aba5a132fd64391b5a/',
        url='https://www.novels.com.tw/novels/nod288593604df337cb749726f76484b107a165581c286f9aba5a132fd64391b5a/',
        website='www.novels.com.tw',
        lastest_chapter=922,
    )

    # print(mock_html)
    chapters = extractor.extract_chapters(novel)

    assert chapters is not None and len(chapters) > 0
    assert chapters[-1].number == 922
    assert str(chapters[0]) == "第1章 夫人有新歡了，霍總全球追妻 /novels/nod288593604df337cb749726f76484b107a165581c286f9aba5a132fd64391b5a/30215025.html"
    assert str(chapters[-1]) == "第922章 夫人有新歡了，霍總全球追妻 /novels/nod288593604df337cb749726f76484b107a165581c286f9aba5a132fd64391b5a/58850169.html"

def test_wrong_novel_website(extractor: novels_com_extractor):
    novel = Novel(
        name='Test Novel',
        id='5502',
        url='https://xyi6.com/Book/Indexd3/bookshow/bookId/5502.html',
        website='www.google.com',
        lastest_chapter=830,
    )

    chapters = extractor.extract_chapters(novel)

    assert chapters == []

@patch('requests.post')
def test_extract_chapters_network_error(mock_post, extractor: novels_com_extractor):
    # Mock the post request to raise a RequestException
    mock_post.side_effect = RequestException("Network error")

    # Create a sample Novel instance
    novel = Novel(
        name='Test Novel',
        id='5502',
        url='https://xyi6.com/Book/Indexd3/bookshow/bookId/5502.html',
        website='www.novels.com.tw',
        lastest_chapter=900,
    )

    # Call the method under test
    chapters = extractor.extract_chapters(novel)

    # Assert that the result is an empty list as expected
    assert chapters == []

def test_wrong_novel_type(extractor: novels_com_extractor):
    novel = 'Test Novel'

    chapters = extractor.extract_chapters(novel)

    assert chapters == []