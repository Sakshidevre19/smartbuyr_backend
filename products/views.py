from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Product
from .recommender import get_recommendations
from .utils import get_product_image
import random   

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all().order_by('product_id')

    paginator = PageNumberPagination()
    paginator.page_size = 20   # ek page me 20 products

    result_page = paginator.paginate_queryset(products, request)

    data = []
    for product in result_page:
        price = round(random.uniform(500, 25000), 0)
        data.append({
            'id': product.product_id,
            'name': product.title,
            'title': product.title,
            'description': product.description,
            'price': int(price),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'reviews': random.randint(50, 300),
            'category': 'General',
            'image': get_product_image(
                product.product_id,
                product.title,
                product.description
            )
        })

    return paginator.get_paginated_response(data)



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

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    paginator = PageNumberPagination()
    paginator.page_size = 20   # per page 20 results

    result_page = paginator.paginate_queryset(products, request)

    data = []
    for product in result_page:
        price = round(random.uniform(500, 25000), 0)
        data.append({
            'id': product.product_id,
            'name': product.title,
            'title': product.title,
            'description': product.description,
            'price': int(price),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'reviews': random.randint(50, 300),
            'category': 'General',
            'image': get_product_image(
                product.product_id,
                product.title,
                product.description
            )
        })

    return paginator.get_paginated_response(data)



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

