import type { Word } from "@/types";
import { useMemo } from "react";

type GridProps = {
  words: Word[];
  selectedWords: Word[];
  onSelectionChange: (updatedWords: Word[]) => void;
};

export function Grid({ words, selectedWords, onSelectionChange }: GridProps) {
  const selectedIds = useMemo(
    () => new Set(selectedWords.map((word) => word.id)),
    [selectedWords]
  );

  const toggleWord = (word: Word) => {
    const isSelected = selectedWords.some((x) => x.id === word.id);
    const nextSelectedWords = isSelected
      ? selectedWords.filter((x) => x.id !== word.id)
      : [...selectedWords, word];
    onSelectionChange(nextSelectedWords);
  };

  return (
    <>
      <div role="group">
        {words.map((word) => (
          <button
            key={word.id}
            onClick={() => toggleWord(word)}
            aria-pressed={selectedIds.has(word.id)}
          >
            {word.text}
          </button>
        ))}
      </div>
    </>
  );
}
