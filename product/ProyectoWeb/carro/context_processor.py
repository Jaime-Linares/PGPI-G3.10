# Esta clase se encarga de agregar al contexto de la aplicación los datos del carro de compras

def importe_total_carro(request):
    total = 0
    if request.user.is_authenticated:
        for key, value in request.session['carro'].items():
            total += float(value['precio'])
    else:
        total = "Debes hacer login"
    return {'importe_total_carro': total}