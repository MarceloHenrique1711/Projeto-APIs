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
    
    turma = requests.post('http://localhost:5000/turmas',json= {

            "descricao": "Teste",
            "professor_id": 1,
            "ativo": True
  })
    def teste_000_verifica_se_a_rota_aluno_existe(self):
        resultado=requests.get('http://localhost:5000/alunos')
        
        if resultado.status_code == 404:
            self.fail("Voce não definiu a rota ou digitou a rota errado")

        self.assertEqual(resultado.status_code, 200, "A rota aluno foi nao esta respondendo como deveria") #assertEqual verifica se dois valores são iguais. No nosso caso se a API esta retornando 200 valor correto, Se não forem, ele quebra o teste e mostra a mensagem de erro.
            
    
    def teste_001_adiciona_aluno_POST(self):
        r = requests.post('http://localhost:5000/alunos',json= {

            "nome": "Nicolas",
            "data_de_nascimento": "14_10_2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10
  })
        r_lista =requests.get('http://localhost:5000/alunos')
        lista_retorna = r_lista.json()
        
        achei_Nicolas = False
        for aluno in lista_retorna:
            if aluno['nome'] == 'Nicolas':
                achei_Nicolas = True

        if not achei_Nicolas:
            self.fail('O aluno Nicolas nao foi adicionado na lista de alunos')

    def teste_002_reseta_alunos(self):
        r = requests.post('http://localhost:5000/alunos', json={
            "id": 11,
            "nome": "Nicolas",
            "data_de_nascimento": "14_10_2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10,
            })
     
        r_lista = requests.get('http://localhost:5000/alunos') 
        self.assertTrue(len(r_lista.json()) > 0)           #e a condição len(Aluno criado no POST) > 0 for verdadeira, o teste passa. Se for falsa, o teste falha.
         
        r_reseta = requests.post('http://localhost:5000/reseta') #reseta nome da ROTA MUDAR AMANHA 
        self.assertEqual(r_reseta.status_code,200)
         
        r_lista_depois = requests.get('http://localhost:5000/alunos')
        self.assertEqual(len(r_lista_depois.json()),0)
 
         
    def teste_003_delete_aluno(self): 
        reseta_lista = requests.post('http://localhost:5000/reseta')  #O Aluno continua armazenado dos outros testes por isso esta limpando tudo
        self.assertEqual(reseta_lista.status_code, 200, "A rota reseta não retornou o status 200. Verifique se ela está implementada corretamente.")

        r_cria = requests.post('http://localhost:5000/alunos', json={  
            "nome": "Samuel",
            "data_de_nascimento": "14_10_2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10
        })
        self.assertEqual(r_cria.status_code, 201, "A rota POST alunos não retornou 201 como esperado. Verifique se foi criado corretamente")

        requests.delete('http://localhost:5000/alunos/1')

        retorno_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = retorno_lista.json()
        
        acheiSamuel = any(aluno['nome'] == 'Samuel' for aluno in lista_retornada) #O any é uma função do Python que retorna True se pelo menos um item de um iterável (como uma lista ou um for) for True

        if acheiSamuel: # Se o *ANY* aparecer true entra esse if
            self.fail("O aluno Samuel ainda está na lista. O delete nao funcionou")

    def teste_004_editar_aluno(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code,200)
        
        requests.post('http://localhost:5000/alunos', json={  
            "nome": "Matheus",
            "data_de_nascimento": "14_10_2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10
            })   

        lista_antiga = requests.get('http://localhost:5000/alunos/1')
        self.assertEqual(lista_antiga.json()['nome'],'Matheus')
         
        requests.put('http://localhost:5000/alunos/1', json={  
            "nome": "Octavio",
            "data_de_nascimento": "14_10_2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10           
            })  
         
        lista_depois = requests.get('http://localhost:5000/alunos/1')
        self.assertEqual(lista_depois.json()['nome'],'Octavio')
        self.assertEqual(lista_depois.json()['id'],1)

    def teste_005_id_nao_existe_no_put(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        r = requests.put('http://localhost:5000/alunos/1', json={'nome': 'MINEIRO', 'id': 1})
        self.assertIn(r.status_code, [400, 404])

        resposta = r.json()
        self.assertIn('erro', resposta)
        self.assertEqual(resposta['erro'], 'Aluno não encontrado')

    def teste_006_id_nao_existe_no_get(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        r = requests.get('http://localhost:5000/alunos/1')
        self.assertIn(r.status_code, [400, 404])

        resposta = r.json()
        self.assertIn('erro', resposta)
        self.assertEqual(resposta['erro'], 'Aluno não encontrada')

    def teste_007_id_nao_existe_no_delete(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        r = requests.delete('http://localhost:5000/alunos/15')
        self.assertIn(r.status_code, [400, 404])

        resposta = r.json()
        self.assertIn('erro', resposta)
        self.assertEqual(resposta['erro'], 'Aluno não encontrada')


    

    def teste_009_put_sem_o_nome(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        resposta_create = requests.post('http://localhost:5000/alunos', json={  
            "nome": "Gabriel Martins",
            "data_de_nascimento": "14_10_2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10  
        })
        self.assertEqual(resposta_create.status_code, 201)

        resposta_update = requests.put('http://localhost:5000/alunos/1', json={  
            "data_de_nascimento": "14_10_2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10  
        })
        
        self.assertIn(resposta_update.status_code, [400, 422])  # código de erro esperado
        resposta = resposta_update.json()
        self.assertIn('erro', resposta)
        self.assertEqual(resposta['erro'], 'Preencha o nome novamente')
  
    def teste_010_post_sem_nome(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code,200)

        resposta = requests.post('http://localhost:5000/alunos', json={  
            "data_de_nascimento": "14_10_2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10  
            })
        self.assertEqual(resposta.status_code,400)

    def teste_011_aluno_sem_dataNasci_post(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        resultado = requests.post('http://localhost:5000/alunos', json={  
            "nome": "Gabriel Martins",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10  
        })

        self.assertEqual(resultado.status_code, 400)
        resposta = resultado.json()
        self.assertIn("erro", resposta)
        self.assertEqual(resposta["erro"], 'Data de nascimento é obrigatória')


    def teste_012_aluno_sem_dataNasc_put(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        resposta_create = requests.post('http://localhost:5000/alunos', json={  
            "nome": "Gabriel Martins",
            "data_de_nascimento": "14_10_2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10  
        })
        self.assertEqual(resposta_create.status_code, 201)
        
        resposta_update = requests.put('http://localhost:5000/alunos/1', json={  

            "nome": "Gabriel Martins",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10  
        })
        
        self.assertEqual(resposta_update.status_code, 400)
        resposta = resposta_update.json()
        self.assertIn('erro', resposta)
        self.assertEqual(resposta['erro'], 'Data de nascimento é obrigatória')

   
    def teste_015_post_com_nome_vazio(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        resultado = requests.post('http://localhost:5000/alunos', json={  
            "nome": "", 
            "data_de_nascimento": "12_05_2005",
            "turma_id": 1,
            "nota_primeiro_semestre": 9,
            "nota_segundo_semestre": 8
        })

        self.assertEqual(resultado.status_code, 400)
        resposta = resultado.json()
        self.assertIn("erro", resposta)
        self.assertEqual(resposta["erro"], 'Preencha o nome')
    
    def teste_016_put_com_nome_vazio(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        resposta_create = requests.post('http://localhost:5000/alunos', json={  
            "nome": "Gabriel Martins",
            "data_de_nascimento": "14_10_2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10  
        })
        self.assertEqual(resposta_create.status_code, 201)

        resposta_update = requests.put('http://localhost:5000/alunos/1', json={  
            "nome": "",
            "data_de_nascimento": "14_10_2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10  
        })

        self.assertEqual(resposta_update.status_code, 400)
        resposta = resposta_update.json()
        self.assertIn("erro", resposta)
        self.assertEqual(resposta["erro"], 'Preencha o nome novamente')

    def teste_017_post_com_data_nasc_invalida(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)
        
        resposta = requests.post('http://localhost:5000/alunos', json={
            "nome": "caio",
            "data_de_nascimento": "14-10-2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10 
        })

        self.assertEqual(resposta.status_code, 400)
        resposta_json = resposta.json()
        self.assertIn("erro", resposta_json)
        self.assertEqual(resposta_json["erro"], 'Formato inválido. Use "dd_mm_aaaa", como "10_10_2000"')

    def teste_018_put_com_data_nasc_invalida(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        resposta_create = requests.post('http://localhost:5000/alunos', json={
            "nome": "João Pedro",
            "data_de_nascimento": "22_10_2004",
            "turma_id": 1,
            "nota_primeiro_semestre": 9,
            "nota_segundo_semestre": 8
        })
        self.assertEqual(resposta_create.status_code, 201)

        # Agora tenta atualizar com data de nascimento em formato inválido
        resposta_put = requests.put('http://localhost:5000/alunos/1', json={
            "nome": "João Pedro",
            "data_de_nascimento": "2004-10-10",  # formato inválido
            "turma_id": 1,
            "nota_primeiro_semestre": 9,
            "nota_segundo_semestre": 8
        })
        
        self.assertEqual(resposta_put.status_code, 400)
        resposta_json = resposta_put.json()
        self.assertIn("erro", resposta_json)
        self.assertEqual(resposta_json["erro"], 'Formato inválido. Use "DD_MM_YYYY", exemplo 10_10_2020')

    def teste_019_post_sem_turma_id(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        resposta = requests.post('http://localhost:5000/alunos', json={
            "nome": "João Pedro",
            "turma_id": "",
            "data_de_nascimento":  "10_10_2004",
            "nota_primeiro_semestre": 9,
            "nota_segundo_semestre": 8
        })

        self.assertEqual(resposta.status_code, 400)
        resposta_json = resposta.json()
        self.assertIn("erro", resposta_json)
        self.assertEqual(resposta_json["erro"], "O campo 'turma_id' é obrigatório e deve ser um inteiro")

    def teste_020_put_sem_turma_id(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        resposta_create = requests.post('http://localhost:5000/alunos', json={
            "nome": "João Pedro",
            "turma_id": 1,
            "data_de_nascimento": "10_10_2004",
            "nota_primeiro_semestre": 9,
            "nota_segundo_semestre": 8
        })
        self.assertEqual(resposta_create.status_code, 201)

        resposta_update = requests.put('http://localhost:5000/alunos/1', json={
            "nome": "João Pedro",  
            "data_de_nascimento": "10_10_2004",
            "nota_primeiro_semestre": 9,
            "nota_segundo_semestre": 8
        })

        self.assertEqual(resposta_update.status_code, 400)
        resposta_json = resposta_update.json()
        self.assertIn("erro", resposta_json)
        self.assertEqual(resposta_json["erro"], "O campo 'turma_id' é obrigatório.")

    def teste_021_post_com_notas_fora_intervalo(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        # Teste 1: nota_primeiro_semestre maior que 10
        resposta1 = requests.post('http://localhost:5000/alunos', json={
            "nome": "SAYMUEL",
            "turma_id": 1,
            "data_de_nascimento": "10_10_2004",
            "nota_primeiro_semestre": 11,  
            "nota_segundo_semestre": 8
        })
        self.assertEqual(resposta1.status_code, 400)
        resposta_json1 = resposta1.json()
        self.assertIn("erro", resposta_json1)
        self.assertEqual(resposta_json1["erro"], "Nota do primeiro semestre deve ser um número entre 0 e 10")

        # Teste 2: nota_segundo_semestre negativa
        resposta2 = requests.post('http://localhost:5000/alunos', json={
            "nome": "SAMUEL",
            "turma_id": 1,
            "data_de_nascimento": "10_10_2004",
            "nota_primeiro_semestre": 8,
            "nota_segundo_semestre": -10
        })
        self.assertEqual(resposta2.status_code, 400)
        resposta_json2 = resposta2.json()
        self.assertIn("erro", resposta_json2)
        self.assertEqual(resposta_json2["erro"], "Nota do segundo semestre deve ser um número entre 0 e 10")


    def teste_022_put_com_notas_fora_intervalo(self):
        reseta_lista = requests.post('http://localhost:5000/reseta')
        self.assertEqual(reseta_lista.status_code, 200)

        resposta_create = requests.post('http://localhost:5000/alunos', json={
            "nome": "Aluno de Teste",
            "turma_id": 1,
            "data_de_nascimento": "10_10_2004",
            "nota_primeiro_semestre": 8,
            "nota_segundo_semestre": 9
        })
        self.assertEqual(resposta_create.status_code, 201)

        resposta_put1 = requests.put('http://localhost:5000/alunos/1', json={
            "nome": "Aluno de Teste",
            "turma_id": 1,
            "data_de_nascimento": "10_10_2004",
            "nota_primeiro_semestre": 11,
            "nota_segundo_semestre": 8
        })
        self.assertEqual(resposta_put1.status_code, 400)
        resposta_json1 = resposta_put1.json()
        self.assertIn("erro", resposta_json1)
        self.assertEqual(resposta_json1["erro"], "Nota do primeiro semestre deve ser um número entre 0 e 10")

        resposta_put2 = requests.put('http://localhost:5000/alunos/1', json={
            "nome": "Aluno de Teste",
            "turma_id": 1,
            "data_de_nascimento": "10_10_2004",
            "nota_primeiro_semestre": 8,
            "nota_segundo_semestre": -5
        })
        self.assertEqual(resposta_put2.status_code, 400)
        resposta_json2 = resposta_put2.json()
        self.assertIn("erro", resposta_json2)
        self.assertEqual(resposta_json2["erro"], "Nota do segundo semestre deve ser um número entre 0 e 10")

    def teste_023_post_sem_a_turma_existir(self):
            reseta_lista = requests.post('http://localhost:5000/resetaTurma') 
            self.assertEqual(reseta_lista.status_code, 200)

            reseta_lista = requests.post('http://localhost:5000/reseta')
            self.assertEqual(reseta_lista.status_code, 200)

            r = requests.post('http://localhost:5000/alunos',json= {
                "nome": "Nicolas",
                "data_de_nascimento": "14_10_2004",
                "turma_id": 1,
                "nota_primeiro_semestre": 10,
                "nota_segundo_semestre": 10,
    })
            self.assertEqual(r.status_code, 400)

def runTests():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()