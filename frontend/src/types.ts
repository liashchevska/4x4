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
  hasEmptyFields: boolean;
  emptyFields: GroupEmptyFlags[];
};

export type Word = {
  id: string;
  text: string;
};

export type GuessedGroup = {
  title: string;
  words: Set<string>;
};
