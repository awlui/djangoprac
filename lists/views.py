from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request, list_id):
    try:
        list_ = List.objects.get(id=list_id)
    except ObjectDoesNotExist as ex:
        return HttpResponse("Returned not 500")

    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect('/lists/%d/' % (list_.id,))
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'lists/lists.html', {'list': list_, 'error': error})

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'lists/home.html', {"error": error})
    return redirect('/lists/%d/' % (list_.id))

