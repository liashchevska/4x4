import type { PuzzleValidationResult as ValidationResult } from "@/types";

export function ValidationErrors({ result }: { result: ValidationResult }) {
  return (
    <>
      <p>{result.hasDuplicateTitles && "Group titles must be unique."}</p>
      <p>{result.hasDuplicateWords && "Words must be unique."}</p>
      <p>{result.hasEmptyFields && "All fields must be filled in."}</p>
    </>
  );
}
