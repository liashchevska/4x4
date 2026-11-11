import type { Group, Word } from "@/types";
import apiClient from "./apiClient";

const puzzles = {
  create(groups: Group[]) {
    return apiClient.post("/puzzles/", { groups });
  },
  get(id: string) {
    return apiClient.get(`/puzzles/${id}`);
  },
  guessGroup(id: string, selectedIds: Set<string>) {
    return apiClient.post(`/puzzles/${id}/guess`, { words: [...selectedIds] });
  },
};

export default puzzles;
