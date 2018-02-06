from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse
from lists.forms import ItemForm, EMPTY_LIST_ERROR, ExistingListItemForm
# Create your views here.

def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    try:
        list_ = List.objects.get(id=list_id)
    except ObjectDoesNotExist as ex:
        return HttpResponse("List Doesn't Exists!")
    except Exception as ex:
        return HttpResponse("Don't know what went wrong")

    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'lists/lists.html', {'list': list_, 'form': form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        # Item.objects.create(text=request.POST['text'], list=list_)
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'lists/home.html', {"form": form})
