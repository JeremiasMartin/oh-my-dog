from django.shortcuts import render
from .forms import *
from django.utils.timezone import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required
def solicitar_turno(request):
    if request.method == 'POST':
        form = SolicitarTurnoForm(request.POST)
        if form.is_valid():
            cliente = request.user.cliente
            turno = form.save(commit=False)
            turno.cliente = cliente
            turno.estado_id = 3
            if Turno.objects.filter(cliente=cliente, fecha=form.cleaned_data['fecha']).exists():
                messages.error(request, 'Ya tiene un turno asignado para la fecha seleccionada.')
                return redirect('solicitar_turno')
            
            turno.save()

            messages.success(request, 'Turno solicitado correctamente.')
            return redirect('solicitar_turno')
    else:
        form = SolicitarTurnoForm()
    return render(request, 'solicitar_turno.html', {'form': form})
