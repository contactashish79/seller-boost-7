import requests
import sys
import json
import base64
import time
from datetime import datetime

class AmazonContentGeneratorTester:
    def __init__(self, base_url="https://seller-boost-7.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.test_project_id = None
        self.tests_run = 0
        self.tests_passed = 0
        
        # Test image (small 1x1 PNG in base64)
        self.test_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        self.test_image = f"data:image/png;base64,{self.test_image_b64}"

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                if files:
                    # For file uploads, don't set Content-Type header
                    headers = {k: v for k, v in headers.items() if k != 'Content-Type'}
                    response = requests.post(url, headers=headers, files=files)
                else:
                    response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return True, response.json()
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Error details: {error_detail}")
                except:
                    print(f"   Response text: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        success, response = self.run_test("Root Endpoint", "GET", "/", 200)
        return success

    def test_signup(self):
        """Test user signup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        test_email = f"test_{timestamp}@example.com"
        test_password = "TestPass123!"
        
        success, response = self.run_test(
            "User Signup",
            "POST",
            "/auth/signup",
            200,
            data={"email": test_email, "password": test_password}
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            if 'user' in response and 'id' in response['user']:
                self.user_id = response['user']['id']
            print(f"   ✅ Token acquired: {self.token[:20]}...")
            return True
        return False

    def test_login(self):
        """Test user login (create user first if no token)"""
        if not self.token:
            # Create a user first
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            test_email = f"login_test_{timestamp}@example.com"
            test_password = "TestPass123!"
            
            # Signup first
            success, response = self.run_test(
                "Signup for Login Test",
                "POST",
                "/auth/signup", 
                200,
                data={"email": test_email, "password": test_password}
            )
            
            if not success:
                return False
                
            # Now test login
            success, response = self.run_test(
                "User Login",
                "POST",
                "/auth/login",
                200,
                data={"email": test_email, "password": test_password}
            )
            
            if success and 'access_token' in response:
                self.token = response['access_token']
                if 'user' in response and 'id' in response['user']:
                    self.user_id = response['user']['id']
                print(f"   ✅ Login token acquired: {self.token[:20]}...")
                return True
        return True  # Already have token

    def test_create_project(self):
        """Test project creation"""
        if not self.token:
            print("❌ No token available for project creation")
            return False
            
        success, response = self.run_test(
            "Create Project",
            "POST",
            "/projects",
            200,
            data={"name": "Test A+ Content Project"}
        )
        
        if success and 'id' in response:
            self.test_project_id = response['id']
            print(f"   ✅ Project created with ID: {self.test_project_id}")
            return True
        return False

    def test_get_projects(self):
        """Test getting user projects"""
        success, response = self.run_test("Get Projects", "GET", "/projects", 200)
        if success:
            print(f"   ✅ Found {len(response)} projects")
        return success

    def test_get_project(self):
        """Test getting specific project"""
        if not self.test_project_id:
            print("❌ No test project ID available")
            return False
            
        success, response = self.run_test(
            "Get Specific Project",
            "GET",
            f"/projects/{self.test_project_id}",
            200
        )
        return success

    def test_image_upload(self):
        """Test image upload"""
        # Create a small test image file
        import io
        test_file = io.BytesIO(base64.b64decode(self.test_image_b64))
        test_file.name = 'test.png'
        
        success, response = self.run_test(
            "Image Upload",
            "POST",
            "/image/upload",
            200,
            files={'file': ('test.png', test_file, 'image/png')}
        )
        
        if success and 'image' in response:
            print(f"   ✅ Image uploaded successfully")
            return True, response['image']
        return False, None

    def test_remove_background(self):
        """Test background removal"""
        success, uploaded_image = self.test_image_upload()
        if not success:
            return False
            
        success, response = self.run_test(
            "Remove Background",
            "POST",
            "/image/remove-background",
            200,
            data={"image": uploaded_image}
        )
        
        if success and 'image' in response:
            print(f"   ✅ Background removed successfully")
            return True
        return False

    def test_generate_background(self):
        """Test AI background generation"""
        success, uploaded_image = self.test_image_upload()
        if not success:
            return False
            
        print("   🔄 Testing AI background generation (may take a few seconds)...")
        success, response = self.run_test(
            "Generate AI Background",
            "POST",
            "/image/generate-background",
            200,
            data={
                "prompt": "luxury marble background for product photography",
                "reference_image": uploaded_image
            }
        )
        
        if success and 'image' in response:
            print(f"   ✅ AI background generated successfully")
            return True
        return False

    def test_enhance_image(self):
        """Test image enhancement"""
        success, uploaded_image = self.test_image_upload()
        if not success:
            return False
            
        success, response = self.run_test(
            "Enhance Image",
            "POST",
            "/image/enhance",
            200,
            data={"image": uploaded_image}
        )
        
        if success and 'image' in response:
            print(f"   ✅ Image enhanced successfully")
            return True
        return False

    def test_generate_content(self):
        """Test AI content generation"""
        print("   🔄 Testing AI content generation (may take a few seconds)...")
        success, response = self.run_test(
            "Generate AI Content",
            "POST",
            "/content/generate",
            200,
            data={
                "product_type": "Wireless Bluetooth Headphones",
                "key_features": "Noise cancellation, 30-hour battery, premium sound quality"
            }
        )
        
        if success and 'title' in response and 'description' in response:
            print(f"   ✅ AI content generated - Title: {response['title'][:50]}...")
            print(f"   ✅ Description length: {len(response['description'])} characters")
            return True
        return False

    def test_update_project(self):
        """Test project update"""
        if not self.test_project_id:
            print("❌ No test project ID available")
            return False
            
        success, response = self.run_test(
            "Update Project",
            "PUT",
            f"/projects/{self.test_project_id}",
            200,
            data={
                "name": "Updated Test Project",
                "ai_title": "Test AI Title",
                "ai_description": "Test AI Description"
            }
        )
        return success

    def test_delete_project(self):
        """Test project deletion"""
        if not self.test_project_id:
            print("❌ No test project ID available")
            return False
            
        success, response = self.run_test(
            "Delete Project",
            "DELETE",
            f"/projects/{self.test_project_id}",
            200
        )
        
        if success:
            print(f"   ✅ Project {self.test_project_id} deleted")
            self.test_project_id = None
        return success

def main():
    print("🚀 Starting Amazon A+ Content Generator API Tests")
    print("=" * 60)
    
    tester = AmazonContentGeneratorTester()
    
    # Run all tests
    tests = [
        ("Root Endpoint", tester.test_root_endpoint),
        ("User Signup", tester.test_signup),
        ("User Login", tester.test_login),
        ("Create Project", tester.test_create_project),
        ("Get Projects", tester.test_get_projects),
        ("Get Specific Project", tester.test_get_project),
        ("Image Upload", lambda: tester.test_image_upload()[0]),
        ("Remove Background", tester.test_remove_background),
        ("Image Enhancement", tester.test_enhance_image),
        ("AI Content Generation", tester.test_generate_content),
        ("AI Background Generation", tester.test_generate_background),
        ("Update Project", tester.test_update_project),
        ("Delete Project", tester.test_delete_project),
    ]
    
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            if not success:
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            failed_tests.append(test_name)
            tester.tests_run += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} passed")
    print(f"✅ Success Rate: {(tester.tests_passed/tester.tests_run*100):.1f}%")
    
    if failed_tests:
        print(f"\n❌ Failed Tests:")
        for test in failed_tests:
            print(f"   - {test}")
        return 1
    else:
        print("\n🎉 All tests passed!")
        return 0

if __name__ == "__main__":
    sys.exit(main())