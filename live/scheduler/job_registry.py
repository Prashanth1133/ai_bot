class JobRegistry:

    def __init__(self):

        self._jobs = {}

    def register(self, job):

        self._jobs[job.id] = job

    def remove(self, job_id):

        self._jobs.pop(job_id, None)

    def get(self, job_id):

        return self._jobs.get(job_id)

    def jobs(self):

        return list(self._jobs.values())

    def clear(self):

        self._jobs.clear()