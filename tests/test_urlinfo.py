import pytest
import json

def test_get_successful_bad_site(client, app):
	result = client.get("/urlinfo/1/xxvtrrmbuqshu.biz/news/?s=1681")
	actual = result.get_json()
	expected = 1 # malware exist
	assert actual['malware'] == expected

def test_get_successful_good_site(client, app):
	result = client.get("/urlinfo/1/google.com/search?ei=pxnIW7CWJZzB0PEPnKyTuAo&q=whitelist+url&oq=whitelist+url&gs_l=psy-ab.3..0l10.1628.1843.0.1977.3.2.0.1.1.0.126.126.0j1.1.0....0...1c.1.64.psy-ab..1.2.127....0.kwayDVX1rY0")
	actual = result.get_json()
	expected = 0 # malware exist
	assert actual['malware'] == expected

def test_get_404(client, app):
	result = client.get("/urlinfo/1/example.com/")
	actual = result.status_code
	expected = 404
	assert actual == expected