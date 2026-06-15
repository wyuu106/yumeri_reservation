// 席パターン管理ページ

import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { getErrorMessage } from "../utils/error_util";

function SeatPattern() {
  const [patterns, setPatterns] = useState([]);
  const [seats, setSeats] = useState([]);

  const [name, setName] = useState("");
  const [seatType, setSeatType] = useState("counter");
  const [isPrivate, setIsPrivate] = useState(false);

  const [minPeople, setMinPeople] = useState(1);
  const [maxPeople, setMaxPeople] = useState(1);

  const [selectedSeats, setSelectedSeats] = useState([]);

  const navigate = useNavigate();

  const token = localStorage.getItem("token"); // トークン
  
  // トークン取得
  const headers = {
    Authorization: `Bearer ${token}`,
  };

  // 席一覧取得
  const getSeats = async () => {
    try {
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

  // パターン一覧取得
  const getPatterns = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/admin/patterns",
        { headers }
      );

      const patternData = response.data;

      const patternsWithMembers = await Promise.all(
        patternData.map(async (pattern) => {
          const memberResponse = await axios.get(
            `http://127.0.0.1:8000/admin/members?pattern_id=${pattern.id}`,
            { headers }
          );

          return {
            ...pattern,
            members: memberResponse.data,
          };
        })
      );

      setPatterns(patternsWithMembers);
    } catch (error) {
      console.log(error);
      alert(getErrorMessage(error));
    }
  };

  // 席選択
  const toggleSeat = (seatId) => {
    if (selectedSeats.includes(seatId)) {
      setSelectedSeats(
        selectedSeats.filter((id) => id !== seatId)
      );
    } else {
      setSelectedSeats([...selectedSeats, seatId]);
    }
  };

  // パターン作成
  const createPattern = async () => {
    try {
      // パターン作成
      const response = await axios.post(
        "http://127.0.0.1:8000/admin/patterns",
        {
          name: name,
          seat_type: seatType,
          is_private: isPrivate,
          min_people: Number(minPeople),
          max_people: Number(maxPeople),
        },
        { headers }
      );

      const patternId = response.data.id;

      // member作成
      for (const seatId of selectedSeats) {
        await axios.post(
          "http://127.0.0.1:8000/admin/members",
          {
            pattern_id: patternId,
            seat_id: seatId,
          },
          { headers }
        );
      }

      setName("");
      setSeatType("counter");
      setIsPrivate(false);

      setMinPeople(1);
      setMaxPeople(1);

      setSelectedSeats([]);

      getPatterns();
    } catch (error) {
      console.log(error);
      alert(getErrorMessage(error));
    }
  };

  // パターン削除
  const deletePattern = async (patternId) => {
    try {
      await axios.delete(
        `http://127.0.0.1:8000/admin/pattern?pattern_id=${patternId}`,
        { headers }
      );

      getPatterns();
    } catch (error) {
      console.log(error);
      alert(getErrorMessage(error));
    }
  };

  useEffect(() => {
    getSeats();
    getPatterns();
  }, []);

  return (
    <div>
      <h1>席パターン管理</h1>

      <button onClick={() => navigate("/admin/seats")}>
        戻る
      </button>

      <h2>登録済み席パターン</h2>

      {patterns.length === 0 ? (
        <p>席パターンがありません</p>
      ) : (
        <table border="1">
          <thead>
            <tr>
              <th>ID</th>
              <th>名前</th>
              <th>席タイプ</th>
              <th>個室</th>
              <th>最小人数</th>
              <th>最大人数</th>
              <th>使用席</th>
              <th>削除</th>
            </tr>
          </thead>

          <tbody>
            {patterns.map((pattern) => (
              <tr key={pattern.id}>
                <td>{pattern.id}</td>

                <td>{pattern.name}</td>

                <td>{pattern.seat_type}</td>

                <td>
                  {pattern.is_private ? "○" : "×"}
                </td>

                <td>{pattern.min_people}</td>

                <td>{pattern.max_people}</td>

                <td>
                  {pattern.members.map((seat) => (
                    <span key={seat.id}>
                      {seat.name}
                    </span>
                  ))}
                </td>

                <td>
                  <button
                    onClick={() => deletePattern(pattern.id)}
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

      <h2>席パターン追加</h2>

      <div>
        <p>名前</p>

        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <div>
        <p>席タイプ</p>

        <select
          value={seatType}
          onChange={(e) => setSeatType(e.target.value)}
          >
          <option value="counter">カウンター</option>

          <option value="horigotatsu">掘りごたつ</option>

          <option value="tatami">座敷</option>
        </select>
      </div>

      <div>
        <label>
          <input
            type="checkbox"
            checked={isPrivate}
            onChange={(e) => setIsPrivate(e.target.checked)}
          />

          個室
        </label>
      </div>

      <div>
        <p>最小人数</p>

        <input
          type="number"
          value={minPeople}
          onChange={(e) => setMinPeople(e.target.value)}
        />
      </div>

      <div>
        <p>最大人数</p>

        <input
          type="number"
          value={maxPeople}
          onChange={(e) => setMaxPeople(e.target.value)}
        />
      </div>

      <div>
        <p>使用する席</p>

        {seats.map((seat) => (
          <div key={seat.id}>
            <label>
              <input
                type="checkbox"
                checked={selectedSeats.includes(seat.id)}
                onChange={() => toggleSeat(seat.id)}
              />

              {seat.name}
            </label>
          </div>
        ))}
      </div>

      <button onClick={createPattern}>
        追加
      </button>
    </div>
  );
}

export default SeatPattern;