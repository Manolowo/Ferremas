from django.http import HttpResponse
from .models import Pedido, Factura
from django.template.loader import render_to_string
from weasyprint import HTML

def generar_factura(request, pedido_id):
    try:
        pedido = Pedido.objects.get(ped_id=pedido_id)
    except Pedido.DoesNotExist:
        return HttpResponse('Pedido no encontrado', status=404)

    cliente = pedido.cliente

    html_string = render_to_string('cliente/factura.html', {'pedido': pedido, 'cliente': cliente})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="factura_{pedido_id}.pdf"'

    return response

def generar_factura_local(request, fac_id):
    try:
        factura = Factura.objects.get(fac_id=fac_id)
    except Pedido.DoesNotExist:
        return HttpResponse('Factura no encontrada', status=404)

    empleado = Factura.vendedor

    html_string = render_to_string('empleado/factura.html', {'factura': factura, 'vendedor': empleado})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="factura_{fac_id}.pdf"'

    return response