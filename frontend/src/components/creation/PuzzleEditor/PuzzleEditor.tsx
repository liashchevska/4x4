import { useState } from "react";
import type { Group } from "@/types";
import { GroupEditor } from "../GroupEditor";
import styles from "./PuzzleEditor.module.css";

export function PuzzleEditor() {
  const [groups, setGroups] = useState<Group[]>(
    Array.from({ length: 4 }, () => ({ title: "", words: ["", "", "", ""] }))
  );

  const handleTitleChange = (groupIndex: number, value: string) => {
    setGroups((current) =>
      current.map((group, i) => (i === groupIndex ? { ...group, title: value } : group))
    );
  };

  const handleWordChange = (groupIndex: number, wordIndex: number, value: string) => {
    const updateWords = (group: Group) => {
      return group.words.map((word, j) => (wordIndex === j ? value : word));
    };

    setGroups((current) =>
      current.map((group, i) =>
        i === groupIndex ? { ...group, words: updateWords(group) } : group
      )
    );
  };

  const createPuzzle = () => {
    console.log(groups);
    return;
  };

  return (
    <>
      <form action={createPuzzle}>
        {groups.map((group, groupIndex) => (
          <GroupEditor
            key={groupIndex}
            group={group}
            onTitleChange={(value) => handleTitleChange(groupIndex, value)}
            onWordChange={(wordIndex, value) =>
              handleWordChange(groupIndex, wordIndex, value)
            }
          />
        ))}
        <button type="submit">Create a puzzle</button>
      </form>
    </>
  );
}
