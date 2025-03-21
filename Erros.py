from flask import jsonify

# Classes de erro personalizadas
class IdDuplicadoError(Exception):
    """Erro para IDs duplicados"""
    pass

class IdNegativoError(Exception):
    """Erro para IDs negativos"""
    pass

# Função que registra os handlers no app
def registrar_handlers(app):
    @app.errorhandler(IdDuplicadoError)
    def id_duplicado(error):
        response = jsonify({"erro": str(error)})
        response.status_code = 400
        return response

    @app.errorhandler(IdNegativoError)
    def id_negativo(error):
        response = jsonify({"erro": str(error)})
        response.status_code = 400
        return response



