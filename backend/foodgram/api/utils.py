from django.db.models.aggregates import Sum
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from api.serializers import RecipeIngredients


def download_cart(request):
    ingredients = RecipeIngredients.objects.filter(
        recipe__cart__user=request.user).values_list(
        'ingredient__name', 'ingredient__measurement_unit',
        'amount')
    cart_list = {}
    for item in ingredients:
        name = item[0]
        if name not in cart_list:
            cart_list[name] = {
                'measurement_unit': item[1],
                'amount': item[2]
            }
        else:
            cart_list[name]['amount'] += item[2]
    height = 700
    buffer = BytesIO()
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))
    page = canvas.Canvas(buffer)
    page.setFont('DejaVuSerif', 13)
    page.drawString(100, 750, "Список покупок")
    for i, (name, data) in enumerate(cart_list.items(), start=1):
        page.drawString(
            80, height, f"{i}. {name} – {data['amount']} {data['unit']}"
        )
        height -= 25
    page.showPage()
    page.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='shopping_list.pdf')


""" def download_cart(self, request):
    ingredients = RecipeIngredients.objects.filter(
        recipe__shopping__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
                amount=Sum('amount'))
    text = ''
    for ingredient in ingredients:
        text += (f'•  {ingredient["ingredient__name"]}'
                 f'({ingredient["ingredient__measurement_unit"]})'
                 f'— {ingredient["amount"]}\n')
    headers = {
        'Content-Disposition': 'attchment; filename=shoping_cart.txt'}
    return HttpResponse(
        text, content_type='text/plain; charset=UTF-8', headers=headers) """
