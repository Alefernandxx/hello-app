# Projeto: Pipeline CI/CD com GitHub Actions, ArgoCD e FastAPI

[cite_start]Este projeto demonstra a automação do ciclo completo de desenvolvimento, build, deploy e execução de uma aplicação FastAPI simples.

[cite_start]O objetivo é implementar práticas modernas de DevOps (especificamente GitOps) para entregar código com velocidade, segurança e consistência[cite: 8]. [cite_start]Para isso, utilizamos GitHub Actions para CI/CD, Docker Hub como registry de contêineres e ArgoCD para a entrega contínua em um cluster Kubernetes local (Rancher Desktop).

## 🏛️ Arquitetura e Fluxo

[cite_start]O fluxo de trabalho é totalmente automatizado e segue os princípios de GitOps, onde o Git é a única fonte da verdade.

1.  Um desenvolvedor faz um `git push` para o repositório `hello-app`.
2.  O **GitHub Actions** é acionado, constrói a imagem Docker da aplicação  e a envia para o **Docker Hub**[cite: 46].
3.  A mesma pipeline do GitHub Actions clona o repositório `hello-manifests` e atualiza o arquivo `deployment.yaml` para usar a nova tag da imagem que acabou de ser construída[cite: 47, 48].
4.  O **ArgoCD**, que está monitorando o repositório `hello-manifests`[cite: 64], detecta a mudança (o novo commit).
5.  O ArgoCD aplica automaticamente as mudanças ao cluster **Kubernetes**, realizando um *rolling update* dos pods para a nova versão da aplicação[cite: 67].

## 🛠️ Tecnologias Utilizadas

* **Aplicação:** FastAPI (Python 3) [cite: 33]
* **Containerização:** Docker [cite: 32]
* **Registry:** Docker Hub [cite: 25]
* **Cluster Local:** Rancher Desktop (com Kubernetes habilitado) [cite: 26]
* **Orquestração:** Kubernetes (`kubectl`) [cite: 27]
* **CI/CD (Automação):** GitHub Actions [cite: 6]
* **Entrega Contínua (GitOps):** ArgoCD [cite: 29]

## 📁 Estrutura do Projeto

Este projeto é dividido em dois repositórios Git, seguindo uma separação clara de responsabilidades (App vs. Infra):

1.  **`hello-app` (Este repositório)**
    * Contém o código-fonte da aplicação FastAPI (`main.py`, `requirements.txt`).
    * Inclui o `Dockerfile` para construir a imagem[cite: 35].
    * Armazena o workflow do GitHub Actions (`.github/workflows/cicd.yml`) que define o pipeline[cite: 45].

2.  **`hello-manifests` (Repositório separado)**
    * Contém *apenas* os manifestos Kubernetes (`deployment.yaml`, `service.yaml`)[cite: 36, 61].
    * Atua como a "fonte da verdade" para o estado desejado da infraestrutura, que é lido pelo ArgoCD.

## 📋 Pré-requisitos

Antes de começar, garanta que você possui:

* Conta no GitHub (repo público) [cite: 23]
* Conta no Docker Hub (e um Token de Acesso gerado) [cite: 25]
* Git instalado localmente [cite: 30]
* Rancher Desktop instalado e com Kubernetes habilitado [cite: 26]
* `kubectl` configurado e apontando para o contexto `rancher-desktop` [cite: 27]
* ArgoCD instalado no cluster [cite: 29]

## ⚙️ Configuração

1.  **Chaves SSH:**
    * Gere duas chaves SSH distintas (ex: `id_rsa_app` para seu uso pessoal e `id_rsa_manifests` para o bot de CI/CD).
    * Adicione `id_rsa_app.pub` à sua conta do GitHub (`Settings > SSH and GPG keys`).
    * Adicione `id_rsa_manifests.pub` como **Deploy Key** no repositório `hello-manifests` (`Settings > Deploy keys`) e marque **"Allow write access"**[cite: 53].

2.  **Configuração do `~/.ssh/config`:**
    * Configure seu arquivo `~/.ssh/config` local para que o Git saiba qual chave usar para cada repositório.

3.  **Segredos do GitHub Actions:**
    * No repositório `hello-app`, navegue até `Settings > Secrets and variables > Actions`.
    * Crie os três segredos de repositório a seguir[cite: 50, 51, 52]:
        * `DOCKER_USERNAME`: Seu nome de usuário do Docker Hub.
        * `DOCKER_PASSWORD`: Seu token de acesso do Docker Hub.
        * `SSH_PRIVATE_KEY`: O conteúdo completo da sua chave privada `id_rsa_manifests`.

4.  **Configuração do ArgoCD:**
    * Instale o ArgoCD no seu cluster (ex: `kubectl create namespace argocd` e `kubectl apply -f ...`).
    * Registre o repositório `hello-manifests` no ArgoCD (via UI ou YAML declarativo)[cite: 64].
    * Crie a aplicação `hello-app` no ArgoCD, apontando para o repositório `hello-manifests`, `PATH: /` e `DESTINATION: https://kubernetes.default.svc` (namespace `default`)[cite: 64].

## 🏁 Testando o Fluxo

1.  **Disparando o Pipeline (CI):**
    * Faça uma alteração no código da aplicação (ex: mude a mensagem em `main.py`)[cite: 67].
    * Faça o `commit` e `push` para a branch `main` do repositório `hello-app`.
    * Acompanhe a execução do pipeline na aba **Actions** do GitHub.

2.  **Observando o Deploy (CD):**
    * Após o pipeline ser concluído com sucesso, observe a UI do ArgoCD.
    * O ArgoCD detectará o novo commit no `hello-manifests` e mudará o status da aplicação para `Syncing`.
    * Em poucos instantes, a aplicação estará `Healthy` e sincronizada com a nova versão[cite: 67].

3.  **Acessando a Aplicação:**
    * Use `port-forward` para expor o serviço do Kubernetes localmente[cite: 66]:
        ```bash
        kubectl port-forward svc/hello-app-service 8080:80
        ```
    * Acesse `http://localhost:8080/` no seu navegador[cite: 66].
    * Você verá a mensagem atualizada que você enviou no seu último commit[cite: 67].
