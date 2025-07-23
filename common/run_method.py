# http_session.py  —— 轻量封装，内部自动调用日志器
from typing import Any, Dict

import requests
from api_logs import RequestLogger


class HttpSession:
    """带日志的 requests 封装"""

    def __init__(self):
        self.session = requests.Session()
        self.logger = RequestLogger()  # 单例

    def send(self, case_spec: Dict[str, Any]) -> requests.Response:
        """
        case_spec 必须包含：
        method, url, headers, data/json/body(可选)
        """
        method = case_spec["method"].upper()
        url = case_spec["url"]
        headers = case_spec.get("headers", {})
        body = case_spec.get("data") or case_spec.get("json") or case_spec.get("body")

        # 记录请求
        self.logger.log_request(method, url, headers, body)

        # 真正发送
        resp = self.session.request(
            method=method,
            url=url,
            headers=headers,
            json=body if isinstance(body, (dict, list)) else None,
            data=None if isinstance(body, (dict, list)) else body,
            timeout=10,
        )
        # 调试
        # print(resp.text)

        # 记录响应
        try:
            resp_json = resp.json()
        except ValueError:
            resp_json = resp.text
        self.logger.log_response(resp.status_code, dict(resp.headers), resp_json)

        return resp


if __name__ == "__main__":
    import dotenv

    from common.read_yaml import get_case

    dotenv.load_dotenv("config/.env")

    case = get_case("selectCrmCluePage", "success")
    session = HttpSession()
    resp = session.send(case)
    try:
        if resp.status_code == 200:
            try:
                print(resp.json())
            except ValueError:
                print("响应不是有效的JSON格式:")
                print(resp.text)
        else:
            print(f"请求失败，状态码: {resp.status_code}")
            print(resp.text)
    except Exception as e:
        print(f"发生错误: {e}")
