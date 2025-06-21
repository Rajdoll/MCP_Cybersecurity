# MCP FOR CYBERSECURITY (ZAP Integration + External Recon)

## Dokumentasi dan Penggunaan

### Ringkasan
Dokumen ini menjelaskan agen MCP eksternal dan integrasinya dengan ZAP (Zed Attack Proxy) untuk pengujian keamanan web otomatis. Sistem ini menggabungkan kemampuan analisis Claude dengan alat keamanan melalui protokol MCP.

### Diagram Arsitektur
```mermaid
flowchart TD
    User -->|Natural Language Command| ClaudeAI
    ClaudeAI --> MCP
    ClaudeAI -->|Human-Readable Report| User
    MCP --> Recon
    Recon -->|DNS/Subdomain Data| ZAP
    ZAP --> ClaudeAI
    MCP --> ZAP
    ZAP -->|Vulnerability Report| ClaudeAI

    subgraph Agents
        MCP[MCP Orchestrator]
        Recon[external-recon Agent]
        ZAP[ZAP Agent]
        ClaudeAI[Claude AI]
    end
```
### Dokumentasi Penggunaan
#### Fitur Utama
-. DNS Reconnaissance (Menggunakan dig dan whois)
-. Subdomain Enumeration (dns recon)
-. Email security checks
-. HTTP Header Analysis
