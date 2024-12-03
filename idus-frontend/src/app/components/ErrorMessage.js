const ErrorMessage = ({ errors }) => {
  if (!errors) return null;

  if (typeof errors === "object" && !Array.isArray(errors)) {
    return (
      <div className="mt-6 text-red-600">
        <ul className="list-disc pl-5">
          {Object.entries(errors).map(([field, message]) => (
            <li key={field}>
              <strong>{field}:</strong> {message}
            </li>
          ))}
        </ul>
      </div>
    );
  }

 
  return null;
};

export default ErrorMessage;
