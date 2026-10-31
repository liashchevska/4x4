import { PuzzleEditor } from "./components/creation/PuzzleEditor/PuzzleEditor";
import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router";
import { PuzzleView } from "./components/solving/PuzzleView";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PuzzleEditor />} />
        <Route path="/p/:id" element={<PuzzleView />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
