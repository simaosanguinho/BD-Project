# BD-Project
# Entrega 1
## 2022/2023

## Introdução
<p = align="justify">
Nesta primeira parte do projeto pretende-se conceber um modelo de base de dados para responder aos
requisitos de informação de uma aplicação cujo domínio é apresentado abaixo. O seu trabalho é
fornecer um modelo de dados conciso, coerente e organizado utilizando a notação gráfica modelo
Entidade-Associação, especificando também as Restrições de Integridade adequadas.
</p>

## Descrição do Domínio

<p = align="justify">
Uma empresa de comércio online pretende desenvolver um sistema de informação para gerir as suas
vendas. O sistema gere informação referente a clientes e às suas encomendas. Cada cliente é identificado perante
o sistema pelo seu e-mail e por um número de cliente. Os números de cliente são únicos e imutáveis.
Também é guardado o contacto telefónico do cliente e o seu nome e morada.
Cada cliente pode efectuar uma ou mais encomendas, mas uma encomenda só pode estar associada a
um cliente. Uma encomenda é constituída por diversos produtos. Para cada encomenda é necessário
registar a data da encomenda e o número de encomenda, sendo este último único e imutável. É
necessário registar também qual a quantidade encomendada de cada produto.
</p>
<p = align="justify">
Devido a restrições de privacidade, os operadores do sistema não podem ver os nomes dos clientes.
Cada cliente pode ter também diversos métodos de pagamento conhecidos pelo seu nome e que têm
como atributo um "token" de identificação perante a "gateway" de pagamento. Neste sistema os clientes
têm de introduzir mais do que um método de pagamento e cada método de pagamento tem de ter outro
método como substituto em caso de falha. Os métodos de pagamento são escolhidos de uma lista
conhecida à priori.
</p>
<p = align="justify">
Uma encomenda que é paga pelo cliente passa a ser uma venda. A venda é registrada sempre com o
método de pagamento do cliente que fez a encomenda, na data em que o cliente efetuou o pagamento.
Um cliente não pode pagar encomendas de outro cliente.
</p>
<p = align="justify">
Os produtos encomendados são identificados por um código alfanumérico conhecido como SKU ("stock
keeping unit") e têm um nome, uma descrição e um preço. Podem existir produtos com o mesmo nome.
Alguns produtos têm código EAN (informalmente conhecido como 'código de barras'). Existem
fornecedores dos produtos com nome, endereço e identificação fiscal (Tax Identification Number) para
fins de faturação. Cada fornecedor tem de ter um contrato para fornecer cada produto que fornece,
estabelecido numa determinada data. No âmbito de cada contrato os produtos podem ser entregues em
um ou mais armazéns espalhados pelo país.
</p>
<p = align="justify">
As encomendas são processadas por empregados. Relativamente a cada empregado é necessário
registar o nome, data de nascimento, NIF, e número da segurança social. Os empregados trabalham em
departamentos e locais de trabalho, podendo estes últimos ser escritórios e/ou armazéns, espalhados de norte a sul do país. Todos os locais de trabalho têm um endereço e uma localização com coordenadas
GPS conhecidas. Note-se que não é possível associar um empregado a um departamento sem o associar
também a um local de trabalho, nem é possível associar um empregado a um local de trabalho sem o
associar também a um departamento.
</p>

## Trabalho a desenvolver

1. Desenhe um diagrama de modelo de Entidade-Associação para o domínio de problemas
apresentado na secção anterior.

2. Identifique as situações inconsistentes no domínio do problema, mas que são permitidas no
modelo de Entidade-Associação apresentadas, e defina um conjunto de Restrições de
Integridade que completam o modelo proposto de forma a restringir situações inválidas.


## Aspectos importantes
<p = align="justify">
Tenha em mente os seguintes aspetos enquanto desenvolve o seu trabalho:
</p>
<p = align="justify">
* O modelo de Entidade-Associação deve ser expresso na notação lecionada nas aulas;
* As Restrições de Integridade ao modelo Entidade-Associação devem ser escritos como
afirmações (de obrigatoriedade ou de interdição) expressas em termos de conceitos no modelo
entidade-associação, ou seja, em termos de atributos, entidades e relações entre eles;
* A simplicidade e coerência do modelo serão avaliadas;
* A solução pode ser apresentada em Português ou em Inglês.
</p>
<p = align="justify">
NOTE: O diagrama deve ser desenhado numa ferramenta de diagramagem. Consulte as sugestões que se
encontram no slides da cadeira.
</p>
