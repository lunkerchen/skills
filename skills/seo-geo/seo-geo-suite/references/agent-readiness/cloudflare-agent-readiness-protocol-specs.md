# Protocol Specifications & Schemas

## 1. Agent Skills Index (RFC v0.2.0)
Endpoint: `/.well-known/agent-skills/index.json`
```json
{
  "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
  "skills": [
    {
      "name": "skill-name",
      "type": "skill-md",
      "description": "Description of the skill",
      "url": "/.well-known/agent-skills/skill-name/SKILL.md",
      "digest": "sha256:..."
    }
  ]
}
```

## 2. MCP Server Card
Endpoint: `/.well-known/mcp/server-card.json` & `/.well-known/mcp.json`
```json
{
  "$schema": "https://modelcontextprotocol.io/schemas/server-card.json",
  "name": "service-agent-name",
  "displayName": "Service Display Name",
  "description": "Description",
  "version": "1.0.0",
  "capabilities": {
    "tools": true,
    "resources": true,
    "prompts": true
  },
  "tools": [ ... ]
}
```

## 3. A2A Agent Card
Endpoint: `/.well-known/agent-card.json`
```json
{
  "name": "agent-id",
  "displayName": "Agent Name",
  "version": "1.0.0",
  "description": "Description",
  "supportedInterfaces": [
    {
      "url": "https://domain.com/api/lead",
      "transport": "HTTP-POST",
      "protocol": "A2A/1.0"
    }
  ],
  "skills": [ ... ]
}
```

## 4. ARD (AI Resource Discovery)
Endpoint: `/.well-known/ai-catalog.json`
```json
{
  "specVersion": "1.0",
  "host": {
    "displayName": "Organization Name",
    "identifier": "did:web:domain.com"
  },
  "entries": [
    {
      "identifier": "urn:air:domain.com:mcp:service",
      "displayName": "MCP Service",
      "type": "application/mcp-server-card+json",
      "url": "https://domain.com/.well-known/mcp/server-card.json",
      "representativeQueries": [ ... ]
    }
  ]
}
```

## 5. Auth.md
Endpoint: `/auth.md` & `/.well-known/auth.md`
Markdown with `# Title auth.md`, documenting public APIs, access conditions, and auth methods.
