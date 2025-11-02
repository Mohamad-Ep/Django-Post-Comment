from locust import HttpUser, task

# _______________________________________________________


class QuickstartUser(HttpUser):
    def on_start(self):
        payload = {"email": "reza_bakht@gmail.com", "password": "Aa123456@"}
        response = self.client.post("/accounts/api/v1/jwt/create/", json=payload)

        print("LOGIN RESPONSE:", response.status_code, response.text)

        if response.status_code == 200:
            token = response.json().get("access")
            self.client.headers = {"Authorization": f"Bearer {token}"}
        else:
            self.environment.runner.quit()

    @task
    def get_post_list(self):
        self.client.get("/blog/api/v1/posts/")

    @task
    def get_comment_list(self):
        self.client.get("/comments/api/v1/comment-list/")


# _______________________________________________________
