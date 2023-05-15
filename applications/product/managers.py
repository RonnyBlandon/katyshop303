from django.db import models

class ProductManager(models.Manager):
    """ procedures for category """
    def products_by_category(self, slug_category: int):
        products = self.filter(category__slug=slug_category)
        return products
    
    def search_product_trgm(self, kword):
        # We use the trigram method and icontains to find the product
        if kword:
            result = self.filter(name__trigram_similar=kword).order_by('-modified')
            if result:
                return result 
            
            result2 = self.filter(name__icontains=kword)
            if result2:
                return result2
        
        return None

