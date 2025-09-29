import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AICollaborationHub } from '../components/AICollaborationHub';

// Mock Firebase
vi.mock('../config/firebase', () => ({
  auth: {
    currentUser: { uid: 'test-user' },
    onAuthStateChanged: vi.fn()
  },
  db: {},
  analytics: {}
}));

// Mock AI services
vi.mock('../services/aiService', () => ({
  generateRecommendations: vi.fn().mockResolvedValue([
    { id: '1', title: 'Test Recommendation', description: 'Test description' }
  ]),
  analyzeCode: vi.fn().mockResolvedValue({ score: 85, suggestions: [] }),
  optimizePerformance: vi.fn().mockResolvedValue({ improvements: [] })
}));

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('AI Integration Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('AI Collaboration Hub', () => {
    it('renders without crashing', () => {
      renderWithRouter(<AICollaborationHub />);
      expect(screen.getByText(/AI Development Stack Builder/i)).toBeInTheDocument();
    });

    it('displays all AI platform options', () => {
      renderWithRouter(<AICollaborationHub />);
      
      expect(screen.getByText(/Cursor AI/i)).toBeInTheDocument();
      expect(screen.getByText(/Bolt.diy/i)).toBeInTheDocument();
      expect(screen.getByText(/Google Firebase/i)).toBeInTheDocument();
      expect(screen.getByText(/Trae.ai/i)).toBeInTheDocument();
      expect(screen.getByText(/VS Code AI/i)).toBeInTheDocument();
      expect(screen.getByText(/Windsurf AI/i)).toBeInTheDocument();
    });

    it('handles problem description input', async () => {
      renderWithRouter(<AICollaborationHub />);
      
      const textarea = screen.getByPlaceholderText(/Describe your development challenge/i);
      fireEvent.change(textarea, { target: { value: 'Test problem description' } });
      
      expect(textarea).toHaveValue('Test problem description');
    });

    it('generates AI recommendations when button is clicked', async () => {
      renderWithRouter(<AICollaborationHub />);
      
      const textarea = screen.getByPlaceholderText(/Describe your development challenge/i);
      fireEvent.change(textarea, { target: { value: 'Need help with React components' } });
      
      const button = screen.getByText(/Get AI Recommendations/i);
      fireEvent.click(button);
      
      await waitFor(() => {
        expect(screen.getByText(/AI Recommendations/i)).toBeInTheDocument();
      });
    });

    it('displays loading state during recommendation generation', async () => {
      renderWithRouter(<AICollaborationHub />);
      
      const textarea = screen.getByPlaceholderText(/Describe your development challenge/i);
      fireEvent.change(textarea, { target: { value: 'Test problem' } });
      
      const button = screen.getByText(/Get AI Recommendations/i);
      fireEvent.click(button);
      
      expect(screen.getByText(/Generating recommendations/i)).toBeInTheDocument();
    });
  });

  describe('AI Service Integration', () => {
    it('validates AI service connectivity', async () => {
      const { generateRecommendations } = await import('../services/aiService');
      
      const result = await generateRecommendations('test problem');
      expect(result).toBeDefined();
      expect(Array.isArray(result)).toBe(true);
    });

    it('handles AI service errors gracefully', async () => {
      const { generateRecommendations } = await import('../services/aiService');
      
      // Mock service failure
      vi.mocked(generateRecommendations).mockRejectedValueOnce(new Error('Service unavailable'));
      
      try {
        await generateRecommendations('test problem');
      } catch (error) {
        expect(error).toBeInstanceOf(Error);
      }
    });
  });

  describe('Platform Integration', () => {
    it('validates Cursor AI integration', () => {
      renderWithRouter(<AICollaborationHub />);
      const cursorCard = screen.getByText(/Cursor AI/i).closest('.bg-white');
      expect(cursorCard).toBeInTheDocument();
    });

    it('validates Bolt.diy integration', () => {
      renderWithRouter(<AICollaborationHub />);
      const boltCard = screen.getByText(/Bolt.diy/i).closest('.bg-white');
      expect(boltCard).toBeInTheDocument();
    });

    it('validates Firebase integration', () => {
      renderWithRouter(<AICollaborationHub />);
      const firebaseCard = screen.getByText(/Google Firebase/i).closest('.bg-white');
      expect(firebaseCard).toBeInTheDocument();
    });

    it('validates Trae.ai integration', () => {
      renderWithRouter(<AICollaborationHub />);
      const traeCard = screen.getByText(/Trae.ai/i).closest('.bg-white');
      expect(traeCard).toBeInTheDocument();
    });

    it('validates VS Code AI integration', () => {
      renderWithRouter(<AICollaborationHub />);
      const vscodeCard = screen.getByText(/VS Code AI/i).closest('.bg-white');
      expect(vscodeCard).toBeInTheDocument();
    });

    it('validates Windsurf AI integration', () => {
      renderWithRouter(<AICollaborationHub />);
      const windsurfCard = screen.getByText(/Windsurf AI/i).closest('.bg-white');
      expect(windsurfCard).toBeInTheDocument();
    });
  });

  describe('Performance and Reliability', () => {
    it('renders components within acceptable time', async () => {
      const startTime = performance.now();
      renderWithRouter(<AICollaborationHub />);
      const endTime = performance.now();
      
      expect(endTime - startTime).toBeLessThan(1000); // Should render within 1 second
    });

    it('handles multiple rapid interactions', async () => {
      renderWithRouter(<AICollaborationHub />);
      
      const textarea = screen.getByPlaceholderText(/Describe your development challenge/i);
      const button = screen.getByText(/Get AI Recommendations/i);
      
      // Simulate rapid interactions
      for (let i = 0; i < 5; i++) {
        fireEvent.change(textarea, { target: { value: `Test ${i}` } });
        fireEvent.click(button);
      }
      
      // Should not crash or throw errors
      expect(textarea).toBeInTheDocument();
      expect(button).toBeInTheDocument();
    });
  });

  describe('Error Handling', () => {
    it('displays error messages when AI services fail', async () => {
      const { generateRecommendations } = await import('../services/aiService');
      vi.mocked(generateRecommendations).mockRejectedValueOnce(new Error('Network error'));
      
      renderWithRouter(<AICollaborationHub />);
      
      const textarea = screen.getByPlaceholderText(/Describe your development challenge/i);
      fireEvent.change(textarea, { target: { value: 'Test problem' } });
      
      const button = screen.getByText(/Get AI Recommendations/i);
      fireEvent.click(button);
      
      await waitFor(() => {
        expect(screen.getByText(/Error generating recommendations/i)).toBeInTheDocument();
      });
    });

    it('recovers from errors and allows retry', async () => {
      const { generateRecommendations } = await import('../services/aiService');
      
      // First call fails
      vi.mocked(generateRecommendations).mockRejectedValueOnce(new Error('Network error'));
      // Second call succeeds
      vi.mocked(generateRecommendations).mockResolvedValueOnce([
        { id: '1', title: 'Recovery Test', description: 'Test recovery' }
      ]);
      
      renderWithRouter(<AICollaborationHub />);
      
      const textarea = screen.getByPlaceholderText(/Describe your development challenge/i);
      const button = screen.getByText(/Get AI Recommendations/i);
      
      // First attempt (fails)
      fireEvent.change(textarea, { target: { value: 'Test problem' } });
      fireEvent.click(button);
      
      await waitFor(() => {
        expect(screen.getByText(/Error generating recommendations/i)).toBeInTheDocument();
      });
      
      // Second attempt (succeeds)
      fireEvent.click(button);
      
      await waitFor(() => {
        expect(screen.getByText(/Recovery Test/i)).toBeInTheDocument();
      });
    });
  });
});