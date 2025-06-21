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
* DNS Reconnaissance
* Subdomain Enumeration 
* Email security checks
* HTTP Header Analysis

### Example Of Usage
1. Pada percobaan tools ini saya menargetkan target kecamatanciseeng.bogorkab.go.id
2. Prompt yang saya gunakan menggunakan bahasa inggris sebagai berikut: "Perform  reconnaissance test on kecamatanciseeng.bogorkab.go.id"
![image](https://github.com/user-attachments/assets/ef40c28c-e653-4ada-b132-b09f06cc351c)
3. Maka llm akan terhubung ke MCP untuk melakukan reconnaissance menggunakan tools yang sudah disediakan sebelumnya
![image](https://github.com/user-attachments/assets/d92ef183-c6be-4b19-885d-a86f46ff5dff)
Proggress tiap-tiap tools bisa dilihat
![image](https://github.com/user-attachments/assets/fe913317-5dd4-469d-8080-b2518a81965d)
4. Kemudian setelah selesai menjalankan semua tools yang tersedia, llm akan membuat laporan analisis dari output yang ada
![image](https://github.com/user-attachments/assets/9d62f5c9-fd58-4189-9d9a-1ec5c3902184)
5. Walaupun sudah menghasilkan laporan tapi llm masih menawarkan untuk melakukan penjelasan tambahan maupun uji tambahan dengan memanfaatkan tools yang ada (contoh seperti gambar: "Would you like me to elaborate on any specific aspect of the findings or perform additional analysis on particular areas?")
![image](https://github.com/user-attachments/assets/af9a4f43-5f46-4fc2-aa9b-86fe78359962)
6. Coba lanjutkan pengujian untuk api
![image](https://github.com/user-attachments/assets/4f37c35d-945b-4528-96c2-fddc22fbec29)
7. Maka llm akan melakukan pengujian tambahan untuk API bahkan menemukan hasil baru yang berbeda sebelumnya
![image](https://github.com/user-attachments/assets/e6676ad1-caad-4990-a7e5-786d0550a524)
Kendala dalam pengujian adalah akun claude yang saya gunakan masih gratis sehingga terdapat batas dalam penggunaan llm
