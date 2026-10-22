import type { PuzzleValidationResult as ValidationResult } from "@/types";

export function ValidationErrors({
  result,
  serverValidation,
}: {
  result: ValidationResult;
  serverValidation?: string[];
}) {
  if (serverValidation === undefined) {
    return (
      <>
        <p>{result.hasDuplicateTitles && "Group titles must be unique"}</p>
        <p>{result.hasDuplicateWords && "Words must be unique across all groups"}</p>
        <p>{result.hasEmptyFields && "All fields must be filled in"}</p>
      </>
    );
  }
  return (
    <>
      <p>{serverValidation}</p>
    </>
  );
}
