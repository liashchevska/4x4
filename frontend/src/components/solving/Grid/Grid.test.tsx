import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Grid } from "./Grid";
import type { Word } from "@/types";

const words: Word[] = [
  { id: "1", text: "Cat" },
  { id: "2", text: "Dog" },
  { id: "3", text: "Fox" },
];

const onSelectionChange = vi.fn();

const renderGrid = (words: Word[], selectedWords: Word[] = []) => {
  render(
    <Grid
      words={words}
      selectedWords={selectedWords}
      onSelectionChange={onSelectionChange}
    />
  );
};

describe("Grid", () => {
  beforeEach(() => {
    onSelectionChange.mockClear();
  });

  it("renders all words", () => {
    renderGrid(words);

    words.forEach((word) => {
      expect(screen.getByText(word.text)).toBeInTheDocument();
    });
  });

  it("calls onSelectionChange with the updated selection when selecting a word", async () => {
    renderGrid(words);

    const user = userEvent.setup();
    await user.click(screen.getByText(words[0].text));

    expect(onSelectionChange).toHaveBeenCalledWith([words[0]]);
  });

  it("calls onSelectionChange with the updated selection when deselecting a word", async () => {
    renderGrid(words, [words[0]]);

    const user = userEvent.setup();
    await user.click(screen.getByText(words[0].text));

    expect(onSelectionChange).toHaveBeenCalledWith([]);
  });

  it("sets aria-pressed according to selection state", () => {
    renderGrid(words, [words[0]]);
    expect(screen.getByRole("button", { name: words[0].text })).toHaveAttribute(
      "aria-pressed",
      "true"
    );

    expect(screen.getByRole("button", { name: words[1].text })).toHaveAttribute(
      "aria-pressed",
      "false"
    );
  });
});
