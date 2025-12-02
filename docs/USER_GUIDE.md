# 📖 Guia de Uso dos Agentes - RENUM

Este guia explica como usar o sistema RENUM para criar e gerenciar agentes de IA, conduzir entrevistas e executar comandos administrativos.

---

## 🎯 Visão Geral

O RENUM permite criar agentes de IA especializados para diferentes propósitos:
- **Pesquisas e Entrevistas** (Discovery Agent)
- **Marketing Multinível** (MMN Agent)
- **Atendimento ao Cliente** (Support Agent)
- **Agentes Personalizados** (Custom Agents)

---

## 🤖 Como Criar Sub-Agentes

### Passo 1: Acessar o Painel

1. Faça login no dashboard: `http://localhost:5173/auth/login`
2. No menu lateral, clique em **"Configuração RENUS"**
3. Selecione a aba **"Sub-Agentes"**

### Passo 2: Criar Novo Sub-Agente

1. Clique no botão **"+ Novo Sub-Agente"**
2. Preencha o formulário:

#### Campos Obrigatórios

**Nome do Sub-Agente**
```
Exemplo: "Pesquisa MMN Discovery"
```
- Use um nome descritivo
- Será usado para identificar o agente

**System Prompt**
```
Exemplo:
Você é um pesquisador especializado em Marketing Multinível.
Seu objetivo é conduzir entrevistas para entender as dores e 
necessidades dos distribuidores.

Mantenha um tom profissional mas amigável.
Faça perguntas abertas e escute atentamente.
```
- Define o comportamento do agente
- Seja específico sobre o objetivo
- Inclua tom e estilo desejados

#### Campos Opcionais

**Descrição**
```
Agente especializado em entrevistar distribuidores de MMN
```

**Canal de Atendimento**
- ☑️ WhatsApp (recomendado para pesquisas)
- ☐ Site (recomendado para suporte)

**Modelo de IA**
- Padrão do Agente Principal (usa config global)
- Claude Sonnet 4 (melhor qualidade, mais caro)
- GPT-4o Mini (econômico, boa qualidade)
- Llama 3.1 8B (gratuito, qualidade básica)

**Tópicos/Contextos Principais**
```
Exemplos:
- Prospecção
- Atendimento
- Treinamento
- Automação
- Investimento
```
- Adicione palavras-chave relevantes
- Ajuda o agente a entender o contexto

### Passo 3: Configurar e Ativar

1. Revise todas as configurações
2. Toggle **"Status Inicial"** para ativar imediatamente
3. Clique em **"Criar Sub-Agente"**

### Passo 4: Obter URL Pública

Após criar, o agente terá uma URL pública:
```
http://localhost:5173/chat/pesquisa-mmn-discovery
```

Compartilhe esta URL com seus leads para iniciar conversas!

---

## 📝 Como Conduzir Entrevistas

### Método 1: Via URL Pública (Recomendado)

1. Crie um sub-agente do tipo "Discovery"
2. Copie a URL pública gerada
3. Envie a URL para seus leads via:
   - WhatsApp
   - Email
   - SMS
   - Redes sociais

**Exemplo de mensagem:**
```
Olá! Estamos fazendo uma pesquisa rápida sobre [tema].
Suas respostas nos ajudarão a melhorar nossos serviços.

Clique aqui para participar (5 minutos):
http://localhost:5173/chat/pesquisa-mmn-discovery

Obrigado!
```

### Método 2: Via Dashboard Admin

1. Acesse **"Entrevistas"** no menu
2. Clique em **"Nova Entrevista"**
3. Selecione:
   - Lead (contato)
   - Projeto (campanha)
   - Sub-Agente
4. Clique em **"Iniciar Entrevista"**

### Acompanhamento em Tempo Real

1. Vá em **"Entrevistas"** → **"Em Andamento"**
2. Clique em uma entrevista para ver:
   - Mensagens trocadas
   - Status atual
   - Tempo decorrido
   - Taxa de conclusão

### Análise de Resultados

1. Após conclusão, vá em **"Entrevistas"** → **"Concluídas"**
2. Clique em uma entrevista
3. Visualize:
   - Transcrição completa
   - Análise automática por IA
   - Insights extraídos
   - Score de qualificação

---

## 💬 Comandos da ISA

ISA (Intelligent System Assistant) é seu assistente administrativo com IA.

### Como Acessar

1. No dashboard, clique em **"Assistente ISA"** no menu
2. Ou pressione **Ctrl+K** (atalho rápido)

### Comandos Disponíveis

#### Gerenciamento de Clientes

```
Liste todos os clientes ativos
```
Retorna lista de clientes com status ativo

```
Mostre detalhes do cliente [nome]
```
Exibe informações completas de um cliente específico

```
Crie novo cliente com nome [nome] e email [email]
```
Cria um novo registro de cliente

#### Gerenciamento de Leads

```
Liste os 10 leads com maior score
```
Retorna leads mais qualificados

```
Mostre leads sem atividade nos últimos 7 dias
```
Identifica leads inativos

```
Exporte leads do projeto [nome]
```
Gera arquivo CSV com leads

#### Entrevistas e Pesquisas

```
Inicie pesquisa [nome] com 50 contatos da lista [nome]
```
Inicia campanha de pesquisa em lote

```
Pause todas as entrevistas ativas
```
Pausa todas as entrevistas em andamento

```
Mostre estatísticas das entrevistas de hoje
```
Exibe métricas do dia

```
Gere relatório das pesquisas da última semana
```
Cria relatório consolidado

#### Sub-Agentes

```
Crie novo sub-agente chamado [nome]
```
Inicia criação de sub-agente (modo assistido)

```
Liste todos os sub-agentes
```
Mostra todos os agentes configurados

```
Ative/Desative sub-agente [nome]
```
Altera status do agente

#### Relatórios e Analytics

```
Mostre estatísticas gerais do sistema
```
Dashboard com métricas principais

```
Gere relatório mensal de uso
```
Relatório completo do mês

```
Mostre uso de tokens e custos
```
Análise de consumo e gastos

```
Exporte dados de [período]
```
Exporta dados para análise externa

#### Mensagens em Lote

```
Envie mensagem para todos os leads ativos: [mensagem]
```
Disparo em massa via WhatsApp

```
Agende mensagem para [data] às [hora]: [mensagem]
```
Agendamento de envio

### Dicas de Uso

✅ **Seja específico**
```
❌ "mostre clientes"
✅ "Liste todos os clientes ativos criados nos últimos 30 dias"
```

✅ **Use linguagem natural**
```
✅ "Quantos leads temos hoje?"
✅ "Qual foi a taxa de resposta ontem?"
✅ "Me mostre as entrevistas que não foram concluídas"
```

✅ **Combine comandos**
```
"Liste os 20 leads com maior score e exporte para CSV"
```

---

## 🎨 Personalização de Agentes

### Ajustando o Tom

**Formal:**
```
Você é um assistente profissional. Use linguagem formal,
evite gírias e mantenha distância respeitosa.
```

**Casual:**
```
Você é um amigo prestativo. Use linguagem descontraída,
seja empático e crie conexão genuína.
```

**Técnico:**
```
Você é um especialista técnico. Use terminologia precisa,
forneça detalhes técnicos e seja objetivo.
```

### Definindo Objetivos

**Pesquisa:**
```
Seu objetivo é coletar informações através de perguntas
abertas. Não venda nada, apenas escute e registre.
```

**Vendas:**
```
Seu objetivo é qualificar o lead e agendar uma reunião.
Identifique dores, apresente benefícios e crie urgência.
```

**Suporte:**
```
Seu objetivo é resolver problemas rapidamente.
Seja paciente, faça diagnóstico e ofereça soluções.
```

### Adicionando Conhecimento

Use o campo **"Tópicos/Contextos"** para adicionar conhecimento específico:

```
Tópicos:
- Produtos: [lista de produtos]
- Preços: [tabela de preços]
- Políticas: [políticas da empresa]
- FAQ: [perguntas frequentes]
```

---

## 📊 Monitoramento e Otimização

### Métricas Importantes

**Taxa de Resposta**
- Meta: > 60%
- Como melhorar: Otimize o primeiro contato

**Taxa de Conclusão**
- Meta: > 80%
- Como melhorar: Reduza número de perguntas

**Tempo Médio**
- Meta: < 10 minutos
- Como melhorar: Perguntas mais diretas

**Satisfação**
- Meta: > 4.0/5.0
- Como melhorar: Tom mais empático

### A/B Testing

1. Crie 2 versões do mesmo agente
2. Direcione 50% do tráfego para cada
3. Compare métricas após 100 conversas
4. Mantenha a versão com melhor performance

### Iteração Contínua

1. **Semana 1:** Lance versão inicial
2. **Semana 2:** Analise primeiras 50 conversas
3. **Semana 3:** Ajuste prompts baseado em feedback
4. **Semana 4:** Teste nova versão
5. **Repita** o ciclo mensalmente

---

## ❓ FAQ

### Como sei se meu agente está funcionando bem?

Verifique estas métricas:
- Taxa de conclusão > 70%
- Tempo médio < 15 minutos
- Satisfação > 4.0/5.0
- Leads qualificados > 30%

### Posso usar o mesmo agente para múltiplos propósitos?

Não recomendado. Crie agentes especializados:
- 1 agente = 1 objetivo claro
- Melhor performance
- Mais fácil de otimizar

### Quantos agentes posso criar?

Sem limite! Mas recomendamos:
- Começar com 2-3 agentes
- Otimizar antes de escalar
- Máximo 10 agentes ativos simultaneamente

### Como treino meu agente?

O agente aprende através do System Prompt. Para melhorar:
1. Analise conversas reais
2. Identifique padrões de sucesso
3. Atualize o prompt com exemplos
4. Teste e itere

### Posso integrar com meu CRM?

Sim! Use a API do RENUM:
- Webhook para novos leads
- API para criar entrevistas
- Export automático de dados

---

## 🆘 Suporte

### Problemas Comuns

**Agente não responde**
- Verifique se está ativo
- Confirme que tem créditos na OpenRouter
- Veja logs de erro no dashboard

**Respostas genéricas**
- Melhore o System Prompt
- Adicione mais contexto
- Use exemplos específicos

**Taxa de conclusão baixa**
- Reduza número de perguntas
- Simplifique linguagem
- Adicione motivação

### Contato

- **Email:** suporte@renum.com
- **WhatsApp:** +55 11 99999-9999
- **Discord:** https://discord.gg/renum

---

**Última atualização:** 2024-01-01  
**Versão:** 1.0.0
