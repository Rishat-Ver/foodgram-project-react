import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def download_shopping_cart(request):
    # Создайте файлообразный буфер для приема PDF-данных.
    buffer = io.BytesIO()

    # Создайте объект PDF, используя буфер в качестве его "файла".
    p = canvas.Canvas(buffer)

    # Нарисуйте что-нибудь в формате PDF. Вот где происходит генерация PDF-файла.
    # Полный список функциональных возможностей приведен в документации ReportLab.
    p.drawString(100, 100, "Привет Ришат")

    # Аккуратно закройте PDF-объект, и все готово.
    p.showPage()
    p.save()

    # Файловый ответ устанавливает заголовок Content-Disposition таким образом, чтобы браузеры
    # предоставьте возможность сохранить файл.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')










from django.db.models.aggregates import Sum
from django.http import HttpResponse

from api.serializers import RecipeIngredients


def download_shopping_cart(self, request):
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