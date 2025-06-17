#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import User, Mandato, Planejamento, Objetivo, MetaObjetivo
from datetime import date, timedelta

def create_sample_data():
    print("Criando dados de exemplo...")

    # Lista de mandatos para criar
    mandatos_data = [
        {
            'nome_parlamentar': 'João Silva',
            'casa_legislativa': Mandato.CasaLegislativa.CM,
            'cargo': Mandato.Cargo.VEREADOR,
            'estado': 'SP',
            'municipio': 'São Paulo',
            'posicionamento': Mandato.Posicionamento.CENTRO,
            'perfil': Mandato.Perfil.LEGISLADOR,
            'primeiro_mandato': True
        },
        {
            'nome_parlamentar': 'Ana Costa',
            'casa_legislativa': Mandato.CasaLegislativa.ALE,
            'cargo': Mandato.Cargo.DEP_ESTADUAL,
            'estado': 'RJ',
            'posicionamento': Mandato.Posicionamento.CENTRO_ESQ,
            'perfil': Mandato.Perfil.FISCALIZADOR,
            'primeiro_mandato': False
        },
        {
            'nome_parlamentar': 'Carlos Mendes',
            'casa_legislativa': Mandato.CasaLegislativa.CF,
            'cargo': Mandato.Cargo.DEP_FEDERAL,
            'estado': 'MG',
            'posicionamento': Mandato.Posicionamento.CENTRO_DIR,
            'perfil': Mandato.Perfil.ARTICULADOR,
            'primeiro_mandato': False
        },
        {
            'nome_parlamentar': 'Maria Santos',
            'casa_legislativa': Mandato.CasaLegislativa.SENADO,
            'cargo': Mandato.Cargo.SENADOR,
            'estado': 'RS',
            'posicionamento': Mandato.Posicionamento.ESQUERDA,
            'perfil': Mandato.Perfil.LEGISLADOR,
            'primeiro_mandato': True
        },
        {
            'nome_parlamentar': 'Pedro Oliveira',
            'casa_legislativa': Mandato.CasaLegislativa.CM,
            'cargo': Mandato.Cargo.VEREADOR,
            'estado': 'PR',
            'municipio': 'Curitiba',
            'posicionamento': Mandato.Posicionamento.DIREITA,
            'perfil': Mandato.Perfil.FISCALIZADOR,
            'primeiro_mandato': True
        }
    ]

    # Dados de planejamento para cada mandato
    planejamentos_data = [
        {
            'oportunidades': 'Crescimento da população jovem no município, aumento da demanda por tecnologia na educação, nova administração municipal receptiva a parcerias.',
            'fraquezas': 'Baixo orçamento para projetos de lei, equipe pequena, falta de experiência parlamentar.',
            'temas_interesse': 'Educação digital, Inclusão social, Meio ambiente urbano',
            'objetivo_ano': 'Aprovar 3 projetos de lei voltados para educação digital e sustentabilidade'
        },
        {
            'oportunidades': 'Experiência prévia na área de saúde, boa relação com sindicatos, momento de reformas no estado.',
            'fraquezas': 'Oposição ao governo estadual, recursos limitados para campanhas, resistência de grupos conservadores.',
            'temas_interesse': 'Saúde pública, Direitos trabalhistas, Transparência',
            'objetivo_ano': 'Fortalecer fiscalização da saúde pública e aprovar PL de transparência'
        },
        {
            'oportunidades': 'Bom relacionamento com governo federal, experiência em articulação política, bancada forte do partido.',
            'fraquezas': 'Pressão de grupos de interesse, agenda muito carregada, distância do estado.',
            'temas_interesse': 'Desenvolvimento econômico, Infraestrutura, Agronegócio',
            'objetivo_ano': 'Destinar R$ 50 milhões em emendas para infraestrutura de MG'
        },
        {
            'oportunidades': 'Mandato de 8 anos, liderança partidária, visibilidade nacional, experiência internacional.',
            'fraquezas': 'Alta expectativa da base, polarização política, agenda conflituosa.',
            'temas_interesse': 'Direitos humanos, Política externa, Meio ambiente',
            'objetivo_ano': 'Liderar comissão de direitos humanos e aprovar marco de sustentabilidade'
        },
        {
            'oportunidades': 'Cidade em crescimento, boa relação com prefeito, experiência empresarial.',
            'fraquezas': 'Primeiro mandato, oposição organizada, orçamento municipal limitado.',
            'temas_interesse': 'Desenvolvimento urbano, Segurança pública, Empreendedorismo',
            'objetivo_ano': 'Criar marco regulatório para startups e melhorar segurança no centro'
        }
    ]

    # Dados de objetivos para cada planejamento
    objetivos_data = [
        [  # João Silva
            {'descricao': 'Implementar laboratórios de informática em 10 escolas municipais', 'ordem': 1},
            {'descricao': 'Criar programa de capacitação digital para professores', 'ordem': 2},
            {'descricao': 'Estabelecer parcerias com universidades locais', 'ordem': 3},
            {'descricao': 'Instalar pontos de coleta seletiva em 20 bairros', 'ordem': 4}
        ],
        [  # Ana Costa
            {'descricao': 'Criar CPI para investigar irregularidades na saúde', 'ordem': 1},
            {'descricao': 'Aprovar lei de transparência em contratos públicos', 'ordem': 2},
            {'descricao': 'Fortalecer ouvidoria do sistema de saúde', 'ordem': 3}
        ],
        [  # Carlos Mendes
            {'descricao': 'Destinar R$ 20 milhões para rodovias de MG', 'ordem': 1},
            {'descricao': 'Aprovar incentivos fiscais para agronegócio sustentável', 'ordem': 2},
            {'descricao': 'Criar frente parlamentar do desenvolvimento regional', 'ordem': 3},
            {'descricao': 'Estabelecer parcerias internacionais para tecnologia agrícola', 'ordem': 4}
        ],
        [  # Maria Santos
            {'descricao': 'Presidir comissão de direitos humanos', 'ordem': 1},
            {'descricao': 'Aprovar PEC de proteção de defensores de direitos humanos', 'ordem': 2},
            {'descricao': 'Criar marco legal de sustentabilidade empresarial', 'ordem': 3}
        ],
        [  # Pedro Oliveira
            {'descricao': 'Aprovar lei municipal de incentivo a startups', 'ordem': 1},
            {'descricao': 'Instalar 50 câmeras de segurança no centro', 'ordem': 2},
            {'descricao': 'Criar programa de microcrédito para empreendedores', 'ordem': 3},
            {'descricao': 'Estabelecer hub de inovação municipal', 'ordem': 4}
        ]
    ]

    # Criar mandatos e dados relacionados
    for i, mandato_data in enumerate(mandatos_data):
        # Criar mandato
        mandato, created = Mandato.objects.get_or_create(
            nome_parlamentar=mandato_data['nome_parlamentar'],
            defaults=mandato_data
        )
        
        if created:
            print(f'✓ Criado mandato: {mandato.nome_parlamentar}')
        else:
            print(f'→ Mandato já existia: {mandato.nome_parlamentar}')

        # Criar planejamento
        planejamento, created = Planejamento.objects.get_or_create(
            mandato=mandato,
            defaults=planejamentos_data[i]
        )
        
        if created:
            print(f'  ✓ Criado planejamento para {mandato.nome_parlamentar}')

        # Criar objetivos
        for obj_data in objetivos_data[i]:
            objetivo, created = Objetivo.objects.get_or_create(
                planejamento=planejamento,
                descricao=obj_data['descricao'],
                defaults={'ordem': obj_data['ordem']}
            )
            
            if created:
                print(f'    ✓ Criado objetivo: {objetivo.descricao[:50]}...')

        # Criar usuários para cada mandato
        usuarios_mandato = [
            {
                'username': f'{mandato.nome_parlamentar.lower().replace(" ", ".")}.admin',
                'first_name': mandato.nome_parlamentar.split()[0],
                'last_name': ' '.join(mandato.nome_parlamentar.split()[1:]),
                'email': f'{mandato.nome_parlamentar.lower().replace(" ", ".")}@exemplo.com',
                'funcao': 'Parlamentar',
                'papel': User.Papel.ADMIN
            },
            {
                'username': f'assessor.{mandato.nome_parlamentar.lower().replace(" ", ".")}',
                'first_name': 'Assessor',
                'last_name': f'de {mandato.nome_parlamentar}',
                'email': f'assessor.{mandato.nome_parlamentar.lower().replace(" ", ".")}@exemplo.com',
                'funcao': 'Assessor Parlamentar',
                'papel': User.Papel.ASSESSOR
            }
        ]

        for user_data in usuarios_mandato:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    **user_data,
                    'mandato': mandato,
                    'password': 'pbkdf2_sha256$260000$exemplo'  # senha: exemplo123
                }
            )
            
            if created:
                user.set_password('exemplo123')
                user.save()
                print(f'    ✓ Criado usuário: {user.username} ({user.papel})')

    # Criar metas para alguns objetivos
    print("\n--- Criando metas para objetivos ---")
    
    # Buscar alguns objetivos para adicionar metas
    objetivos_com_metas = Objetivo.objects.filter(
        descricao__in=[
            'Implementar laboratórios de informática em 10 escolas municipais',
            'Destinar R$ 20 milhões para rodovias de MG',
            'Instalar 50 câmeras de segurança no centro'
        ]
    )

    metas_data = [
        {
            'indicador': 'Escolas com laboratórios implementados',
            'valor_alvo': 10,
            'valor_atual': 2,
            'data_limite': date(2025, 12, 31)
        },
        {
            'indicador': 'Milhões destinados para rodovias',
            'valor_alvo': 20,
            'valor_atual': 5,
            'data_limite': date(2025, 11, 30)
        },
        {
            'indicador': 'Câmeras de segurança instaladas',
            'valor_alvo': 50,
            'valor_atual': 0,
            'data_limite': date(2025, 10, 15)
        }
    ]

    for objetivo, meta_data in zip(objetivos_com_metas, metas_data):
        meta, created = MetaObjetivo.objects.get_or_create(
            objetivo=objetivo,
            indicador=meta_data['indicador'],
            defaults=meta_data
        )
        
        if created:
            print(f'  ✓ Criada meta: {meta.indicador} (alvo: {meta.valor_alvo})')

    print("\n" + "="*60)
    print("Dados de exemplo criados com sucesso!")
    print("="*60)
    print(f"📊 Total de mandatos: {Mandato.objects.count()}")
    print(f"📋 Total de planejamentos: {Planejamento.objects.count()}")
    print(f"🎯 Total de objetivos: {Objetivo.objects.count()}")
    print(f"📈 Total de metas: {MetaObjetivo.objects.count()}")
    print(f"👥 Total de usuários: {User.objects.count()}")
    print("\n💡 Usuários criados (senha: exemplo123):")
    for user in User.objects.all().order_by('mandato__nome_parlamentar', 'papel'):
        print(f"   • {user.username} ({user.get_papel_display()}) - {user.mandato.nome_parlamentar if user.mandato else 'Sem mandato'}")
    print("="*60)

if __name__ == '__main__':
    create_sample_data()
