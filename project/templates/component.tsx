import React from 'react';
import styles from './ComponentName.module.css';

export interface ComponentNameProps {
  /**
   * The primary content of the component
   */
  children?: React.ReactNode;
  
  /**
   * Additional CSS class names
   */
  className?: string;
  
  /**
   * Optional callback when the component is clicked
   */
  onClick?: () => void;
  
  /**
   * Whether the component is disabled
   * @default false
   */
  disabled?: boolean;
}

/**
 * ComponentName component
 * 
 * A brief description of what this component does and when to use it.
 * 
 * @example
 * ```tsx
 * <ComponentName>Content</ComponentName>
 * ```
 */
export const ComponentName: React.FC<ComponentNameProps> = ({
  children,
  className = '',
  onClick,
  disabled = false,
  ...restProps
}) => {
  const handleClick = () => {
    if (!disabled && onClick) {
      onClick();
    }
  };

  return (
    <div 
      className={`component-name ${className} ${disabled ? 'component-name--disabled' : ''}`}
      onClick={handleClick}
      {...restProps}
    >
      {children}
    </div>
  );
};

export default ComponentName;