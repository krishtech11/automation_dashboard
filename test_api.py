import requests
import json
import os

# Test configuration
BASE_URL = "http://localhost:8000/api"
TEST_FILE_PATH = "test_document.txt"

def print_success(message):
    print(f"✅ {message}")

def print_failure(message, response=None):
    print(f"❌ {message}")
    if response is not None:
        print(f"Status code: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except:
            print(f"Response: {response.text}")

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print_success("Root endpoint is working")
            return True
        else:
            print_failure("Root endpoint returned non-200 status code", response)
            return False
    except Exception as e:
        print_failure(f"Error testing root endpoint: {str(e)}")
        return False

def test_web_automation():
    """Test the web automation endpoint"""
    try:
        data = {
            "url": "https://www.google.com",
            "search_query": "test automation"
        }
        response = requests.post(f"{BASE_URL}/web-automate", json=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                print_success("Web automation test passed")
                return True
            else:
                print_failure("Web automation returned error", response)
                return False
        else:
            print_failure("Web automation request failed", response)
            return False
    except Exception as e:
        print_failure(f"Error testing web automation: {str(e)}")
        return False

def test_desktop_automation():
    """Test the desktop automation endpoint"""
    try:
        # Test opening Notepad
        data = {
            "app_name": "notepad",
            "action": "open"
        }
        response = requests.post(f"{BASE_URL}/desktop-automate", json=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                print_success("Desktop automation test passed (opening app)")
                return True
            else:
                print_failure("Desktop automation returned error", response)
                return False
        else:
            print_failure("Desktop automation request failed", response)
            return False
    except Exception as e:
        print_failure(f"Error testing desktop automation: {str(e)}")
        return False

def test_document_automation():
    """Test the document automation endpoint"""
    try:
        # Create a test file
        with open("test_document.txt", "w") as f:
            f.write("This is a test document for OCR testing.")
        
        # Test document text extraction
        with open("test_document.txt", "rb") as f:
            files = {"file": ("test_document.txt", f, "text/plain")}
            response = requests.post(f"{BASE_URL}/document/extract-text", files=files)
        
        # Clean up test file
        if os.path.exists("test_document.txt"):
            os.remove("test_document.txt")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                print_success("Document automation test passed")
                return True
            else:
                print_failure("Document automation returned error", response)
                return False
        else:
            print_failure("Document automation request failed", response)
            return False
    except Exception as e:
        print_failure(f"Error testing document automation: {str(e)}")
        return False

def run_tests():
    """Run all tests and print a summary"""
    print("🚀 Starting API tests...\n")
    
    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Web Automation", test_web_automation),
        ("Desktop Automation", test_desktop_automation),
        ("Document Automation", test_document_automation)
    ]
    
    results = []
    
    for name, test_func in tests:
        print(f"\n🔍 Testing {name}...")
        result = test_func()
        results.append((name, result))
    
    # Print summary
    print("\n📊 Test Summary:" + "="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{name}: {'✅' if result else '❌'} {status}")
    
    print("\n" + "="*60)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    print("="*60 + "\n")
    
    return all(result for _, result in results)

if __name__ == "__main__":
    run_tests()
