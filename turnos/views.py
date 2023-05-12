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
            turno = form.save(commit=False)
            turno.cliente = request.user.cliente
            turno.estado_id = 3
            turno.save()
            messages.success(request, 'Turno solicitado correctamente')
            return redirect('solicitar_turno')
    else:
        form = SolicitarTurnoForm()
    return render(request, 'solicitar_turno.html', {'form': form})
