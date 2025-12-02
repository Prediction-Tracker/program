# program
Source code of Prediction Tracker: system for automatic market signal predictions and audit.


Estructure files:

programin/
│
├── frontend/                ← tudo que roda no navegador
│   ├── index.html           ← formulário principal
│   ├── style.css            ← estilos do site
│   └── script.js            ← validações básicas no frontend (opcional)
│
├── backend/                 ← código que roda no servidor
│   ├── app.py               ← aplicação Flask/FastAPI
│   ├── requirements.txt     ← bibliotecas (yfinance, flask, etc)
│   └── utils.py             ← funções auxiliares (validação, envio de email)
│
├── data/                    ← banco de dados ou armazenamento simples
│   └── used_emails.json     ← controle de emails já utilizados
│
├── docs/                    ← documentação ou README adicional
│
└── README.md                ← descrição completa do projeto
