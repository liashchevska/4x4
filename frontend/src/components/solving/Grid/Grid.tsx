import { GROUP_SIZE } from "@/constants";
import type { Word } from "@/types";
import styles from "./Grid.module.css";

type GridProps = {
  words: Word[];
  selectedIds: Set<string>;
  onSelectionChange: (updatedIds: Set<string>) => void;
};

export function Grid({ words, selectedIds, onSelectionChange }: GridProps) {
  const toggleWord = (word: Word) => {
    const selectedList = selectedIds.has(word.id)
      ? [...selectedIds].filter((id) => id !== word.id)
      : [...selectedIds, word.id];

    if (selectedList.length > GROUP_SIZE) return;
    onSelectionChange(new Set(selectedList));
  };

  return (
    <>
      <div role="group">
        {words.map((word) => {
          const isSelected = selectedIds.has(word.id);

          return (
            <button
              className={isSelected ? styles.selected : ""}
              key={word.id}
              onClick={() => toggleWord(word)}
              aria-pressed={isSelected}
            >
              {word.text}
            </button>
          );
        })}
      </div>
    </>
  );
}
