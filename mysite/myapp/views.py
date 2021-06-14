from django.shortcuts import render
from pandas import DataFrame
from django.template import RequestContext
from mysite.database import Main
from mysite.database.return_games import return_games
from mysite.database.return_class_cmplt import return_class_cmplt
from myapp.rodadas import return_rodadas_dict

rodada_int = 4 #Número da rodada do brasileirão.
RODADA = "Rodada " + str(rodada_int)
MES = "Maio/2021" #Mês em que estamos.

Rodadas_dict = return_rodadas_dict()

def html_sidebar():
    with open('myapp/templates/sidebar.html', 'r') as f:
        html_string = f.read()
    return html_string

# Create your views here.
#Cria a Página Inicial do site com o estagio atual dos jogos da rodada.
def index(request):
    content = {}
    #dicionário a ser utilizado na saída no templante index.html
    gabarito_sheet = Main.get_data('mysite/database/BolaoFutebolClubismo-d44be1b6b394.json','gabarito', RODADA)
    #extração dos valores da planilha formulário na aba 'gabarito' para a rodada atual
    resultados_html = return_games(gabarito_sheet.col_values(1), gabarito_sheet.col_values(2))

    #gabarito = gabarito_sheet.get_all_values()


    #dataframe representado em html dos jogos em 3 colunas
    
    content['tabela'] = resultados_html
    #criação da chave 'tabela' que tem o dataframe resultados_html como valor
    content['rodada'] = RODADA
    #criação da chave 'rodada' que tem a rodada atual como valor

    content['sidebar'] = html_sidebar()

    return render(request, 'index.html',content)
    #retorno da função index com o request, a pagina que vai receber os valores e o dicionário content

def classificacao_rodada(request):
    content = {}
    content['rodada'] = RODADA
    palpites_sheet, gabarito_sheet = Main.get_data('mysite/database/BolaoFutebolClubismo-d44be1b6b394.json','palpites_gabarito', RODADA)
    #placares = list()
    cadastro_sheet = Main.get_data('mysite/database/BolaoFutebolClubismo-d44be1b6b394.json', '', "Cadastro")

    palpites = palpites_sheet.get_all_values()
    gabarito = gabarito_sheet.get_all_values()
    cadastro = cadastro_sheet.get_all_values()

    cadastro_dict = {int(d[2]): d[1] for d in cadastro[1:]}
    

    i = 0
    #for a in gabarito_sheet.col_values(2):
    for a in gabarito:
        if (a[1] == "-"):
            i = i+1
            if(i == len(gabarito)):
                content['tables'] = '<p style="text-align:central"> A Rodada ainda não começou. </p>'
            return render(request, 'classificacao_rodada.html',content)
        else:
            break

    df_format = False
    #content['tables'] = Main.get_boletins(gabarito_sheet,palpites_sheet)
    #content['tables'] = Main.get_boletins(gabarito_sheet,palpites_sheet, df_format)
    content['tables'] = Main.get_boletins(gabarito,palpites,cadastro_dict, df_format)

    content['sidebar'] = html_sidebar
    return render(request, 'classificacao_rodada.html',content)

def classificacao_mes(request):
    content = {}
    palpites_sheet, gabarito_sheet, classificacao_sheet = Main.get_data('mysite/database/BolaoFutebolClubismo-d44be1b6b394.json', '', RODADA)
    df_format = True
    cadastro_sheet = Main.get_data('mysite/database/BolaoFutebolClubismo-d44be1b6b394.json', '', "Cadastro")
    
    gabarito = gabarito_sheet.get_all_values()
    palpites = palpites_sheet.get_all_values()
    cadastro = cadastro_sheet.get_all_values()

    cadastro_dict = {int(d[2]): d[1] for d in cadastro[1:]}
    
    

    
    #print(cadastro_dict[int(codigo_part)])
    #content['tables'] = Main.get_boletins(gabarito_sheet,palpites_sheet)
    nomes_dict = Main.get_boletins(gabarito,palpites,cadastro_dict, df_format)
    #nomes_dict = Main.get_boletins(gabarito_sheet,palpites_sheet, df_format)

    #classificacao = return_class_cmplt(nomes_dict,classificacao_sheet)
    return_class_cmplt(nomes_dict,classificacao_sheet)

    classificacao_mes_sheet = Main.get_data('mysite/database/BolaoFutebolClubismo-d44be1b6b394.json', '', MES)

    valores = classificacao_mes_sheet.get_all_values()

    valores = [[x if x == a[0] else int(x) for x  in a] for a in valores[1:]]

    classificacao_mes = DataFrame(valores,columns=['Nome', 'Pontos Totais', '10 pontos', '7 pontos', '5 pontos', '2 pontos', '0 pontos'])
    classificacao_mes = classificacao_mes.sort_values(by=['Pontos Totais', '10 pontos', '7 pontos', '0 pontos', '5 pontos', '2 pontos'],ascending=[0,0,0,1,0,0])

    classificacao_mes.index = [i+1 for i in range(0, len(classificacao_mes.values))]

    classificacao_mes = classificacao_mes.to_html()
    classificacao_mes = classificacao_mes.replace('<table border="1" class="dataframe">', '<table style="text-align: center; width:100%">')
    classificacao_mes = classificacao_mes.replace('<tr style="text-align: right;">', '<tr>')
    classificacao_mes = classificacao_mes.replace('<tbody>', '<tbody  style="text-align: center;">')
    classificacao_mes = classificacao_mes.replace("\n", "")

    #content['classificacao'] = return_class_cmplt(nomes_dict,classificacao_sheet)
    content['classificacao'] = classificacao_mes
    content['mes'] = MES

    content['sidebar'] = html_sidebar

    return render(request, 'classificacao_mes.html',content)

def classificacao_geral(request):
    content = {}
    palpites_sheet, gabarito_sheet, classificacao_sheet = Main.get_data('mysite/database/BolaoFutebolClubismo-d44be1b6b394.json', '', RODADA)
    df_format = True
    cadastro_sheet = Main.get_data('mysite/database/BolaoFutebolClubismo-d44be1b6b394.json', '', "Cadastro")
    
    gabarito = gabarito_sheet.get_all_values()
    palpites = palpites_sheet.get_all_values()
    cadastro = cadastro_sheet.get_all_values()

    cadastro_dict = {int(d[2]): d[1] for d in cadastro[1:]}
    

    nomes_dict = Main.get_boletins(gabarito,palpites,cadastro_dict, df_format)

    return_class_cmplt(nomes_dict,classificacao_sheet)

    geral_sheet = Main.get_data('mysite/database/BolaoFutebolClubismo-d44be1b6b394.json', '', "Classificação Geral")

    classificacao_geral = geral_sheet.get_all_values()

    valores = [[x if x == a[0] else int(x) for x  in a] for a in classificacao_geral[1:]]

    classificacao_geral = DataFrame(valores,columns=['Nome', 'Pontos Totais', '10 pontos', '7 pontos', '5 pontos', '2 pontos', '0 pontos'])
    classificacao_geral = classificacao_geral.sort_values(by=['Pontos Totais', '10 pontos', '7 pontos', '0 pontos', '5 pontos', '2 pontos'],ascending=[0,0,0,1,0,0])
    
    classificacao_geral.index = [i+1 for i in range(0, len(classificacao_geral.values))]
    
    classificacao_geral = classificacao_geral.to_html()
    classificacao_geral = classificacao_geral.replace('<table border="1" class="dataframe">', '<table style="text-align: center; width:100%">')
    classificacao_geral = classificacao_geral.replace('<tr style="text-align: right;">', '<tr>')
    classificacao_geral = classificacao_geral.replace('<tbody>', '<tbody  style="text-align: center;">')
    classificacao_geral = classificacao_geral.replace("\n", "")

    content['rodada'] = "Classificação Geral"
    content['tabela'] = classificacao_geral

    content['sidebar'] = html_sidebar
    
    return render(request, 'classificacao_geral.html',content)

def prox_rodada(request):
    content = {}
    content['rodada'] = RODADA #não modificar.
    content['link'] = Rodadas_dict[RODADA]

    content['sidebar'] = html_sidebar

    return render(request, 'prox_rodada.html',content)

def rodada_seguinte(request):
    content = {}
    atual = rodada_int+1

    content['rodada'] = "Rodada " + str(atual)
    content['link'] = Rodadas_dict[content['rodada']]

    content['sidebar'] = html_sidebar

    return render(request, 'rodada_seguinte.html',content)

def rodada_depois(request):
    content = {}
    atual = rodada_int+2

    content['rodada'] = "Rodada " + str(atual)
    content['link'] = Rodadas_dict[content['rodada']]

    content['sidebar'] = html_sidebar

    return render(request, 'rodada_depois.html',content)

def proximarodada(request):
    content = {}
    atual = rodada_int+3

    content['rodada'] = "Rodada " + str(atual)
    content['link'] = Rodadas_dict[content['rodada']]

    content['sidebar'] = html_sidebar

    return render(request, 'proximarodada.html',content)

def regulamento(request):
    content = {}
    content['rodada'] = "Regulamento"

    content['sidebar'] = html_sidebar

    return render(request, 'regulamento.html',content)

def galeria_campeoes(request):
    content = {}
    content['rodada'] = "Galeria de Campeões"
    content['sidebar'] = html_sidebar

    return render(request, 'galeria_campeoes.html',content)