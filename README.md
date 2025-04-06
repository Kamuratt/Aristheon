# Sistema de Gestão de Estoque Inteligente (MVP)

**Solução inovadora para controle de estoque, automação de compras e relatórios preditivos**  
[![Licença MIT](https://img.shields.io/badge/Licença-MIT-blue)](https://opensource.org/licenses/MIT)

---

## Índice
1. [Visão Geral](#visão-geral)
2. [Funcionalidades](#funcionalidades)
3. [Hierarquia de Usuários](#hierarquia-de-usuários)
4. [Stack Técnica](#stack-técnica)
5. [Modelagem de Dados](#modelagem-de-dados)
6. [Regras de Negócio](#regras-de-negócio)
7. [Design das Telas](#design-das-telas)
8. [Instalação e Uso](#instalação-e-uso)
9. [Roadmap](#roadmap)
10. [Contribuição](#contribuição)
11. [Contato](#contato)

---

## Visão Geral
O Sistema de Gestão de Estoque Inteligente é uma plataforma modular que combina controle de estoque em tempo real, automação de processos de compra e análise preditiva. Projetado para pequenas e médias empresas, o sistema oferece:

- **Controle hierárquico** com três níveis de acesso (Operador, Comprador, Gerente).  
- **Automação de solicitações de compra** baseada em limites de estoque.  
- **Relatórios inteligentes** para tomada de decisão estratégica.  
- **Integração futura** com ferramentas de mensagem (WhatsApp) e IoT.  

---

## Funcionalidades
### Módulo Básico (MVP)
- **Cadastro de Produtos**: Inclui nome, descrição, estoque mínimo/máximo, e fornecedor principal.  
- **Movimentação de Estoque**: Registro de entradas/saídas com data, responsável e observações.  
- **Solicitação de Compra (SC)**:  
  - Criação automática quando o estoque atinge o mínimo.  
  - Aprovação por Comprador (dentro do limite) ou Gerente (acima do limite).  
- **Ordem de Compra (OC)**:  
  - Geração de mapa de cotações com comparação de fornecedores.  
  - Aprovação hierárquica e rastreamento de status.  
- **Relatórios**:  
  - Estoque crítico.  
  - Histórico de movimentações.  
  - Análise de sazonalidade (versão futura).  

### Funcionalidades Futuras
- **Integração com WhatsApp**: Notificações automáticas de estoque baixo.  
- **Previsão de Demanda**: Modelos de IA para antecipar tendências.  
- **Controle de Validade**: Alertas para produtos perecíveis via sensores IoT.  

---

## Hierarquia de Usuários
| **Perfil**     | **Permissões**                                                                 |
|----------------|-------------------------------------------------------------------------------|
| **Operador**   | Registrar movimentações, criar SCs, visualizar estoque.                      |
| **Comprador**  | Aprovar SCs dentro do limite, criar OCs, gerenciar fornecedores.             |
| **Gerente**    | Aprovar SCs acima do limite, acessar relatórios avançados, gerenciar usuários. |

---

## Stack Técnica
### Backend
- **Linguagem**: Python 3.10+  
- **Framework**: FastAPI para construção de APIs RESTful.  
- **Banco de Dados**: PostgreSQL para dados estruturados e Redis para cache.  
- **Autenticação**: JWT com OAuth2 e criptografia AES-256.  

### Frontend
- **MVP**: Streamlit para prototipagem rápida.  
- **Versão Final**: React.js com Typescript e componentes modularizados.  

### IA/ML
- **Previsão de Demanda**: Facebook Prophet para séries temporais.  
- **Processamento de Dados**: Pandas e NumPy para manipulação de datasets.  

---

## Modelagem de Dados
### Entidades Principais
1. **Usuário**: Armazena dados de login, perfil e permissões.  
2. **Produto**: Contém informações de estoque, fornecedor e validade.  
3. **Fornecedor**: Registra CNPJ, contato e histórico de entregas.  
4. **Solicitação de Compra (SC)**: Vinculada a produtos e aprovadores.  
5. **Ordem de Compra (OC)**: Relacionada a fornecedores e status de entrega.  

### Relacionamentos
- Um **Operador** pode criar múltiplas SCs.  
- Um **Comprador** pode gerar várias OCs com base em cotações.  
- Cada **Produto** está vinculado a um fornecedor principal.  

---

## Regras de Negócio
### Gestão de Compras
1. **Criação de SC**:  
   - Bloqueada se o estoque atual estiver acima do mínimo.  
   - Requer aprovação do Gerente se a quantidade solicitada exceder o estoque máximo.  
2. **Aprovação de OC**:  
   - Exige comparação de pelo menos dois fornecedores.  
   - Notificação automática ao Comprador após aprovação.  
3. **Recebimento de Mercadorias**:  
   - Registro obrigatório dentro de 24 horas após a entrega.  
   - Geração automática de nova SC para itens faltantes.  

### Validações
- **CNPJ**: Validação automática de formato e dígitos verificadores.  
- **Estoque Mínimo/Máximo**: Não pode ser negativo ou igual.  

---

## Design das Telas
### Protótipos
- **Baixa Fidelidade**: Wireframes focados em usabilidade e fluxo de navegação.  
- **Alta Fidelidade**: Design final com paleta corporativa (azul, verde, vermelho) e componentes interativos.  

### Telas Principais
1. **Dashboard**:  
   - Visão consolidada do estoque, SCs pendentes e alertas.  
   - Gráficos interativos de tendências de consumo.  
2. **Detalhes da SC/OC**:  
   - Histórico de aprovações, justificativas e comentários.  
   - Anexos de documentos (ex: mapas de cotação).  
3. **Relatórios Personalizados**:  
   - Filtros por período, produto ou fornecedor.  
   - Exportação em PDF/CSV para auditoria.  

---

## Instalação e Uso
### Pré-requisitos
- Docker e Docker Compose instalados.  
- Conta em um serviço de cloud (AWS, GCP) para deploy.  

### Passos Iniciais
1. Clone o repositório e acesse a pasta do projeto.  
2. Configure as variáveis de ambiente no arquivo `.env`.  
3. Execute `docker-compose up` para iniciar os containers.  
4. Acesse o frontend via `http://localhost:8501`.  

---

## Roadmap
| **Versão** | **Previsão** | **Destaques**                                  |
|------------|--------------|-----------------------------------------------|
| 1.0        | Q3 2024      | MVP com módulo básico de estoque e compras.    |
| 2.0        | Q4 2024      | Integração com IA e WhatsApp.                 |
| 3.0        | Q1 2025      | Controle de validade via IoT e dashboard mobile. |

---

✨ **Agradecemos seu interesse em nosso projeto!** ✨
