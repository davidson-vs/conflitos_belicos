from django.urls import path
from conflitos.views import *


urlpatterns = [
    path('', homepage , name= 'homepage'),
    path('chefe_militar/', chefe_militar, name= 'chefe_militar'),
    path('conflitos/', conflitos, name= 'conflitos'),
    path('divisao/', divisao, name= 'divisao' ),
    path('grafics/', grafics_page, name= 'grafics'),
    path('grupo_armado/', grupo_armado, name= 'grupo_armado'),
    path('lideres_politicos/', liders_politicos, name= 'lideres_politicos'),
    path('lists/', lists_page, name= 'lists'),
    path('tipo_conflito/', tipo_conflito, name= 'tipo_conflito'),
    path('arma/', arma, name = 'arma'),
    path('dialogo/', dialogo, name = 'dialogo'),
    path('mediacao/', mediacao, name = 'mediacao'),
    path('negociacao/', negociacao, name = 'negociacao'),
    path('organizacao_mediadora/', organizacao_mediadora, name = 'organizacao_mediadora'),
    path('pais/', pais, name = 'pais'),
    path('participacao/', participacao, name = 'participacao'),
    path('traficante/', traficante, name = 'traficante')
]