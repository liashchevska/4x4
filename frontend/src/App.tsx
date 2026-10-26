import { PuzzleEditor } from "./components/creation/PuzzleEditor/PuzzleEditor";
import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PuzzleEditor />} />
        {/* <Route path="/link" element={} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
