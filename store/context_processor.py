from category.models import Category

def menu_list(request):
    return {'categories':Category.objects.all()}