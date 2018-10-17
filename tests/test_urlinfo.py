import pytest
import json

def test_get_successful(client, app):
	result = client.get("/urlinfo/1/xxvtrrmbuqshu.biz/news/?s=1681")
	actual = result.get_json()
	expected = 1 # malware exist
	assert actual['malware'] == expected

def test_get_404(client, app):
	result = client.get("/urlinfo/1/example.com/")
	actual = result.status_code
	expected = 404
	assert actual == expected