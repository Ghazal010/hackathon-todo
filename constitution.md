# Hackathon Todo - Project Constitution

## Project Identity
- **Name**: Hackathon Todo - Evolution from CLI to Cloud-Native AI
- **Author**: Ghazal
- **Timeline**: December 1, 2025 - January 18, 2026
- **Objective**: Master Spec-Driven Development with AI-native architecture

## Core Principles

### 1. Spec-Driven Development (NON-NEGOTIABLE)
- **Every feature MUST have a specification first**
- **No manual coding** - Only through Claude Code (via Qwen)
- Specifications are the source of truth
- Code is generated from specs, not written directly
- If spec is unclear, refine spec - don't write code manually

### 2. Incremental Evolution
- Start simple (console app) → evolve to complex (cloud-native AI)
- Each phase builds on previous phase's foundation
- **Never skip phases**
- Reuse and evolve code, don't rewrite from scratch

### 3. AI-Native Architecture
- Use OpenAI as the LLM backend (free tier)
- MCP (Model Context Protocol) for tool integration
- Conversational interface over traditional UI where applicable
- AI agents handle business logic, not just UI

### 4. Clean Code Standards
- Follow Python PEP 8 style guide
- Meaningful variable and function names
- Comprehensive docstrings for all functions
- Type hints wherever possible
- DRY (Don't Repeat Yourself) principle

### 5. Testing & Validation
- Test each feature before moving to next
- Validate against acceptance criteria in specs
- Document bugs and fixes in specs
- Manual testing acceptable for hackathon timeline

## Technology Stack

### Phase 1: Console App
- Python 3.13+
- UV package manager
- In-memory data storage

### Phase 2: Web Application
- Frontend: Next.js 16+
- Backend: Python FastAPI
- Database: Neon Serverless PostgreSQL
- Auth: Better Auth with JWT

### Phase 3: AI Chatbot
- LLM: OpenAI GPT (free tier)
- Frontend: OpenAI ChatKit
- MCP: Official MCP SDK

### Phase 4: Local Kubernetes
- Docker containerization
- Minikube for local K8s
- Helm charts

### Phase 5: Cloud Deployment
- Cloud: DigitalOcean Kubernetes
- Event Streaming: Kafka on Redpanda Cloud
- Dapr for distributed runtime

## Development Workflow

### For Each Feature:
1. **Specify**: Write detailed spec in /specs/phaseN/features/
2. **Review**: Ensure spec covers all acceptance criteria
3. **Generate**: Use Claude Code (Qwen) to generate implementation
4. **Test**: Validate against spec requirements
5. **Refine**: If issues, update spec and regenerate
6. **Commit**: Git commit with reference to spec

## Quality Gates

### Before Moving to Next Phase:
- [ ] All features from current phase working
- [ ] All acceptance criteria met
- [ ] Code pushed to GitHub
- [ ] README updated
- [ ] Demo video recorded (90 seconds max)

## Success Metrics
- [ ] Complete all 5 phases on time
- [ ] Score 1000+ points
- [ ] Working deployments for each phase
- [ ] Clean, well-documented code

---

**This constitution is a living document.**
