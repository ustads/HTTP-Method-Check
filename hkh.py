import requests
#pakhaji

def test_http_methods(url):
    methods = {
        "GET": requests.get,
        "POST": requests.post,
        "PUT": requests.put,
        "DELETE": requests.delete,
        "PATCH": requests.patch,
        "OPTIONS": requests.options,
        "HEAD": requests.head
    }

    for method_name, method_func in methods.items():
        try:
            print(f"\nTesting {method_name} method to {url}")
            response = method_func(url)
            print(f"Status Code: {response.status_code}")
            print(f"Allowed? {'Yes' if response.status_code < 400 else 'No'}")
            if method_name != "HEAD":
                print(f"Response Body:\n{response.text[:200]}...")  # Preview first 200 chars
        except Exception as e:
            print(f"Error during {method_name}: {e}")

if __name__ == "__main__":
    target_url = input("Enter target URL (e.g., https://example.com/api): ")
    test_http_methods(target_url)
