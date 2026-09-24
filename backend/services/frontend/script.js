const modules = {
    dashboard: { title: "Dashboard" },
    vendas: { title: "Vendas", label: "VENDAS", pageTitle: "Inteligência de Vendas", icon: "fa-chart-line" },
    marketing: { title: "Marketing", label: "MARKETING", pageTitle: "Inteligência de Marketing", icon: "fa-bullhorn" },
    financeiro: { title: "Financeiro", label: "FINANCEIRO", pageTitle: "Inteligência Financeira", icon: "fa-wallet" },
    atendimento: { title: "Atendimento", label: "ATENDIMENTO", pageTitle: "Inteligência de Atendimento", icon: "fa-headset" },
    estrategia: { title: "Estratégia", label: "ESTRATÉGIA", pageTitle: "Inteligência Estratégica", icon: "fa-chess" }
};

/* ==========================================================
   OBTER TOKEN DE AUTENTICAÇÃO
   ========================================================== */
function getAuthToken() {
    return localStorage.getItem("token") || localStorage.getItem("access_token");
}

/* ==========================================================
   INICIALIZAÇÃO DA PÁGINA
   ========================================================== */
document.addEventListener("DOMContentLoaded", () => {
    const token = getAuthToken();
    if (!token) {
        openAuthModal();
    } else {
        loadUserProfile();
        loadCompanyProfile();
    }
});

/* ==========================================================
   MODAIS DA APLICAÇÃO (CADA UM COM SUA FUNÇÃO)
   ========================================================== */
function openAuthModal() {
    document.querySelector("#auth-modal").classList.add("active");
}
function closeAuthModal() {
    document.querySelector("#auth-modal").classList.remove("active");
}

function openNotificationsModal() {
    document.querySelector("#notifications-modal").classList.add("active");
}
function closeNotificationsModal() {
    document.querySelector("#notifications-modal").classList.remove("active");
}

function openSettingsModal() {
    const userName = document.querySelector("#sidebar-user-name").innerText;
    document.querySelector("#settings-user-name").value = userName;
    document.querySelector("#settings-modal").classList.add("active");
}
function closeSettingsModal() {
    document.querySelector("#settings-modal").classList.remove("active");
}

function openCompanyModal() {
    document.querySelector("#company-modal").classList.add("active");
}
function closeCompanyModal() {
    document.querySelector("#company-modal").classList.remove("active");
}

function switchAuthTab(tab) {
    document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
    document.querySelector(`#tab-${tab}`).classList.add("active");

    if (tab === 'login') {
        document.querySelector("#form-login").style.display = "block";
        document.querySelector("#form-register").style.display = "none";
    } else {
        document.querySelector("#form-login").style.display = "none";
        document.querySelector("#form-register").style.display = "block";
    }
}

function logout(event) {
    if (event) event.stopPropagation();
    localStorage.removeItem("token");
    localStorage.removeItem("access_token");
    location.reload();
}

/* ==========================================================
   AUTENTICAÇÃO (LOGIN / REGISTRO)
   ========================================================== */
async function handleLogin(event) {
    event.preventDefault();
    const email = document.querySelector("#login-email").value;
    const password = document.querySelector("#login-password").value;
    const errorEl = document.querySelector("#login-error");
    errorEl.style.display = "none";

    try {
        let response = await fetch("/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, username: email, password: password })
        });

        if (response.status === 422) {
            const formData = new URLSearchParams();
            formData.append("username", email);
            formData.append("password", password);

            response = await fetch("/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: formData
            });
        }

        const data = await response.json();

        if (response.ok) {
            const token = data.access_token || data.token;
            localStorage.setItem("token", token);
            closeAuthModal();
            loadUserProfile();
            loadCompanyProfile();
        } else {
            errorEl.innerText = data.detail || "Falha no login. Verifique suas credenciais.";
            errorEl.style.display = "block";
        }
    } catch (err) {
        errorEl.innerText = "Erro ao conectar com o servidor.";
        errorEl.style.display = "block";
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const name = document.querySelector("#register-name").value;
    const email = document.querySelector("#register-email").value;
    const password = document.querySelector("#register-password").value;
    const errorEl = document.querySelector("#register-error");
    errorEl.style.display = "none";

    try {
        const response = await fetch("/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: name, email: email, password: password })
        });

        const data = await response.json();

        if (response.ok) {
            switchAuthTab("login");
            document.querySelector("#login-email").value = email;
            alert("Conta criada com sucesso! Faça login para continuar.");
        } else {
            errorEl.innerText = data.detail || "Erro ao realizar cadastro.";
            errorEl.style.display = "block";
        }
    } catch (err) {
        errorEl.innerText = "Erro ao conectar com o servidor.";
        errorEl.style.display = "block";
    }
}

/* ==========================================================
   PERFIL DO USUÁRIO & EMPRESA
   ========================================================== */
async function loadUserProfile() {
    const token = getAuthToken();
    if (!token) return;

    try {
        const res = await fetch("/auth/me", {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (res.ok) {
            const user = await res.json();
            const userName = user.name || user.email || "Usuário";
            document.querySelector("#sidebar-user-name").innerText = userName;
            document.querySelector("#welcome-user-name").innerText = userName;
            document.querySelector("#sidebar-avatar").innerText = userName.charAt(0).toUpperCase();
        }
    } catch (e) { }
}

async function loadCompanyProfile() {
    const token = getAuthToken();
    if (!token) return;

    try {
        const res = await fetch("/company", {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (res.ok) {
            const company = await res.json();
            if (company && company.name) {
                document.querySelector("#sidebar-company-name").innerText = company.name;
                document.querySelector("#topbar-company-name").innerText = company.name;
                document.querySelector("#topbar-company-sector").innerText = company.sector || "Empresa ativa";
                document.querySelector("#topbar-company-icon").innerText = company.name.charAt(0).toUpperCase();

                document.querySelector("#company-name").value = company.name || "";
                document.querySelector("#company-sector").value = company.sector || "";
                document.querySelector("#company-size").value = company.size || "";
                document.querySelector("#company-description").value = company.description || "";
                document.querySelector("#company-goal").value = company.goal || "";
            } else {
                openCompanyModal();
            }
        }
    } catch (e) { }
}

async function handleSaveCompany(event) {
    event.preventDefault();
    const token = getAuthToken();
    const errorEl = document.querySelector("#company-error");
    errorEl.style.display = "none";

    const companyData = {
        name: document.querySelector("#company-name").value,
        sector: document.querySelector("#company-sector").value,
        size: document.querySelector("#company-size").value,
        description: document.querySelector("#company-description").value,
        goal: document.querySelector("#company-goal").value
    };

    try {
        const response = await fetch("/company", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(companyData)
        });

        if (response.ok) {
            closeCompanyModal();
            loadCompanyProfile();
        } else {
            const data = await response.json();
            errorEl.innerText = data.detail || "Erro ao salvar dados da empresa.";
            errorEl.style.display = "block";
        }
    } catch (err) {
        errorEl.innerText = "Erro ao conectar com o servidor.";
        errorEl.style.display = "block";
    }
}

/* ==========================================================
   NAVEGAÇÃO DOS MÓDULOS
   ========================================================== */
function selectModule(moduleName, button = null) {
    if (moduleName === "dashboard") {
        showDashboard();
        return;
    }

    const module = modules[moduleName];
    if (!module) return;

    document.querySelector("#dashboard").classList.remove("active-section");
    document.querySelector("#module-page").classList.add("active-section");

    document.querySelector("#page-title").innerText = module.title;
    document.querySelector("#selected-module-label").innerText = module.label;
    document.querySelector("#selected-module-title").innerText = module.pageTitle;

    const icon = document.querySelector("#selected-module-icon i");
    if (icon) icon.className = "fa-solid " + module.icon;

    document.querySelectorAll(".nav-item").forEach(item => item.classList.remove("active"));

    if (button) {
        button.classList.add("active");
    } else {
        const navButton = document.querySelector(`.nav-item[onclick*="'${moduleName}'"]`);
        if (navButton) navButton.classList.add("active");
    }
}

function showDashboard() {
    document.querySelector("#module-page").classList.remove("active-section");
    document.querySelector("#dashboard").classList.add("active-section");
    document.querySelector("#page-title").innerText = "Dashboard";

    document.querySelectorAll(".nav-item").forEach(item => item.classList.remove("active"));
    const buttons = document.querySelectorAll(".nav-item");
    buttons.forEach(button => {
        if (button.innerText.toLowerCase().includes("dashboard")) {
            button.classList.add("active");
        }
    });
}

/* ==========================================================
   CHAT COM A CLOUDIX AI
   ========================================================== */
async function sendMessage() {
    const input = document.querySelector("#chat-input");
    if (!input) return;

    const message = input.value.trim();
    if (!message) return;

    const chatInputArea = document.querySelector(".chat-input");
    const parentContainer = chatInputArea ? chatInputArea.parentElement : document.body;

    const userMessage = document.createElement("div");
    userMessage.style.display = "flex";
    userMessage.style.justifyContent = "flex-end";
    userMessage.style.marginTop = "10px";

    userMessage.innerHTML = `
        <div style="background: rgba(86,90,166,0.15); border: 1px solid rgba(86,90,166,0.25); padding: 12px 15px; border-radius: 10px 0 10px 10px; max-width: 600px; color: #b9c1d0; font-size: 11px;">
            ${escapeHtml(message)}
        </div>
    `;

    parentContainer.insertBefore(userMessage, chatInputArea);
    input.value = "";

    const aiMessage = document.createElement("div");
    aiMessage.className = "chat-message";
    aiMessage.innerHTML = `
        <div class="ai-avatar">C</div>
        <div class="message-bubble">
            <strong>CLOUDIX AI</strong>
            <p class="ai-text-response"><em>Analisando sua solicitação...</em></p>
        </div>
    `;

    parentContainer.insertBefore(aiMessage, chatInputArea);
    const textContainer = aiMessage.querySelector(".ai-text-response");
    const token = getAuthToken();

    if (!token) {
        textContainer.innerHTML = `<span style="color: #ff6b6b;">Por favor, faça login para usar a CLOUDIX AI.</span>`;
        openAuthModal();
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
            textContainer.innerHTML = `<span style="color: #ff6b6b;">Sessão expirada. Faça login novamente.</span>`;
            openAuthModal();
            return;
        }

        const data = await response.json();

        if (response.ok) {
            let replyText = (data.response && typeof data.response === "object") ? data.response.text : (data.response || data.message);
            textContainer.innerHTML = formatMarkdown(replyText);
        } else {
            // TRATAMENTO AMIGÁVEL DO ERRO 429
            if (response.status === 429 || (data.detail && data.detail.includes("429"))) {
                textContainer.innerHTML = `
                    <div style="background: rgba(242, 135, 5, 0.1); border: 1px solid rgba(242, 135, 5, 0.3); border-radius: 8px; padding: 12px; color: #f39c12;">
                        <strong>⏳ Limite Temporário de Consultas:</strong><br>
                        Atingimos o limite de requisições do Gemini para este minuto. Aguarde cerca de 30 segundos e tente novamente.
                    </div>
                `;
            } else {
                textContainer.innerHTML = `<span style="color: #ff6b6b;">Erro: ${escapeHtml(data.detail || "Erro ao consultar a IA.")}</span>`;
            }
        }

    } catch (error) {
        textContainer.innerHTML = `<span style="color: #ff6b6b;">Erro de conexão com o servidor.</span>`;
    }
}

/* ==========================================================
   UPLOAD E ANÁLISE DE PLANILHA
   ========================================================== */
async function handleFile(input) {
    if (!input.files || !input.files.length) return;

    const file = input.files[0];
    const analysis = document.querySelector("#analysis-content");
    if (!analysis) return;

    analysis.innerHTML = `
        <div style="padding: 25px 0;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:18px;">
                <div style="width:40px; height:40px; border-radius:9px; background:rgba(242,135,5,0.10); display:flex; align-items:center; justify-content:center; color:#F28705;">
                    <i class="fa-solid fa-file-excel"></i>
                </div>
                <div>
                    <strong style="font-size:12px;">${escapeHtml(file.name)}</strong>
                    <div style="color:#59667a; font-size:9px; margin-top:3px;">Arquivo recebido pela CLOUDIX AI</div>
                </div>
            </div>
            <div style="height:4px; background:#182231; border-radius:10px; overflow:hidden;">
                <div id="progress-bar" style="height:100%; width:15%; background:#565AA6; transition:0.5s;"></div>
            </div>
            <div id="analysis-status" style="color:#687589; font-size:9px; margin-top:12px;">Enviando planilha para o servidor...</div>
            <div id="insights-container" style="margin-top:20px; font-size:11px; color:#b9c1d0; line-height:1.6;"></div>
        </div>
    `;

    const progressBar = document.querySelector("#progress-bar");
    const statusText = document.querySelector("#analysis-status");
    const insightsContainer = document.querySelector("#insights-container");
    const token = getAuthToken();

    if (!token) {
        statusText.innerHTML = `<span style="color: #e74c3c;">Você precisa estar autenticado para enviar arquivos.</span>`;
        openAuthModal();
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        if (progressBar) progressBar.style.width = "40%";
        if (statusText) statusText.innerText = "Processando dados da planilha...";

        const uploadResponse = await fetch("/financial/upload", {
            method: "POST",
            headers: { "Authorization": `Bearer ${token}` },
            body: formData
        });

        if (uploadResponse.status === 401) throw new Error("Sessão expirada.");
        if (!uploadResponse.ok) {
            const errData = await uploadResponse.json().catch(() => ({}));
            throw new Error(errData.detail || "Erro ao enviar arquivo.");
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

        const aiData = await aiResponse.json();

        // TRATAMENTO DO ERRO 429 DE COTA
        if (aiResponse.status === 429 || (aiData.detail && aiData.detail.includes("429"))) {
            if (progressBar) { progressBar.style.width = "100%"; progressBar.style.background = "#f39c12"; }
            statusText.innerHTML = `
                <div style="background: rgba(242, 135, 5, 0.1); border: 1px solid rgba(242, 135, 5, 0.3); border-radius: 8px; padding: 12px; color: #f39c12; font-size: 11px; margin-top: 10px;">
                    <strong>⏳ Limite Temporário de Consultas Excedido:</strong><br>
                    O limite do plano gratuito do Gemini foi atingido por este minuto. Aguarde 30 segundos e envie a pergunta novamente no chat abaixo!
                </div>
            `;
            return;
        }

        if (!aiResponse.ok) throw new Error(aiData.detail || "Erro ao consultar a IA.");

        if (progressBar) progressBar.style.width = "100%";
        if (statusText) statusText.innerText = "Análise concluída com sucesso!";

        let resultText = (aiData.response && typeof aiData.response === "object") ? aiData.response.text : aiData.response;

        if (insightsContainer) {
            insightsContainer.innerHTML = `
                <div style="background: rgba(18, 26, 38, 0.6); border: 1px solid rgba(86, 90, 166, 0.25); border-radius: 8px; padding: 15px; margin-top: 10px;">
                    <strong style="color: #fff; font-size: 12px; display: block; margin-bottom: 12px;">📊 INSIGHTS GERADOS PELA CLOUDIX AI:</strong>
                    ${formatMarkdown(resultText)}
                </div>
            `;
        }

    } catch (error) {
        if (progressBar) { progressBar.style.width = "100%"; progressBar.style.background = "#e74c3c"; }
        if (statusText) statusText.innerHTML = `<span style="color: #e74c3c;">Erro: ${escapeHtml(error.message)}</span>`;
    }
}

/* ==========================================================
   FORMATADOR AVANÇADO DE MARKDOWN (REMOVE ### E ASTERISCOS)
   ========================================================== */
function escapeHtml(text) {
    const div = document.createElement("div");
    div.innerText = text;
    return div.innerHTML;
}

function formatMarkdown(text) {
    if (!text) return "";
    let formatted = escapeHtml(text);

    // Converte Títulos Markdown ###, ##, # em tags HTML elegantes
    formatted = formatted.replace(/^### (.*$)/gim, '<h4 style="color: #999de3; font-size: 13px; font-weight: 700; margin-top: 14px; margin-bottom: 6px;">$1</h4>');
    formatted = formatted.replace(/^## (.*$)/gim, '<h3 style="color: #ffffff; font-size: 14px; font-weight: 700; margin-top: 16px; margin-bottom: 8px;">$1</h3>');
    formatted = formatted.replace(/^# (.*$)/gim, '<h2 style="color: #ffffff; font-size: 16px; font-weight: 800; margin-top: 18px; margin-bottom: 10px;">$1</h2>');

    // Converte Negrito **texto**
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong style="color: #ffffff; font-weight: 600;">$1</strong>');

    // Converte Itálico *texto*
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Converte Linhas Separadoras ---
    formatted = formatted.replace(/^---$/gim, '<hr style="border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 12px 0;">');

    // Converte Marcadores (* item ou - item) em bullet points formatados
    formatted = formatted.replace(/^\s*[\*\-]\s+(.*)$/gim, '<div style="margin-left: 8px; margin-bottom: 4px; display: flex; gap: 6px;"><span style="color: var(--cloudix-purple); font-weight: bold;">•</span><span>$1</span></div>');

    // Converte Quebras de Linha
    formatted = formatted.replace(/\n/g, '<br>');

    return formatted;
}