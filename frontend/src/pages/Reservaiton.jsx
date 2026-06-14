// 予約ページ

import { useState } from "react";
import axios from "axios";

function Reservation() {
  const [date, setDate] = useState("");
  const [people, setPeople] = useState(1);
  const [kids, setKids] = useState(0);
  const [seatType, setSeatType] = useState("any");
  const [course, setCourse] = useState("alacarte");
  const [isPrivate, setIsPrivate] = useState(false);

  const [times, setTimes] = useState([]);
  const [selectedTime, setSelectedTime] = useState(null);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");

  const [loading, setLoading] = useState(false);

  // 空き時間取得
  const getAvailability = async () => {
    setTimes([]);
    setSelectedTime(null);

    try {
      const res = await axios.get("http://localhost:8000/availability", {
        params: {
          date,
          people,
          kids,
          seat_type: seatType,
          course: people >= 4 ? course : "alacarte",
          is_private: people >= 7 && isPrivate,
        },
      });

      setTimes(res.data);
    } catch (error) {
      alert(error.response?.data?.detail || "取得失敗");
    }
  };

  // 予約確定
  const createReservation = async () => {
    if (!selectedTime) {
      alert("時間を選んでください");
      return;
    }

    setLoading(true);

    try {
      await axios.post("http://localhost:8000/reservations", {
        name,
        email,
        phone_number: phoneNumber,

        people,
        kids,
        seat_type: seatType,
        course: people >= 4 ? course : "alacarte",
        is_private: people >= 7 && isPrivate,
        start_at: selectedTime.start_at,
      });

      alert("予約完了！");
    } catch (error) {
      alert(error.response?.data?.detail || "予約失敗");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>予約ページ</h1>

      {/* 日付 */}
      <div>
        <p>日付</p>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </div>

      {/* 人数 */}
      <div>
        <p>人数</p>
        <input
          type="number"
          min={1}
          value={people}
          onChange={(e) => setPeople(Number(e.target.value) || 1)}
        />
      </div>

      {/* 子供 */}
      <div>
        <p>子供</p>
        <input
          type="number"
          min={0}
          value={kids}
          onChange={(e) => setKids(Number(e.target.value) || 0)}
        />
      </div>

      {/* 席タイプ */}
      <div>
        <p>席タイプ</p>
        <select value={seatType} onChange={(e) => setSeatType(e.target.value)}>
          <option value="any">指定なし</option>
          <option value="counter">カウンター</option>
          <option value="zashiki">座敷</option>
          <option value="horigotatsu">掘りごたつ</option>
        </select>
      </div>

      {/* コース */}
      {people >= 4 && (
        <div>
          <p>コース</p>
          <select value={course} onChange={(e) => setCourse(e.target.value)}>
            <option value="alacarte">単品</option>
            <option value="course1">4300円コース</option>
            <option value="course2">4300円＋飲み放題90分</option>
            <option value="course3">4300円＋飲み放題120分</option>
            <option value="course4">5300円＋飲み放題90分</option>
            <option value="course5">5300円＋飲み放題120分</option>
          </select>
        </div>
      )}

      {/* 個室 */}
      {people >= 7 && (
        <div>
          <label>
            <input
              type="checkbox"
              checked={isPrivate}
              onChange={(e) => setIsPrivate(e.target.checked)}
            />
            個室希望
          </label>
        </div>
      )}

      <button onClick={getAvailability}>空き時間検索</button>

      <hr />

      {/* 空き時間 */}
      <h2>空き時間</h2>

      {times.length === 0 ? (
        <p>空いている席がありません</p>
      ) : (
        <table border="1">
          <thead>
            <tr>
              <th>開始</th>
              <th>終了</th>
            </tr>
          </thead>

          <tbody>
            {times.map((t, i) => (
              <tr
                key={i}
                onClick={() => setSelectedTime(t)}
                style={{
                  cursor: "pointer",
                  background:
                    selectedTime?.start_at === t.start_at
                      ? "#ddd"
                      : "white",
                }}
              >
                <td>{t.start_at}</td>
                <td>{t.end_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* 予約入力 */}
      {selectedTime && (
        <div>
          <h3>予約情報</h3>

          <input
            placeholder="名前"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <input
            placeholder="メール"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            placeholder="電話番号"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
          />

          <button onClick={createReservation} disabled={loading}>
            {loading ? "予約中..." : "この時間で予約"}
          </button>
        </div>
      )}
    </div>
  );
}

export default Reservation;