export type Group = {
  title: string;
  words: string[];
};

export type GroupEmptyFlags = {
  title: boolean;
  words: boolean[];
};

export type PuzzleValidationResult = {
  isValid: boolean;
  hasDuplicateTitles: boolean;
  hasDuplicateWords: boolean;
  emptyFields: GroupEmptyFlags[];
};
