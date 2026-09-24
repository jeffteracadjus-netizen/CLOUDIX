const modules = {

    dashboard: {
        title: "Dashboard"
    },

    vendas: {
        title: "Vendas",
        label: "VENDAS",
        pageTitle: "Inteligência de Vendas",
        icon: "fa-chart-line"
    },

    marketing: {
        title: "Marketing",
        label: "MARKETING",
        pageTitle: "Inteligência de Marketing",
        icon: "fa-bullhorn"
    },

    financeiro: {
        title: "Financeiro",
        label: "FINANCEIRO",
        pageTitle: "Inteligência Financeira",
        icon: "fa-wallet"
    },

    atendimento: {
        title: "Atendimento",
        label: "ATENDIMENTO",
        pageTitle: "Inteligência de Atendimento",
        icon: "fa-headset"
    },

    estrategia: {
        title: "Estratégia",
        label: "ESTRATÉGIA",
        pageTitle: "Inteligência Estratégica",
        icon: "fa-chess"
    }

};


/* ==========================================================
   OBTER TOKEN DE AUTENTICAÇÃO DO NAVEGADOR
   ========================================================== */

function getAuthToken() {
    // Procura por chaves comuns onde o token JWT possa ter sido gravado
    return localStorage.getItem("token") ||
           localStorage.getItem("access_token") ||
           localStorage.getItem("user_token") ||
           localStorage.getItem("jwt") ||
           sessionStorage.getItem("token") ||
           sessionStorage.getItem("access_token");
}


/* ==========================================================
   VERIFICAÇÃO DE SESSÃO AO CARREGAR A PÁGINA
   ========================================================== */

document.addEventListener("DOMContentLoaded", () => {
    const token = getAuthToken();
    
    // Se não houver token salvo, você pode redirecionar o usuário para a página de login
    // Basta descomentar a linha abaixo ajustando a rota do seu login:
    /*
    if (!token && window.location.pathname !== "/login") {
        window.location.href = "/login";
    }
    */
});


/* ==========================================================
   SELECIONAR MÓDULO
   ========================================================== */

function selectModule(moduleName, button = null) {

    if (moduleName === "dashboard") {
        showDashboard();
        return;
    }

    const module = modules[moduleName];

    if (!module) {
        return;
    }

    const dashboardEl = document.querySelector("#dashboard");
    const modulePageEl = document.querySelector("#module-page");

    if (dashboardEl) dashboardEl.classList.remove("active-section");
    if (modulePageEl) modulePageEl.classList.add("active-section");

    const pageTitle = document.querySelector("#page-title");
    if (pageTitle) pageTitle.innerText = module.title;

    const selectedLabel = document.querySelector("#selected-module-label");
    if (selectedLabel) selectedLabel.innerText = module.label;

    const selectedTitle = document.querySelector("#selected-module-title");
    if (selectedTitle) selectedTitle.innerText = module.pageTitle;

    const icon = document.querySelector("#selected-module-icon i");
    if (icon) icon.className = "fa-solid " + module.icon;

    document.querySelectorAll(".nav-item").forEach(item => {
        item.classList.remove("active");
    });

    if (button) {
        button.classList.add("active");
    } else {
        const navButton = document.querySelector(`.nav-item[onclick*="'${moduleName}'"]`);
        if (navButton) navButton.classList.add("active");
    }

}


/* ==========================================================
   DASHBOARD
   ========================================================== */

function showDashboard() {

    const dashboardEl = document.querySelector("#dashboard");
    const modulePageEl = document.querySelector("#module-page");

    if (modulePageEl) modulePageEl.classList.remove("active-section");
    if (dashboardEl) dashboardEl.classList.add("active-section");

    const pageTitle = document.querySelector("#page-title");
    if (pageTitle) pageTitle.innerText = "Dashboard";

    document.querySelectorAll(".nav-item").forEach(item => {
        item.classList.remove("active");
    });

    const buttons = document.querySelectorAll(".nav-item");
    buttons.forEach(button => {
        if (button.innerText.toLowerCase().includes("dashboard")) {
            button.classList.add("active");
        }
    });

}


/* ==========================================================
   CHAT REAL DA CLOUDIX AI
   ========================================================== */

async function sendMessage() {

    const input = document.querySelector("#chat-input");
    if (!input) return;

    const message = input.value.trim();
    if (!message) return;

    const chatInputArea = document.querySelector(".chat-input");
    const parentContainer = chatInputArea ? chatInputArea.parentElement : document.body;

    // 1. Inserir a mensagem do usuário no chat
    const userMessage = document.createElement("div");
    userMessage.style.display = "flex";
    userMessage.style.justifyContent = "flex-end";
    userMessage.style.marginTop = "10px";

    userMessage.innerHTML = `
        <div
            style="
                background: rgba(86,90,166,0.15);
                border: 1px solid rgba(86,90,166,0.25);
                padding: 12px 15px;
                border-radius: 10px 0 10px 10px;
                max-width: 600px;
                color: #b9c1d0;
                font-size: 11px;
            "
        >
            ${escapeHtml(message)}
        </div>
    `;

    if (chatInputArea) {
        parentContainer.insertBefore(userMessage, chatInputArea);
    } else {
        parentContainer.appendChild(userMessage);
    }

    input.value = "";

    // 2. Inserir o balão de carregamento da CLOUDIX AI
    const aiMessage = document.createElement("div");
    aiMessage.className = "chat-message";

    aiMessage.innerHTML = `
        <div class="ai-avatar">
            C
        </div>
        <div class="message-bubble">
            <strong>CLOUDIX AI</strong>
            <p class="ai-text-response">
                <em>Analisando sua solicitação...</em>
            </p>
        </div>
    `;

    if (chatInputArea) {
        parentContainer.insertBefore(aiMessage, chatInputArea);
    } else {
        parentContainer.appendChild(aiMessage);
    }

    const textContainer = aiMessage.querySelector(".ai-text-response");
    const token = getAuthToken();

    if (!token) {
        textContainer.innerHTML = `
            <span style="color: #ff6b6b;">
                <strong>Sessão não encontrada:</strong> Faça login na plataforma para utilizar a CLOUDIX AI.
            </span>
        `;
        return;
    }

    try {
        const response = await fetch("/ai/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ message: message })
        });

        if (response.status === 401) {
            textContainer.innerHTML = `
                <span style="color: #ff6b6b;">
                    <strong>Sessão expirada:</strong> Por favor, faça login novamente no sistema.
                </span>
            `;
            return;
        }

        const data = await response.json();

        if (response.ok) {
            let replyText = "";
            if (data.response && typeof data.response === "object" && data.response.text) {
                replyText = data.response.text;
            } else if (typeof data.response === "string") {
                replyText = data.response;
            } else {
                replyText = data.message || "Resposta processada.";
            }

            textContainer.innerHTML = formatMarkdown(replyText);
        } else {
            textContainer.innerHTML = `
                <span style="color: #ff6b6b;">
                    Erro: ${escapeHtml(data.detail || "Não foi possível obter a resposta da IA.")}
                </span>
            `;
        }

    } catch (error) {
        console.error("Erro na comunicação com a API:", error);
        textContainer.innerHTML = `
            <span style="color: #ff6b6b;">
                Erro de conexão com o servidor da CLOUDIX AI. Tente novamente em instantes.
            </span>
        `;
    }

}


/* ==========================================================
   SEGURANÇA E FORMATAÇÃO DE TEXTO
   ========================================================== */

function escapeHtml(text) {

    const div = document.createElement("div");
    div.innerText = text;
    return div.innerHTML;

}

function formatMarkdown(text) {
    if (!text) return "";
    let formatted = escapeHtml(text);
    // Transforma **negrito** em <strong>negrito</strong>
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Transforma marcadores (* item) em bullet points
    formatted = formatted.replace(/^\s*\*\s+(.*)$/gm, '• $1');
    // Transforma quebras de linha em <br>
    formatted = formatted.replace(/\n/g, '<br>');
    return formatted;
}


/* ==========================================================
   UPLOAD E ANÁLISE REAL DE PLANILHA
   ========================================================== */

async function handleFile(input) {

    if (!input.files || !input.files.length) {
        return;
    }

    const file = input.files[0];
    const analysis = document.querySelector("#analysis-content");

    if (!analysis) return;

    analysis.innerHTML = `
        <div style="padding: 25px 0;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:18px;">
                <div
                    style="
                        width:40px;
                        height:40px;
                        border-radius:9px;
                        background:rgba(242,135,5,0.10);
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        color:#F28705;
                    "
                >
                    <i class="fa-solid fa-file-excel"></i>
                </div>

                <div>
                    <strong style="font-size:12px;">
                        ${escapeHtml(file.name)}
                    </strong>
                    <div style="color:#59667a; font-size:9px; margin-top:3px;">
                        Arquivo recebido pela CLOUDIX AI
                    </div>
                </div>
            </div>

            <div style="height:4px; background:#182231; border-radius:10px; overflow:hidden;">
                <div
                    id="progress-bar"
                    style="height:100%; width:15%; background:#565AA6; transition:0.5s;"
                ></div>
            </div>

            <div id="analysis-status" style="color:#687589; font-size:9px; margin-top:12px;">
                Enviando planilha para o servidor...
            </div>

            <div
                id="insights-container"
                style="margin-top:20px; font-size:11px; color:#b9c1d0; line-height:1.6;"
            ></div>
        </div>
    `;

    const progressBar = document.querySelector("#progress-bar");
    const statusText = document.querySelector("#analysis-status");
    const insightsContainer = document.querySelector("#insights-container");
    const token = getAuthToken();

    if (!token) {
        if (progressBar) {
            progressBar.style.width = "100%";
            progressBar.style.background = "#e74c3c";
        }
        if (statusText) {
            statusText.innerHTML = `
                <span style="color: #e74c3c;">
                    <strong>Erro de Autenticação:</strong> É necessário estar autenticado para enviar arquivos.
                </span>
            `;
        }
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        if (progressBar) progressBar.style.width = "40%";
        if (statusText) statusText.innerText = "Processando dados da planilha...";

        const uploadResponse = await fetch("/financial/upload", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: formData
        });

        if (uploadResponse.status === 401) {
            throw new Error("Sessão expirada. Faça login novamente na plataforma.");
        }

        if (!uploadResponse.ok) {
            const errData = await uploadResponse.json().catch(() => ({}));
            throw new Error(errData.detail || "Erro ao fazer upload do arquivo.");
        }

        if (progressBar) progressBar.style.width = "75%";
        if (statusText) statusText.innerText = "Gerando diagnósticos e insights financeiros...";

        const aiResponse = await fetch("/ai/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                message: "Analise detalhadamente a planilha financeira recém-enviada e apresente um resumo executivo com métricas, pontos de atenção e recomendações."
            })
        });

        if (aiResponse.status === 401) {
            throw new Error("Sessão expirada ao consultar a IA.");
        }

        const aiData = await aiResponse.json();

        if (!aiResponse.ok) {
            throw new Error(aiData.detail || "Erro ao consultar a CLOUDIX AI.");
        }

        if (progressBar) progressBar.style.width = "100%";
        if (statusText) statusText.innerText = "Análise financeira concluída com sucesso!";

        let resultText = "";
        if (aiData.response && typeof aiData.response === "object" && aiData.response.text) {
            resultText = aiData.response.text;
        } else if (typeof aiData.response === "string") {
            resultText = aiData.response;
        } else {
            resultText = "Análise concluída.";
        }

        if (insightsContainer) {
            insightsContainer.innerHTML = `
                <div style="background: rgba(18, 26, 38, 0.6); border: 1px solid rgba(86, 90, 166, 0.25); border-radius: 8px; padding: 15px; margin-top: 10px;">
                    <strong style="color: #fff; font-size: 12px; display: block; margin-bottom: 10px;">
                        📊 INSIGHTS GERADOS PELA CLOUDIX AI:
                    </strong>
                    ${formatMarkdown(resultText)}
                </div>
            `;
        }

    } catch (error) {
        console.error("Erro no processamento da planilha:", error);
        if (progressBar) {
            progressBar.style.width = "100%";
            progressBar.style.background = "#e74c3c";
        }
        if (statusText) {
            statusText.innerHTML = `<span style="color: #e74c3c;">Erro: ${escapeHtml(error.message)}</span>`;
        }
    }

}