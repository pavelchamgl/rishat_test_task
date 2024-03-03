import os
from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
import stripe
from .models import Item, Order, Discount


stripe.api_key = os.getenv('STRIPE_API_KEY')


@require_GET
def get_session_id(request, id):
    item = get_object_or_404(Item, id=id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return JsonResponse({'session_id': session.id})


@require_GET
def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    context = {'item': item}
    return render(request, 'payments/item_detail.html', context)


@require_GET
def create_order(request):
    items = Item.objects.all()
    discounts = Discount.objects.all()
    return render(request, 'payments/create_order.html', {'items': items, 'discounts': discounts})


@require_GET
def process_order(request):
    item_ids = request.GET.getlist('items')
    discount_ids = request.GET.getlist('discounts')

    order = Order.objects.create()

    items = get_list_or_404(Item, id__in=item_ids)
    discounts = get_list_or_404(Discount, id__in=discount_ids)

    order.items.add(*items)
    order.discount.add(*discounts)

    order.calculate_total_price()

    line_items = [{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': item.name,
                'description': item.description if item.description else '',
            },
            'unit_amount': int(item.price * 100 - (discount.amount / 100 * item.price * 100)),
        },
        'quantity': 1,
    } for item in order.items.all() for discount in order.discount.all()]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        tax_id_collection={"enabled": True},
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )

    return JsonResponse({'session_id': session.id})
