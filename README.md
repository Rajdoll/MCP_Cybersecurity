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

```mermaid
sequenceDiagram
    User->>Claude: "Scan example.com"
    Claude->>Recon Agent: Gather DNS/subdomains
    Recon Agent-->>Claude: Subdomain list
    Claude->>ZAP Agent: Scan shop.example.com
    ZAP Agent-->>Claude: Vulnerability report
    Claude->>User: Risk analysis + recommendations
```

### Dokumentasi Penggunaan
#### Fitur Utama
* DNS Reconnaissance
* Subdomain Enumeration 
* Email security checks
* HTTP Header Analysis

### Example Of Usage
1. Pada percobaan tools ini saya menargetkan target kecamatanciseeng.bogorkab.go.id
2. Prompt yang saya gunakan menggunakan bahasa inggris sebagai berikut: "Perform  reconnaissance test on kecamatanciseeng.bogorkab.go.id"

![image](https://github.com/user-attachments/assets/ef40c28c-e653-4ada-b132-b09f06cc351c)

3. Maka llm akan terhubung ke MCP untuk melakukan reconnaissance menggunakan tools yang sudah disediakan sebelumnya

![image](https://github.com/user-attachments/assets/179c17ad-d73b-461e-bb41-32b46a020624)

Proggress tiap-tiap tools bisa dilihat

![image](https://github.com/user-attachments/assets/c1f96389-d86a-41a4-90fe-b542a84f3b93)

5. Kemudian setelah selesai menjalankan semua tools yang tersedia, llm akan membuat laporan analisis dari output yang ada

![image](https://github.com/user-attachments/assets/573a76a6-d476-4555-af6c-80115d4bce8a)

6. (Dalam pengujian yang berbeda) walaupun sudah menghasilkan laporan tapi llm masih menawarkan untuk melakukan penjelasan tambahan maupun uji tambahan dengan memanfaatkan tools yang ada (contoh seperti gambar: "Would you like me to elaborate on any specific aspect of the findings or perform additional analysis on particular areas?")

![image](https://github.com/user-attachments/assets/af9a4f43-5f46-4fc2-aa9b-86fe78359962)

7. (Dalam pengujian yang berbeda) Coba lanjutkan pengujian untuk api

![image](https://github.com/user-attachments/assets/4f37c35d-945b-4528-96c2-fddc22fbec29)

8. (Dalam pengujian yang berbeda) Maka llm akan melakukan pengujian tambahan untuk API bahkan menemukan hasil baru yang berbeda sebelumnya

![image](https://github.com/user-attachments/assets/e6676ad1-caad-4990-a7e5-786d0550a524)

Kendala dalam pengujian adalah akun claude yang saya gunakan masih gratis sehingga terdapat batas dalam penggunaan llm
