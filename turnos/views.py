from django.shortcuts import render
from .forms import *
from django.utils.timezone import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def solicitar_turno(request):
    if request.method == 'POST':
        form =SolicitarTurnoForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.user = request.user
            turno.estado = 'pendiente'       
            turno.save()                 
            return redirect('ver_turnos')
    else:
        form = SolicitarTurnoForm(initial={'fecha': datetime.now()})
    return render(request, 'solicitar_turno.html', {'form': form})
