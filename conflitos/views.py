import psycopg2
import pandas as pd

from .utils.banco import Banco
from django.shortcuts import render

# Responsável por exportar as telas para o arquivo de urls


def homepage(request):
    return render(request, 'index.html', status=200, context={})

def grafics_page(request):
    return render(request, 'grafics.html', status=200, context={})

def lists_page(request):
    return render(request, 'lists.html', status=200, context={})


def chefe_militar(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nm_chefe = request.POST.get('chefe_militar', None)
            descricao_lider = request.POST.get('descricao_lider', None)
            lider_politico = request.POST.get('lider_politico', None)
            divisao = request.POST.get('divisao', None)

            insert_query = f""" INSERT INTO conflitosBelicos.ChefeMilitar ( Nome, FaixaHierarquica, IdLiderpolitico, IdDivisao)
            VALUES ('{nm_chefe}', '{descricao_lider}', '{lider_politico}', '{divisao}') """

            db.execute_query(cxn, insert_query, persistence=True,) 

    except Exception as cf_militar_error:
        print(cf_militar_error)
    finally:
        return render(request, 'chefe_militar.html', status=200, context={})

def conflitos(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_org_mediadora', None)
            qtde_mortos = request.POST.get('qtde_mortos', None)
            qtde_feridos = request.POST.get('qtde_feridos', None)
            pais = request.POST.get('pais', None)
            tp_conflito = request.POST.get('tp_conflito', None)

            query = f""" INSERT INTO conflitosBelicos.Conflitos ( Nome, NumeroMortos, NumFeridos, TipoConflito,
            IdPais)
            VALUES ('{nome}', {qtde_mortos}, {qtde_feridos}, {tp_conflito}, {pais}) """

            db.execute_query(cxn, query, persistence=True)        
            
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
        consult = """SELECT IdGrupoArmado, Nome From conflitosBelicos.GrupoArmado"""
        data = db.get_multiple_result(cxn, consult)
        context['data'] = data
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nm_divisao = request.POST.get('nome_divisao', None)
            qtde_barcos = request.POST.get('qtde_barcos', None)
            qtde_tanques = request.POST.get('qtde_tanques', None)
            qtde_homens = request.POST.get('qtde_homens', None)
            qtde_avioes = request.POST.get('qtde_avioes', None)
            qtde_baixas = request.POST.get('qtde_baixas', None)
            select_divisao = request.POST.get('select_divisao', None)

            query = f""" INSERT INTO conflitosBelicos.Divisao ( NmDivisao, NumeroBarcos, NumeroTanques, NumeroBaixas, NumeroHomens, NumeroAvioes, IdGrupoArmado)
            VALUES ('{nm_divisao}', {qtde_barcos}, {qtde_tanques}, {qtde_baixas}, {qtde_homens}, {qtde_avioes}, {select_divisao}) """
            
            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   
        
    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'divisao.html', status=200, context=context)
        
# dar uma olhada na soma do número de baixas.
def grupo_armado(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_grupo_armado', None)

            query = f""" INSERT INTO conflitosBelicos.GrupoArmado ( nome )
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
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('lider_politico', None)
            descricao = request.POST.get('descricao', None)
            grupo_armado = request.POST.get('grupo_armado', None)

            query = f""" INSERT INTO conflitosBelicos.LiderPolitico ( Nome, Descricao, IdGrupoArmado )
            VALUES ('{nome}', '{descricao}', {grupo_armado}) """

            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   
        
    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'lideres_politicos.html', status=200, context={})
    
# TODO: perguntar se vai verificar o tipo para fazer o insert na tabela
def tipo_conflito(request):
    return render(request, 'tipo_conflito.html', status=200, context={})

def arma(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_arma', None)
            tipo_arma = request.POST.get('tipo_arma', None)
            capacidade_destrutiva = request.POST.get('capacidade_destrutiva', None)
            select_arma = request.POST.get('select_arma', None)

            query = f""" INSERT INTO conflitosBelicos.Arma ( Nome, TipoArma, CapacidadeDestrutiva, IdTraficante )
            VALUES ('{nome}', '{tipo_arma}', '{capacidade_destrutiva}', {select_arma}) """
            db.execute_query(cxn, query, persistence=True, params=(
                nome
            ))        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   
        
    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'arma.html', status=200, context={})

def dialogo(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            diaologo = request.POST.get('diaologo', None)
            select_dialogo_org = request.POST.get('select_dialogo_org', None)
            select_dialogo_lider = request.POST.get('select_dialogo_lider', None)

            query = f""" INSERT INTO conflitosBelicos.Dialogo ( Discussao, IdOrganizacao, IdLiderPolitico )
            VALUES ('{dialogo}', {select_dialogo_org}, {select_dialogo_lider}) """
            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   
        
    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'dialogo.html', status=200, context={})
    

def negociacao(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            qtde_armas = request.POST.get('qtde_armas', None)
            select_negociacao_grupo_armado = request.POST.get('select_negociacao_grupo_armado', None)
            select_negociacao_traficante = request.POST.get('select_negociacao_traficante', None)
            select_negociacao_arma = request.POST.get('select_negociacao_arma', None)

            query = f""" INSERT INTO conflitosBelicos.Negociacao ( QtdeArma, IdGrupoArmado, IdTraficante, IdArma )
            VALUES ('{qtde_armas}', {select_negociacao_grupo_armado}, {select_negociacao_traficante}, {select_negociacao_arma}) """
            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   
        
    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'negociacao.html', status=200, context={})

def mediacao(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            data_entrada_mediacao = request.POST.get('data_entrada_mediacao', None)
            data_saida_mediacao = request.POST.get('data_saida_mediacao', None)
            qtde_pessoas = request.POST.get('qtde_pessoas', None)
            select_tipo_ajuda = request.POST.get('select_tipo_ajuda', None)
            select_mediacao_grupo_armado = request.POST.get('select_mediacao_grupo_armado', None)
            select_mediacao_organizacao = request.POST.get('select_mediacao_organizacao', None)

            query = f""" INSERT INTO conflitosBelicos.Mediacao ( TipoAjuda, QtdePessoas, DtEntrada, DtSaida, IdConflito, IdOrganizacao )
            VALUES ('{select_tipo_ajuda}', {qtde_pessoas}, '{data_entrada_mediacao}', '{data_saida_mediacao}', {select_mediacao_grupo_armado}, {select_mediacao_organizacao}) """
            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   
        
    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'mediacao.html', status=200, context={})

def organizacao_mediadora(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_org_mediadora', None)
            tipo = request.POST.get('tipo_org_mediadora', None)
            org = request.POST.get('org_org_mediadora', None)

            query = f""" INSERT INTO conflitosBelicos.OrganizacaoMediadora ( Nome, Tipo, Organizacao )
            VALUES ('{nome}', '{tipo}', '{org}') """

            db.execute_query(cxn, query, persistence=True)        
            
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
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            data_entrada = request.POST.get('data_entrada', None)
            data_saida = request.POST.get('data_saida', None)
            select_participacao_grupo_armado = request.POST.get('select_participacao_grupo_armado', None)
            select_participacao_conflito = request.POST.get('data_entrada', None)
            data_entrada = request.POST.get('data_entrada', None)
            
            query = f""" INSERT INTO conflitosBelicos.Participacao ( DtEntrada, DtSaida, IdConflito, IdGrupoArmado )
            VALUES ('{data_entrada}', '{data_saida}', {select_participacao_conflito}, {select_participacao_grupo_armado}) """

            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   

    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'participacao.html', status=200, context={})

def traficante(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_traficante', None)
            query = f""" INSERT INTO conflitosBelicos.Traficante ( Nome )
            VALUES ('{nome}') """
            
            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   

    except Exception as tp_conflito_error:
        context['mensagem'] = 'Falha ao realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'traficante.html', status=200, context={})
    
