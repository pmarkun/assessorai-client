from typing import List, Dict

def sidebar_menu(request) -> Dict[str, List[Dict]]:
    menu = [
        {
            "title": "Gerencie",
            "items": [
                {"name": "Planejamento de Mandato", "url_name": "core:meu_planejamento"},
                {"name": "Organização da Equipe", "url_name": "core:equipe"},
                {"name": "Gestão de Tarefas (em breve)", "disabled": True},
            ],
        },
        {
            "title": "Produza",
            "items": [
                {"name": "Ofícios (em breve)", "disabled": True},
                {"name": "Emendas de Projetos", "url_name": "expert_pl:sugestao_emendas"},
                {"name": "Legislação (em breve)", "disabled": True},
            ],
        },
    ]
    return {"sidebar_menu": menu}

