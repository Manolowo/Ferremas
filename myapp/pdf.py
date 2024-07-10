from django.http import HttpResponse
from .models import Pedido
from django.template.loader import render_to_string
from weasyprint import HTML

def generar_factura(request, pedido_id):
    try:
        pedido = Pedido.objects.get(ped_id=pedido_id)
    except Pedido.DoesNotExist:
        return HttpResponse('Pedido no encontrado', status=404)

    html_string = render_to_string('cliente/factura.html', {'pedido': pedido})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="factura_{pedido_id}.pdf"'

    return response