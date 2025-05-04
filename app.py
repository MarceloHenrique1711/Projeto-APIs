#python -m venv *nome do ambiente*
#./*nome do ambiente*/Scripts/Activate
#pip install flask
#pip install requests

import os
from config import app
from alunos.alunos_route import alunos_blueprint
from professores.professores_route import professor_blueprint
from turmas.turmas_route import turma_blueprint, reseta_blueprint, resetaTurma_blueprint
from config import app,db
from swagger.swagger_config import configure_swagger


app.register_blueprint(alunos_blueprint)
app.register_blueprint(professor_blueprint)
app.register_blueprint(turma_blueprint)
app.register_blueprint(reseta_blueprint)
app.register_blueprint(resetaTurma_blueprint)

configure_swagger(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
  app.run(
        host=app.config["HOST"],
        port = app.config['PORT'],
        debug=app.config['DEBUG'],
        
    )

