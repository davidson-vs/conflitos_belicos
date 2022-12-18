from django.shortcuts import render
from conflitos.utils.banco import Banco
import psycopg2


def form(request):
    
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
    if request.method == 'POST':
        # aqui vc recebe o valor de cada campo do form
        return render(request, 'conflitos.html', status=200, context={})

def divisao(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        query = """ INSERT INTO """
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nm_divisao = request.POST.get('nome_divisao', None)
            qtde_barcos = request.POST.get('qtde_barcos', None)
            qtde_tanques = request.POST.get('qtde_tanques', None)
            qtde_homens = request.POST.get('qtde_homens', None)
            qtde_avioes = request.POST.get('qtde_avioes', None)
            qtde_baixas = request.POST.get('qtde_baixas', None)
            select_divisao = request.POST.get('select_divisao', None)

            db.execute_query()
            print(nm_divisao)
    except Exception as tp_conflito_error:
        print(tp_conflito_error)
    finally:
        return render(request, 'divisao.html', status=200, context={})

def grupo_armado(request):
    return render(request, 'grupo_armado.html', status=200, context={})

def liders_politicos(request):
    return render(request, 'lideres_politicos.html', status=200, context={})

def tipo_conflito(request):
        return render(request, 'tipo_conflito.html', status=200, context={})