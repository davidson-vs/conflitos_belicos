from django.shortcuts import render

def form(request):
    if request.method == 'POST':
        # aqui vc recebe o valor de cada campo do form
        nm_divisao = request.POST.get('nome_divisao', None)
    return render(request, 'tipo_conflito.html', status=200, context={})

def homepage(request):
    return render(request, 'index.html', status=200, context={})

def grafics_page(request):
    return render(request, 'grafics.html', status=200, context={})

def lists_page(request):
    return render(request, 'lists.html', status=200, context={})


def chefe_militar(request):
    return render(request, 'chefe_militar.html', status=200, context={})

def conflitos(request):
    return render(request, 'conflitos.html', status=200, context={})

def divisao(request):
    return render(request, 'divisao.html', status=200, context={})

def grupo_armado(request):
    return render(request, 'grupo_armado.html', status=200, context={})

def liders_politicos(request):
    return render(request, 'lideres_politicos.html', status=200, context={})

def tipo_conflito(request):
    return render(request, 'tipo_conflito.html', status=200, context={})

