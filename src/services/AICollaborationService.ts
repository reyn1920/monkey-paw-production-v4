/**
 * AI Collaboration Service
 * Routes development problems to the most suitable AI platform and enables collaboration
 */

export interface AICapability {
  id: string;
  name: string;
  strengths: string[];
  specialties: string[];
  confidence: number; // 0-1 scale
}

export interface ProblemContext {
  type: 'frontend' | 'backend' | 'fullstack' | 'debugging' | 'architecture' | 'prototype' | 'deployment';
  complexity: 'low' | 'medium' | 'high';
  scope: 'single-file' | 'multi-file' | 'project-wide';
  technologies: string[];
  description: string;
  urgency: 'low' | 'medium' | 'high';
}

export interface AIRecommendation {
  primaryAI: AICapability;
  collaboratingAIs: AICapability[];
  reasoning: string;
  workflow: string[];
}

export class AICollaborationService {
  private aiCapabilities: Map<string, AICapability> = new Map();

  constructor() {
    this.initializeAICapabilities();
  }

  private initializeAICapabilities(): void {
    // Cursor AI - Multi-file editing and codebase understanding
    this.aiCapabilities.set('cursor', {
      id: 'cursor',
      name: 'Cursor AI',
      strengths: [
        'Multi-file code generation',
        'Codebase understanding', 
        'Complex refactoring',
        'Architectural changes',
        'AI-driven workflows'
      ],
      specialties: [
        'Large codebase navigation',
        'Cross-file dependencies',
        'Code architecture',
        'Advanced refactoring'
      ],
      confidence: 0.95
    });

    // Bolt.diy - Rapid prototyping and full-stack development
    this.aiCapabilities.set('bolt', {
      id: 'bolt',
      name: 'Bolt.diy',
      strengths: [
        'Rapid prototyping',
        'Full-stack development',
        'Zero-setup environments',
        'WebContainers technology',
        'Framework agnostic'
      ],
      specialties: [
        'MVP development',
        'Complete app generation',
        'Browser-based development',
        'Quick iterations'
      ],
      confidence: 0.92
    });

    // Google Firebase AI - Backend and cloud services
    this.aiCapabilities.set('firebase', {
      id: 'firebase',
      name: 'Google Firebase AI',
      strengths: [
        'Backend services',
        'Serverless architecture',
        'Cloud infrastructure',
        'Database management',
        'Authentication systems'
      ],
      specialties: [
        'Scalable backends',
        'Real-time databases',
        'Cloud functions',
        'AI model deployment',
        'Security implementation'
      ],
      confidence: 0.90
    });

    // Trae.ai - Autonomous development and documentation
    this.aiCapabilities.set('trae', {
      id: 'trae',
      name: 'Trae.ai',
      strengths: [
        'Autonomous software building',
        'Independent problem-solving',
        'Documentation generation',
        'SOLO mode development',
        'End-to-end feature creation'
      ],
      specialties: [
        'Complete feature development',
        'Self-directed coding',
        'Technical documentation',
        'Workflow automation'
      ],
      confidence: 0.88
    });

    // VS Code AI - Code assistance and debugging
    this.aiCapabilities.set('vscode', {
      id: 'vscode',
      name: 'VS Code AI (GitHub Copilot)',
      strengths: [
        'Code completions',
        'Real-time debugging',
        'IntelliSense enhancement',
        'Extension ecosystem',
        'Error detection'
      ],
      specialties: [
        'Line-by-line coding',
        'Bug identification',
        'Code optimization',
        'Development workflow'
      ],
      confidence: 0.93
    });

    // Windsurf AI - Collaborative flows and project management
    this.aiCapabilities.set('windsurf', {
      id: 'windsurf',
      name: 'Windsurf AI',
      strengths: [
        'Collaborative coding flows',
        'Project management',
        'Contextual awareness',
        'Cascade system',
        'Multi-step workflows'
      ],
      specialties: [
        'Team collaboration',
        'Iterative development',
        'Project coordination',
        'Flow state maintenance'
      ],
      confidence: 0.89
    });
  }

  /**
   * Analyzes a problem and recommends the best AI to lead, plus collaborating AIs
   */
  public recommendAIForProblem(problem: ProblemContext): AIRecommendation {
    const scores = new Map<string, number>();
    
    // Calculate scores for each AI based on problem context
    for (const [id, ai] of this.aiCapabilities) {
      let score = 0;
      
      // Type-based scoring
      switch (problem.type) {
        case 'frontend':
          if (id === 'cursor' || id === 'vscode') score += 30;
          if (id === 'bolt') score += 25;
          if (id === 'windsurf') score += 20;
          break;
        case 'backend':
          if (id === 'firebase') score += 35;
          if (id === 'trae') score += 25;
          if (id === 'cursor') score += 20;
          break;
        case 'fullstack':
          if (id === 'bolt') score += 35;
          if (id === 'cursor') score += 30;
          if (id === 'trae') score += 25;
          break;
        case 'debugging':
          if (id === 'vscode') score += 35;
          if (id === 'cursor') score += 30;
          if (id === 'windsurf') score += 20;
          break;
        case 'architecture':
          if (id === 'cursor') score += 35;
          if (id === 'trae') score += 30;
          if (id === 'firebase') score += 25;
          break;
        case 'prototype':
          if (id === 'bolt') score += 40;
          if (id === 'trae') score += 25;
          if (id === 'windsurf') score += 20;
          break;
        case 'deployment':
          if (id === 'firebase') score += 35;
          if (id === 'bolt') score += 25;
          if (id === 'trae') score += 20;
          break;
      }

      // Scope-based scoring
      switch (problem.scope) {
        case 'single-file':
          if (id === 'vscode') score += 20;
          if (id === 'cursor') score += 15;
          break;
        case 'multi-file':
          if (id === 'cursor') score += 25;
          if (id === 'windsurf') score += 20;
          break;
        case 'project-wide':
          if (id === 'trae') score += 25;
          if (id === 'bolt') score += 20;
          if (id === 'cursor') score += 20;
          break;
      }

      // Complexity-based scoring
      switch (problem.complexity) {
        case 'low':
          if (id === 'vscode' || id === 'bolt') score += 15;
          break;
        case 'medium':
          if (id === 'cursor' || id === 'windsurf') score += 15;
          break;
        case 'high':
          if (id === 'trae' || id === 'cursor') score += 20;
          break;
      }

      // Apply AI confidence multiplier
      score *= ai.confidence;
      scores.set(id, score);
    }

    // Find primary AI (highest score)
    const sortedScores = Array.from(scores.entries()).sort((a, b) => b[1] - a[1]);
    const primaryAI = this.aiCapabilities.get(sortedScores[0][0])!;

    // Select collaborating AIs (top 2-3 excluding primary)
    const collaboratingAIs = sortedScores
      .slice(1, 4)
      .filter(([_, score]) => score > 20) // Only include AIs with reasonable scores
      .map(([id, _]) => this.aiCapabilities.get(id)!)
      .filter(Boolean);

    return {
      primaryAI,
      collaboratingAIs,
      reasoning: this.generateReasoning(problem, primaryAI, collaboratingAIs),
      workflow: this.generateWorkflow(problem, primaryAI, collaboratingAIs)
    };
  }

  private generateReasoning(
    problem: ProblemContext, 
    primary: AICapability, 
    collaborators: AICapability[]
  ): string {
    let reasoning = `${primary.name} is recommended as the lead AI because it excels at `;
    reasoning += primary.specialties.slice(0, 2).join(' and ');
    reasoning += `, which directly addresses this ${problem.type} problem with ${problem.complexity} complexity.`;
    
    if (collaborators.length > 0) {
      reasoning += ` Collaborating with ${collaborators.map(ai => ai.name).join(', ')} will provide `;
      reasoning += `additional expertise in ${collaborators.flatMap(ai => ai.specialties.slice(0, 1)).join(', ')}.`;
    }

    return reasoning;
  }

  private generateWorkflow(
    problem: ProblemContext, 
    primary: AICapability, 
    collaborators: AICapability[]
  ): string[] {
    const workflow: string[] = [];
    
    workflow.push(`1. ${primary.name} analyzes the problem and creates initial solution approach`);
    
    if (collaborators.length > 0) {
      collaborators.forEach((ai, index) => {
        workflow.push(`${index + 2}. ${ai.name} reviews and enhances the solution with ${ai.specialties[0]}`);
      });
    }
    
    workflow.push(`${workflow.length + 1}. ${primary.name} integrates feedback and implements final solution`);
    workflow.push(`${workflow.length + 1}. All AIs collaborate on testing and validation`);
    
    return workflow;
  }

  /**
   * Gets all available AI capabilities
   */
  public getAvailableAIs(): AICapability[] {
    return Array.from(this.aiCapabilities.values());
  }

  /**
   * Gets specific AI capability by ID
   */
  public getAI(id: string): AICapability | undefined {
    return this.aiCapabilities.get(id);
  }
}

export const aiCollaborationService = new AICollaborationService();