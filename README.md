# Projeto: Pipeline CI/CD com GitHub Actions, ArgoCD e FastAPI

Este projeto demonstra a automação do ciclo completo de desenvolvimento, build, deploy e execução de uma aplicação FastAPI simples.

O objetivo é implementar práticas modernas de DevOps (especificamente GitOps) para entregar código com velocidade, segurança e consistência. Para isso, utilizamos GitHub Actions para CI/CD, Docker Hub como registry de contêineres e ArgoCD para a entrega contínua em um cluster Kubernetes local (Rancher Desktop).

## 🏛️ Arquitetura e Fluxo

O fluxo de trabalho é totalmente automatizado e segue os princípios de GitOps, onde o Git é a única fonte da verdade.

1.  Um desenvolvedor faz um `git push` para o repositório `hello-app`.
2.  O **GitHub Actions** é acionado, constrói a imagem Docker da aplicação e a envia para o **Docker Hub**.
3.  A mesma pipeline do GitHub Actions clona o repositório `hello-manifests` e atualiza o arquivo `deployment.yaml` para usar a nova tag da imagem que acabou de ser construída.
4.  O **ArgoCD**, que está monitorando o repositório `hello-manifests`, detecta a mudança (o novo commit).
5.  O ArgoCD aplica automaticamente as mudanças ao cluster **Kubernetes**, realizando um *rolling update* dos pods para a nova versão da aplicação.

## 🛠️ Tecnologias Utilizadas

* **Aplicação:** FastAPI (Python 3)
* **Containerização:** Docker
* **Registry:** Docker Hub
* **Cluster Local:** Rancher Desktop (com Kubernetes habilitado)
* **Orquestração:** Kubernetes (`kubectl`)
* **CI/CD (Automação):** GitHub Actions
* **Entrega Contínua (GitOps):** ArgoCD

## 📁 Estrutura do Projeto

Este projeto é dividido em dois repositórios Git, seguindo uma separação clara de responsabilidades (App vs. Infra):

1.  **`hello-app` (Este repositório)**
    * Contém o código-fonte da aplicação FastAPI (`main.py`, `requirements.txt`).
    * Inclui o `Dockerfile` para construir a imagem.
    * Armazena o workflow do GitHub Actions (`.github/workflows/cicd.yml`) que define o pipeline.

2.  **`hello-manifests` (Repositório separado)**
    * Contém *apenas* os manifestos Kubernetes (`deployment.yaml`, `service.yaml`).
    * Atua como a "fonte da verdade" para o estado desejado da infraestrutura, que é lido pelo ArgoCD.

## 📋 Pré-requisitos

Antes de começar, garanta que você possui:

* Conta no GitHub (repo público)
* Conta no Docker Hub (e um Token de Acesso gerado)
* Git instalado localmente
* Rancher Desktop instalado e com Kubernetes habilitado
* `kubectl` configurado e apontando para o contexto `rancher-desktop`
* ArgoCD instalado no cluster

## ⚙️ Configuração

1.  **Chaves SSH:**
    * Gere duas chaves SSH distintas (ex: `id_rsa_app` para seu uso pessoal e `id_rsa_manifests` para o bot de CI/CD).
    * Adicione `id_rsa_app.pub` à sua conta do GitHub (`Settings > SSH and GPG keys`).
    * Adicione `id_rsa_manifests.pub` como **Deploy Key** no repositório `hello-manifests` (`Settings > Deploy keys`) e marque **"Allow write access"**.

2.  **Configuração do `~/.ssh/config`:**
    * Configure seu arquivo `~/.ssh/config` local para que o Git saiba qual chave usar para cada repositório.

3.  **Segredos do GitHub Actions:**
    * No repositório `hello-app`, navegue até `Settings > Secrets and variables > Actions`.
    * Crie os três segredos de repositório a seguir:
        * `DOCKER_USERNAME`: Seu nome de usuário do Docker Hub.
        * `DOCKER_PASSWORD`: Seu token de acesso do Docker Hub.
        * `SSH_PRIVATE_KEY`: O conteúdo completo da sua chave privada `id_rsa_manifests`.

4.  **Configuração do ArgoCD:**
    * Instale o ArgoCD no seu cluster (ex: `kubectl create namespace argocd` e `kubectl apply -f ...`).
    * Registre o repositório `hello-manifests` no ArgoCD (via UI ou YAML declarativo).
    * Crie a aplicação `hello-app` no ArgoCD, apontando para o repositório `hello-manifests`, `PATH: /` e `DESTINATION: https://kubernetes.default.svc` (namespace `default`).

## 🏁 Testando o Fluxo

1.  **Disparando o Pipeline (CI):**
    * Faça uma alteração no código da aplicação (ex: mude a mensagem em `main.py`).
    * Faça o `commit` e `push` para a branch `main` do repositório `hello-app`.
    * Acompanhe a execução do pipeline na aba **Actions** do GitHub.

2.  **Observando o Deploy (CD):**
    * Após o pipeline ser concluído com sucesso, observe a UI do ArgoCD.
    * O ArgoCD detectará o novo commit no `hello-manifests` e mudará o status da aplicação para `Syncing`.
    * Em poucos instantes, a aplicação estará `Healthy` e sincronizada com a nova versão.

3.  **Acessando a Aplicação:**
    * Use `port-forward` para expor o serviço do Kubernetes localmente:
        ```bash
        kubectl port-forward svc/hello-app-service 8080:80
        ```
    * Acesse `http://localhost:8080/` no seu navegador.
    * Você verá a mensagem atualizada que você enviou no seu último commit.
