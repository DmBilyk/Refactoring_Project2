from django import forms


class CaseSelectionForm(forms.Form):
    """
    Form for selecting the computer case or laptop form factor.
    """
    CASE_CHOICES = [
        ('Tower', 'Tower Desktop'),
        ('Mini', 'Mini Desktop'),
        ('Slim', 'Slim Desktop'),
        ('Gaming', 'Gaming Desktop'),
    ]

    case_type = forms.ChoiceField(choices=CASE_CHOICES, widget=forms.RadioSelect)


class ProcessorSelectionForm(forms.Form):
    """
    Form for selecting the processor type.
    """
    PROCESSOR_CHOICES = [
        ('i5-12400', 'Intel Core i5-12400'),
        ('i7-12700K', 'Intel Core i7-12700K'),
        ('i9-12900K', 'Intel Core i9-12900K'),
        ('Ryzen-5-5600X', 'AMD Ryzen 5 5600X'),
        ('Ryzen-7-5800X', 'AMD Ryzen 7 5800X'),
    ]

    processor = forms.ChoiceField(choices=PROCESSOR_CHOICES, widget=forms.RadioSelect)


class MemorySelectionForm(forms.Form):
    """
    Form for selecting the amount of RAM.
    """
    MEMORY_CHOICES = [
        ('8', '8GB'),
        ('16', '16GB'),
        ('32', '32GB'),
        ('64', '64GB'),
    ]

    memory = forms.ChoiceField(choices=MEMORY_CHOICES, widget=forms.RadioSelect)


class StorageSelectionForm(forms.Form):
    """
    Form for selecting the storage capacity.
    """
    STORAGE_CHOICES = [
        ('512', '512GB SSD'),
        ('1024', '1TB SSD'),
        ('2048', '2TB SSD'),
    ]

    storage = forms.ChoiceField(choices=STORAGE_CHOICES, widget=forms.RadioSelect)


class GraphicsSelectionForm(forms.Form):
    """
    Form for selecting the graphics card.
    """
    GRAPHICS_CHOICES = [
        ('Integrated', 'Integrated Graphics'),
        ('RTX-3060', 'NVIDIA RTX 3060'),
        ('RTX-3070', 'NVIDIA RTX 3070'),
        ('RTX-3080', 'NVIDIA RTX 3080'),
        ('RX-6700XT', 'AMD RX 6700XT'),
    ]

    graphics_card = forms.ChoiceField(choices=GRAPHICS_CHOICES, widget=forms.RadioSelect)


class ColorSelectionForm(forms.Form):
    """
    Form for selecting the computer color.
    """
    COLOR_CHOICES = [
        ('Black', 'Midnight Black'),
        ('White', 'Arctic White'),
        ('Silver', 'Metallic Silver'),
        ('Blue', 'Royal Blue'),
        ('Red', 'Racing Red'),
    ]

    color = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.RadioSelect)


class PeripheralsSelectionForm(forms.Form):
    """
    Form for selecting additional peripherals.
    """
    monitor = forms.BooleanField(required=False)
    keyboard = forms.BooleanField(required=False)
    mouse = forms.BooleanField(required=False)
    headset = forms.BooleanField(required=False)
    webcam = forms.BooleanField(required=False)


class DeviceTypeSelectionForm(forms.Form):
    """
    Form for selecting between laptop and desktop.
    """
    is_laptop = forms.BooleanField(required=False, label="Make it a Laptop")
