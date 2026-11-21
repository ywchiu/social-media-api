"""Client for the LargitData Social Media Data API.

Collection endpoints are asynchronous: create a task with POST, then GET it by
id until its status leaves INIT / RUNNING. Paths are the ones in the reference,
for example /weibo/search/task or /threads/pushs/task.
"""
import os
import time

import requests

__all__ = ["Client", "TaskFailed"]
__version__ = "0.1.0"

BASE_URL = "https://api.infominer.io/api/v2"


class TaskFailed(RuntimeError):
    """The task ended with status FAILED."""


class Client:
    def __init__(self, api_key=None, base_url=BASE_URL, timeout=30):
        self.api_key = api_key or os.environ["LARGITDATA_API_KEY"]
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method, path, **kwargs):
        resp = requests.request(method, self.base_url + path, headers={"auth-header": self.api_key},
                                timeout=self.timeout, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def create(self, path, **body):
        """POST a task (or a query endpoint) and return the JSON response."""
        return self._request("POST", path, json=body)

    def poll(self, path, task_id, **query):
        """GET a task by id; query holds paging parameters such as page / pageSize."""
        return self._request("GET", f"{path}/{task_id}", params=query or None)

    def wait(self, path, task_id, interval=15, max_polls=120, **query):
        """Poll until the task leaves INIT / RUNNING and return the last response.

        A status other than DONE (PARTIAL, TIMED_OUT) is returned as is, since
        the response can still carry rows; FAILED raises TaskFailed. Only the
        one response is returned: page through larger results with poll(), and
        note that a Threads search, reply or timeline poll carries at most
        1000 rows.
        """
        for _ in range(max_polls):
            result = self.poll(path, task_id, **query)
            status = result.get("status") or (result.get("task") or {}).get("status")
            if status not in ("INIT", "RUNNING"):
                if status == "FAILED":
                    raise TaskFailed(task_id)
                return result
            time.sleep(interval)
        raise TimeoutError(f"task {task_id} still running after {max_polls} polls")
