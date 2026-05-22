from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura, DetalleOrden
from django import forms
from django.forms import inlineformset_factory


class RegistroForm(UserCreationForm):
    email = forms.EmailField(help_text='')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, help_text='')
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, help_text='')
    username = forms.CharField(help_text='')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ClienteForm(forms.ModelForm):
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-estilo',
            'pattern': '[0-9]+',
            'title': 'Solo se permiten números',
            'inputmode': 'numeric'
        })
    )

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-estilo'}),
            'correo': forms.EmailInput(attrs={'class': 'input-estilo'}),
        }


class EmpleadoForm(forms.ModelForm):
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-estilo',
            'pattern': '[0-9]+',
            'title': 'Solo se permiten números',
            'inputmode': 'numeric'
        })
    )

    class Meta:
        model = Empleado
        fields = ['nombre', 'cargo', 'telefono', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-estilo'}),
            'cargo': forms.Select(attrs={'class': 'input-estilo'}),
            'correo': forms.EmailInput(attrs={'class': 'input-estilo'}),
        }


class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero_mesa', 'capacidad', 'estado_mesa']
        widgets = {
            'numero_mesa': forms.NumberInput(attrs={'class': 'input-estilo'}),
            'capacidad': forms.NumberInput(attrs={'class': 'input-estilo'}),
            'estado_mesa': forms.Select(attrs={'class': 'input-estilo'}),
        }


class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre_plato', 'descripcion', 'precio', 'categoria', 'disponible']
        widgets = {
            'nombre_plato': forms.TextInput(attrs={'class': 'input-estilo'}),
            'descripcion': forms.Textarea(attrs={'class': 'input-estilo', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'input-estilo'}),
            'categoria': forms.TextInput(attrs={'class': 'input-estilo'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'checkbox-estilo'}),
        }


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['cliente', 'empleado', 'mesa', 'estado_orden']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'input-estilo'}),
            'empleado': forms.Select(attrs={'class': 'input-estilo'}),
            'mesa': forms.Select(attrs={'class': 'input-estilo'}),
            'estado_orden': forms.Select(attrs={'class': 'input-estilo'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['mesa'].queryset = Mesa.objects.filter(estado_mesa='Disponible')

    def clean_mesa(self):
        mesa = self.cleaned_data.get('mesa')
        if mesa and mesa.estado_mesa == 'Ocupada':
            if self.instance.pk and self.instance.mesa == mesa:
                return mesa
            raise forms.ValidationError('Esta mesa ya está ocupada.')
        return mesa

class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['plato', 'cantidad']
        widgets = {
            'plato': forms.Select(attrs={'class': 'input-estilo'}),
            'cantidad': forms.NumberInput(attrs={'class': 'input-estilo', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plato'].queryset = Plato.objects.filter(disponible=True)

DetalleOrdenFormSet = inlineformset_factory(
    Orden,
    DetalleOrden,
    form=DetalleOrdenForm,
    extra=1,
    can_delete=True,
)


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['orden', 'metodo_pago']
        widgets = {
            'orden': forms.Select(attrs={'class': 'input-estilo'}),
            'metodo_pago': forms.Select(attrs={'class': 'input-estilo'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['orden'].queryset = Orden.objects.filter(factura__isnull=True)