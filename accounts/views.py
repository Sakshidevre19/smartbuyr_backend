from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .models import CartItem, Wishlist
import json
import requests

@csrf_exempt
@api_view(['POST'])
def signup(request):
    try:
        data = json.loads(request.body)
        
        if User.objects.filter(email=data['email']).exists():
            return Response({'error': 'Email already exists'}, status=400)
        
        user = User.objects.create(
            username=data['email'],
            email=data['email'],
            password=make_password(data['password']),
            first_name=data.get('firstName', ''),
            last_name=data.get('lastName', '')
        )
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'User created successfully',
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name
            }
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['POST'])
def signin(request):
    try:
        data = json.loads(request.body)
        user = authenticate(username=data['email'], password=data['password'])
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful',
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'firstName': user.first_name,
                    'lastName': user.last_name
                }
            })
        
        return Response({'error': 'Invalid user login, please signup to create account'}, status=400)
    except Exception as e:
        return Response({'error': 'Invalid user login, please signup to create account'}, status=400)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data['product_id']
        
        # Get product details from products API
        product_response = requests.get(f'http://localhost:8000/api/products/{product_id}/')
        if not product_response.ok:
            return Response({'error': 'Product not found'}, status=404)
        
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product_id=product_id,
            defaults={'quantity': data.get('quantity', 1)}
        )
        if not created:
            cart_item.quantity += data.get('quantity', 1)
            cart_item.save()
        return Response({'message': 'Added to cart successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    items = []
    total = 0
    
    for item in cart_items:
        # Get product details from products API
        try:
            product_response = requests.get(f'http://localhost:8000/api/products/{item.product_id}/')
            if product_response.ok:
                product = product_response.json()
                item_total = product['price'] * item.quantity
                total += item_total
                items.append({
                    'id': item.id,
                    'product': {
                        'id': product['id'],
                        'name': product['name'],
                        'price': product['price'],
                        'image': product.get('image', '')
                    },
                    'quantity': item.quantity,
                    'total': item_total
                })
        except:
            continue
    
    return Response({'items': items, 'total': total})

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    try:
        CartItem.objects.filter(id=item_id, user=request.user).delete()
        return Response({'message': 'Removed from cart'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    try:
        data = json.loads(request.body)
        product_id = data['product_id']
        
        # Get product details from products API
        product_response = requests.get(f'http://localhost:8000/api/products/{product_id}/')
        if not product_response.ok:
            return Response({'error': 'Product not found'}, status=404)
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product_id=product_id
        )
        if created:
            return Response({'message': 'Added to wishlist'})
        else:
            return Response({'message': 'Already in wishlist'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    items = []
    
    for item in wishlist_items:
        # Get product details from products API
        try:
            product_response = requests.get(f'http://localhost:8000/api/products/{item.product_id}/')
            if product_response.ok:
                product = product_response.json()
                items.append({
                    'id': item.id,
                    'product': {
                        'id': product['id'],
                        'name': product['name'],
                        'price': product['price'],
                        'image': product.get('image', ''),
                        'rating': product.get('rating', 4.0)
                    }
                })
        except:
            continue
    
    return Response({'items': items})

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, item_id):
    try:
        Wishlist.objects.filter(id=item_id, user=request.user).delete()
        return Response({'message': 'Removed from wishlist'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)