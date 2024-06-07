from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.contrib.auth.models import auth
from .models import User
from store.models import Product
from django.db.models import Q
from category.models import Category
from carts.models import Cart, CartItem
from .utils import _number
from .forms import RegistrationForm
from django.contrib import messages as mg
from django.contrib.auth.decorators import login_required
import requests

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from carts.utils import _cart_id

# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    products = Product.objects.filter(
        Q(slug__icontains=q) |
        Q(product_name__icontains=q) |
        Q(category__category_name__icontains=q), is_available=True
    )

    categories = Category.objects.all()
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        "categories": categories,
        'number': _number(request),
        'page_obj': page_obj
    }
    return render(request, 'store.html', context)


@login_required(login_url='login')
def dashboard(request):
    context = {

    }
    return render(request, 'dashboard.html')


def register(request):
    form = RegistrationForm()

    error_msg = ''

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            # auth.login(request, user)

            # USER ACTIVATION

            with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS
            ) as connection:
                current_site = get_current_site(request)
                mail_subject = 'ACCOUNT ACTIVATION MAIL'
                message = render_to_string('email_verification.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })
                to_email = user.email
                email_from = settings.DEFAULT_FROM_EMAIL
                send_mail = EmailMessage(
                    mail_subject, message, email_from, to_email, connection=connection)
                send_mail.send()

                mg.success(request, "Check your email to Verify your Account")
                return redirect('dashboard')
        else:
            errors = form.errors.get_json_data(escape_html=True)
            for error in errors:
                error_msg = errors[error][0]['message']

            mg.error(request, error_msg)

    context = {
        'number': _number(request),
        'form': form,
    }
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)
        # user = auth.authenticate(
        #     email=email, password=password, is_active=True)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_exist = CartItem.objects.filter(cart=cart).exists()

                if is_cart_exist:
                    cart_item = CartItem.objects.all()

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass

            auth.login(request, user)

            url = request.META.get('HTTP_REFERER')

            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))   
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except: return redirect('dashboard')

        else:
            mg.error(request, 'Invalid Email or Password!')

    context = {
        'number': _number(request)
    }
    return render(request, 'signin.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        mg.success(request, 'Your Account has been Activated! You can Login')
        return redirect('login')
    else:
        mg.error(request, 'Invalid Activation Link')
        return redirect('register')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        mg.warning(request, 'You are Logged Out!')
        return redirect('login')
