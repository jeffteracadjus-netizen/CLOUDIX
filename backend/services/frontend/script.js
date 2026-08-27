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


/* SELECIONAR MÓDULO */

function selectModule(moduleName, button = null) {

    if (moduleName === "dashboard") {

        showDashboard();

        return;
    }

    const module = modules[moduleName];

    if (!module) {
        return;
    }


    document
        .querySelector("#dashboard")
        .classList.remove("active-section");

    document
        .querySelector("#module-page")
        .classList.add("active-section");


    document
        .querySelector("#page-title")
        .innerText = module.title;


    document
        .querySelector("#selected-module-label")
        .innerText = module.label;


    document
        .querySelector("#selected-module-title")
        .innerText = module.pageTitle;


    const icon = document.querySelector(
        "#selected-module-icon i"
    );

    icon.className =
        "fa-solid " + module.icon;


    document
        .querySelectorAll(".nav-item")
        .forEach(item => {

            item.classList.remove("active");

        });


    if (button) {

        button.classList.add("active");

    } else {

        const navButton =
            document.querySelector(
                `.nav-item[onclick*="'${moduleName}'"]`
            );

        if (navButton) {

            navButton.classList.add("active");

        }

    }

}


/* DASHBOARD */

function showDashboard() {

    document
        .querySelector("#module-page")
        .classList.remove("active-section");

    document
        .querySelector("#dashboard")
        .classList.add("active-section");

    document
        .querySelector("#page-title")
        .innerText = "Dashboard";


    document
        .querySelectorAll(".nav-item")
        .forEach(item => {

            item.classList.remove("active");

        });


    const dashboardButton =
        document.querySelector(
            ".nav-item.active"
        );

    const buttons =
        document.querySelectorAll(".nav-item");

    buttons.forEach(button => {

        if (
            button.innerText
                .toLowerCase()
                .includes("dashboard")
        ) {

            button.classList.add("active");

        }

    });

}


/* CHAT */

function sendMessage() {

    const input =
        document.querySelector("#chat-input");

    const message =
        input.value.trim();


    if (!message) {
        return;
    }


    const chat =
        document.querySelector(".chat-message");


    const userMessage =
        document.createElement("div");


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


    chat.parentElement.insertBefore(
        userMessage,
        document.querySelector(".chat-input")
    );


    input.value = "";


    setTimeout(() => {

        const aiMessage =
            document.createElement("div");

        aiMessage.className =
            "chat-message";

        aiMessage.innerHTML = `

            <div class="ai-avatar">
                C
            </div>

            <div class="message-bubble">

                <strong>CLOUDIX AI</strong>

                <p>
                    Entendi. Essa funcionalidade será
                    conectada ao motor de inteligência da
                    CLOUDIX AI.
                </p>

            </div>

        `;


        chat.parentElement.insertBefore(
            aiMessage,
            document.querySelector(".chat-input")
        );

    }, 700);

}


/* SEGURANÇA DO TEXTO */

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.innerText = text;

    return div.innerHTML;

}


/* UPLOAD */

function handleFile(input) {

    if (!input.files.length) {
        return;
    }


    const file =
        input.files[0];


    const analysis =
        document.querySelector(
            "#analysis-content"
        );


    analysis.innerHTML = `

        <div
            style="
                padding: 25px 0;
            "
        >

            <div
                style="
                    display:flex;
                    align-items:center;
                    gap:12px;
                    margin-bottom:18px;
                "
            >

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

                    <strong
                        style="
                            font-size:12px;
                        "
                    >
                        ${escapeHtml(file.name)}
                    </strong>

                    <div
                        style="
                            color:#59667a;
                            font-size:9px;
                            margin-top:3px;
                        "
                    >
                        Arquivo recebido pela CLOUDIX AI
                    </div>

                </div>

            </div>


            <div
                style="
                    height:4px;
                    background:#182231;
                    border-radius:10px;
                    overflow:hidden;
                "
            >

                <div
                    id="progress-bar"
                    style="
                        height:100%;
                        width:0%;
                        background:#565AA6;
                        transition:1.2s;
                    "
                ></div>

            </div>


            <div
                id="analysis-status"
                style="
                    color:#687589;
                    font-size:9px;
                    margin-top:12px;
                "
            >
                Preparando análise inteligente...
            </div>

        </div>

    `;


    setTimeout(() => {

        document
            .querySelector("#progress-bar")
            .style.width = "100%";

        document
            .querySelector("#analysis-status")
            .innerText =
                "Análise concluída. Aguardando conexão com o backend.";

    }, 1200);

}