import { BrowserRouter, Routes, Route } from "react-router-dom";

// 各ページのファイルをimport
import Reservation from "./pages/Reservation";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* 予約画面 */}
        <Route
          path="/" // URL
          element={<Reservation />} // page関数
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App