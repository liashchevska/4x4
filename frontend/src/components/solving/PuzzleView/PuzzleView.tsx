import puzzles from "@/services/puzzleService";
import type { Word } from "@/types";
import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router";

export function PuzzleView() {
  const { id } = useParams();
  const [words, setWords] = useState<Word[]>([]);
  // filter word list after successful guess (like vue computed?)

  useEffect(() => {
    if (!id) {
      // handle missing id
      return;
    }
    const fetchPuzzle = async () => {
      try {
        const response = await puzzles.get(id);
        setWords(response.data.words);
      } catch (e) {
        if (axios.isAxiosError(e)) {
          // handle 404 not found
          console.log(e);
        }
      }
    };

    fetchPuzzle();
  }, [id]);

  return (
    <>
      <div>
        {words.map((item) => (
          <p>{item.text}</p>
        ))}
      </div>
    </>
  );
}
