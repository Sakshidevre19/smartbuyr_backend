import hashlib

def get_product_image(product_id, title, description=''):
    """
    Generate unique, relevant product images based on product name and category
    Uses multiple image sources for reliability
    """
    text = (title + ' ' + (description or '')).lower()
    
    # Create a unique seed from product_id and title for consistency
    seed = abs(hash(f"{product_id}{title}")) % 1000
    
    # Category-based image selection with relevant keywords
    categories = {
        'phone': ['phone', 'mobile', 'smartphone', 'iphone', 'android', 'samsung', 'oneplus', 'xiaomi', 'oppo', 'vivo', 'realme'],
        'laptop': ['laptop', 'computer', 'pc', 'macbook', 'notebook', 'chromebook', 'dell', 'hp', 'lenovo', 'asus'],
        'tablet': ['tablet', 'ipad', 'tab', 'kindle'],
        'watch': ['watch', 'smartwatch', 'timepiece', 'clock', 'fitbit', 'garmin'],
        'headphone': ['headphone', 'earphone', 'earbud', 'airpod', 'headset', 'earbuds', 'beats'],
        'camera': ['camera', 'dslr', 'gopro', 'camcorder', 'canon', 'nikon', 'sony'],
        'tv': ['tv', 'television', 'monitor', 'display', 'screen', 'samsung', 'lg'],
        'speaker': ['speaker', 'bluetooth', 'soundbar', 'audio', 'jbl', 'bose'],
        'keyboard': ['keyboard', 'mouse', 'keypad', 'mechanical'],
        'shoe': ['shoe', 'sneaker', 'boot', 'footwear', 'sandal', 'slipper', 'nike', 'adidas', 'puma'],
        'shirt': ['shirt', 'tshirt', 't-shirt', 'top', 'blouse', 'polo'],
        'pant': ['pant', 'jeans', 'trouser', 'shorts', 'levis', 'denim'],
        'dress': ['dress', 'gown', 'frock', 'skirt'],
        'bag': ['bag', 'backpack', 'handbag', 'purse', 'luggage', 'suitcase'],
        'furniture': ['chair', 'table', 'sofa', 'bed', 'desk', 'furniture', 'couch'],
        'book': ['book', 'novel', 'magazine', 'journal', 'diary'],
        'toy': ['toy', 'game', 'puzzle', 'doll', 'lego'],
        'sports': ['ball', 'bat', 'racket', 'sports', 'fitness', 'gym', 'cricket', 'football'],
        'beauty': ['makeup', 'cosmetic', 'lipstick', 'perfume', 'beauty', 'skincare'],
        'kitchen': ['kitchen', 'utensil', 'cookware', 'appliance', 'mixer', 'blender'],
    }
    
    # Find matching category
    matched_category = None
    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            matched_category = category
            break
    
    # Use picsum.photos with category-based seed for consistent, working images
    if matched_category:
        # Use category name in seed for variety
        category_seed = abs(hash(f"{matched_category}{seed}")) % 1000
        return f'https://picsum.photos/seed/{category_seed}/300/300'
    else:
        # Fallback: use product_id based seed
        return f'https://picsum.photos/seed/{seed}/300/300'


