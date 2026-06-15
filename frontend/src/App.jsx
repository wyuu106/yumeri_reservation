import { BrowserRouter, Routes, Route } from "react-router-dom";

// 各ページのファイルをimport
import Reservation from "./pages/Reservation";
import Login from "./pages/Login";
import Admin from "./pages/Admin";
import Seat from "./pages/Seat";
import SeatPattern from "./pages/SeatPattern"

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* 予約画面 */}
        <Route
          path="/" // URL
          element={<Reservation />} // page関数
        />

        {/* ログイン画面 */}
        <Route
          path="/Login"
          element={<Login />}
        />

        {/* 管理者画面 */}
        <Route
          path="/Admin"
          element={<Admin />}
        />

        {/* 席管理画面 */}
        <Route
          path="/Admin/seats"
          element={<Seat />}
        />

        {/* 席の組み合わせ管理画面 */}
        <Route
          path="/Admin/seats/patterns"
          element={<SeatPattern />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App