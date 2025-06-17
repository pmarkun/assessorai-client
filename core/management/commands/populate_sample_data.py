from django.core.management.base import BaseCommand
from core.models import User, Mandato, Planejamento, Objetivo, MetaObjetivo
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo'

    def handle(self, *args, **options):
        self.stdout.write('Criando dados de exemplo...')

        # Criar Mandato
        mandato, created = Mandato.objects.get_or_create(
            nome_parlamentar="João Silva",
            defaults={
                'casa_legislativa': Mandato.CasaLegislativa.CM,
                'cargo': Mandato.Cargo.VEREADOR,
                'estado': 'SP',
                'municipio': 'São Paulo',
                'posicionamento': Mandato.Posicionamento.CENTRO,
                'perfil': Mandato.Perfil.LEGISLADOR,
                'primeiro_mandato': True
            }
        )
        
        if created:
            self.stdout.write(f'✓ Criado mandato: {mandato.nome_parlamentar}')
        else:
            self.stdout.write(f'→ Mandato já existia: {mandato.nome_parlamentar}')

        # Criar usuário assessor
        user, created = User.objects.get_or_create(
            username='assessor1',
            defaults={
                'email': 'assessor1@example.com',
                'first_name': 'Maria',
                'last_name': 'Santos',
                'funcao': 'Assessora Parlamentar',
                'papel': User.Papel.ASSESSOR,
                'mandato': mandato
            }
        )
        
        if created:
            user.set_password('123456')
            user.save()
            self.stdout.write(f'✓ Criado usuário: {user.get_full_name()}')
        else:
            self.stdout.write(f'→ Usuário já existia: {user.get_full_name()}')

        # Criar Planejamento
        planejamento, created = Planejamento.objects.get_or_create(
            mandato=mandato,
            defaults={
                'oportunidades': 'Crescimento da população jovem no município, aumento da demanda por tecnologia na educação.',
                'fraquezas': 'Baixo orçamento para projetos de lei, equipe pequena.',
                'temas_interesse': 'Educação, Tecnologia, Meio Ambiente, Saúde Pública',
                'objetivo_ano': 'Aprovar 3 projetos de lei voltados para educação digital'
            }
        )
        
        if created:
            self.stdout.write(f'✓ Criado planejamento para {mandato.nome_parlamentar}')
        else:
            self.stdout.write(f'→ Planejamento já existia para {mandato.nome_parlamentar}')

        # Criar Objetivos
        objetivos_data = [
            {'descricao': 'Implementar laboratórios de informática em 10 escolas municipais', 'ordem': 1},
            {'descricao': 'Criar programa de capacitação digital para professores', 'ordem': 2},
            {'descricao': 'Estabelecer parcerias com universidades locais', 'ordem': 3}
        ]

        for obj_data in objetivos_data:
            objetivo, created = Objetivo.objects.get_or_create(
                planejamento=planejamento,
                descricao=obj_data['descricao'],
                defaults={'ordem': obj_data['ordem']}
            )
            
            if created:
                self.stdout.write(f'  ✓ Criado objetivo: {objetivo.descricao[:50]}...')
                
                # Criar algumas metas para cada objetivo
                if obj_data['ordem'] == 1:  # Primeiro objetivo
                    MetaObjetivo.objects.get_or_create(
                        objetivo=objetivo,
                        indicador='Número de laboratórios implementados',
                        defaults={
                            'valor_alvo': 10,
                            'valor_atual': 2,
                            'data_limite': date.today() + timedelta(days=365)
                        }
                    )
                    MetaObjetivo.objects.get_or_create(
                        objetivo=objetivo,
                        indicador='Percentual de execução orçamentária',
                        defaults={
                            'valor_alvo': 100,
                            'valor_atual': 15,
                            'data_limite': date.today() + timedelta(days=300)
                        }
                    )
            else:
                self.stdout.write(f'  → Objetivo já existia: {objetivo.descricao[:50]}...')

        # Criar segundo mandato para exemplo
        mandato2, created = Mandato.objects.get_or_create(
            nome_parlamentar="Ana Costa",
            defaults={
                'casa_legislativa': Mandato.CasaLegislativa.ALE,
                'cargo': Mandato.Cargo.DEP_ESTADUAL,
                'estado': 'RJ',
                'posicionamento': Mandato.Posicionamento.CENTRO_ESQ,
                'perfil': Mandato.Perfil.FISCALIZADOR,
                'primeiro_mandato': False
            }
        )
        
        if created:
            self.stdout.write(f'✓ Criado mandato: {mandato2.nome_parlamentar}')

        self.stdout.write(
            self.style.SUCCESS('Dados de exemplo criados com sucesso!')
        )
