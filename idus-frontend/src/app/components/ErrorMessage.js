const ErrorMessage = ({ errors, message }) => {
  if (!errors && !message) return null;

  const singleMessage = message || (typeof errors === "string" ? errors : null);

  if (singleMessage) {
    return <p className="mt-6 text-red-600">{singleMessage}</p>;
  }

  if (typeof errors === "object" && !Array.isArray(errors)) {
    return (
      <div className="mt-6 text-red-600">
        <ul className="list-disc pl-5">
          {Object.entries(errors).map(([field, errorMessage]) => (
            <li key={field}>
              <strong>{field}:</strong> {errorMessage}
            </li>
          ))}
        </ul>
      </div>
    );
  }

  return null;
};

export default ErrorMessage;
