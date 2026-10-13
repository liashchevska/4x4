import { describe, expect, test } from "@jest/globals";
import {
  hasDuplicateTitles,
  hasDuplicateWords,
  validateGroups,
  validatePuzzle,
} from "./utils";

describe("puzzle validation", () => {
  test("validateGroups marks empty title and words", () => {
    const groups = [
      {
        title: "fruits",
        words: ["apple", "banana", "", "orange"],
      },
      {
        title: "",
        words: ["tomato", "potato", "", ""],
      },
    ];

    expect(validateGroups(groups)).toEqual([
      { title: false, words: [false, false, true, false] },
      { title: true, words: [false, false, true, true] },
    ]);
  });

  test("detects duplicate words", () => {
    const groups = [
      { title: "fruits", words: ["apple", "banana", "orange", "banana"] },
    ];

    expect(hasDuplicateWords(groups)).toBe(true);
  });

  test("detects duplicate titles", () => {
    const groups = [
      { title: "fruits", words: ["apple"] },
      { title: "fruits", words: ["tomato"] },
    ];

    expect(hasDuplicateTitles(groups)).toBe(true);
  });

  test("ignores empty values when checking for duplicates", () => {
    const groups = [
      { title: "", words: ["apple", "", "orange"] },
      { title: "", words: ["tomato", "", "potato"] },
    ];

    expect(hasDuplicateWords(groups)).toBe(false);
    expect(hasDuplicateTitles(groups)).toBe(false);
  });

  test("validates the puzzle", () => {
    const validPuzzle = [
      {
        title: "fruits",
        words: ["apple", "banana", "orange", "pear"],
      },
      {
        title: "vegetables",
        words: ["tomato", "potato", "carrot", "onion"],
      },
    ];

    expect(validatePuzzle(validPuzzle)).toEqual({
      isValid: true,
      hasDuplicateWords: false,
      hasDuplicateTitles: false,
      hasEmptyFields: false,
      emptyFields: [
        { title: false, words: [false, false, false, false] },
        { title: false, words: [false, false, false, false] },
      ],
    });

    const invalidPuzzle = [
      {
        title: "fruits",
        words: ["apple", "banana", "", "banana"],
      },
      {
        title: "",
        words: ["tomato", "potato", "carrot", "onion"],
      },
    ];
    expect(validatePuzzle(invalidPuzzle)).toEqual({
      isValid: false,
      hasDuplicateWords: true,
      hasDuplicateTitles: false,
      hasEmptyFields: true,
      emptyFields: [
        { title: false, words: [false, false, true, false] },
        { title: true, words: [false, false, false, false] },
      ],
    });
  });
});
