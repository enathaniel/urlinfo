import pytest
import json

def test_get_successful(client, app):
	result = client.get("/urlinfo/1/www.google.com:8080/index.html%3Fname%3Dedwin")
	actual = result.get_json()
	expected = 1 # malware exist
	assert actual['malware'] == expected

def test_get_404(client, app):
	result = client.get("/urlinfo/1/example.com/")
	actual = result.status_code
	expected = 404
	assert actual == expected