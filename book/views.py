
from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from book.models import Book, Category
from django.contrib.auth.decorators import login_required
from .forms import BookForm  # forms.py'den formu import ediyoruz
from django.contrib.auth.models import User
from .models import Book, TradeOffer
from django.contrib import messages




# Create your views here.

def index(request):
    
    context ={
    
        "books": Book.objects.filter(is_active=True, is_home=True),
        "categories": Category.objects.all()
    }
    return render(request, "book/index.html", context)


@login_required
def books(request):
    query = request.GET.get('q')
    category_slug = request.GET.get('category')

    # Tüm aktif kitaplar
    books = Book.objects.filter( is_active=True)

    # Kategori filtresi uygula
    if category_slug:
        books = books.filter(categories__slug=category_slug)

    # Arama filtresi uygula
    if query:
        books = books.filter(title__icontains=query)

    # Kullanıcının kendi kitapları ve diğer kullanıcıların kitapları
    my_books = books.filter(owner=request.user)
    other_books = books.exclude(owner=request.user)

    context = {
        "my_books": my_books,
        "other_books": other_books,
        "categories": Category.objects.all(),
        "query": query,
        "selected_category": category_slug
    }
    return render(request, "book/books.html", context)


def book_details(request, slug):
    book = Book.objects.get(slug=slug)
    return render(request, "book/book-details.html", {
        "book": book
    })



@login_required
def books_by_category(request, slug):
    # Seçilen kategoriye ait tüm aktif kitapları al
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(categories=category, is_active=True)

    # Kullanıcıya göre kitapları ayır
    my_books = books.filter(owner=request.user)
    other_books = books.exclude(owner=request.user)

    context = {
        "my_books": my_books,
        "other_books": other_books,
        "categories": Category.objects.all(),
        "selected_category": slug,
    }
    return render(request, "book/books.html", context)


# Kitap ekleme işlemi
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)   # Henüz veritabanına kaydetme
            book.owner = request.user        # Giriş yapan kullanıcıyı ata
            book.save()                      # Şimdi kaydet
            form.save_m2m()                  # ManyToMany alanları (categories) için
            return redirect('books')         # Kitap listesine yönlendir
    else:
        form = BookForm()
    return render(request, 'book/add_book.html', {'form': form})

# Takas teklifi gönderme işlemi
@login_required
def make_trade_offer(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        receiver_book_id = request.POST.get('receiver_book_id')
        receiver_book = get_object_or_404(Book, id=receiver_book_id)

        # Kullanıcı kendi kitabıyla takas yapamaz
        if book.owner == receiver_book.owner:
            messages.error(request, "Hatalı işlem.")
            return redirect('book_details', slug=book.slug)


        # Takas teklifini oluştur
        trade_offer = TradeOffer.objects.create(
            sender=request.user,
            receiver=book.owner,  # 🔧 Hata buradaydı
            sender_book=receiver_book,  # Kullanıcının gönderdiği kitap
            receiver_book=book,         # Almak istediği kitap
            status='pending'
    )


        return redirect('book_details', slug=book.slug)

    available_books = Book.objects.exclude(owner=request.user)

    return render(request, 'book/make_trade_offer.html', {'book': book, 'available_books': available_books})

@login_required
def accept_trade_offer(request, offer_id):
    offer = get_object_or_404(TradeOffer, id=offer_id)

    if offer.receiver_book.owner != request.user:
        return redirect('error_page')
    
    # Admin onayı yoksa işlem yapılmaz
    if not offer.approved_by_admin:
        messages.warning(request, "Bu takas henüz admin tarafından onaylanmamış.")
        return redirect('trade_offers')

    if offer.status == 'accepted':
        # Daha önce kabul edilmişse tekrar işlem yapılmasın
        return redirect('trade_offers')
    
     # Aynı kullanıcıya geçerse kitabı görünmez yap
    if offer.sender_book.owner == offer.receiver_book.owner:
        offer.receiver_book.is_active = False
        offer.receiver_book.save()

    

    # Durumu güncelle
    offer.status = 'accepted'
    offer.save()

    # Sahiplikleri güvenli şekilde değiştir
    temp_owner = offer.sender_book.owner
    offer.sender_book.owner = offer.receiver_book.owner
    offer.receiver_book.owner = temp_owner

    offer.sender_book.save()
    offer.receiver_book.save()
    messages.success(request, "Takas başarıyla gerçekleştirildi.")
    

    return redirect('trade_offers')


@login_required
def trade_offers(request):
    # Kullanıcının aldığı takas teklifleri
    received_offers = TradeOffer.objects.filter(receiver=request.user)

    # Kullanıcının gönderdiği takas teklifleri
    sent_offers = TradeOffer.objects.filter(sender=request.user)

    # Şablona gönderme
    return render(request, 'book/trade_offers.html', {
        'received_offers': received_offers,
        'sent_offers': sent_offers
    })

@login_required
def all_trade_offers(request):
    offers = TradeOffer.objects.all().select_related('sender', 'receiver', 'sender_book', 'receiver_book')
    return render(request, 'book/all_trade_offers.html', {'offers': offers})