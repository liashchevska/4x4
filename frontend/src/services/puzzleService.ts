import type { Group } from "@/types";
import apiClient from "./apiClient";

const puzzles = {
  create(groups: Group[]) {
    return apiClient.post("/puzzles/", { groups });
  },
  get(id: string) {
    return apiClient.get(`/puzzles/${id}`);
  },
  // makeGuess() {},
};

export default puzzles;
