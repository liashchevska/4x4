import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Grid } from "./Grid";
import type { Word } from "@/types";
import { GROUP_SIZE, words } from "@/constants";

const onSelectionChange = vi.fn();

const renderGrid = (words: Word[], selectedIds: Set<string> = new Set()) => {
  render(
    <Grid
      words={words}
      selectedIds={selectedIds}
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

    expect(onSelectionChange).toHaveBeenCalledWith(new Set([words[0].id]));
  });

  it("calls onSelectionChange with the updated selection when deselecting a word", async () => {
    renderGrid(words, new Set([words[0].id]));

    const user = userEvent.setup();
    await user.click(screen.getByText(words[0].text));

    expect(onSelectionChange).toHaveBeenCalledWith(new Set());
  });

  it("does not allow selecting more than GROUP_SIZE items", async () => {
    const ids = words.map((item) => item.id);
    renderGrid(words, new Set(ids.slice(0, GROUP_SIZE)));

    const user = userEvent.setup();
    await user.click(screen.getByText(words[GROUP_SIZE].text));

    expect(onSelectionChange).not.toHaveBeenCalled();
  });

  it("sets aria-pressed according to selection state", () => {
    renderGrid(words, new Set([words[0].id]));
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
