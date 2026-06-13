from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import ProductForm, CheckoutForm


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(customer=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key, customer=None)
    return cart


def home(request):
    products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    featured = Product.objects.filter(is_available=True).order_by('?')[:4]
    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
        'featured': featured,
    })


def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
    })


def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect('store:cart')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('store:cart')


def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('store:cart')


@login_required
def checkout(request):
    if not request.user.is_customer():
        messages.error(request, 'Only customers can place orders.')
        return redirect('store:home')

    cart = get_or_create_cart(request)
    if not cart.cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                customer=request.user,
                shipping_address=form.cleaned_data['shipping_address'],
                phone=form.cleaned_data['phone'],
                notes=form.cleaned_data.get('notes', ''),
            )
            total = 0
            for item in cart.cart_items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
                total += item.subtotal
            order.total_price = total
            order.save()
            cart.cart_items.all().delete()
            messages.success(request, f'Order #{order.id} placed successfully!')
            return redirect('store:order_detail', order_id=order.id)
    else:
        form = CheckoutForm(initial={
            'shipping_address': request.user.address,
            'phone': request.user.phone,
        })
    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})


@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


# Owner Views
@login_required
def owner_dashboard(request):
    if not (request.user.is_owner() or request.user.is_superuser):
        messages.error(request, 'Access denied. Owner accounts only.')
        return redirect('store:home')
    products = Product.objects.filter(owner=request.user)
    orders = Order.objects.filter(items__product__owner=request.user).distinct().order_by('-created_at')[:10]
    return render(request, 'store/owner_dashboard.html', {
        'products': products,
        'orders': orders,
        'total_products': products.count(),
        'total_orders': orders.count(),
    })


@login_required
def add_product(request):
    if not (request.user.is_owner() or request.user.is_superuser):
        messages.error(request, 'Access denied.')
        return redirect('store:home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('store:owner_dashboard')
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('store:owner_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form, 'title': 'Edit Product', 'product': product})


@login_required
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug, owner=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    return redirect('store:owner_dashboard')


@login_required
def update_order_status(request, order_id):
    if not (request.user.is_owner() or request.user.is_superuser):
        messages.error(request, 'Access denied.')
        return redirect('store:home')
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {status}.')
    return redirect('store:owner_dashboard')
