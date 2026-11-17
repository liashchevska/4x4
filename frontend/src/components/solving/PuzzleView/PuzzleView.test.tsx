// enables button only if selected is GROUP SIZE
// doesnt call api if selected is already guessed

import { GROUP_SIZE, words, group } from "@/constants";
import puzzles from "@/services/puzzleService";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { PuzzleView } from "./PuzzleView";
import { serialize } from "@/hooks/useLocalStorage";

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

describe("PuzzleView", () => {
  it("enables guess button only when 4 words are selected", async () => {
    const user = userEvent.setup();
    render(<PuzzleView />);

    const submit = screen.getByRole("button", { name: /submit/i });

    expect(submit).toBeDisabled();
    for (const word of words.slice(0, GROUP_SIZE - 1)) {
      await user.click(await screen.findByRole("button", { name: word.text }));
    }
    expect(submit).toBeDisabled();
    await user.click(
      await screen.findByRole("button", { name: words[GROUP_SIZE].text })
    );
    expect(submit).toBeEnabled();
  });

  it("does not call API if currently selected are already guessed", async () => {
    const user = userEvent.setup();
    render(<PuzzleView />);

    const submit = screen.getByRole("button", { name: /submit/i });

    for (const word of words.slice(0, GROUP_SIZE)) {
      await user.click(await screen.findByRole("button", { name: word.text }));
    }
    await user.click(submit);
    expect(puzzles.guessGroup).toHaveBeenCalledOnce();

    await user.click(submit);
    expect(puzzles.guessGroup).toHaveBeenCalledOnce();
  });

  it("removes correctly guessed words from the grid", async () => {
    vi.mocked(puzzles.guessGroup, { partial: true }).mockResolvedValue({
      data: { correct: true, group: group },
    });

    const user = userEvent.setup();
    render(<PuzzleView />);

    for (const word of words.slice(0, GROUP_SIZE)) {
      await user.click(await screen.findByRole("button", { name: word.text }));
    }
    await user.click(screen.getByRole("button", { name: /submit/i }));
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
    const user = userEvent.setup();
    render(<PuzzleView />);

    const submit = screen.getByRole("button", { name: /submit/i });
    const wordsInGuess = words.slice(0, GROUP_SIZE);
    for (const word of wordsInGuess) {
      await user.click(await screen.findByRole("button", { name: word.text }));
    }
    await user.click(submit);

    const guessed = localStorage.getItem("guessed");
    expect(guessed).toEqual(serialize([group]));

    const history = localStorage.getItem("history");
    expect(history).toEqual(serialize([new Set(wordsInGuess.map((item) => item.id))]));
  });
});
