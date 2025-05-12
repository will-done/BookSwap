from django.contrib import admin
from book.models import Book,Category
from django.utils.safestring import mark_safe

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active","is_home", "slug","selected_categories",)
    list_editable =("is_active","is_home",)
    search_fields =("title", "description",)
    readonly_fields =("slug",)
    list_filter = ("is_active","categories",)

    def selected_categories(self, obj):
        html = "<ul>"

        for category in obj.categories.all():
            html += "<li>" + category.name + "</li>"

        html += "</ul>"
        return mark_safe(html)


admin.site.register(Book, BookAdmin)
admin.site.register(Category)

from django.contrib import admin
from .models import TradeOffer

@admin.register(TradeOffer)
class TradeOfferAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver','sender_book__title', 'receiver_book__title', 'status', 'approved_by_admin', 'created_at')
    list_filter = ('status', 'approved_by_admin')
    search_fields = ('sender__username', 'receiver__username', 'sender_book__title', 'receiver_book__title')

    list_editable = ('approved_by_admin',)
