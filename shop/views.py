import stripe
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

MIN_STRIPE_AMOUNT = Decimal("0.50")


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

    quantity = int(request.POST.get('quantity', 1))

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        item=item
    )

    if created:
        order_item.quantity = quantity
    else:
        order_item.quantity += quantity

    order_item.save()
    return redirect('home')


def buy_now(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    quantity = int(request.POST.get('quantity', 1))

    total_amount = Decimal(item.price) * quantity / 100

    if total_amount < MIN_STRIPE_AMOUNT:
        messages.warning(request, "Payment is not possible. Minimum amount is $0.50.")
        return redirect('home')

    session = stripe.checkout.Session.create(
        mode='payment',
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {'name': item.name},
                'unit_amount': item.price,
            },
            'quantity': quantity,
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

    total_amount = Decimal("0.00")
    for oi in order.items.all():
        total_amount += Decimal(oi.item.price) * oi.quantity / 100

    if total_amount < MIN_STRIPE_AMOUNT:
        messages.warning(request, "Payment is not possible. Minimum amount is $0.50.։")
        return redirect('order')

    line_items = []
    for oi in order.items.all():
        line_items.append({
            'price_data': {
                'currency': oi.item.currency,
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


def cancel_order_item(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    order_item.delete()
    return redirect('order')


def success(request):
    request.session.pop('order_id', None)
    return render(request, 'shop/success.html')


def cancel(request):
    return render(request, 'shop/cancel.html')
