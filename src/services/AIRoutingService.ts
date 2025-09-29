/**
 * AI Routing Service
 * Advanced routing logic for assigning problems to optimal AI combinations
 */

import { 
  AICapability, 
  ProblemContext, 
  AIRecommendation, 
  aiCollaborationService 
} from './AICollaborationService';

export interface RoutingRule {
  id: string;
  name: string;
  condition: (problem: ProblemContext) => boolean;
  primaryAI: string;
  collaborators: string[];
  priority: number;
}

export interface RoutingResult {
  recommendation: AIRecommendation;
  confidence: number;
  alternativeRoutes: AIRecommendation[];
  routingReason: string;
}

export class AIRoutingService {
  private routingRules: RoutingRule[] = [];

  constructor() {
    this.initializeRoutingRules();
  }

  private initializeRoutingRules(): void {
    this.routingRules = [
      // Frontend-focused rules
      {
        id: 'rapid-prototype',
        name: 'Rapid Prototyping',
        condition: (p) => p.type === 'prototype' && p.urgency === 'high',
        primaryAI: 'bolt',
        collaborators: ['cursor', 'windsurf'],
        priority: 10
      },
      {
        id: 'complex-frontend',
        name: 'Complex Frontend Development',
        condition: (p) => p.type === 'frontend' && p.complexity === 'high' && p.scope === 'project-wide',
        primaryAI: 'cursor',
        collaborators: ['windsurf', 'vscode'],
        priority: 9
      },
      {
        id: 'ui-generation',
        name: 'UI Component Generation',
        condition: (p) => p.type === 'frontend' && p.technologies.some(t => 
          ['react', 'vue', 'angular', 'svelte'].includes(t.toLowerCase())
        ),
        primaryAI: 'bolt',
        collaborators: ['cursor'],
        priority: 8
      },

      // Backend-focused rules
      {
        id: 'serverless-backend',
        name: 'Serverless Backend Development',
        condition: (p) => p.type === 'backend' && p.technologies.some(t => 
          ['firebase', 'serverless', 'lambda', 'vercel'].includes(t.toLowerCase())
        ),
        primaryAI: 'firebase',
        collaborators: ['trae', 'cursor'],
        priority: 9
      },
      {
        id: 'ai-integration',
        name: 'AI/ML Integration',
        condition: (p) => p.technologies.some(t => 
          ['ai', 'ml', 'openai', 'gemini', 'claude'].includes(t.toLowerCase())
        ) || p.description.toLowerCase().includes('ai'),
        primaryAI: 'firebase',
        collaborators: ['trae', 'cursor'],
        priority: 8
      },

      // Full-stack rules
      {
        id: 'fullstack-mvp',
        name: 'Full-Stack MVP',
        condition: (p) => p.type === 'fullstack' && p.scope === 'project-wide',
        primaryAI: 'trae',
        collaborators: ['bolt', 'firebase', 'cursor'],
        priority: 9
      },
      {
        id: 'enterprise-fullstack',
        name: 'Enterprise Full-Stack',
        condition: (p) => p.type === 'fullstack' && p.complexity === 'high',
        primaryAI: 'cursor',
        collaborators: ['trae', 'windsurf', 'firebase'],
        priority: 8
      },

      // Debugging and maintenance rules
      {
        id: 'complex-debugging',
        name: 'Complex Debugging',
        condition: (p) => p.type === 'debugging' && p.complexity === 'high',
        primaryAI: 'windsurf',
        collaborators: ['cursor', 'vscode'],
        priority: 9
      },
      {
        id: 'code-review',
        name: 'Code Review and Optimization',
        condition: (p) => p.type === 'debugging' && p.scope === 'multi-file',
        primaryAI: 'vscode',
        collaborators: ['cursor', 'windsurf'],
        priority: 7
      },

      // Architecture and design rules
      {
        id: 'system-architecture',
        name: 'System Architecture Design',
        condition: (p) => p.type === 'architecture',
        primaryAI: 'trae',
        collaborators: ['cursor', 'windsurf'],
        priority: 8
      },

      // Deployment rules
      {
        id: 'deployment-automation',
        name: 'Deployment and CI/CD',
        condition: (p) => p.type === 'deployment',
        primaryAI: 'trae',
        collaborators: ['bolt', 'firebase'],
        priority: 7
      },

      // Technology-specific rules
      {
        id: 'react-ecosystem',
        name: 'React Ecosystem Development',
        condition: (p) => p.technologies.some(t => 
          ['react', 'next.js', 'gatsby', 'remix'].includes(t.toLowerCase())
        ),
        primaryAI: 'cursor',
        collaborators: ['bolt', 'vscode'],
        priority: 7
      },
      {
        id: 'node-backend',
        name: 'Node.js Backend Development',
        condition: (p) => p.technologies.some(t => 
          ['node.js', 'express', 'fastify', 'nest.js'].includes(t.toLowerCase())
        ),
        primaryAI: 'cursor',
        collaborators: ['trae', 'vscode'],
        priority: 7
      },

      // Fallback rules
      {
        id: 'single-file-edit',
        name: 'Single File Editing',
        condition: (p) => p.scope === 'single-file',
        primaryAI: 'vscode',
        collaborators: ['cursor'],
        priority: 5
      },
      {
        id: 'general-development',
        name: 'General Development',
        condition: () => true, // Always matches as fallback
        primaryAI: 'cursor',
        collaborators: ['vscode', 'windsurf'],
        priority: 1
      }
    ];

    // Sort rules by priority (highest first)
    this.routingRules.sort((a, b) => b.priority - a.priority);
  }

  public routeProblem(problem: ProblemContext): RoutingResult {
    // Find matching rules
    const matchingRules = this.routingRules.filter(rule => rule.condition(problem));
    
    if (matchingRules.length === 0) {
      // Fallback to general recommendation
      const fallbackRecommendation = aiCollaborationService.recommendAIForProblem(problem);
      return {
        recommendation: fallbackRecommendation,
        confidence: 0.5,
        alternativeRoutes: [],
        routingReason: 'No specific routing rules matched. Using general AI recommendation.'
      };
    }

    // Use the highest priority matching rule
    const selectedRule = matchingRules[0];
    const primaryAI = aiCollaborationService.getAI(selectedRule.primaryAI);
    
    if (!primaryAI) {
      throw new Error(`Primary AI '${selectedRule.primaryAI}' not found`);
    }

    // Get collaborating AIs
    const collaboratingAIs = selectedRule.collaborators
      .map(id => aiCollaborationService.getAI(id))
      .filter((ai): ai is AICapability => ai !== undefined);

    // Create recommendation
    const recommendation: AIRecommendation = {
      primaryAI,
      collaboratingAIs,
      reasoning: this.generateAdvancedReasoning(problem, selectedRule, primaryAI, collaboratingAIs),
      workflow: this.generateAdvancedWorkflow(problem, selectedRule, primaryAI, collaboratingAIs)
    };

    // Calculate confidence based on rule specificity and matches
    const confidence = this.calculateConfidence(problem, selectedRule, matchingRules);

    // Generate alternative routes from other matching rules
    const alternativeRoutes = matchingRules
      .slice(1, 4) // Take up to 3 alternatives
      .map(rule => this.createAlternativeRecommendation(problem, rule))
      .filter((rec): rec is AIRecommendation => rec !== null);

    return {
      recommendation,
      confidence,
      alternativeRoutes,
      routingReason: `Matched routing rule: ${selectedRule.name} (Priority: ${selectedRule.priority})`
    };
  }

  private generateAdvancedReasoning(
    problem: ProblemContext,
    rule: RoutingRule,
    primary: AICapability,
    collaborators: AICapability[]
  ): string {
    const reasons = [
      `Selected ${primary.name} as the lead AI based on routing rule: ${rule.name}.`,
      `This choice is optimal because ${primary.name} excels in ${primary.strengths.slice(0, 2).join(' and ')}.`
    ];

    if (collaborators.length > 0) {
      const collabNames = collaborators.map(ai => ai.name).join(', ');
      reasons.push(`Collaborating with ${collabNames} to provide comprehensive coverage of ${problem.type} development needs.`);
    }

    // Add context-specific reasoning
    if (problem.urgency === 'high') {
      reasons.push('High urgency detected - this AI combination prioritizes rapid delivery and iteration.');
    }

    if (problem.complexity === 'high') {
      reasons.push('High complexity requires the advanced capabilities and collaborative approach of this AI team.');
    }

    if (problem.scope === 'project-wide') {
      reasons.push('Project-wide scope benefits from the comprehensive codebase understanding of this AI selection.');
    }

    return reasons.join(' ');
  }

  private generateAdvancedWorkflow(
    problem: ProblemContext,
    rule: RoutingRule,
    primary: AICapability,
    collaborators: AICapability[]
  ): string[] {
    const workflow: string[] = [];

    // Phase 1: Analysis and Planning
    workflow.push(`${primary.name} analyzes the ${problem.type} requirements and creates an implementation plan`);
    
    if (collaborators.length > 0) {
      workflow.push(`${collaborators.map(ai => ai.name).join(' and ')} review the plan and provide specialized input`);
    }

    // Phase 2: Implementation
    if (problem.scope === 'project-wide') {
      workflow.push(`${primary.name} leads the architectural setup and core implementation`);
      if (collaborators.length > 0) {
        workflow.push(`Collaborating AIs handle specialized components in parallel`);
      }
    } else {
      workflow.push(`${primary.name} implements the solution with real-time collaboration from the team`);
    }

    // Phase 3: Integration and Testing
    if (collaborators.length > 0) {
      workflow.push('All AIs collaborate on integration testing and cross-validation');
    }
    
    workflow.push(`${primary.name} performs final optimization and quality assurance`);

    // Phase 4: Deployment (if applicable)
    if (problem.type === 'deployment' || problem.type === 'fullstack') {
      const deploymentAI = collaborators.find(ai => ai.id === 'firebase' || ai.id === 'bolt') || primary;
      workflow.push(`${deploymentAI.name} handles deployment and production setup`);
    }

    return workflow;
  }

  private calculateConfidence(
    problem: ProblemContext,
    selectedRule: RoutingRule,
    allMatches: RoutingRule[]
  ): number {
    let confidence = 0.7; // Base confidence

    // Increase confidence based on rule priority
    confidence += (selectedRule.priority / 10) * 0.2;

    // Increase confidence if multiple specific conditions are met
    const specificityBonus = this.calculateSpecificity(problem, selectedRule);
    confidence += specificityBonus * 0.1;

    // Decrease confidence if many rules match (indicates ambiguity)
    if (allMatches.length > 3) {
      confidence -= 0.1;
    }

    // Ensure confidence stays within bounds
    return Math.max(0.5, Math.min(1.0, confidence));
  }

  private calculateSpecificity(problem: ProblemContext, rule: RoutingRule): number {
    let specificity = 0;

    // Check how many problem attributes the rule considers
    const ruleString = rule.condition.toString();
    
    if (ruleString.includes('type')) specificity++;
    if (ruleString.includes('complexity')) specificity++;
    if (ruleString.includes('scope')) specificity++;
    if (ruleString.includes('urgency')) specificity++;
    if (ruleString.includes('technologies')) specificity++;

    return specificity;
  }

  private createAlternativeRecommendation(
    problem: ProblemContext,
    rule: RoutingRule
  ): AIRecommendation | null {
    const primaryAI = aiCollaborationService.getAI(rule.primaryAI);
    if (!primaryAI) return null;

    const collaboratingAIs = rule.collaborators
      .map(id => aiCollaborationService.getAI(id))
      .filter((ai): ai is AICapability => ai !== undefined);

    return {
      primaryAI,
      collaboratingAIs,
      reasoning: `Alternative approach using ${rule.name} strategy`,
      workflow: [`Alternative workflow led by ${primaryAI.name}`]
    };
  }

  public getRoutingRules(): RoutingRule[] {
    return [...this.routingRules];
  }

  public addCustomRule(rule: RoutingRule): void {
    this.routingRules.push(rule);
    this.routingRules.sort((a, b) => b.priority - a.priority);
  }

  public removeRule(ruleId: string): boolean {
    const index = this.routingRules.findIndex(rule => rule.id === ruleId);
    if (index !== -1) {
      this.routingRules.splice(index, 1);
      return true;
    }
    return false;
  }
}

export const aiRoutingService = new AIRoutingService();