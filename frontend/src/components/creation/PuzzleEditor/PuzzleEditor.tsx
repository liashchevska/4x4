import { useState } from "react";
import { type PuzzleValidationResult, type Group } from "@/types";
import { GroupEditor } from "../GroupEditor";
import { createEmptyGroups, validateGroups, validatePuzzle } from "@/utils";

import styles from "./PuzzleEditor.module.css";
import { ValidationErrors } from "./ValidationErrors";
import puzzles from "@/services/puzzleService";
import axios from "axios";

export function PuzzleEditor() {
  const [groups, setGroups] = useState(createEmptyGroups());
  const [validationResult, setValidationResult] = useState<PuzzleValidationResult>();
  const [serverValidation, setServerValidation] = useState<string[]>();
  const [puzzleId, setPuzzleId] = useState<string>();

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

  const createPuzzle = async () => {
    // reset previous errors
    setServerValidation(undefined);
    setValidationResult(undefined);

    const result = validatePuzzle(groups);
    setValidationResult(result);
    if (!result.isValid) {
      return;
    }
    try {
      const response = await puzzles.create(groups);
      setPuzzleId(response.data.id);
    } catch (e) {
      if (axios.isAxiosError(e)) {
        if (e.response?.status === 422) {
          const detail = e.response.data?.detail;
          if (Array.isArray(detail)) {
            setServerValidation(detail.map((item) => item.msg));
          }
        }
      }
    }
  };

  if (puzzleId) {
    // copy on click / go to link
    return <p>created puzzle id: {puzzleId}</p>;
  }
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
      {validationResult && !validationResult.isValid && (
        <ValidationErrors
          result={validationResult}
          serverValidation={serverValidation}
        />
      )}
    </>
  );
}
