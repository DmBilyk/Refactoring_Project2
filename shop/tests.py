# python

from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from .models import Computer, Order
from .builder import ConcreteComputerBuilder
from .facade import ComputerShopFacade
from .views import (
    case_selection, processor_selection, memory_selection, storage_selection,
    graphics_selection, color_selection, peripherals_selection,
    device_type_selection, summary, order_success, my_orders, order_detail, index
)


class ComputerBuilderTests(TestCase):
    """Tests for the ConcreteComputerBuilder class."""

    def setUp(self):
        self.builder = ConcreteComputerBuilder()

    def test_builder_reset_method(self):
        """Check that reset method initializes a fresh computer dictionary."""
        self.builder.computer = {'test': 'value'}
        self.builder.reset()
        expected_computer = {
            'case_type': '', 'processor': '', 'memory': 0, 'storage': 0,
            'graphics_card': '', 'color': '', 'peripherals': [],
            'is_laptop': False, 'price': 0
        }
        self.assertEqual(self.builder.computer, expected_computer)

    def test_build_case_price_calculation(self):
        """Check that build_case adds price for a gaming case."""
        self.builder.build_case('Gaming')
        self.assertEqual(self.builder.computer['case_type'], 'Gaming')
        self.assertEqual(self.builder.computer['price'], 150)

    def test_install_processor_price_calculation(self):
        """Check that install_processor adds price for an i7 processor."""
        self.builder.install_processor('i7-12700K')
        self.assertEqual(self.builder.computer['processor'], 'i7-12700K')
        self.assertEqual(self.builder.computer['price'], 350)

    def test_install_memory_price_calculation(self):
        """Check that install_memory adds price for 16GB RAM."""
        self.builder.install_memory(16)
        self.assertEqual(self.builder.computer['memory'], 16)
        self.assertEqual(self.builder.computer['price'], 100)

    def test_apply_color_adds_fee(self):
        """Check that applying a color adds the standard fee."""
        self.builder.apply_color('Red')
        self.assertEqual(self.builder.computer['color'], 'Red')
        self.assertEqual(self.builder.computer['price'], 20)

    def test_add_peripherals_calculates_total_price(self):
        """Check that add_peripherals sums the price of peripheral items."""
        self.builder.add_peripherals(['monitor', 'keyboard', 'mouse'])
        self.assertEqual(self.builder.computer['peripherals'], ['monitor', 'keyboard', 'mouse'])
        self.assertEqual(self.builder.computer['price'], 280)

    def test_laptop_premium_price(self):
        """Check that setting is_laptop to True adds the laptop premium."""
        self.builder.set_device_type(True)
        self.assertTrue(self.builder.computer['is_laptop'])
        self.assertEqual(self.builder.computer['price'], 200)

    def test_calculate_price_adds_assembly_fee(self):
        """Check that calculate_price adds the assembly fee."""
        self.builder.calculate_price()
        self.assertEqual(self.builder.computer['price'], 50)

    def test_discount_for_high_memory_laptop(self):
        """
        Check that a laptop with 32GB memory and a monitor peripheral
        now receives the updated discount.
        """
        self.builder.computer['is_laptop'] = True
        self.builder.computer['memory'] = 32
        self.builder.computer['peripherals'] = ['monitor']
        self.builder.calculate_price()
        # Updated discount logic for laptops with 32 or more GB memory.
        self.assertEqual(self.builder.computer['price'], 0)

    def test_full_computer_build(self):
        """Check full configuration of a gaming desktop."""
        computer = (
            self.builder.build_case('Gaming')
                        .install_processor('i7-12700K')
                        .install_memory(16)
                        .install_storage(1024)
                        .install_graphics('RTX-3070')
                        .apply_color('Black')
                        .add_peripherals(['keyboard', 'mouse'])
                        .set_device_type(False)
                        .calculate_price()
                        .get_computer()
        )
        self.assertEqual(computer['case_type'], 'Gaming')
        self.assertEqual(computer['processor'], 'i7-12700K')
        self.assertEqual(computer['memory'], 16)
        self.assertEqual(computer['storage'], 1024)
        self.assertEqual(computer['graphics_card'], 'RTX-3070')
        self.assertEqual(computer['color'], 'Black')
        self.assertEqual(computer['peripherals'], ['keyboard', 'mouse'])
        self.assertFalse(computer['is_laptop'])
        self.assertEqual(computer['price'], 1470)


class ComputerShopFacadeTests(TestCase):
    """Tests for the ComputerShopFacade class."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    @patch('shop.singleton.DatabaseConnectionSingleton')
    @patch('shop.facade.Computer')
    def test_create_computer_saves_to_db(self, mock_computer, mock_singleton):
        """Check that create_computer saves the computer to the database."""
        mock_computer.return_value.save.return_value = None
        mock_instance = mock_computer.return_value
        result = ComputerShopFacade.create_computer(
            self.user, 'Gaming', 'i7-12700K', 16, 1024, 'RTX-3070', 'Black',
            ['keyboard', 'mouse'], False
        )
        self.assertEqual(result, mock_instance)
        mock_instance.save.assert_called_once()

    @patch('shop.singleton.DatabaseConnectionSingleton')
    @patch('shop.facade.Order.objects.create')
    def test_place_order_creates_order(self, mock_create, mock_singleton):
        """Check that place_order creates an order in the database."""
        computer = MagicMock()
        ComputerShopFacade.place_order(self.user, computer)
        mock_create.assert_called_once_with(user=self.user, computer=computer)

    @patch('shop.singleton.DatabaseConnectionSingleton')
    @patch('shop.facade.get_object_or_404')
    def test_get_computer_details_returns_formatted_dict(self, mock_get, mock_singleton):
        """Check that get_computer_details formats computer info correctly."""
        mock_computer = MagicMock()
        mock_computer.id = 1
        mock_computer.case_type = 'Gaming'
        mock_computer.processor = 'i7-12700K'
        mock_computer.memory = 16
        mock_computer.storage = 1024
        mock_computer.graphics_card = 'RTX-3070'
        mock_computer.color = 'Black'
        mock_computer.peripherals = 'keyboard, mouse'
        mock_computer.is_laptop = False
        mock_computer.price = 1470
        mock_get.return_value = mock_computer

        result = ComputerShopFacade.get_computer_details(1)
        expected = {
            'id': 1,
            'case_type': 'Gaming',
            'processor': 'i7-12700K',
            'memory': 16,
            'storage': 1024,
            'graphics_card': 'RTX-3070',
            'color': 'Black',
            'peripherals': ['keyboard', 'mouse'],
            'is_laptop': False,
            'price': 1470
        }
        self.assertEqual(result, expected)

    @patch('shop.singleton.DatabaseConnectionSingleton')
    @patch('shop.facade.Order.objects.filter')
    def test_get_user_orders_returns_filtered_queryset(self, mock_filter, mock_singleton):
        """Check that get_user_orders filters orders by user."""
        mock_queryset = MagicMock()
        mock_filter.return_value = mock_queryset
        mock_queryset.order_by.return_value = 'filtered_orders'
        result = ComputerShopFacade.get_user_orders(self.user)
        mock_filter.assert_called_once_with(user=self.user)
        mock_queryset.order_by.assert_called_once_with('-order_date')
        self.assertEqual(result, 'filtered_orders')


class ViewTests(TestCase):

    """Tests for view functions."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def _add_session_to_request(self, request):
        """Helper to add session to request."""
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()

    @patch('shop.singleton.DatabaseConnectionSingleton')
    @patch('shop.views.render')
    def test_index_view_renders_correct_template(self, mock_render, mock_singleton):
        """Check that index view renders the correct template."""
        request = self.factory.get('/')
        request.user = self.user
        index(request)
        mock_render.assert_called_once_with(request, 'shop/index.html')

    @patch('shop.singleton.DatabaseConnectionSingleton')
    @patch('shop.views.render')
    def test_case_selection_get_request(self, mock_render, mock_singleton):
        """Check that case_selection renders with form on GET request."""
        request = self.factory.get('/case-selection/')
        request.user = self.user
        self._add_session_to_request(request)
        case_selection(request)
        mock_render.assert_called_once()
        self.assertEqual(mock_render.call_args[0][1], 'shop/case_selection.html')
        self.assertIsNotNone(mock_render.call_args[0][2].get('form'))

    @patch('shop.singleton.DatabaseConnectionSingleton')
    @patch('shop.views.CaseSelectionForm')
    @patch('shop.views.redirect')
    def test_case_selection_post_valid_form(self, mock_redirect, mock_form, mock_singleton):
        """Check that case_selection redirects on valid POST."""
        mock_form_instance = MagicMock()
        mock_form_instance.is_valid.return_value = True
        mock_form_instance.cleaned_data = {'case_type': 'Gaming'}
        mock_form.return_value = mock_form_instance
        request = self.factory.post('/case-selection/')
        request.user = self.user
        self._add_session_to_request(request)
        case_selection(request)
        mock_redirect.assert_called_once_with('processor_selection')
        self.assertEqual(request.session['computer_builder'], {'case_type': 'Gaming'})

    @patch('shop.singleton.DatabaseConnectionSingleton')
    @patch('shop.views.ProcessorSelectionForm')
    @patch('shop.views.redirect')
    @patch('shop.views.messages')
    def test_processor_selection_without_case(self, mock_messages, mock_redirect, mock_form, mock_singleton):
        """Check processor_selection redirects if case is not selected."""
        request = self.factory.get('/processor-selection/')
        request.user = self.user
        self._add_session_to_request(request)
        request.session['computer_builder'] = {}
        processor_selection(request)
        mock_messages.error.assert_called_once()
        mock_redirect.assert_called_once_with('case_selection')

    @patch('shop.singleton.DatabaseConnectionSingleton')
    @patch('shop.views.get_object_or_404')
    @patch('shop.views.render')
    def test_order_detail_view(self, mock_render, mock_get, mock_singleton):
        """Check that order_detail retrieves the correct order and renders template."""
        request = self.factory.get('/order/1/')
        request.user = self.user
        mock_order = MagicMock()
        mock_get.return_value = mock_order
        with patch.object(ComputerShopFacade, 'get_computer_details', return_value='computer_details'):
            order_detail(request, 1)
            mock_get.assert_called_once_with(Order, id=1, user=self.user)
            mock_render.assert_called_once_with(
                request, 'shop/order_detail.html',
                {'order': mock_order, 'computer': 'computer_details'}
            )

    @patch('shop.views.ComputerShopFacade.get_computer_details')
    @patch('shop.views.Order.objects.filter')
    @patch('shop.singleton.DatabaseConnectionSingleton')
    def test_my_orders_view(self, mock_singleton, mock_filter, mock_get_computer_details):
        """Check that my_orders view returns enhanced order data."""
        request = self.factory.get('/my-orders/')
        request.user = self.user


        mock_order = MagicMock()
        mock_order.computer.id = 1


        mock_queryset = MagicMock()
        mock_filter.return_value = mock_queryset
        mock_queryset.order_by.return_value = [mock_order]


        mock_get_computer_details.return_value = {
            'name': 'Test Computer',
            'specs': 'Test Specs'
        }

        with patch('shop.views.render') as mock_render:
            my_orders(request)
            mock_render.assert_called_once()
            self.assertEqual(mock_render.call_args[0][1], 'shop/my_orders.html')
            enhanced_orders = mock_render.call_args[0][2]['enhanced_orders']
            self.assertEqual(len(enhanced_orders), 1)


if __name__ == "__main__":
    import unittest
    unittest.main()