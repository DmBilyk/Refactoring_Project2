from abc import ABC, abstractmethod


class ComputerBuilder(ABC):
    """
    Abstract builder class for computer configuration.
    """
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def build_case(self, case_type):
        pass

    @abstractmethod
    def install_processor(self, processor):
        pass

    @abstractmethod
    def install_memory(self, memory):
        pass

    @abstractmethod
    def install_storage(self, storage):
        pass

    @abstractmethod
    def install_graphics(self, graphics_card):
        pass

    @abstractmethod
    def apply_color(self, color):
        pass

    @abstractmethod
    def add_peripherals(self, peripherals):
        pass

    @abstractmethod
    def set_device_type(self, is_laptop):
        pass

    @abstractmethod
    def calculate_price(self):
        pass

    @abstractmethod
    def get_computer(self):
        pass


class ConcreteComputerBuilder(ComputerBuilder):
    """
    Concrete implementation of computer builder pattern.
    Handles the step-by-step construction of computer configurations.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        """
        Reset builder state to start fresh.
        """
        self.computer = {
            'case_type': '', 'processor': '', 'memory': 0, 'storage': 0,
            'graphics_card': '', 'color': '', 'peripherals': [],
            'is_laptop': False, 'price': 0
        }

    def build_case(self, case_type):
        """
        Configure the computer case or laptop form factor.
        """
        self.computer['case_type'] = case_type
        prices = {'Tower': 100, 'Mini': 80, 'Slim': 90, 'Gaming': 150}
        self.computer['price'] += prices.get(case_type, 0)
        return self

    def install_processor(self, processor):
        """
        Install a processor in the computer.
        """
        self.computer['processor'] = processor
        prices = {
            'i5-12400': 200, 'i7-12700K': 350, 'i9-12900K': 550,
            'Ryzen-5-5600X': 220, 'Ryzen-7-5800X': 320
        }
        self.computer['price'] += prices.get(processor, 0)
        return self

    def install_memory(self, memory):
        """
        Install RAM in the computer.
        """
        self.computer['memory'] = memory
        prices = {8: 50, 16: 100, 32: 180, 64: 320}
        self.computer['price'] += prices.get(memory, 0)
        return self

    def install_storage(self, storage):
        """
        Install storage in the computer.
        """
        self.computer['storage'] = storage
        prices = {512: 70, 1024: 120, 2048: 220}
        self.computer['price'] += prices.get(storage, 0)
        return self

    def install_graphics(self, graphics_card):
        """
        Install a graphics card in the computer.
        """
        self.computer['graphics_card'] = graphics_card
        prices = {'Integrated': 0, 'RTX-3060': 400, 'RTX-3070': 600,
                  'RTX-3080': 800, 'RX-6700XT': 450}
        self.computer['price'] += prices.get(graphics_card, 0)
        return self

    def apply_color(self, color):
        """
        Apply color to the computer case.
        """
        self.computer['color'] = color
        self.computer['price'] += 20  # Small price for color customization
        return self

    def add_peripherals(self, peripherals):
        """
        Add selected peripherals to the order.
        """
        self.computer['peripherals'] = peripherals
        prices = {'monitor': 200, 'keyboard': 50, 'mouse': 30, 'headset': 70, 'webcam': 40}
        self.computer['price'] += sum(prices.get(acc, 0) for acc in peripherals)
        return self

    def set_device_type(self, is_laptop):
        """
        Set whether the computer is a laptop or desktop.
        """
        self.computer['is_laptop'] = is_laptop
        if is_laptop:
            self.computer['price'] += 200  # Premium for laptop form factor
        return self

    def calculate_price(self):
        """
        Calculate the final price of the computer.
        """

        assembly_fee = 50
        self.computer['price'] += assembly_fee


        if self.computer['is_laptop'] and self.computer['memory'] >= 16 and 'monitor' in self.computer['peripherals']:

            discount = 50
            self.computer['price'] -= discount

        return self

    def get_computer(self):
        """
        Return the fully configured computer.
        """
        return self.computer


class ComputerDirector:
    """
    Director class that knows how to use a builder to create specific computer configurations.
    """
    def __init__(self, builder: ComputerBuilder = None):
        self.builder = builder if builder else ConcreteComputerBuilder()

    def change_builder(self, builder: ComputerBuilder):
        """
        Change the builder instance.
        """
        self.builder = builder

    def make_gaming_desktop(self, processor, memory, storage, graphics_card, color, peripherals):
        """
        Create a pre-configured gaming desktop.
        """
        self.builder.reset()
        return (self.builder.build_case('Gaming')
                .install_processor(processor)
                .install_memory(memory)
                .install_storage(storage)
                .install_graphics(graphics_card)
                .apply_color(color)
                .add_peripherals(peripherals)
                .set_device_type(False)
                .calculate_price()
                .get_computer())

    def make_business_laptop(self, processor, memory, storage, color, peripherals):
        """
        Create a pre-configured business laptop.
        """
        self.builder.reset()
        return (self.builder.build_case('Slim')
                .install_processor(processor)
                .install_memory(memory)
                .install_storage(storage)
                .install_graphics('Integrated')
                .apply_color(color)
                .add_peripherals(peripherals)
                .set_device_type(True)
                .calculate_price()
                .get_computer())
