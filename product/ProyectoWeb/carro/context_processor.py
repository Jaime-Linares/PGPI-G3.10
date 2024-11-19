def importe_total_carro(request):
    total = 0
    if request.user.is_authenticated and "reserva" in request.session.get("carro", {}):
        total = float(request.session['carro']['reserva']['precio_total'])
    return {'importe_total_carro': total}
