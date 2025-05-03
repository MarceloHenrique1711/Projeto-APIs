#Tabela de Códigos de Status HTTP

#100	Continue	O cliente pode continuar com a requisição.

#200	OK	Requisição bem-sucedida.

#201	Created	Recurso criado com sucesso (ex: POST)

#204	No Content	Requisição bem-sucedida, mas sem conteúdo para retornar.

#404	Not Found	Recurso não encontrado.

#python -m testes.teste

import requests #pip install requests
import unittest


class TestStringMethods(unittest.TestCase):
    professor = requests.post('http://localhost:5000/professores',json= {

            "nome":"felipe",
            "idade": 22,
            "materia": "TESTE",
            "observacoes": "sos"
  })
    
    def teste_000_verifica_se_a_rota_turma_existe(self):
        r=requests.get('http://localhost:5000/turmas')
        
        if r.status_code == 404:
            self.fail("Voce não definiu a rota ou digitou a rota errado")

        self.assertEqual(r.status_code, 200, "A rota turma foi nao esta respondendo como deveria") #assertEqual verifica se dois valores são iguais. No nosso caso se a API esta retornando 200 valor correto, Se não forem, ele quebra o teste e mostra a mensagem de erro.
            
    def teste_001_reseta_turmas(self):
        r = requests.post('http://localhost:5000/turmas', json={
            "ativo": True,
            "descricao": "",
            "id": 1,
            "professor_id": 1
            })
         
        r_reseta = requests.post('http://localhost:5000/resetaTurma') #reseta nome da ROTA MUDAR AMANHA 
        self.assertEqual(r_reseta.status_code,200)
         
        r_lista_depois = requests.get('http://localhost:5000/turmas')
        self.assertEqual(len(r_lista_depois.json()),0)
    
    def teste_002_adiciona_turma_POST(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma')  #A Turma continua armazenado dos outros testes por isso esta limpando tudo
        self.assertEqual(reseta_lista.status_code, 200, "A rota reseta não retornou o status 200. Verifique se ela está implementada corretamente.")

        r = requests.post('http://localhost:5000/turmas',json= {
            "id":1,
            "descricao": "123",
            "professor_id": 1,
            "ativo": True
        
  })
        self.assertEqual(r.status_code, 201, "A rota POST turmas não retornou 201 como esperado. Verifique se foi criado corretamente")
        r_lista =requests.get('http://localhost:5000/turmas')
        lista_retorna = r_lista.json()
        
        achei_Turma = False
        for turma in lista_retorna:
            if turma['id'] == 1:
                achei_Turma = True

        if not achei_Turma:
            self.fail('A turma não foi adicionada na lista de turmas')

    def teste_003_delete_turma(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma')  #A Turma continua armazenado dos outros testes por isso esta limpando tudo
        self.assertEqual(reseta_lista.status_code, 200, "A rota reseta não retornou o status 200. Verifique se ela está implementada corretamente.")

        r_cria = requests.post('http://localhost:5000/turmas', json={  
            "id":1,
            "descricao": "",
            "professor_id": 1,
            "ativo": True
        })
        self.assertEqual(r_cria.status_code, 201, "A rota POST turmas não retornou 201 como esperado. Verifique se foi criado corretamente")

        requests.delete('http://localhost:5000/turmas/1')

        retorno_lista = requests.get('http://localhost:5000/turmas')
        lista_retornada = retorno_lista.json()
        
        acheiTurma = any(turma['id'] == 1 for turma in lista_retornada) #O any é uma função do Python que retorna True se pelo menos um item de um iterável (como uma lista ou um for) for True

        if acheiTurma: # Se o *ANY* aparecer true entra esse if
            self.fail("A turma 1 ainda está na lista. O delete nao funcionou")

    def teste_004_editar_turma(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma')  #A Turma continua armazenado dos outros testes por isso esta limpando tudo
        self.assertEqual(reseta_lista.status_code, 200, "A rota reseta não retornou o status 200. Verifique se ela está implementada corretamente.")

        requests.post('http://localhost:5000/turmas', json={  
            "id":1,
            "descricao": "",
            "professor_id": 1,
            "ativo": True
            })   

        lista_antiga = requests.get('http://localhost:5000/turmas/1')
        self.assertEqual(lista_antiga.json()['id'],1)
         
        requests.put('http://localhost:5000/turmas/1', json={  
            "descricao": "asd",
            "professor_id": 1,
            "ativo": True          
            })  
        
        lista_depois = requests.get('http://localhost:5000/turmas/1')
        self.assertEqual(lista_depois.json()['descricao'],'asd')

    def teste_005_id_nao_existe_no_put(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma')  #A Turma continua armazenado dos outros testes por isso esta limpando tudo
        self.assertEqual(reseta_lista.status_code, 200, "A rota reseta não retornou o status 200. Verifique se ela está implementada corretamente.")

        r = requests.put('http://localhost:5000/turmas/1', json={"descricao": "oi"})
        self.assertEqual(r.status_code, 404)

    def teste_006_id_nao_existe_no_get(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma')  #A Turma continua armazenado dos outros testes por isso esta limpando tudo
        self.assertEqual(reseta_lista.status_code, 200, "A rota reseta não retornou o status 200. Verifique se ela está implementada corretamente.")

        r = requests.get('http://localhost:5000/turmas/1')
        self.assertEqual(r.status_code, 404)

    def teste_007_id_nao_existe_no_delete(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma') 
        self.assertEqual(reseta_lista.status_code, 200)

        r = requests.delete('http://localhost:5000/turmas/1')
        self.assertEqual(r.status_code, 404)



    def teste_012_post_com_ativo_vazio(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma') 
        self.assertEqual(reseta_lista.status_code, 200)

        resultado = requests.post('http://localhost:5000/turmas', json={  
            "descricao": "",
            "id": 1,
            "professor_id": 1,
            "ativo": "true"
        })

        self.assertEqual(resultado.status_code, 400)

    def teste_013_post_sem_professor_id(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma') 
        self.assertEqual(reseta_lista.status_code, 200)

        resposta = requests.post('http://localhost:5000/turmas', json={
            "ativo": True,
            "descricao": "",
            "id": 1,
            "professor_id" : ""
        })

        self.assertEqual(resposta.status_code, 400)

    def teste_014_post_com_descricao_acima_caracteres_validos(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma') 
        self.assertEqual(reseta_lista.status_code, 200)

        resposta = requests.post('http://localhost:5000/turmas', json={
            "ativo": True,
            "descricao": "oi" * 100,
            "id": 1,
            "professor_id": 1 
        })

        self.assertEqual(resposta.status_code, 400)

    def teste_015_put_com_descricao_acima_caracteres_validos(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma') 
        self.assertEqual(reseta_lista.status_code, 200)

        resposta_post = {
            "ativo": True,
            "descricao": "",
            "id": 1,
            "professor_id": 1 
        }
        resposta_create = requests.post('http://localhost:5000/turmas', json=resposta_post)
        self.assertEqual(resposta_create.status_code, 201)

        resposta_put = requests.put('http://localhost:5000/turmas/1', json={
            "ativo": True,
            "descricao": "oi" * 100,
            "professor_id": 1 
        })

        self.assertEqual(resposta_put.status_code, 400)

    def teste_016_post_descricao_sem_ser_string(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma') 
        self.assertEqual(reseta_lista.status_code, 200)

        resposta = requests.post('http://localhost:5000/turmas', json={
           "ativo": True,
            "descricao": 111,
            "id": 1,
            "professor_id": 1 
        })

        self.assertEqual(resposta.status_code, 400)

    def teste_017_put_descricao_sem_ser_string(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma') 
        self.assertEqual(reseta_lista.status_code, 200)

        resposta_post = {
            "ativo": True,
            "descricao": "oi",
            "id": 1,
            "professor_id": 1 
        }
        resposta_create = requests.post('http://localhost:5000/turmas', json=resposta_post)
        self.assertEqual(resposta_create.status_code, 201)


        resposta_put = requests.put('http://localhost:5000/turmas/1', json={
            "ativo": True,
            "descricao": 123,
            "id": 1,
            "professor_id": 1 
        })

        self.assertEqual(resposta_put.status_code, 400)

    def teste_018_post_sem_o_professor_existir(self):
        reseta_lista = requests.post('http://localhost:5000/resetaTurma') 
        self.assertEqual(reseta_lista.status_code, 200)

        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        resposta = requests.post('http://localhost:5000/turmas', json={
           "ativo": True,
            "descricao": "",
            "id": 1,
            "professor_id": 1 
        })
        self.assertEqual(resposta.status_code, 400)


def runTests():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()