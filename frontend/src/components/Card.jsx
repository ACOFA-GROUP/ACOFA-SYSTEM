const Card = ({ children, className = '', onClick }) => {
  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-lg shadow-sm p-6 ${
        onClick ? 'cursor-pointer hover:shadow-md transition-shadow' : ''
      } ${className}`}
    >
      {children}
    </div>
  );
};

export default Card;
