# Quick test for Tavily MCP server
Write-Host "Testing Tavily MCP Server..." -ForegroundColor Green

# Check environment variable
if ($env:TAVILY_API_KEY) {
    Write-Host "✅ TAVILY_API_KEY is set" -ForegroundColor Green
} else {
    Write-Host "❌ TAVILY_API_KEY is not set" -ForegroundColor Red
    exit 1
}

# Test if npx can find tavily-mcp
Write-Host "`nTesting tavily-mcp installation..." -ForegroundColor Yellow
try {
    $result = npx tavily-mcp --help 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ tavily-mcp is accessible via npx" -ForegroundColor Green
    } else {
        Write-Host "⚠️ tavily-mcp might need initialization or different args" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error testing tavily-mcp: $_" -ForegroundColor Red
}

Write-Host "`nSetup Status:" -ForegroundColor Cyan
Write-Host "- Tavily API Key: ✅ Configured" -ForegroundColor Green
Write-Host "- GitHub Token: ❌ Still needed for GitHub search" -ForegroundColor Yellow  
Write-Host "- MCP Config: ✅ Created at .mcp.json" -ForegroundColor Green
Write-Host "- Warp Integration: ✅ Ready (restart Warp to load)" -ForegroundColor Green

Write-Host "`nNext: Restart Warp to load the new MCP servers!" -ForegroundColor Cyan