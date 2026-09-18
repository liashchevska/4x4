import styles from "./GroupEditor.module.css";
import { WordInput } from "../WordInput";
import type { Group } from "@/types";
import { useId } from "react";

type GroupEditorProps = {
  group: Group;
  onTitleChange: (value: string) => void;
  onWordChange: (index: number, value: string) => void;
};

export function GroupEditor({ group, onTitleChange, onWordChange }: GroupEditorProps) {
  const id = useId() + "-group";

  return (
    <div className={styles.group}>
      <fieldset className={styles.wordList}>
        <legend className={styles.groupTitle}>Group</legend>
        <label htmlFor={id}>title: </label>
        <input
          id={id}
          value={group.title}
          onChange={(e) => onTitleChange(e.target.value)}
          placeholder="group title"
        />
        <span id="words-list">words:</span>
        {group.words.map((word, index) => (
          <WordInput
            key={index}
            text={word}
            onTextChange={(value) => {
              onWordChange(index, value);
            }}
          />
        ))}
      </fieldset>
    </div>
  );
}
