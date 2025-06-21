# zap_integration.py
from mcp.server.fastmcp import FastMCP
import httpx
import asyncio
import time

# Initialize FastMCP server
mcp = FastMCP("zap-integration")

# Konfigurasi ZAP
ZAP_API_URL = "http://localhost:8081"
ZAP_API_KEY = "ub8r31kc82at3voc0khv5r4un9"

async def zap_api_request(endpoint: str, params: dict = None) -> dict:
    """Membuat permintaan ke ZAP API"""
    try:
        async with httpx.AsyncClient() as client:
            # Tambahkan API key ke parameter
            params = params or {}
            params['apikey'] = ZAP_API_KEY
            
            response = await client.get(f"{ZAP_API_URL}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": str(e)}

### Prompt untuk inisialisasi AI
@mcp.prompt()
def setup_prompt(target_url: str) -> str:
    return f"""
You are a web application security expert using ZAP (Zed Attack Proxy) for security testing. Your task is to perform comprehensive security scanning on the target URL: {target_url}

Perform the following actions:
1. Spider the target to discover endpoints
2. Run an active scan to identify vulnerabilities
3. Analyze scan results and report critical findings
4. Suggest remediation steps for identified vulnerabilities

Think step by step and use the available tools to execute the scanning process.
"""

### Memulai spider scan
@mcp.tool()
async def start_zap_spider(target_url: str) -> str:
    """
    Initiates a spider scan to crawl the target website
    
    Args:
        target_url: URL target untuk discan (contoh: https://example.com)
    
    Returns:
        Status scan dan ID scan
    """
    try:
        # Memulai spider scan
        spider_params = {
            'url': target_url,
            'maxChildren': 50,
            'recurse': True
        }
        start_response = await zap_api_request('/JSON/spider/action/scan/', spider_params)
        
        if 'error' in start_response:
            return f"Spider failed to start: {start_response['error']}"
        
        scan_id = start_response.get('scan')
        return f"Spider scan started successfully. Scan ID: {scan_id}"
    except Exception as e:
        return f"Error starting spider: {str(e)}"

### Memeriksa status spider
@mcp.tool()
async def check_spider_status(scan_id: str) -> str:
    """
    Checks the status of an ongoing spider scan
    
    Args:
        scan_id: ID scan dari spider yang sedang berjalan
    
    Returns:
        Persentase penyelesaian dan status
    """
    try:
        status_params = {'scanId': scan_id}
        status_response = await zap_api_request('/JSON/spider/view/status/', status_params)
        
        if 'error' in status_response:
            return f"Failed to get spider status: {status_response['error']}"
        
        status = status_response.get('status')
        progress = status_response.get('progress')
        return f"Spider status: {status} - Progress: {progress}%"
    except Exception as e:
        return f"Error checking spider status: {str(e)}"

### Memulai active scan
@mcp.tool()
async def start_zap_active_scan(target_url: str) -> str:
    """
    Initiates an active security scan to identify vulnerabilities
    
    Args:
        target_url: URL target untuk discan (contoh: https://example.com)
    
    Returns:
        Status scan dan ID scan
    """
    try:
        # Memulai active scan
        scan_params = {
            'url': target_url,
            'recurse': True,
            'inScopeOnly': True
        }
        start_response = await zap_api_request('/JSON/ascan/action/scan/', scan_params)
        
        if 'error' in start_response:
            return f"Active scan failed to start: {start_response['error']}"
        
        scan_id = start_response.get('scan')
        return f"Active scan started successfully. Scan ID: {scan_id}"
    except Exception as e:
        return f"Error starting active scan: {str(e)}"

### Memeriksa status active scan
@mcp.tool()
async def check_scan_status(scan_id: str) -> str:
    """
    Checks the status of an ongoing active scan
    
    Args:
        scan_id: ID scan dari active scan yang sedang berjalan
    
    Returns:
        Persentase penyelesaian dan status
    """
    try:
        status_params = {'scanId': scan_id}
        status_response = await zap_api_request('/JSON/ascan/view/status/', status_params)
        
        if 'error' in status_response:
            return f"Failed to get scan status: {status_response['error']}"
        
        status = status_response.get('status')
        return f"Scan status: {status}"
    except Exception as e:
        return f"Error checking scan status: {str(e)}"

### Mendapatkan laporan hasil scan
@mcp.tool()
async def get_zap_alerts(target_url: str) -> str:
    """
    Retrieves security alerts found by ZAP
    
    Args:
        target_url: URL target yang telah discan (contoh: https://example.com)
    
    Returns:
        Daftar kerentanan yang ditemukan
    """
    try:
        alert_params = {
            'baseurl': target_url,
            'start': 0,
            'count': 50
        }
        alerts_response = await zap_api_request('/JSON/core/view/alerts/', alert_params)
        
        if 'error' in alerts_response:
            return f"Failed to get alerts: {alerts_response['error']}"
        
        alerts = alerts_response.get('alerts', [])
        if not alerts:
            return "No security alerts found"
        
        # Format hasil untuk Claude
        summary = []
        for alert in alerts:
            summary.append(
                f"Risk: {alert['risk']}\n"
                f"Alert: {alert['alert']}\n"
                f"URL: {alert['url']}\n"
                f"Description: {alert['description']}\n"
                f"Solution: {alert['solution']}\n"
                "---"
            )
        
        return f"Security Alerts:\n\n" + "\n".join(summary)
    except Exception as e:
        return f"Error retrieving alerts: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport='stdio')