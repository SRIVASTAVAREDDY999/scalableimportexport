import requests
import json
from django.shortcuts import render
from django.http import JsonResponse

BASE_URL = "https://hy7qoqj043.execute-api.us-east-1.amazonaws.com/dev/products"
OTP_SERVICE_URL = "https://tezo7kqd0k.execute-api.eu-west-1.amazonaws.com/prod/OTP-service-v1"

def home(request):
    return render(request, 'product/home.html')  # Updated to display all API options

# External API Product Fetch
def fetch_products_from_external_api():
    FAKE_STORE_API_URL = "https://fakestoreapi.com/products"  # Define this URL properly
    try:
        response = requests.get(FAKE_STORE_API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from external API: {e}")
        return None

def view_external_products(request):
    external_products = fetch_products_from_external_api()
    if external_products:
        return render(request, 'product/view-external-products.html', {'products': external_products})
    else:
        return JsonResponse({'message': 'Failed to fetch products from external API'}, status=500)    

# ✅ OTP Service Integration
def generate_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Ensure the form sends the email properly
        purpose = request.POST.get('purpose', 'account verification')  # Default value
        
        if not email:
            return JsonResponse({'message': 'Email is required'}, status=400)
        
        otp_payload = {'email': email, 'purpose': purpose}
        otp_response = requests.post(OTP_SERVICE_URL, json=otp_payload)
        
        if otp_response.status_code == 200:
            otp_data = otp_response.json()
            return JsonResponse({'message': 'OTP sent successfully', 'otp': otp_data.get('otp')}, status=200)
        else:
            return JsonResponse({'message': 'Failed to generate OTP', 'error': otp_response.json()}, status=500)

    return render(request, 'product/generate-otp.html')  # Make sure this HTML form exists

# ✅ Product CRUD Operations
def create_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8')) if request.content_type == 'application/json' else request.POST  

            product_id = data.get('productId')
            product_name = data.get('productName')
            product_price = data.get('productPrice')

            if not product_id or not product_name or not product_price:
                return JsonResponse({'message': 'Missing required fields'}, status=400)

            response = requests.post(BASE_URL, json={'productId': product_id, 'productName': product_name, 'productPrice': product_price})
            response_data = response.json()
            return JsonResponse({'message': 'Product created successfully!', 'api_response': response_data}, status=response.status_code)
        
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)

    return render(request, 'product/create-product.html')

def update_product(request):
    if request.method == "POST":
        product_id = request.POST.get('productId')
        product_name = request.POST.get('productName')
        product_price = request.POST.get('productPrice')

        if not product_id:
            return JsonResponse({'message': 'Product ID is required'}, status=400)

        response = requests.put(f"{BASE_URL}?productId={product_id}", json={'productId': product_id, 'productName': product_name, 'productPrice': product_price})
        return JsonResponse(response.json())

    return render(request, 'product/update-product.html')

def delete_product(request):
    if request.method == "POST":
        product_id = request.POST.get('productId')
        if not product_id:
            return JsonResponse({'message': 'Product ID is required'}, status=400)

        response = requests.delete(f"{BASE_URL}?productId={product_id}")
        return JsonResponse(response.json())

    return render(request, 'product/delete-product.html')

def view_products(request):
    response = requests.get(BASE_URL)
    products = response.json()
    return render(request, 'product/view-products.html', {'products': products})

# ✅ Dashboard Page
def dashboard(request):
    return render(request, 'product/dashboard.html')

# ✅ Debugging Endpoint
def debug_products(request):
    response = requests.get(BASE_URL)
    products = response.json()
    return JsonResponse({'products': products}, status=200)
