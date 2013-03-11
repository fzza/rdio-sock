# rdio-sock - Rdio WebSocket Library
# Copyright (C) 2013  fzza- <fzzzzzzzza@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from multiprocessing import Pool
import requests
from rdiosock.utils import return_data_type, random_id

DEFAULT_POOL_PROCESSES = 1
GENERATE_ID_MAX_RETRY = 5


pool = None
active_jobs = None


class RequestJob(object):
    def __init__(self, method, url, **kwargs):
        self.method = method
        self.url = url
        self.kwargs = kwargs

        self.job_id = None
        self.response_callback = None

    def generate_id(self):
        retry_count = 0

        while self.job_id is None:
            if retry_count > GENERATE_ID_MAX_RETRY:
                raise Exception()

            job_id = random_id()
            if job_id not in active_jobs:
                self.job_id = job_id
                active_jobs[self.job_id] = self
                return
            retry_count += 1

    def execute_sync(self):
        _, result = _request(None, self.method, self.url, self.kwargs)
        return result

    def execute(self, response_callback):
        self.response_callback = response_callback
        if self.job_id is None:
            self.generate_id()

        pool.apply_async(_request, [
            self.job_id, self.method, self.url, self.kwargs
        ], callback=_callback)


def _request(job_id, method, url, params):
    return job_id, return_data_type(requests.request(method, url, **params))


def _callback(result):
    job_id, result = result
    job = active_jobs.pop(job_id)
    job.response_callback(result)


def configure(processes=DEFAULT_POOL_PROCESSES):
    global pool
    pool = Pool(processes=processes)

    global active_jobs
    active_jobs = {}


def request(method, url, **kwargs):
    if pool is None:
        configure()
    job = RequestJob(method, url, **kwargs)
    return job
