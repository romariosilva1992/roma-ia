# ROMA AI

API inicial para apoiar a criação de capítulos com módulos separados de pesquisa, escrita, revisão, estilo, memória e feedback.

## Executar localmente

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

A documentação interativa fica em `http://127.0.0.1:8000/docs`; a verificação de saúde fica em `/health`.
Abra `http://127.0.0.1:8000` no Google Chrome para usar a tela de criação de capítulos.

## Gerar capítulos com o OpenRouter

Abra o arquivo `.env` existente (ou copie `.env.example` para criá-lo), substitua o valor de `OPENROUTER_API_KEY` por uma chave nova e reinicie o servidor:

```env
OPENROUTER_API_KEY=sua-chave-nova
OPENROUTER_MODEL=openrouter/free
```

Não reutilize chaves que já foram compartilhadas em chats. O padrão `openrouter/free` tenta escolher um modelo gratuito disponível, mas disponibilidade, limites e velocidade variam conforme a conta e os modelos ativos. Você pode definir `OPENROUTER_MODEL` para outro identificador aceito; modelos como `openai/gpt-4o` podem exigir créditos. A chave é lida somente pelo backend e nunca deve ser colocada na tela do navegador.

## Publicar no Render

1. Envie o projeto para um repositório GitHub seu. Não inclua o arquivo `.env`; ele contém segredos e está excluído da imagem Docker.
2. No Render, selecione **New → Blueprint**, conecte o repositório e confirme a configuração de `render.yaml`.
3. Quando solicitado, informe `OPENROUTER_API_KEY` como variável secreta. Nunca coloque a chave no GitHub.
4. Aguarde o deploy e abra o endereço `onrender.com` exibido pelo Render.

O serviço usa o plano gratuito do Render; ele pode suspender a instância após inatividade e levar alguns segundos para acordar no primeiro acesso. Como o acesso ao app ficará público e sem senha, qualquer pessoa com o endereço poderá enviar solicitações usando a cota da chave OpenRouter configurada. O roteador `openrouter/free` e seus modelos disponíveis têm limites que podem variar. O armazenamento local de feedback no serviço gratuito não é persistente entre novos deploys.

## Endpoints

- `POST /api/v1/book/create`: gera um rascunho de capítulo a partir do título e do contexto fornecidos.
- `POST /api/v1/assistant/command`: envia um comando editorial ao OpenRouter usando o contexto e o texto atual do capítulo.
- `POST /api/v1/chapter/feedback`: registra o texto gerado e a versão editada em `data/feedback_logs.jsonl`.

Na tela, o assistente inclui atalhos para continuar, revisar, expandir, melhorar a escrita e resumir. A resposta fica separada até você escolher substituir ou acrescentar texto no editor. Os agentes de pesquisa e recuperação de conhecimento ainda são implementações locais demonstrativas; Supabase e banco vetorial não estão conectados.
