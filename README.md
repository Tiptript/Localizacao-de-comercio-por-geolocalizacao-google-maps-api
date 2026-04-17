Extrator de Dados Geográficos
Google Maps API
Documentação Técnica do Script buscar.py
1. Descrição
Script em Python desenvolvido para automatizar a extração de dados de estabelecimentos comerciais utilizando a API do Google Maps. A ferramenta realiza buscas baseadas em palavras-chave dentro de um raio geográfico específico a partir de um endereço base. O script processa os dados de retorno e gera um arquivo CSV formatado para importação direta no Google My Maps.

Dados extraídos por estabelecimento:
•	Nome comercial
•	Endereço formatado
•	Telefone de contato
•	Latitude e Longitude (coordenadas geográficas)
•	Termo de busca que originou o resultado

2. Pré-Requisitos
2.1 Ambiente de Execução
•	Python 3.x instalado no sistema
2.2 Bibliotecas Necessárias
googlemaps
pandas
2.3 Credenciais do Google Cloud Console
•	Chave de API válida (API_KEY)
•	Geocoding API ativada — converte o endereço base em coordenadas
•	Places API ativada — realiza a busca dos estabelecimentos

3. Instalação de Dependências
Execute o comando abaixo no terminal para instalar os pacotes necessários:

pip install googlemaps pandas

4. Configuração
Antes da execução, altere os parâmetros no bloco de configurações do arquivo buscar.py:

Parâmetro	Tipo	Descrição / Exemplo
API_KEY	String	Chave de API do Google Cloud Console
ENDERECO	String	Endereço central (marco zero) da busca. Ex: 'Av. Paulista, 1000, São Paulo'
RAIO_METROS	Inteiro	Raio de abrangência em metros. Ex: 5000 para um raio de 5 km
PALAVRAS_CHAVE	Lista	Termos de busca. Ex: ['marcenaria', 'móveis planejados', 'carpintaria']

5. Execução
Inicie o script via linha de comando a partir do diretório onde o arquivo buscar.py está localizado:

python buscar.py

6. Estrutura de Saída (Output)
O script gera um arquivo nomeado marcenarias_para_mapa.csv no diretório de execução. O uso da vírgula como delimitador e a codificação UTF-8 garantem compatibilidade nativa com a ferramenta de importação do Google My Maps.

Coluna	Descrição
Nome	Nome comercial do estabelecimento registrado no Google Places.
Endereco	Endereço completo e formatado do local.
Telefone	Número de contato. Retorna 'Não informado' caso ausente.
Latitude	Coordenada Y — necessária para georreferenciamento no mapa.
Longitude	Coordenada X — necessária para georreferenciamento no mapa.
Termo	Palavra-chave específica que originou o retorno do estabelecimento.

7. Tratamento de Exceções Integrado
7.1 Validação de Geocoding
O script valida se o endereço base fornecido pode ser convertido em coordenadas geográficas antes de iniciar o loop de busca. Caso o endereço seja inválido ou não reconhecido, a execução é interrompida com uma mensagem de erro descritiva.
7.2 Controle de Paginação
Implementa uma pausa de 2 segundos (timeout exigido pela documentação oficial do Google) entre chamadas sequenciais que utilizam o page_token. Isso previne bloqueios por excesso de requisições por segundo (rate limiting).
7.3 Eliminação de Duplicatas
Utiliza um conjunto (set) de place_id para garantir que estabelecimentos retornados em múltiplas palavras-chave sejam registrados apenas uma vez no arquivo final, evitando entradas redundantes.

Observações Importantes
•	O uso da API do Google Maps pode gerar custos conforme o volume de requisições. Consulte a tabela de preços no Google Cloud Console.
•	A Places API retorna no máximo 60 resultados por consulta (3 páginas de 20). Para coberturas mais amplas, utilize múltiplas palavras-chave ou subdivida o raio de busca.
•	Mantenha a API_KEY em variáveis de ambiente ou arquivos .env — nunca a exponha em repositórios públicos.
