# LIVE ENVIRONMENT RULES

## CRITICAL RULE: NO VIRTUAL OR SIMULATED ENVIRONMENTS

### Rule 1: Live Environment Only
- ALL development, testing, and deployment MUST occur in a complete live environment
- NO virtual environments, simulations, or mock services are permitted
- Every API integration MUST use real, live API endpoints
- All database operations MUST use actual production databases
- All services MUST be fully functional and connected to live systems

### Rule 2: Functionality Preservation
- NEVER remove existing functionality from the application
- When updating or refactoring code, ALL existing features MUST be preserved
- If a feature needs modification, it MUST be enhanced, not removed
- Any code changes MUST maintain backward compatibility
- All existing API integrations MUST remain functional after updates

### Rule 3: Live Testing Requirements
- ALL tests MUST be performed against live APIs and services
- Connection tests MUST use actual API keys and live endpoints
- Database tests MUST use real database connections
- No mocking, stubbing, or simulation of any kind is permitted

### Rule 4: Real API Integration Standards
- All API integrations MUST use actual API keys from live services
- API connection tests MUST make real HTTP requests to live endpoints
- Rate limiting MUST be respected for live API services
- Error handling MUST account for real API response patterns

### Rule 5: Production-Ready Code Only
- All code MUST be production-ready from the start
- No placeholder or dummy implementations
- All environment variables MUST point to live services
- All configurations MUST be production-grade

### Rule 6: Continuous Live Validation
- Every code change MUST be validated against live systems immediately
- API integrations MUST be tested with real API calls
- Database changes MUST be applied to live databases
- All functionality MUST work in the live environment before completion

### Rule 7: No Functionality Removal Policy
- Existing working features are SACRED and MUST NOT be removed
- Code refactoring MUST preserve all existing capabilities
- New implementations MUST extend, not replace, existing functionality
- If conflicts arise, find solutions that maintain all features

### Implementation Guidelines
1. Always use real API keys from actual service providers
2. Connect to live databases and services
3. Test all functionality in the live environment
4. Preserve all existing working code
5. Enhance rather than replace existing features
6. Validate all changes against live systems

### Violation Consequences
- Any violation of these rules requires immediate correction
- Removed functionality MUST be restored
- Virtual/simulated components MUST be replaced with live equivalents
- All testing MUST be redone in the live environment

These rules are MANDATORY and NON-NEGOTIABLE for all development work.
