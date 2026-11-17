// enables button only if selected is GROUP SIZE
// doesnt call api if selected is already guessed

import { GROUP_SIZE, words, group } from "@/constants";
import puzzles from "@/services/puzzleService";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { PuzzleView } from "./PuzzleView";
import { serialize } from "@/hooks/useLocalStorage";
import type { Word } from "@/types";

vi.mock("@/services/puzzleService", () => ({
  default: {
    get: vi.fn(),
    guessGroup: vi.fn(),
  },
}));

vi.mock("react-router", () => ({
  useParams: () => ({ id: "puzzle-id-1" }),
}));

beforeEach(() => {
  localStorage.clear();
  vi.clearAllMocks();
  vi.mocked(puzzles.get, { partial: true }).mockResolvedValue({ data: { words } });
});

function setup() {
  render(<PuzzleView />);
  const user = userEvent.setup();
  const submit = screen.getByRole("button", { name: /submit/i });

  const selectWords = async (wordsToSelect: Word[]) => {
    for (const word of wordsToSelect) {
      await user.click(await screen.findByRole("button", { name: word.text }));
    }
  };

  const submitGuess = async (wordsToSelect: Word[]) => {
    await selectWords(wordsToSelect);
    await user.click(submit);
  };

  return { user, submit, selectWords, submitGuess };
}

describe("PuzzleView", () => {
  it("enables guess button only when 4 words are selected", async () => {
    const { submit, selectWords } = setup();
    expect(submit).toBeDisabled();

    await selectWords(words.slice(0, GROUP_SIZE - 1));
    expect(submit).toBeDisabled();

    await selectWords(words.slice(GROUP_SIZE - 1, GROUP_SIZE));
    expect(submit).toBeEnabled();
  });

  it("disables submit and displays a message for an already guessed combination", async () => {
    vi.mocked(puzzles.guessGroup, { partial: true }).mockResolvedValue({
      data: { correct: false },
    });

    const { submit, selectWords, submitGuess } = setup();
    const wordsInAGuess = words.slice(0, GROUP_SIZE);
    await submitGuess(wordsInAGuess);

    // [fix & test] clear selected on submit; reselect manually
    await selectWords(wordsInAGuess);
    await selectWords(wordsInAGuess);

    expect(submit).toBeDisabled();
    expect(screen.getByText(/already/i)).toBeInTheDocument();

    expect(puzzles.guessGroup).toHaveBeenCalledOnce();
  });

  it("does not call API if currently selected are already guessed", async () => {
    // [fix & test] clear selected on submit; reselect manually
    vi.mocked(puzzles.guessGroup, { partial: true }).mockResolvedValue({
      data: { correct: false },
    });

    const { user, submit, selectWords } = setup();
    await selectWords(words.slice(0, GROUP_SIZE));

    await user.click(submit);
    expect(puzzles.guessGroup).toHaveBeenCalledOnce();

    await user.click(submit);
    expect(puzzles.guessGroup).toHaveBeenCalledOnce();
  });

  it("removes correctly guessed words from the grid", async () => {
    vi.mocked(puzzles.guessGroup, { partial: true }).mockResolvedValue({
      data: { correct: true, group: group },
    });

    const { submitGuess } = setup();
    await submitGuess(words.slice(0, GROUP_SIZE));

    await waitFor(() => {
      expect(
        screen.queryByRole("button", { name: words[0].text })
      ).not.toBeInTheDocument();
    });

    expect(
      screen.getByRole("button", { name: words.at(-1)!.text })
    ).toBeInTheDocument();
  });

  it("saves solving progress to local storage", async () => {
    const { submitGuess } = setup();
    const wordsInAGuess = words.slice(0, GROUP_SIZE);
    await submitGuess(wordsInAGuess);

    const guessed = localStorage.getItem("guessed");
    expect(guessed).toEqual(serialize([group]));

    const history = localStorage.getItem("history");
    expect(history).toEqual(serialize([new Set(wordsInAGuess.map((item) => item.id))]));
  });
});
