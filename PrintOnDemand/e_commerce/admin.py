from django.contrib import admin
from .models import Category, Product, Order,OrderItem, User  # Import models

admin.site.register(User)
# Register the Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

# Register the Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_trending', 'added_by', 'created_at', 'updated_at')
    list_filter = ('category', 'added_by_admin','is_trending')
    search_fields = ('name', 'description')
    raw_id_fields = ('category', 'added_by')  # Use raw ID fields for better performance

admin.site.register(Product, ProductAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # No empty rows

# Register the Order model
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'total_amount')
    list_filter = ('status', 'created_at')  # Use created_at instead of order_date
    search_fields = ('user__username',)
    inlines = [OrderItemInline]

    # Display total amount in the admin list
    def total_amount(self, obj):
        return sum(item.price * item.quantity for item in obj.order_items.all())
    total_amount.short_description = 'Total Amount'

admin.site.register(Order, OrderAdmin)