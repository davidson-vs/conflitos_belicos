import os
import io
import json
import psycopg2
import pandas as pd

import matplotlib.pyplot as plt
from .utils.banco import Banco
from django.shortcuts import render

# Responsável por exportar as telas para o arquivo de urls


def homepage(request):
    return render(request, 'index.html', status=200, context={})

def grafics_page(request):
    try:
        db = Banco()
        cxn = db.connection()
        consult = "SELECT TipoConflito FROM conflitosBelicos.Conflito"
        data = db.get_multiple_result(cxn, consult)
        df = pd.DataFrame(data)
        
        plt.figure(figsize=(14, 7))
        plt.xlabel('Tipo de Conflito', fontsize=18)
        plt.ylabel('Número de Conflitos', fontsize=18)
        plt.tick_params(labelsize=12)
        plt.hist(df, len(set(df['tipoconflito'])), rwidth=0.8, color='#435f70', alpha=0.7, edgecolor='black')
        plt.savefig("./conflitos/static/images/histograma.jpg", format='jpg')
        
    except Exception as gf_error:
        ...
    finally:
        return render(request, 'grafics.html', status=200)

def lists_page(request):
    try:
        db = Banco()
        cxn = db.connection()
        context = {}
        if request.method == 'POST':
            opt = request.POST.get('list_opt', None)
            if opt == '1': # ii. Listar os traficantes e os grupos armados (Nome) para os quais os traficantes fornecem armas “Barret M82” ou “M200 intervention”. 
                data = db.get_multiple_result(cxn, """SELECT DISTINCT T.Nome AS Nome_Traficante, GA.Nome AS Nome_Grupo_Armado, A.Nome AS Arma_Fornecida
                FROM conflitosBelicos.Arma AS A, conflitosBelicos.Negociacao AS N, conflitosBelicos.GrupoArmado AS GA, conflitosBelicos.Traficante AS T
                WHERE A.IdTraficante = A.IdTraficante AND GA.IdGrupoArmado = N.IdGrupoArmado AND A.IdArma = N.IdArma
                AND (A.nome = 'Barret M82' OR A.nome = 'M200 intervention')""")

            elif opt == '2': # iii. Listar os 5 maiores conflitos em número de mortos.
                data = db.get_multiple_result(cxn, """SELECT Nome, NumeroMortos AS Numero_Mortos
                FROM conflitosbelicos.Conflito
                ORDER BY Numero_Mortos DESC LIMIT 5""")

            elif opt == "3": # iv. Listar as 5 maiores organizações em número de mediações.
                data = db.get_multiple_result(cxn,  """SELECT Nome AS Nome_Organizacoes, COUNT(*) AS Numero_Mediacoes
                FROM conflitosbelicos.OrganizacaoMediadora AS OM, conflitosbelicos.Mediacao AS MED
                WHERE OM.IdOrganizacao = MED.IdOrganizacao
                GROUP BY OM.idOrganizacao
                ORDER BY Numero_Mediacoes DESC LIMIT 5""")


            elif opt == "4": # v. Listar os 5 maiores grupos armados com maior número de armas fornecidos.
                data = db.get_multiple_result(cxn, """SELECT Nome AS Nome_Grupo_Armado, SUM(QtdeArma) AS Numero_Armas
                FROM conflitosbelicos.GrupoArmado AS G, conflitosbelicos.Negociacao AS N
                WHERE G.IdGrupoArmado = N.IdGrupoArmado
                GROUP BY G.IdGrupoArmado
                ORDER BY Numero_Armas DESC LIMIT 5""")

            elif opt == "5": # vi. Listar o país e número de conflitos com maior número de conflitos religiosos.
                data = db.get_multiple_result(cxn, """SELECT P.Nome AS Nome_Pais, COUNT(*) AS Numero_Conflitos_Religiosos
                FROM conflitosbelicos.Pais AS P, conflitosbelicos.Conflito AS C
                WHERE P.idPais = C.idPais AND tipoconflito = 'religioso'
                GROUP BY P.idPais
                ORDER BY Numero_Conflitos_Religiosos DESC LIMIT 1""")

            print(data)
            df = pd.DataFrame(data)
            colunas = df.columns
            new_colunas = []
            for coluna in colunas:
                lista = coluna.split("_")
                new_coluna = " ".join(lista)
                new_colunas.append(new_coluna.capitalize())
            df.columns = new_colunas
            context['data'] = df.to_html(justify='center')

            if data == []:
                context['mensagem'] = 'A consulta não retornou nenhum caso. Não há dados cadastrados suficientes.'
    except Exception as error:
        print(error)
    finally:    
        return render(request, 'lists.html', status=200, context=context)


def chefe_militar(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        consult_lider_politico = """SELECT IdLiderPolitico, Nome From conflitosBelicos.LiderPolitico"""
        data_lp = db.get_multiple_result(cxn, consult_lider_politico)
        context['data_lp'] = data_lp
        
        consult_divisao = """SELECT DISTINCT D.IdDivisao, GA.Nome, GA.IdGrupoArmado as idga
                            FROM conflitosbelicos.Divisao AS D, conflitosbelicos.GrupoArmado AS GA
                            WHERE D.IdDivisao = GA.IdGrupoArmado """
        data_d = db.get_multiple_result(cxn, consult_divisao)
        context['data_d'] = data_d
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nm_chefe = request.POST.get('chefe_militar', None)
            descricao_lider = request.POST.get('descricao_lider', None)
            lider_politico = request.POST.get('lider_politico', None)
            divisao_ga = request.POST.get('divisao', None)
            divisao = divisao_ga.split('|')[0]
            grupo_armado = divisao_ga.split('|')[1]

            insert_query = f""" INSERT INTO conflitosBelicos.ChefeMilitar ( Nome, FaixaHierarquica, IdLiderpolitico, IdDivisao, idGrupoArmado)
            VALUES ('{nm_chefe}', '{descricao_lider}', {lider_politico}, {divisao}, {grupo_armado}) """

            db.execute_query(cxn, insert_query, persistence=True,)
            context['mensagem'] = 'Cadastro concluido com sucesso!' 

    except Exception as cf_militar_error:
        context['mensagem'] = 'Não foi possível realizar o cadastro!' 
        print(cf_militar_error)
    finally:
        return render(request, 'chefe_militar.html', status=200, context=context)

def conflitos(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        consult = """SELECT IdPais, Nome FROM conflitosBelicos.Pais"""
        data = db.get_multiple_result(cxn, consult)
        context['data'] = data
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_conflito', None)
            qtde_mortos = request.POST.get('qtde_mortos', None)
            qtde_feridos = request.POST.get('qtde_feridos', None)
            pais = request.POST.get('pais', None)
            tp_conflito = request.POST.get('tp_conflito', None)

            query = f""" INSERT INTO conflitosBelicos.Conflito ( Nome, NumeroMortos, NumeroFeridos, TipoConflito,
            IdPais)
            VALUES ('{nome}', {qtde_mortos}, {qtde_feridos}, '{tp_conflito}', {pais}) """

            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   

    except Exception as tp_conflito_error:
        context['mensagem'] = 'Não foi possível realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'conflitos.html', status=200, context=context)
    

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
            num_div = request.POST.get('num_div', None)
            qtde_barcos = request.POST.get('qtde_barcos', None)
            qtde_tanques = request.POST.get('qtde_tanques', None)
            qtde_homens = request.POST.get('qtde_homens', None)
            qtde_avioes = request.POST.get('qtde_avioes', None)
            qtde_baixas = request.POST.get('qtde_baixas', None)
            select_divisao = request.POST.get('select_divisao', None)

            query = f""" INSERT INTO conflitosBelicos.Divisao ( idDivisao, NumeroBarcos, NumeroTanques, NumeroBaixas, NumeroHomens, NumeroAvioes, IdGrupoArmado)
            VALUES ( {num_div}, {qtde_barcos}, {qtde_tanques}, {qtde_baixas}, {qtde_homens}, {qtde_avioes}, {select_divisao}) """
            
            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   
        
    except Exception as tp_conflito_error:
        context['mensagem'] = 'Não foi possível realizar o cadastro!'   
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
        context['mensagem'] = 'Não foi possível realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'grupo_armado.html', status=200, context=context)
    

def liders_politicos(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        consult = """SELECT IdGrupoArmado, Nome FROM conflitosBelicos.GrupoArmado"""
        data = db.get_multiple_result(cxn, consult)
        context['data'] = data
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
        context['mensagem'] = 'Não foi possível realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'lideres_politicos.html', status=200, context=context)
    
# TODO: perguntar se vai verificar o tipo para fazer o insert na tabela
def tipo_conflito(request):
    try:
        db = Banco()
        context = {}
        # headers = json.load(open(r'{}\conflitos\utils\tp_conflitos.json'.format(os.getcwd()), 'r'))
        with open(r'{}\conflitos\utils\tp_conflitos.json'.format(os.getcwd()), encoding='utf8') as f:
            headers = json.load(f)
            context['json'] = [headers]
        cxn = db.connection()
        consult =  """SELECT idconflito, nome from conflitosbelicos.conflito"""
        data = db.get_multiple_result(cxn, consult)
        context['data'] = data
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            
            tp_conflito = request.POST.get('tp_conflito', None)
            tp_descricao = request.POST.get('tp_descricao', None)
            
            idConflito = data[0]['idconflito']
            nome = data[0]['nome']

            if tp_conflito =='Territorial':
               query = f""" INSERT INTO conflitosBelicos.Territorial ( Regiao, idConflito)
                VALUES ( {tp_descricao}, {idConflito}) """
            elif tp_conflito == "Religioso":
                query = f""" INSERT INTO conflitosBelicos.Religioso ( Religiao, idConflito)
                VALUES ( {tp_descricao}, {idConflito}) """
            elif tp_conflito == "Economico":
                query = f""" INSERT INTO conflitosBelicos.Economico ( MateriaPrima, idConflito)
                VALUES ( {tp_descricao}, {idConflito}) """
            elif tp_conflito == "Racial":
                query = f""" INSERT INTO conflitosBelicos.Racial ( Etnia, idConflito)
                VALUES ( {tp_descricao}, {idConflito}) """

            
            response = db.execute_query(cxn, query, persistence=True)        

            if response:
                context['mensagem'] = 'Cadastro realizado com sucesso!'
            else:
                context['mensagem'] = 'Os dados não foram inseridos por conta da regra de negócio.'   
        
    except Exception as tp_conflito_error:
        context['mensagem_erro'] = 'Não foi possível realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'tipo_conflito.html', status=200, context=context)

def arma(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        consult = """SELECT idtraficante, nome from conflitosbelicos.traficante"""
        data = db.get_multiple_result(cxn, consult)
            
        context['data'] = data
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_arma', None)
            tipo_arma = request.POST.get('tipo_arma', None)
            capacidade_destrutiva = request.POST.get('capacidade_destrutiva', None)
            select_arma = request.POST.get('select_arma', None)
            
            

            query = f""" INSERT INTO conflitosBelicos.Arma ( Nome, TipoArma, CapacidadeDestrutiva, IdTraficante )
            VALUES ('{nome}', '{tipo_arma}', {capacidade_destrutiva}, {select_arma}) """
            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   
        
    except Exception as tp_conflito_error:
        context['mensagem'] = 'Não foi possível realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'arma.html', status=200, context=context)

def dialogo(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        consult_l = """SELECT idliderpolitico, nome from conflitosbelicos.liderpolitico"""
        data_l = db.get_multiple_result(cxn, consult_l)
            
        context['data_l'] = data_l
        consult_o = """SELECT idorganizacao, nome from conflitosbelicos.organizacaomediadora"""
        data_o = db.get_multiple_result(cxn, consult_o)
            
        context['data_o'] = data_o
        
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
        context['mensagem'] = 'Não foi possível realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'dialogo.html', status=200, context=context)
    

def negociacao(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        consult_ga = """SELECT idgrupoarmado, nome from conflitosbelicos.grupoarmado"""
        data_ga = db.get_multiple_result(cxn, consult_ga)
        context['data_ga'] = data_ga
        consult_a = """SELECT idarma, nome from conflitosbelicos.arma"""
        data_a = db.get_multiple_result(cxn, consult_a)
        context['data_a'] = data_a
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            qtde_armas = request.POST.get('qtde_arma', None)
            select_negociacao_grupo_armado = request.POST.get('select_negociacao_grupo_armado', None)
            select_negociacao_arma = request.POST.get('select_negociacao_arma', None)

            query = f""" INSERT INTO conflitosBelicos.Negociacao ( QtdeArma, IdGrupoArmado, IdArma )
            VALUES ({qtde_armas}, {select_negociacao_grupo_armado},  {select_negociacao_arma}) """
            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   
        
    except Exception as tp_conflito_error:
        context['mensagem'] = 'Não foi possível realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'negociacao.html', status=200, context=context)

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
        context['mensagem'] = 'Não foi possível realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'mediacao.html', status=200, context=context)

def organizacao_mediadora(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        
        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            nome = request.POST.get('nome_org_mediadora', None)
            tipo = request.POST.get('tipo_org_mediadora', None)
            # org = request.POST.get('org_org_mediadora', None)

            query = f""" INSERT INTO conflitosBelicos.OrganizacaoMediadora ( Nome, Tipo )
            VALUES ('{nome}', '{tipo}') """

            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   

    except Exception as tp_conflito_error:
        context['mensagem'] = 'Não foi possível realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'organizacao_mediadora.html', status=200, context=context)
    

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
        context['mensagem'] = 'Não foi possível realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'pais.html', status=200, context=context)
    

def participacao(request):
    try:
        db = Banco()
        context = {}
        cxn = db.connection()
        consult = """SELECT IdGrupoArmado, Nome From conflitosBelicos.GrupoArmado"""
        data_ga = db.get_multiple_result(cxn, consult)
        context['data_ga'] = data_ga

        consult_c = """SELECT IdConflito, Nome From conflitosBelicos.Conflito"""
        data_c = db.get_multiple_result(cxn, consult_c)
        context['data_c'] = data_c

        if request.method == 'POST':
            # aqui vc recebe o valor de cada campo do form
            data_entrada = request.POST.get('data_entrada', None)
            data_saida = request.POST.get('data_saida', None)
            select_participacao_grupo_armado = request.POST.get('select_participacao_grupo_armado', None)
            select_participacao_conflito = request.POST.get('select_participacao_conflito', None)
            data_entrada = request.POST.get('data_entrada', None)
            
            query = f""" INSERT INTO conflitosBelicos.Participacao ( DtEntrada, DtSaida, IdConflito, IdGrupoArmado )
            VALUES ('{data_entrada}', '{data_saida}', {select_participacao_conflito}, {select_participacao_grupo_armado}) """

            db.execute_query(cxn, query, persistence=True)        
            
            context['mensagem'] = 'Cadastro realizado com sucesso!'   

    except Exception as tp_conflito_error:
        context['mensagem'] = 'Não foi possível realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'participacao.html', status=200, context=context)

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
        context['mensagem'] = 'Não foi possível realizar o cadastro!'   
        print(tp_conflito_error)
    finally:
        return render(request, 'traficante.html', status=200, context=context)
    
