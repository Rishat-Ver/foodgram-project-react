from django.db.models.aggregates import Sum
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO

from api.serializers import RecipeIngredients


""" def download_cart(self, request):
    ingredients = RecipeIngredients.objects.filter(
        recipe__cart__user=request.user).values_list(
        'ingredient__name', 'ingredient__measurement_unit',
        'amount')
    cart_list = {}
    for name, amount, unit in ingredients:
        if name not in cart_list:
            cart_list[name] = {"amount": amount, "unit": unit}
        else:
            cart_list[name]["amount"] += amount
    height = 700
    buffer = BytesIO()

    page = canvas.Canvas(buffer)

    page.drawString(100, 750, "Список покупок")
    for i, (name, data) in enumerate(cart_list.items(), start=1):
        page.drawString(
            80, height, f"{i}. {name} – {data['amount']} {data['unit']}"
        )
        height -= 25
    page.showPage()
    page.save()
    buffer.seek(0)
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="shopping_list.pdf"')
    return response """


def download_cart(self, request):
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
        text, content_type='text/plain; charset=UTF-8', headers=headers)
