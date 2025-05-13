from django.shortcuts import get_object_or_404
from .models import Computer, Order
from .builder import ConcreteComputerBuilder


class ComputerShopFacade:
    """
    Facade pattern implementation that simplifies the complex computer configuration
    and ordering process for clients.
    """

    @staticmethod
    def create_computer(user, case_type, processor, memory, storage, graphics_card, color, peripherals, is_laptop):
        """
        Create and save a new computer configuration based on specifications.
        """


        memory = ComputerShopFacade._safe_cast_to_int(memory, default=8)
        storage = ComputerShopFacade._safe_cast_to_int(storage, default=512)
        peripherals = ComputerShopFacade._normalize_peripherals(peripherals)

        builder = ConcreteComputerBuilder()
        computer_details = (
            builder.build_case(case_type)
                   .install_processor(processor)
                   .install_memory(memory)
                   .install_storage(storage)
                   .install_graphics(graphics_card)
                   .apply_color(color)
                   .add_peripherals(peripherals)
                   .set_device_type(is_laptop)
                   .calculate_price()
                   .get_computer()
        )


        computer = Computer(
            **{
                'case_type': computer_details['case_type'],
                'processor': computer_details['processor'],
                'memory': computer_details['memory'],
                'storage': computer_details['storage'],
                'graphics_card': computer_details['graphics_card'],
                'color': computer_details['color'],
                'peripherals': ', '.join(computer_details['peripherals']),
                'is_laptop': computer_details['is_laptop'],
                'price': computer_details['price'],
                'owner': user
            }
        )
        computer.save()
        return computer

    @staticmethod
    def place_order(user, computer):
        """
        Create a new order for the specified computer.
        """
        return Order.objects.create(user=user, computer=computer)

    @staticmethod
    def get_computer_details(computer_id):
        """
        Retrieve detailed information about a specific computer.
        """
        computer = get_object_or_404(Computer, id=computer_id)
        return {
            'id': computer.id,
            'case_type': computer.case_type,
            'processor': computer.processor,
            'memory': computer.memory,
            'storage': computer.storage,
            'graphics_card': computer.graphics_card,
            'color': computer.color,
            'peripherals': computer.peripherals.split(', ') if computer.peripherals else [],
            'is_laptop': computer.is_laptop,
            'price': computer.price,
        }

    @staticmethod
    def get_user_orders(user):
        """
        Retrieve all orders placed by a specific user.
        """
        return Order.objects.filter(user=user).order_by('-order_date')



    @staticmethod
    def _safe_cast_to_int(value, default):
        """
        Try casting value to int; return default on failure.
        """
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _normalize_peripherals(peripherals):
        """
        Ensure peripherals is a list.
        """
        if isinstance(peripherals, str):
            return [peripherals]
        return peripherals if isinstance(peripherals, list) else []
