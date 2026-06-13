from .models import Cart


def cart_count(request):
    count = 0
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(customer=request.user).first()
        else:
            if request.session.session_key:
                cart = Cart.objects.filter(session_key=request.session.session_key, customer=None).first()
            else:
                cart = None
        if cart:
            count = cart.get_count()
    except Exception:
        pass
    return {'cart_count': count}
