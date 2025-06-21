const MCQChallenge = ({
  challenge,
  selectedOption,
  setSelectedOption,
  shouldShowExplanation,
  setShouldShowExplanation,
  isLoading,
}) => {
  const options =
    typeof challenge.options === "string"
      ? JSON.parse(challenge.options)
      : challenge.options;

  const handleOptionSelect = (index) => {
    if (selectedOption !== null) return;
    setSelectedOption(index);
    setShouldShowExplanation(true);
  };

  const getOptionClass = (index) => {
    if (selectedOption === null) return "option";

    if (index === challenge.correct_answer_id) {
      return "option correct";
    }
    if (selectedOption === index && index !== challenge.correct_answer_id) {
      return "option incorrect";
    }

    return "option";
  };

  if (isLoading) {
    return (
      <div
        className="challenge-display"
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "300px",
        }}
      >
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="challenge-display">
      <p>
        <strong>Difficulty</strong>: {challenge.difficulty}
      </p>
      <p className="challenge-title">{challenge.title}</p>
      <div className="options">
        {options.map((option, index) => (
          <div
            className={getOptionClass(index)}
            key={index}
            onClick={() => handleOptionSelect(index)}
          >
            {option}
          </div>
        ))}
      </div>
      {shouldShowExplanation && selectedOption !== null && (
        <div className="explanation">
          <h4>Explanation</h4>
          <p>{challenge.explanation}</p>
        </div>
      )}
    </div>
  );
};
export default MCQChallenge;
