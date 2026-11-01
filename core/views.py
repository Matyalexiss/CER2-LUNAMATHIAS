from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import LugarPatrimoniales, Categoria

def home(request):
    return render(request, 'core/home.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario= form.get_user()
            auth_login(request, usuario)
            return redirect('home')
    else:
        form = AuthenticationForm()
    data = {
        'form': form
    }
    return render(request, 'core/login.html', data)

def catalogo(request):
    categoria_id=request.GET.get('categoria_id')
    categorias=Categoria.objects.all()

    if categoria_id:
        lugares=LugarPatrimoniales.objects.filter(categoria_id=categoria_id)
    else:
        lugares=LugarPatrimoniales.objects.all()

    data = {
        'categorias': categorias,
        'lugares': lugares,
        'categoria_id': categoria_id
    }
    return render(request, 'core/catalogo.html', data)

def detalle_lugar(request, lugar_id):
    lugar = get_object_or_404(LugarPatrimoniales, id=lugar_id)
    data = {
        'lugar': lugar
    }
    return render(request, 'core/detalle_lugar.html', data)

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
@permission_required('core.add_lugarpatrimoniales', raise_exception=True)
def crear_lugar(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        LugarPatrimoniales.objects.create(
            id=request.POST.get('id'),
            nombre=request.POST.get('nombre'),
            descripcion=request.POST.get('descripcion'),
            ubicacion=request.POST.get('ubicacion'),
            anio_construccion=request.POST.get('anio_construccion'),
            imagen=request.POST.get('imagen'),
            categoria=get_object_or_404(Categoria, id=request.POST.get('categoria'))
        )
        return redirect('catalogo')
    
    data = {
        'categorias': categorias,
        'accion': 'Agregar'
    }
    return render(request, 'core/lugar_form.html', data)

@login_required
@permission_required('core.change_lugarpatrimoniales', raise_exception=True)
def editar_lugar(request, lugar_id):
    lugar = get_object_or_404(LugarPatrimoniales, id=lugar_id)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        lugar.nombre = request.POST.get('nombre')
        lugar.descripcion = request.POST.get('descripcion')
        lugar.ubicacion = request.POST.get('ubicacion')
        lugar.anio_construccion = request.POST.get('anio_construccion')
        lugar.imagen = request.POST.get('imagen')
        lugar.categoria = get_object_or_404(Categoria, id=request.POST.get('categoria'))
        lugar.save()
        return redirect('catalogo')

    data = {
        'lugar': lugar,
        'categorias': categorias,
        'accion': 'Editar'
    }
    return render(request, 'core/lugar_form.html', data)