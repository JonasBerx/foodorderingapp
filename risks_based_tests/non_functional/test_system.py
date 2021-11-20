from locust import HttpUser, task, between


class WebsiteTestCase(HttpUser):
    wait_time = between(0, 0.1)

    def on_start(self):
        # on_start is called when a Locust start before any task is scheduled.
        pass

    def on_stop(self):
        # on_stop is called when the TaskSet is stopping
        pass

    @task(1)
    def test_index(self):
        self.client.get("http://localhost:5000")
