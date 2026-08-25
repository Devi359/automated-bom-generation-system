# Automated Bill of Materials Generation System

An automated **Bill of Materials (BOM) generation and costing system** that integrates with the **Onshape API** to retrieve assembly data, process component hierarchies, calculate part quantities and costs, and generate downloadable BOM reports.

## 🚀 Live Application

**Live Demo:** https://automated-bom-generation-system.onrender.com

> The application is deployed using **Render** and integrated with **Onshape OAuth 2.0** for secure user authentication.

---

## 📌 Project Overview

The **Automated BOM Generation System** simplifies the process of generating a Bill of Materials from an Onshape assembly.

Instead of manually collecting component information, the system:

* Authenticates users through Onshape OAuth 2.0
* Retrieves assembly information using the Onshape REST API
* Processes assembly and sub-assembly hierarchies
* Identifies individual parts and calculates quantities
* Assigns unit prices to components
* Calculates total component costs
* Displays BOM details through a web dashboard
* Provides hierarchy visualization
* Exports BOM data as CSV
* Generates a PDF invoice

---

## ✨ Key Features

### 🔐 Onshape OAuth Authentication

Securely authenticates users through the Onshape OAuth 2.0 authorization flow.

### 📊 BOM Generation

Automatically extracts component information from an Onshape assembly and generates a structured Bill of Materials.

### 🌳 Assembly Hierarchy

Displays the assembly structure and its component hierarchy.

### 💰 Cost Calculation

Calculates:

* Part quantity
* Unit price
* Total price
* Overall BOM cost

### 👨‍💼 Admin Price Management

Provides an administrator dashboard for updating component prices.

### 📄 CSV Export

Allows users to download the generated BOM as a CSV file.

### 🧾 PDF Invoice

Generates a professional PDF invoice containing BOM components, quantities, prices, and totals.

### ☁️ Cloud Deployment

The application is deployed and accessible online using Render.

---

## 🛠️ Technology Stack

| Technology       | Purpose                         |
| ---------------- | ------------------------------- |
| Python           | Backend development             |
| Flask            | Web application framework       |
| Onshape REST API | Assembly and CAD data retrieval |
| OAuth 2.0        | User authentication             |
| HTML             | Frontend structure              |
| CSS              | Frontend styling                |
| ReportLab        | PDF generation                  |
| Requests         | API communication               |
| GitHub           | Version control                 |
| Render           | Cloud deployment                |

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Flask Web App     │
                    │      Dashboard      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Onshape OAuth 2.0  │
                    │   Authentication    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Onshape REST     │
                    │        API          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Assembly Data       │
                    │ Processing &        │
                    │ Hierarchy Analysis  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    BOM Engine       │
                    │ Quantity + Cost     │
                    │ Calculation         │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
          ┌──────────┐   ┌──────────┐   ┌──────────┐
          │ BOM View │   │ CSV File │   │ PDF Bill │
          └──────────┘   └──────────┘   └──────────┘
```

---

## 🔄 Application Workflow

```text
User
  ↓
Login with Onshape
  ↓
OAuth Authorization
  ↓
OAuth Callback
  ↓
Access Token
  ↓
Fetch Assembly Data
  ↓
Process Parts & Sub-Assemblies
  ↓
Generate BOM
  ↓
Calculate Component Costs
  ↓
Display BOM
  ↓
Export CSV / Generate PDF
```

---

## 📂 Project Structure

```text
automated-bom-generation-system/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── update_price.html
│   ├── bom.html
│   └── tree.html
│
└── ...
```

---

## 🔑 Environment Variables

The application uses environment variables for sensitive OAuth configuration.

```text
CLIENT_ID
CLIENT_SECRET
REDIRECT_URI
```

Example:

```text
CLIENT_ID=<Onshape OAuth Client ID>
CLIENT_SECRET=<Onshape OAuth Client Secret>
REDIRECT_URI=https://automated-bom-generation-system.onrender.com/callback
```

> **Security:** OAuth credentials and secrets are not stored directly in the source code or committed to GitHub.

---

## ▶️ Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Devi359/automated-bom-generation-system.git
```

### 2. Navigate to the project

```bash
cd automated-bom-generation-system
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Set the required Onshape OAuth credentials:

```text
CLIENT_ID
CLIENT_SECRET
REDIRECT_URI
```

### 5. Run the Flask application

```bash
python app.py
```

The application will be available locally at:

```text
http://127.0.0.1:5000
```

---

## ☁️ Deployment

The application is deployed on **Render** using Gunicorn.

### Production Start Command

```bash
gunicorn app:app
```

### Production URL

https://automated-bom-generation-system.onrender.com

---

## 📊 Main Modules

### 1. Authentication Module

Handles secure Onshape OAuth 2.0 authentication and access-token management.

### 2. Data Extraction Module

Retrieves assembly information from the Onshape REST API.

### 3. Hierarchy Processing Module

Processes root assemblies, sub-assemblies, and individual parts.

### 4. BOM Generation Module

Calculates component quantities and creates structured BOM data.

### 5. Cost Calculation Module

Assigns prices and calculates individual and total component costs.

### 6. Export Module

Generates downloadable CSV and PDF reports.

### 7. Administration Module

Allows administrators to update component prices.

---

## 🎯 Project Objectives

* Automate BOM generation from CAD assemblies
* Reduce manual BOM preparation
* Improve accuracy in component counting
* Provide automated cost estimation
* Integrate CAD data with web-based applications
* Generate downloadable engineering reports
* Demonstrate practical use of REST APIs and OAuth authentication

---

## 🔮 Future Enhancements

* Database integration for persistent price management
* Advanced BOM search and filtering
* Excel export
* User management and role-based access control
* Improved hierarchy visualization
* Automated email report generation
* Historical BOM tracking
* Advanced cost analytics and dashboards

---

## 👩‍💻 Project Team

**Devi P**
**Niranjana S**
**Subhasri K**

**B.E. Computer Science and Engineering**

### Technologies & Skills

`Python` `Flask` `REST API` `OAuth 2.0` `HTML` `CSS` `GitHub` `Render`


---

## ⭐ Project Status

**Status: Completed and Deployed**

The application is currently live and the major features including **Onshape authentication, BOM generation, hierarchy viewing, cost calculation, CSV export, and PDF generation** are working successfully.

---

## 📜 License

This project is developed for academic and educational purposes.
