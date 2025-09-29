import React, { useState, useEffect } from 'react';
import { 
  aiCollaborationService, 
  ProblemContext, 
  AIRecommendation, 
  AICapability 
} from '../services/AICollaborationService';
import { aiRoutingService, RoutingResult } from '../services/AIRoutingService';

interface AICollaborationHubProps {
  className?: string;
}

export const AICollaborationHub: React.FC<AICollaborationHubProps> = ({ className = '' }) => {
  const [problemContext, setProblemContext] = useState<ProblemContext>({
    type: 'frontend',
    complexity: 'medium',
    scope: 'multi-file',
    technologies: [],
    description: '',
    urgency: 'medium'
  });

  const [recommendation, setRecommendation] = useState<AIRecommendation | null>(null);
  const [routingResult, setRoutingResult] = useState<RoutingResult | null>(null);
  const [availableAIs, setAvailableAIs] = useState<AICapability[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [useAdvancedRouting, setUseAdvancedRouting] = useState(true);

  useEffect(() => {
    setAvailableAIs(aiCollaborationService.getAvailableAIs());
  }, []);

  const handleAnalyzeProblem = async () => {
    if (!problemContext.description.trim()) {
      alert('Please provide a problem description');
      return;
    }

    setIsAnalyzing(true);
    
    // Simulate analysis time for better UX
    setTimeout(() => {
      if (useAdvancedRouting) {
        const routing = aiRoutingService.routeProblem(problemContext);
        setRoutingResult(routing);
        setRecommendation(routing.recommendation);
      } else {
        const result = aiCollaborationService.recommendAIForProblem(problemContext);
        setRecommendation(result);
        setRoutingResult(null);
      }
      setIsAnalyzing(false);
    }, 1500);
  };

  const handleTechnologyAdd = (tech: string) => {
    if (tech && !problemContext.technologies.includes(tech)) {
      setProblemContext(prev => ({
        ...prev,
        technologies: [...prev.technologies, tech]
      }));
    }
  };

  const handleTechnologyRemove = (tech: string) => {
    setProblemContext(prev => ({
      ...prev,
      technologies: prev.technologies.filter(t => t !== tech)
    }));
  };

  return (
    <div className={`ai-collaboration-hub ${className}`}>
      <div className="max-w-6xl mx-auto p-6 space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI Collaboration Hub
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Describe your development problem and get AI-powered recommendations for the best 
            collaborative approach using our 6 specialized AI platforms.
          </p>
        </div>

        {/* Problem Input Form */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            Describe Your Problem
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Problem Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Problem Type
              </label>
              <select
                value={problemContext.type}
                onChange={(e) => setProblemContext(prev => ({ 
                  ...prev, 
                  type: e.target.value as ProblemContext['type'] 
                }))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="frontend">Frontend Development</option>
                <option value="backend">Backend Development</option>
                <option value="fullstack">Full-Stack Development</option>
                <option value="debugging">Debugging & Troubleshooting</option>
                <option value="architecture">Architecture & Design</option>
                <option value="prototype">Rapid Prototyping</option>
                <option value="deployment">Deployment & DevOps</option>
              </select>
            </div>

            {/* Complexity */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Complexity Level
              </label>
              <select
                value={problemContext.complexity}
                onChange={(e) => setProblemContext(prev => ({ 
                  ...prev, 
                  complexity: e.target.value as ProblemContext['complexity'] 
                }))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="low">Low - Simple task</option>
                <option value="medium">Medium - Moderate complexity</option>
                <option value="high">High - Complex challenge</option>
              </select>
            </div>

            {/* Scope */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Project Scope
              </label>
              <select
                value={problemContext.scope}
                onChange={(e) => setProblemContext(prev => ({ 
                  ...prev, 
                  scope: e.target.value as ProblemContext['scope'] 
                }))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="single-file">Single File</option>
                <option value="multi-file">Multiple Files</option>
                <option value="project-wide">Entire Project</option>
              </select>
            </div>

            {/* Urgency */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Urgency Level
              </label>
              <select
                value={problemContext.urgency}
                onChange={(e) => setProblemContext(prev => ({ 
                  ...prev, 
                  urgency: e.target.value as ProblemContext['urgency'] 
                }))}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="low">Low - Can wait</option>
                <option value="medium">Medium - Moderate priority</option>
                <option value="high">High - Urgent</option>
              </select>
            </div>
          </div>

          {/* Technologies */}
          <div className="mt-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Technologies Involved
            </label>
            <div className="flex flex-wrap gap-2 mb-3">
              {problemContext.technologies.map((tech) => (
                <span
                  key={tech}
                  className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800"
                >
                  {tech}
                  <button
                    onClick={() => handleTechnologyRemove(tech)}
                    className="ml-2 text-blue-600 hover:text-blue-800"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
            <input
              type="text"
              placeholder="Add technology (press Enter)"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleTechnologyAdd(e.currentTarget.value);
                  e.currentTarget.value = '';
                }
              }}
            />
          </div>

          {/* Problem Description */}
          <div className="mt-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Problem Description
            </label>
            <textarea
              value={problemContext.description}
              onChange={(e) => setProblemContext(prev => ({ 
                ...prev, 
                description: e.target.value 
              }))}
              placeholder="Describe your development challenge in detail..."
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Analyze Button */}
          <div className="mt-6 space-y-4">
            {/* Advanced Routing Toggle */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <h4 className="font-medium text-gray-900">Advanced AI Routing</h4>
                <p className="text-sm text-gray-600">
                  Use intelligent routing rules for optimal AI selection and collaboration
                </p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={useAdvancedRouting}
                  onChange={(e) => setUseAdvancedRouting(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>

            <button
              onClick={handleAnalyzeProblem}
              disabled={isAnalyzing || !problemContext.description.trim()}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {isAnalyzing ? 'Analyzing Problem...' : 'Get AI Recommendations'}
            </button>
          </div>
        </div>

        {/* AI Recommendation Results */}
        {recommendation && (
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-semibold text-gray-900">
                AI Collaboration Recommendation
              </h2>
              {routingResult && (
                <div className="flex items-center space-x-2">
                  <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                    Confidence: {Math.round(routingResult.confidence * 100)}%
                  </span>
                  {useAdvancedRouting && (
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                      Advanced Routing
                    </span>
                  )}
                </div>
              )}
            </div>

            {/* Routing Information */}
            {routingResult && (
              <div className="mb-6 p-4 bg-indigo-50 rounded-lg">
                <h3 className="text-sm font-semibold text-indigo-900 mb-2">Routing Analysis</h3>
                <p className="text-sm text-indigo-700">{routingResult.routingReason}</p>
              </div>
            )}

            {/* Primary AI */}
            <div className="mb-8">
              <h3 className="text-xl font-semibold text-green-700 mb-4">
                🎯 Lead AI: {recommendation.primaryAI.name}
              </h3>
              <div className="bg-green-50 rounded-lg p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Strengths:</h4>
                    <ul className="list-disc list-inside text-gray-700 space-y-1">
                      {recommendation.primaryAI.strengths.map((strength, index) => (
                        <li key={index}>{strength}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Specialties:</h4>
                    <ul className="list-disc list-inside text-gray-700 space-y-1">
                      {recommendation.primaryAI.specialties.map((specialty, index) => (
                        <li key={index}>{specialty}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            {/* Collaborating AIs */}
            {recommendation.collaboratingAIs.length > 0 && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold text-blue-700 mb-4">
                  🤝 Collaborating AIs
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {recommendation.collaboratingAIs.map((ai) => (
                    <div key={ai.id} className="bg-blue-50 rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900 mb-2">{ai.name}</h4>
                      <p className="text-sm text-gray-600 mb-2">
                        Key Specialty: {ai.specialties[0]}
                      </p>
                      <div className="text-xs text-gray-500">
                        Confidence: {Math.round(ai.confidence * 100)}%
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Reasoning */}
            <div className="mb-8">
              <h3 className="text-xl font-semibold text-purple-700 mb-4">
                💡 Why This Recommendation?
              </h3>
              <div className="bg-purple-50 rounded-lg p-6">
                <p className="text-gray-700">{recommendation.reasoning}</p>
              </div>
            </div>

            {/* Workflow */}
            <div className="mb-8">
              <h3 className="text-xl font-semibold text-orange-700 mb-4">
                🔄 Suggested Workflow
              </h3>
              <div className="bg-orange-50 rounded-lg p-6">
                <ol className="list-decimal list-inside space-y-2 text-gray-700">
                  {recommendation.workflow.map((step, index) => (
                    <li key={index}>{step}</li>
                  ))}
                </ol>
              </div>
            </div>

            {/* Alternative Routes */}
            {routingResult && routingResult.alternativeRoutes.length > 0 && (
              <div className="mb-8">
                <h3 className="text-xl font-semibold text-gray-700 mb-4">
                  🔀 Alternative Approaches
                </h3>
                <div className="space-y-4">
                  {routingResult.alternativeRoutes.map((alt, index) => (
                    <div key={index} className="bg-gray-50 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-semibold text-gray-900">{alt.primaryAI.name} Lead</h4>
                        <span className="text-sm text-gray-500">Alternative #{index + 1}</span>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{alt.reasoning}</p>
                      {alt.collaboratingAIs.length > 0 && (
                        <div className="text-xs text-gray-500">
                          Collaborators: {alt.collaboratingAIs.map(ai => ai.name).join(', ')}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Available AIs Overview */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            Available AI Platforms
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {availableAIs.map((ai) => (
              <div key={ai.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <h3 className="font-semibold text-gray-900 mb-2">{ai.name}</h3>
                <div className="text-sm text-gray-600 mb-3">
                  Confidence: {Math.round(ai.confidence * 100)}%
                </div>
                <div className="space-y-2">
                  <div>
                    <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                      Top Strengths:
                    </span>
                    <p className="text-sm text-gray-700">
                      {ai.strengths.slice(0, 2).join(', ')}
                    </p>
                  </div>
                  <div>
                    <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                      Specialties:
                    </span>
                    <p className="text-sm text-gray-700">
                      {ai.specialties.slice(0, 2).join(', ')}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};