from django.shortcuts import render, redirect
from .forms import AdopcionForm
from django.contrib import messages

def adoptar_perro(request):
    if request.method == 'POST':
        form = AdopcionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subido exitosamente')
            return redirect('confirmacion_adopcion')
        else:
            messages.error(request, 'Debe completar todos los campos')
    else:
        form = AdopcionForm()
        
    return render(request, 'adoptar_perro.html', {'form': form})