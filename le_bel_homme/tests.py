from decimal import Decimal

from django.test import TestCase, override_settings, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Perfume, Brand, Cart
from .forms import CustomAuthenticationForm, UserRegistrationForm, BrandForm, SortingForm


class IndexViewTest(TestCase):
    def setUp(self):
        # Create a sample image file for testing
        self.image = SimpleUploadedFile("test_perfume.png", b"file_content", content_type="image/png")

        # Create some sample data with the image field set
        Perfume.objects.create(name='Perfume1', price=10.99, volume=50, image=self.image, url_name='perfume1')
        Perfume.objects.create(name='Perfume2', price=20.99, volume=100, image=self.image, url_name='perfume2')

    def test_index_view(self):
        # Make a GET request to the index view
        response = self.client.get(reverse('index'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the expected context data is present
        self.assertIn('perfumes', response.context)
        perfumes = response.context['perfumes']
        self.assertEqual(len(perfumes), 2)  # Adjust based on your actual data


class LoginViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view_with_valid_credentials(self):
        # Make a POST request to the login view with valid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})

        # Check if the response redirects to the index page upon successful login
        self.assertRedirects(response, reverse('index'))

        # Check if the user is now logged in
        self.assertTrue(self.client.session['_auth_user_id'])

    def test_login_view_with_invalid_credentials(self):
        # Make a POST request to the login view with invalid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})

        # Check if the response status code is 200 (login form should be redisplayed)
        self.assertEqual(response.status_code, 200)

        # Check if the form in the context is an instance of CustomAuthenticationForm
        self.assertIsInstance(response.context['form'], CustomAuthenticationForm)

        # Check if the user is not logged in
        self.assertFalse(self.client.session.get('_auth_user_id'))

        # Add more specific assertions if needed


class RegisterViewTest(TestCase):
    def test_register_view_with_valid_data(self):
        # Create a valid form data dictionary
        valid_form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        # Make a POST request to the register view with valid data
        response = self.client.post(reverse('register'), data=valid_form_data)

        # Check if the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the 'index' page after successful registration
        self.assertRedirects(response, reverse('index'))

        # Check if the user was actually created in the database
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_view_with_invalid_data(self):
        # Create invalid form data (missing required fields)
        invalid_form_data = {}

        # Make a POST request to the register view with invalid data
        response = self.client.post(reverse('register'), data=invalid_form_data)

        # Check if the form is not valid and the user is not redirected
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.status_code, 200)  # Status code for a successful form submission

        # Check if the user was not created in the database
        self.assertFalse(User.objects.exists())

    def test_register_view_get_request(self):
        # Make a GET request to the register view
        response = self.client.get(reverse('register'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the correct form is used in the context
        self.assertIsInstance(response.context['form'], UserRegistrationForm)

class ShopViewTest(TestCase):
    def setUp(self):
        # Create a sample image file for testing
        self.image = SimpleUploadedFile("test_perfume.png", b"file_content", content_type="image/png")

        self.brand1 = Brand.objects.create(name='Brand1')
        self.brand2 = Brand.objects.create(name='Brand2')

        # Create some sample data with the image field set
        self.perfume1 = Perfume.objects.create(name='Perfume1', price=10.99, volume=50, image=self.image, url_name='perfume1', brand=self.brand1)
        self.perfume2 = Perfume.objects.create(name='Perfume2', price=20.99, volume=100, image=self.image, url_name='perfume2', brand=self.brand2)


    def test_shop_view(self):
        # Test the shop view with no filters
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['perfumes'], [repr(self.perfume1), repr(self.perfume2)], ordered=False)

    def test_shop_view_with_query(self):
        # Test the shop view with a query parameter
        response = self.client.get(reverse('shop'), {'query': 'Perfume1'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['perfumes'], [repr(self.perfume1)], ordered=False)

    def test_shop_view_with_brand_filter(self):
        # Test the shop view with a brand filter
        response = self.client.get(reverse('shop'), {'brand_choices': [self.brand1.id]})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['perfumes'], [repr(self.perfume1)], ordered=False)

    def test_shop_view_with_sorting(self):
        # Test the shop view with sorting
        response = self.client.get(reverse('shop'), {'sorting_option': 'price_low_high'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['perfumes'], [repr(self.perfume2), repr(self.perfume1)], ordered=False)

    def test_shop_view_clear_form(self):
        # Test clearing the form data
        response = self.client.get(reverse('shop'), {'clear': 'true'})
        self.assertEqual(response.status_code, 302)

class InfoViewTest(TestCase):
    def test_info_view(self):
        # Make a GET request to the info view
        response = self.client.get(reverse('info'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

class CartViewTest(TestCase):
    def setUp(self):
        self.image = SimpleUploadedFile("test_perfume.png", b"file_content", content_type="image/png")

        # Create a user for testing (you can use the existing User model or create a custom one)
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create some sample data for testing
        self.perfume = Perfume.objects.create(name='Test Perfume', price=16.00, volume=50, image=self.image, url_name='test-perfume')

        # Create a Cart item for the user
        self.cart_item = Cart.objects.create(user=self.user, perfume=self.perfume, quantity=2)

        self.factory = RequestFactory()

    def test_cart_view_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the cart view
        response = self.client.get(reverse('cart'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the correct cart items and total price are present in the context
        self.assertIn('cart_items', response.context)
        self.assertIn('total_price', response.context)
        cart_items = response.context['cart_items']
        total_price = response.context['total_price']
        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0], self.cart_item)
        self.assertEqual(total_price, self.cart_item.perfume.price * self.cart_item.quantity)

    def test_cart_view_unauthenticated_user(self):
        # Make a GET request to the cart view without logging in
        response = self.client.get(reverse('cart'))

        # Check if the response status code is 302 (redirect to login page for authentication)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('cart'))

class PerfumeDetailViewTest(TestCase):
    def setUp(self):
        self.image = SimpleUploadedFile("test_perfume.png", b"file_content", content_type="image/png")

        # Create some sample data for testing
        self.perfume = Perfume.objects.create(name='Test Perfume', price=16.00, volume=50, image=self.image, url_name='test-perfume')

    def test_perfume_detail_view(self):
        # Make a GET request to the perfume_detail view
        response = self.client.get(reverse('perfume_detail', args=[self.perfume.url_name]))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the correct perfume is present in the context
        self.assertIn('perfume', response.context)
        self.assertEqual(response.context['perfume'], self.perfume)

# class CustomAuthenticationFormTest(TestCase):
#     def test_valid_authentication_form(self):
#         data = {'username': 'testuser', 'password': 'testpassword'}
#         form = CustomAuthenticationForm(data=data)
#         self.assertTrue(form.is_valid())
#
#     def test_invalid_authentication_form(self):
#         data = {'username': 'testuser', 'password': ''}
#         form = CustomAuthenticationForm(data=data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('password', form.errors)
#
# class UserRegistrationFormTest(TestCase):
#     def test_valid_registration_form(self):
#         data = {
#             'username': 'newuser',
#             'first_name': 'New',
#             'last_name': 'User',
#             'email': 'newuser@example.com',
#             'password1': 'newpassword',
#             'password2': 'newpassword',
#         }
#         form = UserRegistrationForm(data=data)
#         self.assertTrue(form.is_valid())
#
#     def test_invalid_registration_form(self):
#         # Test for invalid data, such as mismatched passwords
#         data = {
#             'username': 'newuser',
#             'first_name': 'New',
#             'last_name': 'User',
#             'email': 'newuser@example.com',
#             'password1': 'newpassword',
#             'password2': 'differentpassword',
#         }
#         form = UserRegistrationForm(data=data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('password2', form.errors)
#
#     def test_duplicate_email(self):
#         # Test for duplicate email address
#         existing_user = User.objects.create(username='existinguser', email='existing@example.com')
#         data = {
#             'username': 'newuser',
#             'first_name': 'New',
#             'last_name': 'User',
#             'email': 'existing@example.com',
#             'password1': 'newpassword',
#             'password2': 'newpassword',
#         }
#         form = UserRegistrationForm(data=data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('email', form.errors)
#
#     def test_duplicate_username(self):
#         # Test for duplicate username
#         existing_user = User.objects.create(username='existinguser', email='existing@example.com')
#         data = {
#             'username': 'existinguser',
#             'first_name': 'New',
#             'last_name': 'User',
#             'email': 'newuser@example.com',
#             'password1': 'newpassword',
#             'password2': 'newpassword',
#         }
#         form = UserRegistrationForm(data=data)
#         self.assertFalse(form.is_valid())
#         self.assertIn('username', form.errors)

class SortingFormTest(TestCase):
    def test_valid_sorting_form(self):
        data = {'sorting_option': 'price_low_high'}
        form = SortingForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_sorting_form(self):
        data = {'sorting_option': 'invalid_option'}
        form = SortingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('sorting_option', form.errors)

class BrandFormTest(TestCase):
    def test_valid_brand_form(self):
        brand1 = Brand.objects.create(name='Brand1')
        brand2 = Brand.objects.create(name='Brand2')
        data = {'brand_choices': [brand1.pk, brand2.pk]}
        form = BrandForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_brand_form(self):
        # Test for invalid brand choices
        data = {'brand_choices': [999, 888]}
        form = BrandForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('brand_choices', form.errors)