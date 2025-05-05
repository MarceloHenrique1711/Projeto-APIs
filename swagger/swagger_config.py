from . import api
from swagger.namespace.aluno_namespace import alunos_ns
from swagger.namespace.turma_namespace import turmas_ns
from swagger.namespace.professor_namespace import professores_ns

# Função para registrar os namespaces
def configure_swagger(app):
    api.init_app(app)
    
    # Registra os namespace 
    api.add_namespace(alunos_ns, path="/alunos")
    api.add_namespace(turmas_ns, path="/turmas")
    api.add_namespace(professores_ns, path="/professores")

    api.mask_swagger = False