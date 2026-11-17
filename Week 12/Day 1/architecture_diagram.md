# W12D1 – Production Architecture Diagram

## 1. Existing Architecture

The diagram shows the two independently implemented analytics workflows reviewed in this assessment.

```mermaid
flowchart TD
    A[Sales CSV Dataset]

    A --> B[W8D1 Analytics Pipeline]
    A --> C[W11D5 Stakeholder Analysis]

    subgraph W8D1 [AI Executive Summary]
        B --> D[Pandas Data Processing]
        D --> E[Calculate Five Insights]
        E --> F[Groq API]
        F --> G[Generate Executive Summary]
        G --> H[PowerPoint Export]
        H --> I[Seven Slide PPTX]
    end

    subgraph W11D5 [Stakeholder Reporting]
        C --> J[Data Validation]
        J --> K[Pandas Analysis]
        K --> L[CSV Analysis Outputs]
        K --> M[Matplotlib Charts]
        L --> N[Word Report Generator]
        M --> N
        N --> O[Stakeholder DOCX Report]
    end
```

## 2. Recommended Production Architecture

```mermaid
flowchart TD
    A[Data Sources] --> B[Data Ingestion]
    B --> C[Input Validation]
    C --> D[Secure Data Storage]
    D --> E[Analytics Processing]

    E --> F[Business Insights]
    F --> G[AI Integration Layer]
    G --> H[External AI API]

    F --> I[Report Generation]
    H --> I

    I --> J[Centralized Report Storage]

    E --> K[Logging and Monitoring]
    G --> K
    I --> K

    K --> L[Alerts and Error Tracking]

    M[Automated Testing and CI/CD] --> E
    N[Backup and Recovery] --> D
    N --> J
```

## 3. Architecture Explanation

| Component            | Purpose                        |
| -------------------- | ------------------------------ |
| Data Sources         | Provides sales datasets        |
| Data Ingestion       | Receives input files           |
| Input Validation     | Checks data quality and format |
| Secure Storage       | Stores data safely             |
| Analytics Processing | Calculates business metrics    |
| AI Integration       | Generates AI-based summaries   |
| Report Generation    | Creates PPTX and DOCX reports  |
| Monitoring           | Tracks errors and performance  |
| Automated Testing    | Checks application quality     |
| Backup and Recovery  | Protects important data        |

## 4. Key Observation

The existing architecture uses local Python scripts and files. The recommended architecture introduces centralized storage, monitoring, secure API integration, automated testing, and backup mechanisms.

The recommended architecture is a proposed future design, not a description of infrastructure currently deployed.
