# Setup script for MCP servers in Warp
# This script helps configure the required environment variables

Write-Host "Setting up MCP Servers for Warp..." -ForegroundColor Green

# Check if required API keys are set
$requiredVars = @{
    'TAVILY_API_KEY' = 'Tavily API key for web search'
    'GITHUB_TOKEN' = 'GitHub personal access token for repository search'
}

$missingVars = @()

foreach ($var in $requiredVars.Keys) {
    $envValue = [Environment]::GetEnvironmentVariable($var)
    if (-not $envValue) {
        $missingVars += @{
            name = $var
            description = $requiredVars[$var]
        }
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host "`nMissing environment variables:" -ForegroundColor Yellow
    foreach ($var in $missingVars) {
        Write-Host "  - $($var.name): $($var.description)" -ForegroundColor Yellow
    }
    
    Write-Host "`nTo set up these variables:" -ForegroundColor Cyan
    Write-Host "1. For Tavily API key (web search):" -ForegroundColor Cyan
    Write-Host "   - Sign up at https://tavily.com" -ForegroundColor Gray
    Write-Host "   - Get your API key" -ForegroundColor Gray
    Write-Host "   - Run: `$env:TAVILY_API_KEY = 'your_api_key_here'" -ForegroundColor Gray
    
    Write-Host "`n2. For GitHub token (repository search):" -ForegroundColor Cyan
    Write-Host "   - Go to https://github.com/settings/tokens" -ForegroundColor Gray
    Write-Host "   - Generate a new personal access token" -ForegroundColor Gray
    Write-Host "   - Run: `$env:GITHUB_TOKEN = 'your_github_token_here'" -ForegroundColor Gray
    
    Write-Host "`nTo make these permanent, add them to your PowerShell profile:" -ForegroundColor Cyan
    Write-Host "   notepad `$PROFILE" -ForegroundColor Gray
} else {
    Write-Host "`nAll required environment variables are set! ✅" -ForegroundColor Green
}

# Test MCP server installations
Write-Host "`nTesting MCP server installations..." -ForegroundColor Green

$servers = @(
    @{ name = "tavily-mcp"; package = "tavily-mcp" },
    @{ name = "github-mcp-server"; package = "github-mcp-server" },
    @{ name = "browser-mcp"; package = "@agent-infra/mcp-server-browser" },
    @{ name = "filesystem-mcp"; package = "@modelcontextprotocol/server-filesystem" }
)

foreach ($server in $servers) {
    try {
        $result = npm list -g $server.package 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ $($server.name) installed" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $($server.name) not found - run: npm install -g $($server.package)" -ForegroundColor Red
        }
    } catch {
        Write-Host "  ❌ $($server.name) not found - run: npm install -g $($server.package)" -ForegroundColor Red
    }
}

Write-Host "`nMCP configuration file created at: .mcp.json" -ForegroundColor Green
Write-Host "Warp should automatically detect and use these MCP servers." -ForegroundColor Green

# Show current .mcp.json content
if (Test-Path ".mcp.json") {
    Write-Host "`nCurrent .mcp.json configuration:" -ForegroundColor Cyan
    Get-Content ".mcp.json" | Write-Host -ForegroundColor Gray
}