from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Sum

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def process_checkout(request):
    if request.method == "POST":
        quantity_from_form = int(request.POST["quantity"])
        price_from_form = float(request.POST["price"])
        total_charge = quantity_from_form * price_from_form
        print("Charging credit card...")
        Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
        return redirect("/checkout")
    else:
        return redirect("/")

def checkout(request):
    all_orders = Order.objects.all()
    total_quantity = 0
    total_due = 0
    for order in all_orders:
        total_quantity += order.quantity_ordered
        total_due += order.total_price

    context = {
        "last_order": Order.objects.last(),
        # "total_quantity": Order.objects.annotate(total_quantity=Sum('quantity_ordered')),
        # "total_due": Order.objects.annotate(total_due=Sum('total_price')),
        "total_quantity": total_quantity,
        "total_due": total_due,
    }    
    return render(request, "store/checkout.html", context)

