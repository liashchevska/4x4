import type { GuessedGroup, Word } from "./types";

export const GROUP_SIZE = 4;
// [add] error messages

// Test fixtures
export const words: Word[] = [
  { id: "1", text: "Cat" },
  { id: "2", text: "Dog" },
  { id: "3", text: "Fox" },
  { id: "4", text: "Pig" },
  { id: "5", text: "Bream" },
];

export const group: GuessedGroup = {
  title: "Animals",
  //   words.map((item) => item.id).slice(0, 4)
  words: new Set(["1", "2", "3", "4"]),
};
