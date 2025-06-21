from mcp.server.fastmcp import FastMCP
import subprocess
import httpx
import os
import asyncio

# Initialise FastMCP server
mcp = FastMCP("external-recon")

# Fungsi untuk menjalankan perintah di WSL
async def execute_wsl_command(command: str) -> str:
    try:
        escaped_command = command.replace("'", "'\\''")
        wsl_command = f"wsl /bin/bash -c '{escaped_command}'"
        
        proc = await asyncio.create_subprocess_shell(
            wsl_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Timeout setelah 60 detik
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=60)
        except asyncio.TimeoutError:
            proc.terminate()
            await proc.wait()
            return "Command timed out"
        
        output = ""
        if stdout:
            output += stdout.decode().strip()
        if stderr:
            output += "\n[ERROR] " + stderr.decode().strip()
        
        return output or "No output"
    except Exception as e:
        return f"Command execution error: {str(e)}"

## Prompt to initialise the AI model to the task
@mcp.prompt()
def setup_prompt(domainname: str) -> str:
    return f"""
Your role is a highly skilled penetration tester specialising in network reconnaissance. Your primary objective is to enumerate the {domainname} domain and report on discovered IP addresses, subdomains, and email security.

First, reflect on the objective, then execute any tools you have access to on the target domain {domainname} and report your findings on all IP addresses and subdomains discovered.
"""

### run dig to query DNS A records
@mcp.tool()
async def run_dig_lookup(domainname: str) -> str:
    try:
        command = f"dig +short '{domainname}'"
        return await execute_wsl_command(command)
    except Exception as e:
        return f"Error performing DNS lookup: {str(e)}"

### run whois on each IP address
@mcp.tool()
async def run_whois_lookup(ipaddress: str) -> str:
    try:
        command = f"whois {ipaddress}"
        return await execute_wsl_command(command)
    except Exception as e:
        return f"Error performing whois lookup: {str(e)}"

### perform DNS zone transfer attempt
@mcp.tool()
async def attempt_zone_transfer(domainname: str) -> str:
    try:
        command = f"dig axfr {domainname}"
        return await execute_wsl_command(command)
    except Exception as e:
        return f"Error performing zone transfer: {str(e)}"

### perform subdomain enumeration using dnsrecon
@mcp.tool()
async def enumerate_subdomains(domainname: str) -> str:
    try:
        command = f"dnsrecon -d '{domainname}' -t std"
        return await execute_wsl_command(command)
    except Exception as e:
        return f"Error performing subdomain enumeration: {str(e)}"
    
### bruteforce subdomains using dnsrecon
@mcp.tool()
async def bruteforce_subdomains(domainname: str) -> str:
    try:
        # Path ke wordlist di WSL (pastikan file sudah ada di WSL)
        command = f"dnsrecon -d {domainname} -t brt -D subdomains-top1million-5000.txt"
        results = await execute_wsl_command(command)
    except Exception as e:
        return f"Error performing subdomain bruteforce: {str(e)}"
        return f"""
Subdomain Bruteforce Results:
----------------------------
{results}
"""
    except Exception as e:
        return f"Error performing subdomain bruteforce: {str(e)}"

### perform DNS record enumeration
@mcp.tool()
async def enumerate_dns_records(domainname: str) -> str:
    try:
        command = f"dig ANY '{domainname}' +noall +answer"
        return await execute_wsl_command(command)
    except Exception as e:
        return f"Error enumerating DNS records: {str(e)}"

### perform HTTP headers analysis
@mcp.tool()
async def analyze_http_headers(domainname: str) -> str:
    try:
        command = f"curl -s -I -L 'https://{domainname}' || curl -s -I -L 'http://{domainname}'"
        return await execute_wsl_command(command)
    except Exception as e:
        return f"Error analyzing HTTP headers: {str(e)}"

### check email security
@mcp.tool()
async def check_email_security(domainname: str) -> str:
    try:
        # Hindari penggunaan grep, proses di Python saja
        commands = [
            f"dig +short '{domainname}' TXT",
            f"dig +short '_dmarc.{domainname}' TXT",
            f"dig +short 'default._domainkey.{domainname}' TXT"
        ]
        
        results = []
        for cmd in commands:
            output = await execute_wsl_command(cmd)
            # Filter hasil secara manual tanpa grep
            filtered = [line for line in output.split('\n') if 'v=spf' in line or 'v=DMARC' in line]
            results.append("\n".join(filtered) if filtered else "No record found")
        
        return "\n\n".join([
            f"SPF Record: {results[0]}",
            f"DMARC Record: {results[1]}",
            f"DKIM Record: {results[2]}"
        ])
    except Exception as e:
        return f"Error checking email security: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport='stdio')