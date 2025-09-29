import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Plus, 
  Search, 
  Filter, 
  Download, 
  Play, 
  Star,
  Clock,
  Code,
  Database,
  Globe,
  Layers,
  Settings,
  Trash2,
  Edit
} from 'lucide-react'

interface StackTemplate {
  id: string
  name: string
  description: string
  category: 'frontend' | 'backend' | 'fullstack' | 'mobile' | 'ai'
  technologies: string[]
  rating: number
  downloads: number
  lastUpdated: string
  author: string
  featured: boolean
  testId: string
}

const mockTemplates: StackTemplate[] = [
  {
    id: '1',
    name: 'React + TypeScript + Vite',
    description: 'Modern React application with TypeScript, Vite, and Tailwind CSS',
    category: 'frontend',
    technologies: ['React', 'TypeScript', 'Vite', 'Tailwind CSS'],
    rating: 4.8,
    downloads: 1250,
    lastUpdated: '2024-01-15',
    author: 'StackBuilder Team',
    featured: true,
    testId: 'template-react-typescript'
  },
  {
    id: '2',
    name: 'FastAPI + PostgreSQL',
    description: 'High-performance API with FastAPI, PostgreSQL, and Redis caching',
    category: 'backend',
    technologies: ['FastAPI', 'PostgreSQL', 'Redis', 'Docker'],
    rating: 4.7,
    downloads: 890,
    lastUpdated: '2024-01-12',
    author: 'StackBuilder Team',
    featured: true,
    testId: 'template-fastapi-postgres'
  },
  {
    id: '3',
    name: 'Next.js Full Stack',
    description: 'Complete full-stack application with Next.js, Prisma, and tRPC',
    category: 'fullstack',
    technologies: ['Next.js', 'Prisma', 'tRPC', 'NextAuth.js'],
    rating: 4.9,
    downloads: 2100,
    lastUpdated: '2024-01-18',
    author: 'Community',
    featured: false,
    testId: 'template-nextjs-fullstack'
  },
  {
    id: '4',
    name: 'AI Chatbot Starter',
    description: 'AI-powered chatbot with OpenAI integration and vector database',
    category: 'ai',
    technologies: ['Python', 'OpenAI', 'Pinecone', 'Streamlit'],
    rating: 4.6,
    downloads: 650,
    lastUpdated: '2024-01-10',
    author: 'AI Team',
    featured: false,
    testId: 'template-ai-chatbot'
  }
]

const categories = [
  { id: 'all', name: 'All Templates', icon: Layers },
  { id: 'frontend', name: 'Frontend', icon: Globe },
  { id: 'backend', name: 'Backend', icon: Database },
  { id: 'fullstack', name: 'Full Stack', icon: Code },
  { id: 'ai', name: 'AI/ML', icon: Star }
]

export default function StackTemplates() {
  const [templates] = useState<StackTemplate[]>(mockTemplates)
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [showCreateModal, setShowCreateModal] = useState(false)

  const filteredTemplates = templates.filter(template => {
    const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory
    const matchesSearch = template.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         template.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         template.technologies.some(tech => tech.toLowerCase().includes(searchQuery.toLowerCase()))
    return matchesCategory && matchesSearch
  })

  const handleCreateTemplate = () => {
    setShowCreateModal(true)
  }

  const handleDeployTemplate = (template: StackTemplate) => {
    console.log(`Deploying template: ${template.name}`)
    // Implementation for template deployment
  }

  const getCategoryIcon = (category: string) => {
    const categoryData = categories.find(cat => cat.id === category)
    return categoryData ? categoryData.icon : Code
  }

  const getCategoryColor = (category: string) => {
    const colors = {
      frontend: 'bg-blue-100 text-blue-800',
      backend: 'bg-green-100 text-green-800',
      fullstack: 'bg-purple-100 text-purple-800',
      mobile: 'bg-orange-100 text-orange-800',
      ai: 'bg-pink-100 text-pink-800'
    }
    return colors[category as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Stack Templates</h1>
          <p className="mt-2 text-gray-600">
            Browse and deploy pre-configured development stacks
          </p>
        </div>
        <motion.button
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          onClick={handleCreateTemplate}
          className="btn-primary mt-4 sm:mt-0"
          data-testid="create-template-btn"
        >
          <Plus className="h-4 w-4 mr-2" />
          Create Template
        </motion.button>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search templates..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input pl-10"
            data-testid="search-templates"
          />
        </div>
        <div className="flex items-center space-x-2">
          <Filter className="h-4 w-4 text-gray-400" />
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="input min-w-[150px]"
            data-testid="category-filter"
          >
            {categories.map(category => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Category Tabs */}
      <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg overflow-x-auto">
        {categories.map(category => {
          const Icon = category.icon
          return (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`flex items-center px-3 py-2 rounded-md text-sm font-medium whitespace-nowrap transition-colors ${
                selectedCategory === category.id
                  ? 'bg-white text-primary-700 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              data-testid={`category-${category.id}`}
            >
              <Icon className="h-4 w-4 mr-2" />
              {category.name}
            </button>
          )
        })}
      </div>

      {/* Templates Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredTemplates.map((template, index) => {
          const CategoryIcon = getCategoryIcon(template.category)
          return (
            <motion.div
              key={template.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * index }}
              className="card hover:shadow-lg transition-shadow"
              data-testid={template.testId}
            >
              {/* Template Header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <CategoryIcon className="h-5 w-5 text-primary-600" />
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${getCategoryColor(template.category)}`}>
                    {template.category}
                  </span>
                  {template.featured && (
                    <Star className="h-4 w-4 text-yellow-500 fill-current" />
                  )}
                </div>
                <div className="flex items-center space-x-1">
                  <button className="p-1 text-gray-400 hover:text-gray-600">
                    <Edit className="h-4 w-4" />
                  </button>
                  <button className="p-1 text-gray-400 hover:text-red-600">
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>

              {/* Template Info */}
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{template.name}</h3>
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">{template.description}</p>

              {/* Technologies */}
              <div className="flex flex-wrap gap-1 mb-4">
                {template.technologies.slice(0, 3).map(tech => (
                  <span
                    key={tech}
                    className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-md"
                  >
                    {tech}
                  </span>
                ))}
                {template.technologies.length > 3 && (
                  <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-md">
                    +{template.technologies.length - 3} more
                  </span>
                )}
              </div>

              {/* Stats */}
              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center">
                    <Star className="h-3 w-3 mr-1 text-yellow-500" />
                    {template.rating}
                  </div>
                  <div className="flex items-center">
                    <Download className="h-3 w-3 mr-1" />
                    {template.downloads}
                  </div>
                </div>
                <div className="flex items-center">
                  <Clock className="h-3 w-3 mr-1" />
                  {new Date(template.lastUpdated).toLocaleDateString()}
                </div>
              </div>

              {/* Actions */}
              <div className="flex space-x-2">
                <button
                  onClick={() => handleDeployTemplate(template)}
                  className="btn-primary flex-1"
                  data-testid={`deploy-${template.id}`}
                >
                  <Play className="h-4 w-4 mr-2" />
                  Deploy
                </button>
                <button className="btn-secondary">
                  <Settings className="h-4 w-4" />
                </button>
              </div>

              {/* Author */}
              <div className="mt-3 pt-3 border-t border-gray-200">
                <p className="text-xs text-gray-500">by {template.author}</p>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Empty State */}
      {filteredTemplates.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-12"
        >
          <Layers className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No templates found</h3>
          <p className="text-gray-600 mb-4">
            Try adjusting your search or filter criteria, or create a new template.
          </p>
          <button
            onClick={handleCreateTemplate}
            className="btn-primary"
          >
            <Plus className="h-4 w-4 mr-2" />
            Create Your First Template
          </button>
        </motion.div>
      )}

      {/* Create Template Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-screen items-center justify-center p-4">
            <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setShowCreateModal(false)} />
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="relative bg-white rounded-lg shadow-xl max-w-md w-full p-6"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Template</h3>
              <p className="text-gray-600 mb-4">
                Template creation feature coming soon! This will allow you to save your current
                project configuration as a reusable template.
              </p>
              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="btn-secondary"
                >
                  Close
                </button>
                <button className="btn-primary" disabled>
                  Coming Soon
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      )}
    </div>
  )
}