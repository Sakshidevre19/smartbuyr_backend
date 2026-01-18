from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Product
from .recommender import get_recommendations
import random
import hashlib

def get_product_image(product_id, title, description):
    """Generate product-specific image URL based on product ID, title and description"""
    # Use a simple approach - different image for each product ID
    base_id = (product_id % 100) + 1  # Use IDs 1-100
    
    text = (title + ' ' + (description or '')).lower()
    
    # Create categories with actual product images
    if any(word in text for word in ['phone', 'mobile', 'smartphone', 'iphone', 'android']):
        return f'https://cdn.dummyjson.com/product-images/{base_id}/1.jpg'
    elif any(word in text for word in ['laptop', 'computer', 'pc', 'macbook']):
        return f'https://cdn.dummyjson.com/product-images/{base_id + 100}/1.jpg'
    elif any(word in text for word in ['shirt', 'tshirt', 't-shirt', 'top', 'blouse']):
        return f'https://cdn.dummyjson.com/product-images/{base_id + 200}/1.jpg'
    elif any(word in text for word in ['shoe', 'sneaker', 'boot', 'footwear']):
        return f'https://cdn.dummyjson.com/product-images/{base_id + 300}/1.jpg'
    elif any(word in text for word in ['watch', 'smartwatch']):
        return f'https://cdn.dummyjson.com/product-images/{base_id + 400}/1.jpg'
    else:
        return f'https://picsum.photos/300/300?random={product_id}'


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    data = []
    for product in products:
        price = round(random.uniform(500, 25000), 0)  # INR range
        data.append({
            'id': product.product_id,
            'name': product.title,
            'title': product.title,
            'description': product.description,
            'price': int(price),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'reviews': random.randint(50, 300),
            'category': 'General',
            'image': get_product_image(product.product_id, product.title, product.description)
        })
    return Response(data)


@api_view(['GET'])
def product_detail(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
        price = round(random.uniform(500, 25000), 0)  # INR range
        data = {
            'id': product.product_id,
            'name': product.title,
            'title': product.title,
            'description': product.description or 'High-quality product with excellent features.',
            'price': int(price),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'reviews': random.randint(50, 300),
            'category': 'General',
            'image': get_product_image(product.product_id, product.title, product.description)
        }
        return Response(data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)


@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )[:50]
    else:
        products = Product.objects.all()[:50]
    
    data = []
    for product in products:
        price = round(random.uniform(500, 25000), 0)  # INR range
        data.append({
            'id': product.product_id,
            'name': product.title,
            'title': product.title,
            'description': product.description,
            'price': int(price),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'reviews': random.randint(50, 300),
            'category': 'General',
            'image': get_product_image(product.product_id, product.title, product.description)
        })
    return Response(data)


@api_view(['GET'])
def recommend_products(request, product_id):
    try:
        recs = get_recommendations(product_id)
        recommendations = []
        for _, rec in recs.iterrows():
            try:
                product = Product.objects.get(product_id=rec['product_id'])
                price = round(random.uniform(500, 25000), 0)  # INR range
                recommendations.append({
                    'id': product.product_id,
                    'name': product.title,
                    'title': product.title,
                    'price': int(price),
                    'rating': round(random.uniform(3.5, 5.0), 1),
                    'reviews': random.randint(50, 300),
                    'image': get_product_image(product.product_id, product.title, product.description)
                })
            except Product.DoesNotExist:
                continue
        
        return Response(recommendations[:4])
    except Exception:
        # Fallback to random products
        products = Product.objects.all().order_by('?')[:4]
        recommendations = []
        for product in products:
            price = round(random.uniform(500, 25000), 0)  # INR range
            recommendations.append({
                'id': product.product_id,
                'name': product.title,
                'title': product.title,
                'price': int(price),
                'rating': round(random.uniform(3.5, 5.0), 1),
                'reviews': random.randint(50, 300),
                'image': get_product_image(product.product_id, product.title, product.description)
            })
        return Response(recommendations)

