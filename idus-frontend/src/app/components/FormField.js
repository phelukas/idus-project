const FormField = ({
  label,
  id,
  name,
  type,
  value,
  onChange,
  required,
  options,
}) => (
  <div className="mb-4">
    <label className="block text-gray-700 font-semibold mb-2" htmlFor={id}>
      {label}
    </label>
    {type === "select" ? (
      <select
        id={id}
        name={name}
        value={value}
        onChange={onChange}
        className="w-full px-3 py-2 border border-gray-900 rounded text-black"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    ) : (
      <input
        type={type}
        id={id}
        name={name}
        value={value}
        onChange={onChange}
        className="w-full px-3 py-2 border border-gray-900 rounded text-black"
        required={required}
      />
    )}
  </div>
);

export default FormField;
