// 予約ページ

import { useEffect, useState } from "react";
import axios from "axios";
import { getErrorMessage } from "../utils/error_util";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

function Reservation() {
  const [closedDates, setClosedDates] = useState([]);
  const [date, setDate] = useState(null);
  
  const [people, setPeople] = useState("1");
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

  // 今日 から 翌月末 を計算
  const today = new Date();
  const maxDate = new Date(
    today.getFullYear(),
    today.getMonth() + 2,
    0
  );

  // 休業日一覧取得
  const getClosedDates = async () => {
    try {
      const res = await axios.get(
        "http://localhost:8000/closed_dates"
      );

      setClosedDates(
        res.data.map((d) => d.date)
      );

    } catch (error) {
      console.log(error);
      alert(getErrorMessage(error));
    }
  };

  // getClosedDatesを実行
  useEffect(() => {
    getClosedDates();
  }, []);

  // closedDateの型変換
  const closedDateObjects = closedDates.map(
    (d) => new Date(d)
  );

  // 空き時間取得
  const getAvailability = async () => {

    if (people === "" || Number(people) < 1) {
      alert("人数を入力してください");
      return;
    }

    if (people === "" || Number(people) < 1) {
      alert("人数を入力してください");
      return;
    }

    setTimes([]);
    setSelectedTime(null);

    try {
      const res = await axios.get("http://localhost:8000/availability", {
        params: {
          reservation_date: date.toISOString().split("T")[0],
          people: Number(people),
          kids,
          seat_type: seatType,
          course: Number(people) >= 4 ? course : "alacarte",
          is_private: Number(people) >= 7 && isPrivate,
        },
      });

      setTimes(res.data);
      console.log(times[0]);

    } catch (error) {
      console.log(error);
      alert(getErrorMessage(error));
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

        people: Number(people),
        kids,
        seat_type: seatType,
        course: Number(people) >= 4 ? course : "alacarte",
        is_private: Number(people) >= 7 && isPrivate,

        // 選択肢した日付と時間をdatetimeに変換して送る
        start_at: `${date}T${selectedTime.time}:00`,
      });

      alert("予約完了！");
      
    } catch (error) {
      console.log(error);
      alert(getErrorMessage(error));
    }
  };

  return (
    <div>
      <h1>予約ページ</h1>

      {/* 日付 */}
      <div>
        <p>日付</p>

        <DatePicker
          selected={date}
          onChange={(d) => setDate(d)}
          minDate={today}
          maxDate={maxDate}
          excludeDates={closedDateObjects}
          dateFormat="yyyy-MM-dd"
        />
      </div>

      {/* 人数 */}
      <div>
        <p>人数</p>
        <input
          type="number"
          min={1}
          value={people}
          onChange={(e) => setPeople(e.target.value)}
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
          <option value="horigotatsu">掘りごたつ</option>
          <option value="tatami">座敷</option>
        </select>
      </div>

      {/* コース */}
      {Number(people) >= 4 && (
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
      {Number(people) >= 7 && (
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
      <table
        border="1"
        style={{
          width: "100%",
          borderCollapse: "collapse",
        }}
      >
        <thead>
          <tr>
            <th style={{ padding: "8px" }}>
              開始
            </th>
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
              <td style={{ padding: "8px" }}>
                {t.start_at}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

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