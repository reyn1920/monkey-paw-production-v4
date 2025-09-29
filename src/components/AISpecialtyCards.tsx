import React from 'react';
import { AICapability } from '../services/AICollaborationService';

interface AISpecialtyCardsProps {
  ais: AICapability[];
  onSelectAI?: (ai: AICapability) => void;
  selectedAI?: string;
}

const aiIcons: Record<string, string> = {
  'cursor': '🎯',
  'bolt': '⚡',
  'firebase': '🔥',
  'trae': '🤖',
  'vscode': '💻',
  'windsurf': '🌊'
};

const aiColors: Record<string, string> = {
  'cursor': 'from-blue-500 to-purple-600',
  'bolt': 'from-yellow-400 to-orange-500',
  'firebase': 'from-orange-500 to-red-600',
  'trae': 'from-green-500 to-teal-600',
  'vscode': 'from-blue-600 to-indigo-700',
  'windsurf': 'from-cyan-500 to-blue-500'
};

export const AISpecialtyCards: React.FC<AISpecialtyCardsProps> = ({
  ais,
  onSelectAI,
  selectedAI
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {ais.map((ai) => {
        const isSelected = selectedAI === ai.id;
        const icon = aiIcons[ai.id] || '🤖';
        const colorGradient = aiColors[ai.id] || 'from-gray-500 to-gray-600';
        
        return (
          <div
            key={ai.id}
            className={`relative overflow-hidden rounded-xl transition-all duration-300 cursor-pointer transform hover:scale-105 ${
              isSelected 
                ? 'ring-4 ring-blue-500 shadow-2xl' 
                : 'shadow-lg hover:shadow-xl'
            }`}
            onClick={() => onSelectAI?.(ai)}
          >
            {/* Gradient Background */}
            <div className={`absolute inset-0 bg-gradient-to-br ${colorGradient} opacity-90`} />
            
            {/* Content */}
            <div className="relative p-6 text-white">
              {/* Header */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <span className="text-3xl">{icon}</span>
                  <div>
                    <h3 className="text-xl font-bold">{ai.name}</h3>
                    <div className="text-sm opacity-90">
                      Confidence: {Math.round(ai.confidence * 100)}%
                    </div>
                  </div>
                </div>
                {isSelected && (
                  <div className="bg-white bg-opacity-20 rounded-full p-2">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                )}
              </div>

              {/* Primary Strengths */}
              <div className="mb-4">
                <h4 className="text-sm font-semibold mb-2 opacity-90">Primary Strengths</h4>
                <div className="space-y-1">
                  {ai.strengths.slice(0, 3).map((strength, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <div className="w-1.5 h-1.5 bg-white rounded-full opacity-75" />
                      <span className="text-sm">{strength}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Specialties */}
              <div className="mb-4">
                <h4 className="text-sm font-semibold mb-2 opacity-90">Key Specialties</h4>
                <div className="flex flex-wrap gap-1">
                  {ai.specialties.slice(0, 4).map((specialty, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-white bg-opacity-20 rounded-full text-xs font-medium"
                    >
                      {specialty}
                    </span>
                  ))}
                </div>
              </div>

              {/* Top Specialties */}
              <div>
                <h4 className="text-sm font-semibold mb-2 opacity-90">Best For</h4>
                <div className="text-sm opacity-90">
                  {ai.specialties.slice(0, 2).join(' • ')}
                </div>
              </div>

              {/* Selection Indicator */}
              {isSelected && (
                <div className="absolute top-4 right-4">
                  <div className="bg-white bg-opacity-30 rounded-full p-1">
                    <div className="bg-white rounded-full w-3 h-3" />
                  </div>
                </div>
              )}
            </div>

            {/* Hover Effect Overlay */}
            <div className="absolute inset-0 bg-white opacity-0 hover:opacity-10 transition-opacity duration-300" />
          </div>
        );
      })}
    </div>
  );
};

// Individual AI Detail Card Component
interface AIDetailCardProps {
  ai: AICapability;
  className?: string;
}

export const AIDetailCard: React.FC<AIDetailCardProps> = ({ ai, className = '' }) => {
  const icon = aiIcons[ai.id] || '🤖';
  const colorGradient = aiColors[ai.id] || 'from-gray-500 to-gray-600';

  return (
    <div className={`bg-white rounded-xl shadow-lg overflow-hidden ${className}`}>
      {/* Header with Gradient */}
      <div className={`bg-gradient-to-r ${colorGradient} p-6 text-white`}>
        <div className="flex items-center space-x-4">
          <span className="text-4xl">{icon}</span>
          <div>
            <h2 className="text-2xl font-bold">{ai.name}</h2>
            <p className="opacity-90">Confidence Level: {Math.round(ai.confidence * 100)}%</p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-6 space-y-6">
        {/* Strengths */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Core Strengths</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {ai.strengths.map((strength, index) => (
              <div key={index} className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full" />
                <span className="text-gray-700">{strength}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Specialties */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Specialties</h3>
          <div className="flex flex-wrap gap-2">
            {ai.specialties.map((specialty, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
              >
                {specialty}
              </span>
            ))}
          </div>
        </div>

        {/* Core Capabilities */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Core Capabilities</h3>
          <div className="space-y-2">
            {ai.specialties.map((specialty, index) => (
              <div key={index} className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-purple-500 rounded-full" />
                <span className="text-gray-700">{specialty}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Integration Status */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-2">Integration Status</h4>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full" />
            <span className="text-sm text-gray-600">Ready for collaboration</span>
          </div>
        </div>
      </div>
    </div>
  );
};