import requests
from urllib.parse import quote

BASE_URL = "http://localhost:8000"  # Adjust if your API is running on a different port or host

def test_root_endpoint():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Twitter Analysis Service"}
    print("Root endpoint test passed.")

def test_user_recommendation_endpoint():
    user_id = "123456"  # Replace with a valid user ID from your dataset
    type = "both"
    phrase = "test phrase"
    hashtag = "example"

    encoded_phrase = quote(phrase)
    
    url = f"{BASE_URL}/q2?user_id={user_id}&type={type}&phrase={encoded_phrase}&hashtag={hashtag}"
    
    response = requests.get(url)
    
    assert response.status_code == 200
    
    lines = response.text.split('\n')
    assert lines[0].startswith("TeamCoolCloud,")
    
    if len(lines) > 1:
        for line in lines[1:]:
            parts = line.split('\t')
            assert len(parts) == 4, f"Expected 4 parts, got {len(parts)}: {line}"
    
    print("User recommendation endpoint test passed.")

def test_invalid_type():
    user_id = "123456"
    type = "invalid"
    phrase = "test"
    hashtag = "example"

    encoded_phrase = quote(phrase)
    
    url = f"{BASE_URL}/q2?user_id={user_id}&type={type}&phrase={encoded_phrase}&hashtag={hashtag}"
    
    response = requests.get(url)
    
    assert response.status_code == 400
    assert "Invalid type parameter" in response.text
    
    print("Invalid type test passed.")

if __name__ == "__main__":
    test_root_endpoint()
    test_user_recommendation_endpoint()
    test_invalid_type()
    print("All tests passed!")