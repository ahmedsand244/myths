from django.shortcuts import render
from .models import ServiceCategory

def services_list_view(request):
    categories = ServiceCategory.objects.prefetch_related('services').all()
    return render(request, 'services/services_list.html', {'categories': categories})


from django.shortcuts import render, get_object_or_404
from .models import ServiceCategory, SubCategory

def subcategories_by_category(request, category_id):
    category = get_object_or_404(ServiceCategory, id=category_id)
    subcategories = SubCategory.objects.filter(category=category)
    return render(request, 'services/subcategories.html', {
        'category': category,
        'subcategories': subcategories
    })


from .models import ServiceCategory, SubCategory

def subcategories_view(request, category_id):
    category = ServiceCategory.objects.get(id=category_id)
    subcategories = category.subcategories.all()
    return render(request, 'services/subcategories.html', {
        'category': category,
        'subcategories': subcategories
    })


from .models import Service

def subcategory_services_view(request, subcategory_id):
    subcategory = SubCategory.objects.get(id=subcategory_id)
    services = Service.objects.filter(subcategory=subcategory)
    return render(request, 'services/subcategory_services.html', {
        'subcategory': subcategory,
        'services': services
    })


def service_detail_view(request, service_id):
    service = Service.objects.get(id=service_id)
    return render(request, 'services/service_detail.html', {
        'service': service
    })



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import CartItem

@login_required
def add_to_cart_view(request, service_id):
    service = Service.objects.get(id=service_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, service=service)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CartItem

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user, order__isnull=True)

    # حساب الإجمالي
    total_price = sum(item.service.price * item.quantity for item in cart_items)

    return render(request, 'services/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })



@login_required
def remove_from_cart_view(request, item_id):
    cart_item = CartItem.objects.get(id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')


from .models import Order, OrderItem, CartItem
from django.core.mail import send_mail


from django.conf import settings


from django.core.mail import send_mail

@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user, order__isnull=True)

    if not cart_items.exists():
        return redirect('cart')

    total_price = sum(item.service.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        order = Order.objects.create(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                service=item.service,
                quantity=item.quantity
            )
        cart_items.delete()

        # 📨 إرسال الإيميل
        subject = 'تم تأكيد طلبك على موقعنا'
        message = f'شكراً لك يا {request.user.username}، تم تأكيد طلبك رقم {order.id}.'
        recipient_list = [request.user.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)

        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'services/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })




from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

@login_required
def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    items_with_prices = []
    total = 0

    for item in order.items.all():
        item_total = item.quantity * item.service.price
        total += item_total
        items_with_prices.append({
            'title': item.service.title,
            'quantity': item.quantity,
            'price': item.service.price,
            'total': item_total
        })

    return render(request, 'services/order_confirmation.html', {
        'order': order,
        'items_with_prices': items_with_prices,
        'total': total
    })



from .models import Order

@login_required
def my_account_view(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')

    return render(request, 'services/my_account.html', {
        'user': user,
        'orders': orders
    })




from django.shortcuts import get_object_or_404

def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart_items = CartItem.objects.filter(order=order)

    context = {
        'order': order,
        'cart_items': cart_items,
    }
    return render(request, 'services/order_detail.html', context)




from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import Count

from django.contrib.auth.models import User

@staff_member_required
def admin_dashboard_view(request):
    status_filter = request.GET.get('status')
    user_filter = request.GET.get('user')

    orders = Order.objects.all()

    if status_filter:
        orders = orders.filter(status=status_filter)

    if user_filter:
        orders = orders.filter(user__id=user_filter)

    status_counts = Order.objects.values('status').annotate(count=Count('status'))
    users = User.objects.all()

    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'status_counts': status_counts,
        'users': users,
        'selected_user': int(user_filter) if user_filter else None,
    }
    return render(request, 'services/admin_dashboard.html', context)


from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def update_order_status_view(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.status = request.POST.get('status')
        order.save()
    return redirect('admin_dashboard')


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'services/admin_order_detail.html', {'order': order})


def about_us_view(request):
    return render(request, 'pages/about.html')



from django.shortcuts import render
from .models import Event
from .models import Event, EventRequest

def events_view(request):
    events = Event.objects.all()

    if request.method == 'POST':
        EventRequest.objects.create(
            client_name=request.POST.get('client_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            event_name=request.POST.get('event_name'),
            date=request.POST.get('date'),
            number_of_organizers=request.POST.get('number_of_organizers'),
            notes=request.POST.get('notes'),
        )
        return render(request, 'services/event_request_success.html', {'events': events})

    return render(request, 'services/events.html', {'events': events})



from django.db.models import Avg

def organizer_detail_view(request, organizer_id):
    organizer = get_object_or_404(Organizer, id=organizer_id)
    reviews = organizer.reviews.all().order_by('-created_at')
    total_reviews = reviews.count()
    return render(request, 'services/organizer_detail.html', {
        'organizer': organizer,
        'reviews': reviews,
        'total_reviews': total_reviews,
    })


from .models import Organizer
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect

from .models import Organizer, ContactMessage

def contact_organizer_view(request, organizer_id):
    organizer = Organizer.objects.get(id=organizer_id)

    if request.method == "POST":
        name = request.POST.get('name')
        message = request.POST.get('message')

        # حفظ في قاعدة البيانات
        ContactMessage.objects.create(
            organizer=organizer,
            name=name,
            message=message
        )

        # إرسال على البريد أيضًا لو حابب
        send_mail(
            subject=f"طلب تواصل مع {organizer.name}",
            message=f"من: {name}\n\n{message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
        )

        return render(request, 'services/contact_success.html', {'organizer': organizer})

    return render(request, 'services/contact_form.html', {'organizer': organizer})


def event_request_view(request):
    if request.method == "POST":
        EventRequest.objects.create(
            client_name=request.POST.get('client_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            event_name=request.POST.get('event_name'),
            date=request.POST.get('date'),
            number_of_organizers=request.POST.get('number_of_organizers'),
            notes=request.POST.get('notes'),
        )
        return render(request, 'services/event_request_success.html')
    return render(request, 'services/event_request_form.html')

from .models import Organizer
from django.shortcuts import render, get_object_or_404

def organizer_profile_view(request, organizer_id):
    organizer = get_object_or_404(Organizer, id=organizer_id)
    return render(request, 'services/organizer_profile.html', {'organizer': organizer})



def all_organizers_view(request):
    organizers = Organizer.objects.all()
    return render(request, 'services/all_organizers.html', {'organizers': organizers})


from .forms import OrganizerReviewForm

from django.db.models import Avg, Count

def organizer_profile_view(request, organizer_id):
    organizer = get_object_or_404(Organizer, id=organizer_id)
    reviews = organizer.reviews.all().order_by('-created_at')

    # total_reviews = reviews.count()
    # average_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    average_rating = organizer.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    average_rating = round(average_rating, 1)  # علشان تطلع 4.3 أو 4.0 وهكذا


    if request.method == "POST":
        form = OrganizerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.organizer = organizer
            review.save()
            return redirect('organizer_profile', organizer_id=organizer.id)
    else:
        form = OrganizerReviewForm()

    return render(request, 'services/organizer_profile.html', {
        'organizer': organizer,
        'reviews': reviews,
        # 'total_reviews': total_reviews,
        'average_rating': average_rating,  # تقريبه لرقم عشري واحد
        'form': form
    })



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import UserUpdateForm  # هنعمله تحت

User = get_user_model()

@login_required
def update_account(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account information has been updated successfully.')
            return redirect('my_account')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'services/update_account.html', {'form': form})



from .models import Order, ServiceProvider, Service

@login_required
def my_account(request):
    orders = Order.objects.filter(user=request.user)

    # الخدمات اللي بيقدمها المستخدم كبائع (مزود خدمة)
    my_services = Service.objects.filter(provider__user=request.user)

    context = {
        'orders': orders,
        'my_services': my_services,
    }
    return render(request, 'services/my_account.html', context)



from django.shortcuts import render

from .models import Service, Event, Category

from pages.models import Partner

from services.models import Event

def home(request):
    services = Service.objects.all()[:8]
    events = Event.objects.order_by('-date')[:3]
    categories = Category.objects.all()
    providers = ServiceProvider.objects.all()[:3]
    partners = Partner.objects.all()

    return render(request, 'pages/home.html', {
    'services': services,
    'events': events,
    'categories': categories,
    'providers': providers,
    'partners': partners  # ✅ إضافة الشركاء هنا
})



from django.db.models import Q
from .models import OrganizerProfile 
from django.db.models import Q

from .models import OrganizerProfile, ServiceProvider  # تأكد إنك مستوردهم

def search_services(request):
    query = request.GET.get('q')

    service_results = Service.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ) if query else []

    event_results = Event.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ) if query else []

    # organizer_results = OrganizerProfile.objects.filter(
    #     Q(user__username__icontains=query) |
    #     # Q(user__first_name__icontains=query) |
    #     # Q(user__last_name__icontains=query) |
    #     Q(bio__icontains=query)
    # ) if query else []

    service_provider_results = ServiceProvider.objects.filter(
        Q(user__username__icontains=query) |
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(bio__icontains=query)
    ) if query else []

    return render(request, 'services/search_results.html', {
        'query': query,
        'service_results': service_results,
        'event_results': event_results,
        # 'organizer_results': organizer_results,
        'provider_results': service_provider_results
    })

from django.shortcuts import render, redirect
from .models import ContactMessage
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # حفظ البيانات في قاعدة البيانات
        ContactMessage.objects.create(name=name, email=email, message=message)

        # إرسال رسالة نجاح للواجهة
        return render(request, 'pages/contact.html', {'success': True})

    return render(request, 'pages/contact.html')










