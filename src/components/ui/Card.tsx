import { forwardRef, HTMLAttributes } from 'react'
import { motion, MotionProps } from 'framer-motion'

interface CardProps extends Omit<HTMLAttributes<HTMLDivElement>, keyof MotionProps> {
  variant?: 'default' | 'elevated' | 'outlined'
  padding?: 'none' | 'sm' | 'md' | 'lg'
  hover?: boolean
  children?: React.ReactNode
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ 
    className = '', 
    variant = 'default', 
    padding = 'md',
    hover = false,
    children, 
    ...props 
  }, ref) => {
    const baseClasses = 'rounded-lg transition-all duration-200'
    
    const variants = {
      default: 'bg-white border border-gray-200',
      elevated: 'bg-white shadow-md',
      outlined: 'bg-white border-2 border-gray-300'
    }
    
    const paddings = {
      none: '',
      sm: 'p-3',
      md: 'p-6',
      lg: 'p-8'
    }
    
    const hoverClasses = hover ? 'hover:shadow-lg hover:border-gray-300' : ''
    
    const classes = `
      ${baseClasses}
      ${variants[variant]}
      ${paddings[padding]}
      ${hoverClasses}
      ${className}
    `.trim()

    return (
      <motion.div
        ref={ref}
        className={classes}
        whileHover={hover ? { y: -2 } : undefined}
        {...props}
      >
        {children}
      </motion.div>
    )
  }
)

Card.displayName = 'Card'

export { Card }
export type { CardProps }