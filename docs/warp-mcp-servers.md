# Efficient MCP Servers for Warp AI Assistant
*Enhanced search and development capabilities*

## Overview

Three powerful MCP servers have been configured to enhance Warp's search and development capabilities:

1. **Web Search MCP** (tavily-mcp) - Direct API access to search engines
2. **GitHub Search MCP** (github-mcp-server) - Repository-specific searches  
3. **Browser MCP** (@agent-infra/mcp-server-browser) - Advanced browser automation
4. **Filesystem MCP** (@modelcontextprotocol/server-filesystem) - Local file operations

## Installation Status

✅ All MCP servers are installed and configured in `.mcp.json`

## Setup Required

### Environment Variables

To use the search capabilities, set these environment variables:

```powershell
# For web search via Tavily
$env:TAVILY_API_KEY = 'your_tavily_api_key_here'

# For GitHub repository search
$env:GITHUB_TOKEN = 'your_github_token_here'
```

### Getting API Keys

1. **Tavily API Key**:
   - Sign up at https://tavily.com
   - Navigate to API section
   - Copy your API key

2. **GitHub Token**:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo`, `public_repo`, `user`
   - Copy the generated token

### Making Variables Permanent

Add to your PowerShell profile:
```powershell
notepad $PROFILE
```

Add these lines:
```powershell
$env:TAVILY_API_KEY = 'your_actual_key_here'
$env:GITHUB_TOKEN = 'your_actual_token_here'
```

## MCP Server Capabilities

### 1. Web Search MCP (tavily-mcp)
**Purpose**: High-quality web searches with direct API access

**Benefits over browser MCP**:
- Faster search results
- Structured data responses
- No rate limiting issues
- Real-time web content

**Use Cases**:
- Finding AI agent notification systems
- Technical documentation searches
- Current best practices research
- API documentation discovery

### 2. GitHub Search MCP (github-mcp-server)
**Purpose**: Efficient repository and code searches

**Capabilities**:
- Search repositories by keywords
- Find specific code implementations
- Discover popular libraries and tools
- Access repository metadata

**Use Cases**:
- Finding MCP server implementations
- Discovering notification systems
- Locating code examples
- Repository analysis

### 3. Browser MCP (@agent-infra/mcp-server-browser)
**Purpose**: Advanced browser automation and interaction

**Capabilities**:
- Navigate web pages
- Extract structured data
- Interact with web applications
- Take screenshots
- Execute JavaScript

**Use Cases**:
- Detailed documentation reading
- Interactive web research
- Form submissions
- Complex web interactions

### 4. Filesystem MCP
**Purpose**: Local file system operations

**Capabilities**:
- Read/write files efficiently
- Directory operations
- File searching
- Content analysis

## Usage Examples

### Web Search for AI Notifications
Instead of manually browsing, Warp can now:
```
Search for "AI agent turn completion notification systems" using web search
Find Claude Code hooks documentation
Discover agent-notifications GitHub repository
```

### GitHub Repository Discovery
```
Search GitHub for "mcp server notifications"
Find popular notification libraries
Analyze implementation patterns
```

### Documentation Deep Dive
```
Use browser MCP to:
- Navigate to official Claude documentation
- Extract specific hook configurations
- Screenshot important sections
- Test live examples
```

## Configuration File (`.mcp.json`)

```json
{
  "mcpServers": {
    "web-search": {
      "command": "npx",
      "args": ["tavily-mcp"],
      "env": {
        "TAVILY_API_KEY": "${TAVILY_API_KEY}"
      }
    },
    "github-search": {
      "command": "npx",
      "args": ["github-mcp-server"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "browser": {
      "command": "npx",
      "args": ["@agent-infra/mcp-server-browser"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "C:\\home\\dawson\\code\\lang-trak-in-progress"]
    }
  }
}
```

## Advantages Over Basic Browser MCP

1. **Speed**: Direct API calls vs. browser navigation
2. **Reliability**: No browser crashes or timeouts
3. **Structure**: JSON responses vs. HTML parsing
4. **Scope**: Multiple data sources vs. single websites
5. **Efficiency**: Parallel searches vs. sequential browsing

## Troubleshooting

### MCP Servers Not Working
1. Verify environment variables are set
2. Check `.mcp.json` is in project root
3. Ensure npm packages are installed globally
4. Restart Warp to reload configuration

### API Rate Limits
- Tavily: Generous free tier, upgrade available
- GitHub: 5000 requests/hour for authenticated users

### Network Issues
- Ensure internet connectivity
- Check firewall settings
- Verify API endpoints are accessible

## Integration with Warp Workflow

These MCP servers integrate seamlessly with the Trickle-Down documentation system:

- **Research Phase**: Web search and GitHub discovery
- **Implementation Phase**: Browser automation for detailed docs
- **File Operations**: Filesystem MCP for local development
- **Documentation**: All tools working together for comprehensive research

---

*Configuration complete and ready for enhanced Warp AI development*