import puzzles from "@/services/puzzleService";
import type { GuessedGroup, Word } from "@/types";
import axios from "axios";
import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router";
import { Grid } from "../Grid";
import { areSetsEqual } from "@/utils/utils";

export function PuzzleView() {
  const { id } = useParams();
  const [words, setWords] = useState<Word[]>([]);

  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [guessHistory, setGuessHistory] = useState<Set<string>[]>([]);
  const [correctlyGuessed, setCorrectlyGuessed] = useState<GuessedGroup[]>([]);

  useEffect(() => {
    if (!id) {
      return; // [add] handle missing id
    }
    const fetchPuzzle = async () => {
      try {
        const response = await puzzles.get(id);
        setWords(response.data.words);
      } catch (e) {
        if (axios.isAxiosError(e)) {
          console.log(e); // [add] handle 404 not found
        }
      }
    };

    fetchPuzzle();
  }, [id]);

  const remainingWords = useMemo(() => {
    const alreadyGuessedIds = new Set(
      correctlyGuessed.flatMap((guess) => [...guess.words])
    );
    return words.filter(({ id }) => !alreadyGuessedIds.has(id));
  }, [words, correctlyGuessed]);

  const guessGroup = async () => {
    if (guessHistory.some((guess) => areSetsEqual(guess, selectedIds))) {
      console.log("Already guessed!"); // [add] display message
      return;
    }

    setGuessHistory([...guessHistory, selectedIds]);

    try {
      const response = await puzzles.guessGroup(id!, selectedIds);
      if (response.data.correct) {
        setCorrectlyGuessed([...correctlyGuessed, response.data.group]);
        setSelectedIds(new Set());
      }
      // [add] handle incorrect & oneway
    } catch (e) {
      // [add] handle server errors
    }
  };

  return (
    <>
      <Grid
        words={remainingWords}
        selectedIds={selectedIds}
        onSelectionChange={setSelectedIds}
      />
      <button disabled={selectedIds.size !== 4} onClick={guessGroup}>
        submit
      </button>
    </>
  );
}
