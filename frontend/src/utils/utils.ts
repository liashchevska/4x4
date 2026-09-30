import type { Group, GroupEmptyFlags } from "../types";

function createEmptyGroups(groupsPerPuzzle = 4, wordsPerGroup = 4): Group[] {
  return Array.from({ length: groupsPerPuzzle }, () => ({
    title: "",
    words: Array.from({ length: wordsPerGroup }, () => ""),
  }));
}

function normalizeForComparison(value: string): string {
  return value.trim().toLowerCase();
}

/**
 * Checks a group for empty fields.
 * @returns An object containing empty-field flags for the title and words.
 * `true` indicates that the corresponding value is empty.
 */
function validateGroup(group: Group): GroupEmptyFlags {
  return {
    title: group.title.trim() === "",
    words: group.words.map((word) => word.trim() === ""),
  };
}

function validateGroups(groups: Group[]): GroupEmptyFlags[] {
  return groups.map((group) => validateGroup(group));
}

/**
 * Checks the whole puzzle (all words across groups) for duplicate words.
 * @returns Whether duplicate words are present.
 */
function hasDuplicateWords(groups: Group[]): boolean {
  const words = groups
    .flatMap((group) => group.words)
    .map(normalizeForComparison)
    // Empty values are handled separately by validateGroups, thus excluded here.
    .filter(Boolean);
  return new Set(words).size !== words.length;
}

/**
 * Checks the  puzzle for duplicate titles.
 * @returns Whether duplicate titles are present.
 */
function hasDuplicateTitles(groups: Group[]): boolean {
  const titles = groups
    .map((group) => normalizeForComparison(group.title))
    .filter(Boolean);
  return new Set(titles).size !== titles.length;
}

/**
 * Validates the puzzle.
 * @returns Validation results for the puzzle.
 */
function validatePuzzle(groups: Group[]) {
  const emptyFields = validateGroups(groups);
  const duplicateWords = hasDuplicateWords(groups);
  const duplicateTitles = hasDuplicateTitles(groups);

  const hasEmptyFields = emptyFields.some(
    ({ title, words }) => title || words.some(Boolean)
  );

  return {
    isValid: !hasEmptyFields && !duplicateWords && !duplicateTitles,
    hasDuplicateWords: duplicateWords,
    hasDuplicateTitles: duplicateTitles,
    emptyFields,
  };
}

export {
  createEmptyGroups,
  validateGroups,
  hasDuplicateWords,
  hasDuplicateTitles,
  validatePuzzle,
};
