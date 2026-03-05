---
resource_id: "12b334f8-97d8-49fc-abb1-1a5fc35e2d9f"
---
# Efficient MCP Servers for Warp AI Assistant
*Enhanced search and development capabilities*

<!-- section_id: "2949e55a-6281-42e6-b44a-846c8a7eabe7" -->
## Overview

Three powerful MCP servers have been configured to enhance Warp's search and development capabilities:

1. **Web Search MCP** (tavily-mcp) - Direct API access to search engines
2. **GitHub Search MCP** (github-mcp-server) - Repository-specific searches  
3. **Browser MCP** (@agent-infra/mcp-server-browser) - Advanced browser automation
4. **Filesystem MCP** (@modelcontextprotocol/server-filesystem) - Local file operations

<!-- section_id: "7823de98-466b-49e7-877e-8ad42d2e071b" -->
## Installation Status

✅ All MCP servers are installed and configured in `.mcp.json`

<!-- section_id: "447a1c3c-ff4f-402b-b1d9-29b82488850a" -->
## Setup Required

<!-- section_id: "d681ee9f-283c-422c-af94-bb2e0859a008" -->
### Environment Variables

To use the search capabilities, set these environment variables:

```powershell
# For web search via Tavily
$env:TAVILY_API_KEY = 'your_tavily_api_key_here'

# For GitHub repository search
$env:GITHUB_TOKEN = 'your_github_token_here'
```

<!-- section_id: "b7f4fcb0-af41-4a37-930e-ca7d87aff70e" -->
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

<!-- section_id: "51154f90-a8fb-4178-915c-827424882769" -->
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

<!-- section_id: "9a1f74e3-7829-45b5-9910-f492d085608c" -->
## MCP Server Capabilities

<!-- section_id: "028a9a7d-a5d8-42b9-b4b5-b17b1cfd2ded" -->
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

<!-- section_id: "d0f972c1-c0d0-48c5-9722-d6bab5856d1a" -->
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

<!-- section_id: "07cf1423-abb0-4f0e-99eb-94143dc2fcd1" -->
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

<!-- section_id: "4a73e213-c7ef-41ce-97e2-d390b63f7e86" -->
### 4. Filesystem MCP
**Purpose**: Local file system operations

**Capabilities**:
- Read/write files efficiently
- Directory operations
- File searching
- Content analysis

<!-- section_id: "807276e6-207a-48c1-b55d-67c48b25f070" -->
## Usage Examples

<!-- section_id: "535b6249-71b5-40b5-aea2-9b2d597d1194" -->
### Web Search for AI Notifications
Instead of manually browsing, Warp can now:
```
Search for "AI agent turn completion notification systems" using web search
Find Claude Code hooks documentation
Discover agent-notifications GitHub repository
```

<!-- section_id: "46781ead-37ff-486b-9050-9f68426585fd" -->
### GitHub Repository Discovery
```
Search GitHub for "mcp server notifications"
Find popular notification libraries
Analyze implementation patterns
```

<!-- section_id: "b5ef4df6-bc36-4c03-952e-e376795d6287" -->
### Documentation Deep Dive
```
Use browser MCP to:
- Navigate to official Claude documentation
- Extract specific hook configurations
- Screenshot important sections
- Test live examples
```

<!-- section_id: "ead9b786-e452-47de-bf64-649bae86f08f" -->
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

<!-- section_id: "9cd297e4-17e8-4d46-8386-7e2a1a87569c" -->
## Advantages Over Basic Browser MCP

1. **Speed**: Direct API calls vs. browser navigation
2. **Reliability**: No browser crashes or timeouts
3. **Structure**: JSON responses vs. HTML parsing
4. **Scope**: Multiple data sources vs. single websites
5. **Efficiency**: Parallel searches vs. sequential browsing

<!-- section_id: "838b2a73-a5cf-4893-8254-c806266c776d" -->
## Troubleshooting

<!-- section_id: "6796db99-f15d-495a-aeac-5dc7db8c69dd" -->
### MCP Servers Not Working
1. Verify environment variables are set
2. Check `.mcp.json` is in project root
3. Ensure npm packages are installed globally
4. Restart Warp to reload configuration

<!-- section_id: "c8846b66-5ffa-4243-8d1d-30f766ee5d3c" -->
### API Rate Limits
- Tavily: Generous free tier, upgrade available
- GitHub: 5000 requests/hour for authenticated users

<!-- section_id: "32424cc0-f23f-4f90-9e05-8e9b18793f5e" -->
### Network Issues
- Ensure internet connectivity
- Check firewall settings
- Verify API endpoints are accessible

<!-- section_id: "81baece5-b526-4ab5-b50d-aa7a9497380f" -->
## Integration with Warp Workflow

These MCP servers integrate seamlessly with the Trickle-Down documentation system:

- **Research Phase**: Web search and GitHub discovery
- **Implementation Phase**: Browser automation for detailed docs
- **File Operations**: Filesystem MCP for local development
- **Documentation**: All tools working together for comprehensive research

---

*Configuration complete and ready for enhanced Warp AI development*