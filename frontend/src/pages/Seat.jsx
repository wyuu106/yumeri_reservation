// 席情報管理ページ

import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { getErrorMessage } from "../utils/error_util";

function Seat() {
  const [seats, setSeats] = useState([]);
  const [name, setName] = useState("");

  const token = localStorage.getItem("token"); // トークン
  
  // トークン取得
  const headers = {
    Authorization: `Bearer ${token}`,
  };

  const navigate = useNavigate();

  // 席一覧取得
  const getSeats = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.get(
        "http://127.0.0.1:8000/admin/seats",
        { headers }
      );

      setSeats(response.data);
    } catch (error) {
      console.log(error);
      alert(getErrorMessage(error));
    }
  };

  // 席追加
  const createSeat = async () => {
    try {
      const token = localStorage.getItem("token");

      await axios.post(
        "http://127.0.0.1:8000/admin/seats",
        {
          name: name,
        },
        { headers }
      );

      setName("");

      getSeats();
    } catch (error) {
      console.log(error);
      alert(getErrorMessage(error));
    }
  };

  // 席削除
  const deleteSeat = async (seatId) => {
    try {
      const token = localStorage.getItem("token");

      await axios.delete(
        `http://127.0.0.1:8000/admin/seat?seat_id=${seatId}`,
        { headers }
      );

      getSeats();
    } catch (error) {
      setErrorMessage("席削除に失敗しました");
    }
  };

  useEffect(() => {
    getSeats();
  }, []);

  return (
    <div>
      <h1>席管理</h1>

      <button onClick={() => navigate("/admin")}>
        戻る
      </button>

      <button onClick={() => navigate("/admin/seats/patterns")}>
        席の組み合わせ管理画面へ
      </button>

      <h2>登録済み席一覧</h2>

      {seats.length === 0 ? (
        <p>席がありません</p>
      ) : (
        <table
        border="1"
        cellPadding="8"
        style={{
          margin: "0 auto",
          borderCollapse: "collapse",
          textAlign: "center",
        }}
      >
          <thead>
            <tr>
              <th>ID</th>
              <th>席名</th>
              <th>操作</th>
            </tr>
          </thead>

          <tbody>
            {seats.map((seat) => (
              <tr key={seat.id}>
                <td>{seat.id}</td>

                <td>{seat.name}</td>

                <td>
                  <button
                    onClick={() => deleteSeat(seat.id)}
                  >
                    削除
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <hr />

      <h2>席追加</h2>

      <div>
        <p>席名</p>

        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <button onClick={createSeat}>
        追加
      </button>
    </div>
  );
}

export default Seat;