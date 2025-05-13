from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (CaseSelectionForm, ProcessorSelectionForm, MemorySelectionForm,
                    StorageSelectionForm, GraphicsSelectionForm, ColorSelectionForm,
                    PeripheralsSelectionForm, DeviceTypeSelectionForm)
from .facade import ComputerShopFacade
from .models import Order
from .builder import ConcreteComputerBuilder
from .utils.db import get_db_connection
from django.views.decorators.http import require_safe
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def check_computer_builder_session(request, key, redirect_url='case_selection'):
    """
    Checks if a specific key exists in the 'computer_builder' session data.
    If the key is missing, redirects the user to the specified URL with an error message.


    """
    get_db_connection()
    if key not in request.session.get('computer_builder', {}):
        messages.error(request, "Please start from the beginning")
        return redirect(redirect_url)
    return None

@require_safe
@login_required
def index(request):
    """
    Renders the index page of the shop.


    """
    return render(request, 'shop/index.html')

@require_http_methods(["GET", "POST"])
@login_required
def case_selection(request):
    """
    Handles the case selection step in the computer building process.
    Displays a form for selecting the case type and saves the selection to the session.


    """
    get_db_connection()
    form = CaseSelectionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        request.session['computer_builder'] = {'case_type': form.cleaned_data['case_type']}
        return redirect('processor_selection')
    return render(request, 'shop/case_selection.html', {'form': form})

@require_safe
@login_required
def processor_selection(request):
    """
    Handles the processor selection step in the computer building process.
    Displays a form for selecting the processor and saves the selection to the session.


    """
    result = check_computer_builder_session(request, 'case_type')
    if result:
        return result

    form = ProcessorSelectionForm(request.POST or None)
    if form.is_valid():
        request.session['computer_builder']['processor'] = form.cleaned_data['processor']
        request.session.modified = True
        return redirect('memory_selection')
    return render(request, 'shop/processor_selection.html', {'form': form})

@require_safe
@login_required
def memory_selection(request):
    """
    Handles the memory selection step in the computer building process.
    Displays a form for selecting the memory size and saves the selection to the session.


    """
    result = check_computer_builder_session(request, 'case_type')
    if result:
        return result

    form = MemorySelectionForm(request.POST or None)
    if form.is_valid():
        memory = form.cleaned_data['memory']
        request.session['computer_builder']['memory'] = int(memory)
        request.session.modified = True
        return redirect('storage_selection')
    return render(request, 'shop/memory_selection.html', {'form': form})

@require_safe
@login_required
def storage_selection(request):
    """
    Handles the storage selection step in the computer building process.
    Displays a form for selecting the storage size and saves the selection to the session.


    """
    result = check_computer_builder_session(request, 'case_type')
    if result:
        return result

    form = StorageSelectionForm(request.POST or None)
    if form.is_valid():
        storage = form.cleaned_data['storage']
        request.session['computer_builder']['storage'] = int(storage)
        request.session.modified = True
        return redirect('graphics_selection')
    return render(request, 'shop/storage_selection.html', {'form': form})

@require_safe
@login_required
def graphics_selection(request):
    """
    Handles the graphics card selection step in the computer building process.
    Displays a form for selecting the graphics card and saves the selection to the session.


    """
    result = check_computer_builder_session(request, 'case_type')
    if result:
        return result

    form = GraphicsSelectionForm(request.POST or None)
    if form.is_valid():
        request.session['computer_builder']['graphics_card'] = form.cleaned_data['graphics_card']
        request.session.modified = True
        return redirect('color_selection')
    return render(request, 'shop/graphics_selection.html', {'form': form})

@require_safe
@login_required
def color_selection(request):
    """
    Handles the color selection step in the computer building process.
    Displays a form for selecting the color and saves the selection to the session.

    """
    result = check_computer_builder_session(request, 'case_type')
    if result:
        return result

    form = ColorSelectionForm(request.POST or None)
    if form.is_valid():
        request.session['computer_builder']['color'] = form.cleaned_data['color']
        request.session.modified = True
        return redirect('peripherals_selection')
    return render(request, 'shop/color_selection.html', {'form': form})

@require_safe
@login_required
def peripherals_selection(request):
    """
    Handles the peripherals selection step in the computer building process.
    Displays a form for selecting peripherals and saves the selection to the session.

    """
    result = check_computer_builder_session(request, 'case_type')
    if result:
        return result

    form = PeripheralsSelectionForm(request.POST or None)
    if form.is_valid():
        peripherals = [key for key, value in form.cleaned_data.items() if value]
        request.session['computer_builder']['peripherals'] = peripherals
        request.session.modified = True
        return redirect('device_type_selection')
    return render(request, 'shop/peripherals_selection.html', {'form': form})

@require_safe
@login_required
def device_type_selection(request):
    """
    Handles the device type selection step in the computer building process.
    Displays a form for selecting the device type (laptop or desktop) and saves the selection to the session.

    """
    result = check_computer_builder_session(request, 'case_type')
    if result:
        return result

    form = DeviceTypeSelectionForm(request.POST or None)
    if form.is_valid():
        request.session['computer_builder']['is_laptop'] = form.cleaned_data['is_laptop']
        request.session.modified = True
        return redirect('summary')
    return render(request, 'shop/device_type_selection.html', {'form': form})

@require_safe
@login_required
def summary(request):
    """
    Displays a summary of the computer configuration and allows the user to place an order.
    If the user submits the form, creates a computer and places an order.

    """
    result = check_computer_builder_session(request, 'case_type')
    if result:
        return result

    if request.method == 'POST':
        computer = ComputerShopFacade.create_computer(request.user, **request.session['computer_builder'])
        order = ComputerShopFacade.place_order(request.user, computer)
        del request.session['computer_builder']
        return redirect('order_success', order_id=order.id)

    builder = ConcreteComputerBuilder()
    config = request.session['computer_builder']

    try:
        memory = int(config['memory'])
        storage = int(config['storage'])
    except ValueError:
        memory = 8
        storage = 512

    computer_preview = (builder.build_case(config['case_type'])
                        .install_processor(config['processor'])
                        .install_memory(memory)
                        .install_storage(storage)
                        .install_graphics(config['graphics_card'])
                        .apply_color(config['color'])
                        .add_peripherals(config['peripherals'])
                        .set_device_type(config['is_laptop'])
                        .calculate_price()
                        .get_computer())

    context = config.copy()
    context['estimated_price'] = computer_preview['price']

    return render(request, 'shop/summary.html', context)

@require_safe
@login_required
def order_success(request, order_id):
    """
    Displays the order success page with details of the placed order.


    """
    get_db_connection()
    order = get_object_or_404(Order, id=order_id, user=request.user)
    computer_details = ComputerShopFacade.get_computer_details(order.computer.id)
    return render(request, 'shop/order_success.html', {'order': order, 'computer': computer_details})

@require_safe
@login_required
def my_orders(request):
    """
    Displays a list of the user's orders with enhanced computer details.

    """
    get_db_connection()
    orders = ComputerShopFacade.get_user_orders(request.user)

    enhanced_orders = []
    for order in orders:
        computer_details = ComputerShopFacade.get_computer_details(order.computer.id)
        enhanced_orders.append({
            'order': order,
            'computer': computer_details
        })

    return render(request, 'shop/my_orders.html', {'enhanced_orders': enhanced_orders})

@require_safe
@login_required
def order_detail(request, order_id):
    """
    Displays the details of a specific order.
    """
    get_db_connection()
    order = get_object_or_404(Order, id=order_id, user=request.user)
    computer_details = ComputerShopFacade.get_computer_details(order.computer.id)
    return render(request, 'shop/order_detail.html', {'order': order, 'computer': computer_details})