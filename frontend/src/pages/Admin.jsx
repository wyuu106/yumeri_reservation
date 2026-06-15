// 管理者のページ

import { useNavigate } from "react-router-dom";

function Admin() {
  const navigate = useNavigate();

  return (
    <div>
      <h1>管理者メニュー</h1>

      <button
        onClick={() => navigate("/admin/seats")}
      >
        席設定
      </button>

      <br />
      
    </div>
  );
}

export default Admin;