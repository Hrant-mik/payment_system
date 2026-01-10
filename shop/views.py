import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_order(request):
    order_id = request.session.get('order_id')
    if order_id:
        return Order.objects.get(id=order_id)
    order = Order.objects.create()
    request.session['order_id'] = order.id
    return order


def home(request):
    items = Item.objects.all()
    order = get_order(request)
    return render(request, 'shop/home.html', {'items': items, 'order': order})


def add_to_order(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    order = get_order(request)
    order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('home')


def buy_now(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    session = stripe.checkout.Session.create(
            mode='payment',
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item.name},
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )
    return redirect(session.url)


def order_view(request):
    order = get_order(request)
    return render(request, 'shop/order.html', {'order': order})


def pay_order(request):
    order = get_order(request)

    line_items = []
    for oi in order.items.all():
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': oi.item.name},
                'unit_amount': oi.item.price,
            },
            'quantity': oi.quantity,
        })

    session = stripe.checkout.Session.create(
        mode='payment',
        payment_method_types=['card'],
        line_items=line_items,
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )

    return redirect(session.url)


def success(request):
    return render(request, 'shop/success.html')


def cancel(request):
    return render(request, 'shop/cancel.html')



def cancel_order_item(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    order_item.delete()
    return redirect('order')
