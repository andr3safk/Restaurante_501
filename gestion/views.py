from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from decimal import Decimal
from .forms import RegistroForm, ClienteForm, EmpleadoForm, MesaForm, PlatoForm, OrdenForm, FacturaForm, DetalleOrdenFormSet
from .forms import RegistroForm, ClienteForm

# Create your views here.
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura


@login_required
def inicio(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'total_mesas': Mesa.objects.count(),
        'total_platos': Plato.objects.count(),
        'total_ordenes': Orden.objects.count(),
        'total_facturas': Factura.objects.count(),
    }
    return render(request, 'gestion/inicio.html', context)


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegistroForm()
    return render(request, 'gestion/registro.html', {'form': form})


@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'gestion/clientes.html', {'clientes': clientes})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/clientes/')
    else:
        form = ClienteForm()
    return render(request, 'gestion/crear_cliente.html', {'form': form})

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('/clientes/')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'gestion/editar_cliente.html', {'form': form})

@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('/clientes/')


@login_required
def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'gestion/empleados.html', {'empleados': empleados})

@login_required
def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/empleados/')
    else:
        form = EmpleadoForm()
    return render(request, 'gestion/crear_empleado.html', {'form': form})

@login_required
def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('/empleados/')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'gestion/editar_empleado.html', {'form': form})

@login_required
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('/empleados/')
    return render(request, 'gestion/eliminar_empleado.html', {'empleado': empleado})


@login_required
def lista_mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'gestion/mesas.html', {'mesas': mesas})

@login_required
def crear_mesa(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/mesas/')
    else:
        form = MesaForm()
    return render(request, 'gestion/crear_mesa.html', {'form': form})

@login_required
def editar_mesa(request, id):
    mesa = get_object_or_404(Mesa, id=id)
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            return redirect('/mesas/')
    else:
        form = MesaForm(instance=mesa)
    return render(request, 'gestion/editar_mesa.html', {'form': form})

@login_required
def eliminar_mesa(request, id):
    mesa = get_object_or_404(Mesa, id=id)
    if request.method == 'POST':
        mesa.delete()
        return redirect('/mesas/')
    return render(request, 'gestion/eliminar_mesa.html', {'mesa': mesa})


@login_required
def lista_platos(request):
    platos = Plato.objects.all()
    return render(request, 'gestion/platos.html', {'platos': platos})

@login_required
def crear_plato(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/platos/')
    else:
        form = PlatoForm()
    return render(request, 'gestion/crear_plato.html', {'form': form})

@login_required
def editar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == 'POST':
        form = PlatoForm(request.POST, instance=plato)
        if form.is_valid():
            form.save()
            return redirect('/platos/')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'gestion/editar_plato.html', {'form': form})

@login_required
def eliminar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == 'POST':
        plato.delete()
        return redirect('/platos/')
    return render(request, 'gestion/eliminar_plato.html', {'plato': plato})


@login_required
def lista_ordenes(request):
    ordenes = Orden.objects.all()
    return render(request, 'gestion/ordenes.html', {'ordenes': ordenes})

@login_required
def crear_orden(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        formset = DetalleOrdenFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            orden = form.save()
            formset.instance = orden
            formset.save()
            orden.update_total()
            orden.mesa.estado_mesa = 'Ocupada'
            orden.mesa.save()
            return redirect('/ordenes/')
    else:
        form = OrdenForm()
        formset = DetalleOrdenFormSet()
    return render(request, 'gestion/crear_orden.html', {'form': form, 'formset': formset})

@login_required
def editar_orden(request, id):
    orden = get_object_or_404(Orden, id=id)
    if hasattr(orden, 'factura'):
        messages.error(request, 'Esta orden ya fue facturada y no se puede editar.')
        return redirect('/ordenes/')
    if request.method == 'POST':
        form = OrdenForm(request.POST, instance=orden)
        formset = DetalleOrdenFormSet(request.POST, instance=orden)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            orden.update_total()
            return redirect('/ordenes/')
    else:
        form = OrdenForm(instance=orden)
        formset = DetalleOrdenFormSet(instance=orden)
    return render(request, 'gestion/editar_orden.html', {'form': form, 'formset': formset})

@login_required
def eliminar_orden(request, id):
    orden = get_object_or_404(Orden, id=id)
    if request.method == 'POST':
        orden.mesa.estado_mesa = 'Disponible'
        orden.mesa.save()
        orden.delete()
        return redirect('/ordenes/')
    return render(request, 'gestion/eliminar_orden.html', {'orden': orden})


@login_required
def lista_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'gestion/facturas.html', {'facturas': facturas})

@login_required
def crear_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            orden = factura.orden
            orden.update_total()
            subtotal = orden.total
            if subtotal == 0:
                subtotal = Decimal('0.00')
            impuesto = (subtotal * Decimal('0.19')).quantize(Decimal('0.01'))
            total_factura = (subtotal + impuesto).quantize(Decimal('0.01'))
            factura.subtotal = subtotal
            factura.impuesto = impuesto
            factura.total_factura = total_factura
            factura.save()
            orden.estado_orden = 'Facturada'
            orden.save()
            orden.mesa.estado_mesa = 'Disponible'
            orden.mesa.save()
            return redirect('/facturas/')
    else:
        form = FacturaForm()
    return render(request, 'gestion/crear_factura.html', {'form': form})

@login_required
def editar_factura(request, id):
    messages.error(request, 'Las facturas no se pueden editar.')
    return redirect('/facturas/')

@login_required
def eliminar_factura(request, id):
    messages.error(request, 'Las facturas no se pueden eliminar.')
    return redirect('/facturas/')
def registro(request):

    if request.method == 'POST':

        form = RegistroForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('/')

    else:

        form = RegistroForm()

    return render(request, 'gestion/registro.html', {
        'form': form
    })

@login_required
def crear_cliente(request):

    if request.method == 'POST':

        form = ClienteForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/clientes/')

    else:

        form = ClienteForm()

    return render(request, 'gestion/crear_cliente.html', {
        'form': form
    })

@login_required
def editar_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':

        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():

            form.save()

            return redirect('/clientes/')

    else:

        form = ClienteForm(instance=cliente)

    return render(request, 'gestion/editar_cliente.html', {
        'form': form
    })

@login_required
def eliminar_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    cliente.delete()

    return redirect('/clientes/')
