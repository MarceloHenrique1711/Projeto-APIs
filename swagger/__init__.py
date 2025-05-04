from flask_restx import Api

# Inicializa o objeto API do Swagger
api = Api(
    version="1.0",
    title="API de Gestão Escolar",
    description="Documentação da API para Alunos, Professores e Turmas",
    doc="/docs", 	#Define a URL onde o Swagger estará disponível. Exemplo: http://localhost:5000/docs
    mask_swagger=False,  # Desativa o X-Fields no Swagger,
    #prefix="/api"
)