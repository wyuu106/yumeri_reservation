// ログインページ

import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { getErrorMessage } from "../utils/error_util";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  // ログイン処理
  const login = async (e) => {
    e.preventDefault();

    try {
      // OAuth2PasswordRequestForm は form-data 形式で送る必要がある
      const formData = new URLSearchParams();

      formData.append("username", username);
      formData.append("password", password);

      const response = await axios.post(
        "http://127.0.0.1:8000/admin/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      // トークン保存
      localStorage.setItem("token", response.data.access_token);

      navigate("/Admin");
    } catch (error) {
      console.log(error);
      alert(getErrorMessage(error));
    }
  };

  return (
    <div>
      <h1>ログイン</h1>

      <form onSubmit={login}>
        <div>
          <p>ユーザー名</p>

          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div>
          <p>パスワード</p>

          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button type="submit">
          ログイン
        </button>
      </form>
    </div>
  );
}

export default Login;