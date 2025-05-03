# Tabela de Códigos de Status HTTP
# 100  Continue O cliente pode continuar com a requisição.
# 200  OK  Requisição bem-sucedida.
# 201  Created Recurso criado com sucesso (ex: POST)
# 204  No Content Requisição bem-sucedida, mas sem conteúdo para retornar.
# 404  Not Found Recurso não encontrado.

#python -m testes.teste

import requests #pip install requests
import unittest


class TestProfessorAPI(unittest.TestCase):

    def setUp(self):
        """
        Configuração inicial para cada teste.
        """
        self.base_url = 'http://localhost:5000/professores'
        self.reset_url = 'http://localhost:5000/reseta'
        self.reset_database()

    def reset_database(self):
        """
        Reseta o banco de dados para um estado limpo antes de cada teste.
        """
        reseta_lista = requests.post(self.reset_url)
        self.assertEqual(reseta_lista.status_code, 200, "A rota /reseta não está funcionando corretamente.")

    def test_000_verifica_se_a_rota_professores_existe(self):
        """
        Verifica se a rota /professores existe e retorna o código de status correto.
        """
        resultado = requests.get(self.base_url)
        self.assertEqual(resultado.status_code, 200, "A rota /professores não está respondendo como deveria.")

    def test_001_adiciona_professor_POST(self):
        """
        Adiciona um professor via POST e verifica se ele foi adicionado corretamente.
        """
        professor_data = {
            "nome": "Nicolas",
            "idade": 30,
            "materia": "Portugues",
            "observacoes": ""
        }
        r = requests.post(self.base_url, json=professor_data)
        self.assertEqual(r.status_code, 201, "A rota POST /professores não retornou 201 como esperado.")

        r_lista = requests.get(self.base_url)
        lista_retorna = r_lista.json()

        achei_Nicolas = any(professor['nome'] == 'Nicolas' for professor in lista_retorna)
        self.assertTrue(achei_Nicolas, 'O professor Nicolas não foi adicionado na lista de professores')

    def test_002_lista_professores(self):
        """
        Verifica se a lista de professores está sendo retornada corretamente.
        """
        r = requests.get(self.base_url)
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list, "A resposta não é uma lista.")

    def test_003_delete_professor(self):
        """
        Deleta um professor e verifica se ele foi removido corretamente.
        """
        professor_data = {
            "nome": "Samuel",
            "idade": 27,
            "materia": "matemática",
            "observacoes": ""
        }
        r_cria = requests.post(self.base_url, json=professor_data)
        self.assertEqual(r_cria.status_code, 201)

        delete_url = f'{self.base_url}/1'
        r_delete = requests.delete(delete_url)
        self.assertEqual(r_delete.status_code, 200)

        retorno_lista = requests.get(self.base_url)
        lista_retornada = retorno_lista.json()

        acheiSamuel = any(professor['nome'] == 'Samuel' for professor in lista_retornada)
        self.assertFalse(acheiSamuel, "O professor Samuel ainda está na lista. O delete não funcionou.")

    def test_004_editar_professor(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Edita um professor existente e verifica se as alterações foram aplicadas corretamente.
        """
        professor_data = {
            "nome": "Matheus",
            "idade": 30,
            "materia": "Portugues",
            "observacoes": ""
        }
        resposta_create = requests.post(self.base_url, json=professor_data)
        self.assertEqual(resposta_create.status_code, 201)

        professor_data_editado = {
            "nome": "Octavio",
            "idade": 30,
            "materia": "Portugues",
            "observacoes": ""
        }
        put_url = f'{self.base_url}/1'
        resposta_put = requests.put(put_url, json=professor_data_editado)
        self.assertIn(resposta_put.status_code, [200, 201])

        lista_depois = requests.get(f'{self.base_url}/1')
        self.assertEqual(lista_depois.status_code, 200)
        self.assertEqual(lista_depois.json()['nome'], 'Octavio')

    def test_005_id_nao_existe_no_put(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta editar um professor com um ID que não existe e verifica se retorna o erro correto.
        """
        r = requests.put(f'{self.base_url}/1', json={'nome': 'MINEIRO', 'id': 1})
        self.assertIn(r.status_code, [400, 404])

        resposta = r.json()
        self.assertIn('erro', resposta)
        self.assertEqual(resposta['erro'], 'Professor não encontrado')

    def test_006_id_nao_existe_no_get(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta obter um professor com um ID que não existe e verifica se retorna o erro correto.
        """
        r = requests.get(f'{self.base_url}/1')
        self.assertIn(r.status_code, [400, 404])

        resposta = r.json()
        chave_erro = next((key for key in resposta.keys() if key.strip() == 'erro'), None)
        self.assertIsNotNone(chave_erro, "A chave 'erro' não foi encontrada na resposta.")
        self.assertEqual(resposta[chave_erro].strip(), 'Professor não encontrada')

    def test_007_id_nao_existe_no_delete(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta deletar um professor com um ID que não existe e verifica se retorna o erro correto.
        """
        r = requests.delete(f'{self.base_url}/15')
        self.assertIn(r.status_code, [400, 404])

        resposta = r.json()
        chave_erro = next((key for key in resposta.keys() if key.strip() == 'erro'), None)
        self.assertIsNotNone(chave_erro, "A chave 'erro' não foi encontrada na resposta.")
        self.assertEqual(resposta[chave_erro].strip(), 'Professor não encontrada')

    
    def test_009_put_sem_o_nome(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta atualizar um professor sem o nome e verifica se retorna o erro correto.
        """
        professor_data = {
            "nome": "Gabriel Martins",
            "idade": 31,
            "materia": "Portugues",
            "observacoes": ""
        }
        resposta_create = requests.post(self.base_url, json=professor_data)
        self.assertEqual(resposta_create.status_code, 201)

        resposta_update = requests.put(f'{self.base_url}/1', json={
            "idade": 31,
            "materia": "Portugues",
            "observacoes": ""
        })

        self.assertEqual(resposta_update.status_code, 400)
        resposta = resposta_update.json()
        self.assertIn('erro', resposta)
        self.assertEqual(resposta['erro'], "O campo 'nome' é obrigatório e deve ser uma string válida")

    def test_010_post_sem_nome(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta criar um professor sem o nome e verifica se retorna o erro correto.
        """
        resposta = requests.post(self.base_url, json={
            "idade": 31,
            "materia": "Portugues",
            "observacoes": ""
        })
        self.assertEqual(resposta.status_code, 400)
        resposta = resposta.json()
        self.assertIn('erro', resposta)
        self.assertEqual(resposta['erro'], "O campo 'nome' é obrigatório")

    def test_011_professor_sem_idade_post(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta criar um professor sem a idade e verifica se retorna o erro correto.
        """
        resultado = requests.post(self.base_url, json={
            "nome": "Gabriel Martins",
            "materia": "Portugues",
            "observacoes": "",
        })

        self.assertEqual(resultado.status_code, 400)
        resposta = resultado.json()
        self.assertIn("erro", resposta)
        self.assertEqual(resposta["erro"], "O campo 'idade' deve ser um número inteiro positivo")

    def test_012_professor_sem_idade_put(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta atualizar um professor sem a idade e verifica se retorna o erro correto.
        """
        # Cria um professor
        professor_data = {
            "nome": "Gabriel Martins",
            "idade": 31,
            "materia": "Portugues",
            "observacoes": ""
        }
        resposta_create = requests.post(self.base_url, json=professor_data)
        self.assertEqual(resposta_create.status_code, 201)

        # Tenta atualizar sem a idade
        resposta_update = requests.put(f'{self.base_url}/1', json={
            "nome": "Gabriel Martins",
            "materia": "Portugues",
            "observacoes": "",
        })

        self.assertEqual(resposta_update.status_code, 400)
        resposta = resposta_update.json()
        self.assertIn('erro', resposta)
        self.assertEqual(resposta['erro'], "O campo 'idade' deve ser um número inteiro positivo")

    def test_015_post_com_nome_vazio(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta criar um professor com um nome vazio e verifica se retorna o erro correto.
        """
        resultado = requests.post(self.base_url, json={
            "nome": "",
            "idade": 31,
            "materia": "Portugues",
            "observacoes": ""
        })

        self.assertEqual(resultado.status_code, 400)
        resposta = resultado.json()
        self.assertIn("erro", resposta)
        self.assertEqual(resposta["erro"], "O campo 'nome' é obrigatório")

    def test_016_put_com_nome_vazio(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta atualizar um professor com um nome vazio e verifica se retorna o erro correto.
        """
        # Cria um professor válido
        professor_data = {
            "nome": "Gabriel Martins",
            "idade": 31,
            "materia": "Portugues",
            "observacoes": ""
        }
        resposta_create = requests.post(self.base_url, json=professor_data)
        self.assertEqual(resposta_create.status_code, 201)

        # Tenta atualizar com nome vazio (apenas espaços)
        resposta_update = requests.put(f'{self.base_url}/1', json={
            "id": 7,
            "nome": "",
            "idade": 31,
            "materia": "Portugues",
            "observacoes": ""
        })

        self.assertEqual(resposta_update.status_code, 400)
        resposta = resposta_update.json()
        self.assertIn("erro", resposta)
        self.assertEqual(resposta["erro"], "O campo 'nome' é obrigatório e deve ser uma string válida")

    def test_017_post_com_materia_acima_caracteres_validos(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta criar um professor com uma matéria que excede o limite de caracteres e verifica se retorna o erro correto.
        """
        # Matéria com mais de 100 caracteres
        resposta = requests.post(self.base_url, json={
            "nome": "caio",
            "idade": 31,
            "materia": "Algoritmos e Programação" * 10,  # 100 caracteres
            "observacoes": ""
        })

        self.assertEqual(resposta.status_code, 400)
        resposta_json = resposta.json()
        self.assertIn("erro", resposta_json)
        self.assertEqual(resposta_json["erro"].strip(), "O campo 'materia' tem que ser string e no máximo 100 caracteres")

    def test_018_put_com_materia_acima_caracteres_validos(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta atualizar um professor com uma matéria que excede o limite de caracteres e verifica se retorna o erro correto.
        """
        # Primeiro cria um professor válido
        professor_data = {
            "nome": "João Pedro",
            "idade": 30,
            "materia": "Algoritmos e Programação",
            "observacoes": ""
        }
        resposta_create = requests.post(self.base_url, json=professor_data)
        self.assertEqual(resposta_create.status_code, 201)

        # Agora tenta atualizar com uma matéria inválida (mais de 100 caracteres)
        resposta_put = requests.put(f'{self.base_url}/1', json={
            "id": 8,
            "nome": "João Pedro",
            "idade": 30,
            "materia": "Algoritmos e Programação" * 10,  # 100 caracteres
            "observacoes": ""
        })

        self.assertEqual(resposta_put.status_code, 400)
        resposta_json = resposta_put.json()
        self.assertIn("erro", resposta_json)
        self.assertEqual(resposta_json["erro"], "O campo 'materia' deve ser uma string com no máximo 100 caracteres")

    def test_019_post_observacoes_sem_ser_string(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta criar um professor com observações que não são uma string e verifica se retorna o erro correto.
        """
        resposta = requests.post(self.base_url, json={
            "nome": "João Pedro",
            "idade": 30,
            "materia": "Algoritmos e Programação",
            "observacoes": 12345  # Não é uma string
        })

        self.assertEqual(resposta.status_code, 400)
        resposta_json = resposta.json()
        self.assertIn("erro", resposta_json)
        self.assertEqual(resposta_json["erro"], "O campo 'observacoes' deve ser uma string")

    def test_020_put_observacoes_sem_ser_string(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        """
        Tenta atualizar um professor com observações que não são uma string e verifica se retorna o erro correto.
        """
        # Primeiro cria um professor válido
        professor_data = {
            "nome": "João Pedro",
            "idade": 30,
            "materia": "Algoritmos e Programação",
            "observacoes": "teste"
        }
        resposta_create = requests.post(self.base_url, json=professor_data)
        self.assertEqual(resposta_create.status_code, 201)

        # Agora tenta atualizar com observações inválidas (não é uma string)
        resposta_put = requests.put(f'{self.base_url}/1', json={
            "nome": "João Pedro",
            "idade": 30,
            "materia": "Algoritmos e Programação",
            "observacoes": 12345  # Não é uma string
        })

        self.assertEqual(resposta_put.status_code, 400)
        resposta_json = resposta_put.json()
        self.assertIn("erro", resposta_json)
        self.assertEqual(resposta_json["erro"], "O campo 'observacoes' deve ser uma string")


def runTests():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestProfessorAPI)
    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)


if __name__ == '__main__':
    runTests()