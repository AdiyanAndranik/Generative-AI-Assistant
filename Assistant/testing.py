from fastapi.testclient import TestClient
from app import app


client = TestClient(app)

def test_add_vc(url):
    data = {
        "url": url
    }
    response = client.post("/add_vc/", json=data)
    print(f"add_vc response for {url}:", response.json())

def test_extract_info():
    url = "http://www.benchmark.com/"
    response = client.get(f"/extract_info/?url={url}")
    print("extract_info response:", response.json())

def test_find_similar():
    url = "http://www.benchmark.com/"
    response = client.get(f"/find_similar/?url={url}")
    print("find_similar response:", response.json())

test_add_vc("http://www.benchmark.com/")
test_add_vc("http://www.accel.com/")
test_add_vc("http://www.sequoiacap.com/")

test_extract_info()

test_find_similar()