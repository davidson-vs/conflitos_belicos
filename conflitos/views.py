import psycopg2
import pandas as pd

from .utils.banco import Banco
from django.shortcuts import render

# Responsável por exportar as telas para o arquivo de urls
# TODO:descomentar quando a tabela for criada

def homepage(request):
    return render(request, 'index.html', status=200, context={})

def grafics_page(request):
    return render(request, 'grafics.html', status=200, context={})

def lists_page(request):
    return render(request, 'lists.html', status=200, context={})

# TODO: montar o select 
def chefe_militar(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        insert_query = f""" INSERT INTO conflitosBelicos.ChefeMilitar ( Nome, FaixaHierarquica, IdLiderpolitico, IdDivisao)
            VALUES ('{nm_chefe}', '{descricao_lider}', '{lider_politico}', '{divisao}') """
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nm_chefe = request.POST.get('chefe_militar', None)
            descricao_lider = request.POST.get('descricao_lider', None)
            lider_politico = request.POST.get('lider_politico', None)
            divisao = request.POST.get('divisao', None)

            # db.execute_query(cxn, insert_query, persistence=True,) 

    except Exception as cf_militar_error:
        print(cf_militar_error)
    finally:
        return render(request, 'chefe_militar.html', status=200, context={})

def conflitos(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        query = f""" INSERT INTO conflitosBelicos.Conflitos ( Nome, NumeroMortos, NumFeridos, TipoConflito,
        FlagReligiao, Flagregiao, FlagEconomico, FlagEtnia)
            VALUES ('{nome}', {qtde_mortos}, {qtde_feridos}, '{pais}') """
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_org_mediadora', None)
            qtde_mortos = request.POST.get('qtde_mortos', None)
            qtde_feridos = request.POST.get('qtde_feridos', None)
            pais = request.POST.get('pais', None)
            tp_conflito = request.POST.get('tp_conflito', None)

            # db.execute_query(cxn, query, persistence=True, params=(
            #     nome, qtde_mortos, qtde_feridos, pais, tp_conflito
            # ))        
            # 
            context['mensagem'] = 'Cadastro realizado com sucesso!'   

    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'conflitos.html', status=200, context={})
    

#quando for criar a tabela da divisão fazer o id se autoincrementar
def divisao(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        query = """ INSERT INTO conflitosBelicos.Divisao ( NmDivisao, NumeroBarco, NumeroTanque, NumeroBaixas, NumeroHomem, NumeroAviao)
            VALUES (?, ?, ?, ?, ?, ?) """
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nm_divisao = request.POST.get('nome_divisao', None)
            qtde_barcos = request.POST.get('qtde_barcos', None)
            qtde_tanques = request.POST.get('qtde_tanques', None)
            qtde_homens = request.POST.get('qtde_homens', None)
            qtde_avioes = request.POST.get('qtde_avioes', None)
            qtde_baixas = request.POST.get('qtde_baixas', None)
            select_divisao = request.POST.get('select_divisao', None)

            # db.execute_query(cxn, query, persistence=True, params=(
            #     nm_divisao, qtde_barcos, qtde_tanques, qtde_baixas, qtde_homens, qtde_avioes
            # ))        
            # 
            context['mensagem'] = 'Cadastro realizado com sucesso!'   
        
    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'divisao.html', status=200, context=context)
        

def grupo_armado(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_grupo_armado', None)

            query = f""" INSERT INTO conflitosbelicos.grupoarmado ( nome )
            VALUES ('{nome}') """

            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   
        
    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'grupo_armado.html', status=200, context={})
    

def liders_politicos(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        query = """ INSERT INTO conflitosBelicos.GrupoArmado ( Nome )
            VALUES (?) """
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('lider_politico', None)


            db.execute_query(cxn, query, persistence=True, params=(
                nome
            ))        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   
        
    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'lideres_politicos.html', status=200, context={})
    

def tipo_conflito(request):
    return render(request, 'tipo_conflito.html', status=200, context={})

def arma(request):
    return render(request, 'arma.html', status=200, context={})

def dialogo(request):
    return render(request, 'dialogo.html', status=200, context={})

def negociacao(request):
    return render(request, 'negociacao.html', status=200, context={})

def mediacao(request):
    return render(request, 'mediacao.html', status=200, context={})

def organizacao_mediadora(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        query = """ INSERT INTO conflitosBelicos.OrganizacaoMediadora ( Nome, Tipo, Organizacao )
            VALUES (?, ?, ?) """
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_org_mediadora', None)
            tipo = request.POST.get('tipo_org_mediadora', None)
            org = request.POST.get('org_org_mediadora', None)

            # db.execute_query(cxn, query, persistence=True, params=(
            #     nome, tipo, org
            # ))        
            # 
            context['mensagem'] = 'Cadastro realizado com sucesso!'   

    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'organizacao_mediadora.html', status=200, context={})
    

def pais(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
       
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_pais', None)
            query = f""" INSERT INTO conflitosBelicos.Pais ( Nome )
            VALUES ('{nome}') """
            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   

    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'pais.html', status=200, context={})
    

def participacao(request):
    return render(request, 'participacao.html', status=200, context={})

def traficante(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        query = """ INSERT INTO conflitosBelicos.Traficante ( Nome )
            VALUES (?) """
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_traficante', None)

            # db.execute_query(cxn, query, persistence=True, params=(
            #     nome
            # ))        
            # 
            context['mensagem'] = 'Cadastro realizado com sucesso!'   

    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'traficante.html', status=200, context={})
    