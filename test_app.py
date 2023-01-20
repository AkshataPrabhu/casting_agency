import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors

PRODUCER_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBaWlJESm5uRlN2WFl3V1RyUFJYeSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhZ2VuY3ktYWtzaGF0YS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjNjNjhlN2RiMWU2ZDRmMTEyMmEwNjgwIiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjc0MjQ0MTEzLCJleHAiOjE2NzQyNTEzMTMsImF6cCI6IjJJUDRUS1Zncm9CU2hBYUo1dUNyTTZBeVh1N1pxVzM3Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.OW7ZAHMU7tOdhgMjxucs6z7l6CXr-yqTL-zrbbudhQicXxMAJ0Krq5SyIdbDRSL1VkSVfyrAP8tQZe3K2kpHZlUF5B6UTT7yNK_ZYwlF3zncOwcU2AiN14dMfzIsUpUpGpUHm7ffd-JdSMI5TLIuPlO1JE42s8FsNYDt2acZfd3J4bSoKcZpYuGV047z_WZQ6RBDAP3cOLW1XqtxSTfgUC6pUrbJeg_NCqhihmk1-jXhwU9rHvmVUqGT6QFyTnEO8bVuop_z4sVPyNpvWdzOsulbfZpT2AaumJCff608Pkoah5hmKypXED8EcBeogbz5INTwPxtNv-_NI1G9y2bXPA"
ASSISTANT_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBaWlJESm5uRlN2WFl3V1RyUFJYeSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhZ2VuY3ktYWtzaGF0YS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjNjNjhlNWY5N2U3NWUxYzM2ZDhjMmE3IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjc0MjQ0MTU2LCJleHAiOjE2NzQyNTEzNTYsImF6cCI6IjJJUDRUS1Zncm9CU2hBYUo1dUNyTTZBeVh1N1pxVzM3Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.dTMCcd53S7FnZ4d-ovriQaIuiVrmM_g2hGfyioVNuiNeYncPJ6mu7ffXw5ILerG2UAkYxLq_OHFC7NcS1Ls1gibLhYoevmEpesIimIT-SxAMmamDfJ7I85_aR-7WHkrQrX-G4goGJSzritlLZAQU_0AEhNbs4gioPCWBlThoz_tZ8debiamQYqzcQYGE0IpikXEVVw3igWRjtuUM5r15jgkIQeoR28VVb5oodIo4Ij92sdw2h014O6PQUGSeWziQ_xDG0JTRmtqlaICIgUFw-9ecmWW1JJ5uZOHxJR1SpeBSGbEDwThjFGsd23IAO_U6VeMF2cp9Z1L6_LTTyWItFw"
DIRECTOR_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBaWlJESm5uRlN2WFl3V1RyUFJYeSJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmdhZ2VuY3ktYWtzaGF0YS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjNjNjhlOWNkOGVkZDNmNzQwZjMyMTY5IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjc0MjQ0MTkxLCJleHAiOjE2NzQyNTEzOTEsImF6cCI6IjJJUDRUS1Zncm9CU2hBYUo1dUNyTTZBeVh1N1pxVzM3Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.xEFO4ua7sLyjBuTQ_uTUPwORn_0TKMYHgAV3T7LqMNPO72V7tJiFse1ohLTPY4-qiSqZuneNdj-JdRlbFrfT8CpZ4SHBm5_opkYweyk-tPVOwi7bj4PDg3ab1aBiELrsOV_Kf_zPD_jpxWOfzOzrCwfDuA5UPt9GQ0Cbq5onIXm_4WasElipUsC1oZ1sgZ2sanfX4MNR5_7ukpJMD7Wdha3GmaNZomEup10LE8oYNOeqbIbL6X2JDTCb-x9l7J7CCWuxiiKLHCKleMDM-3frjz00m4nEsaiyFedjb9vtySb5TYSnjl3tRf7HrrteIkXoZVAi1RTdwvys_GXtOrTtsg"


class CastingAgenttest(unittest.TestCase):

    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        setup_db(self.app)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_post_actors(self):
        res = self.client().post("/actor",
                                 headers={'Authorization': DIRECTOR_TOKEN},
                                 json={"name": "Jean", "age": "32", "gender": "male"})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_post_movie(self):
        res = self.client().post("/movie", headers={'Authorization': PRODUCER_TOKEN},
                                 json={"title": "Titanic", "release_date": "2023-01-19"})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_post_actors1(self):
        res = self.client().post("/actor",
                                 headers={'Authorization': DIRECTOR_TOKEN},
                                 json={"name": "John", "age": "31", "gender": "male"})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_post_movie1(self):
        res = self.client().post("/movie", headers={'Authorization': PRODUCER_TOKEN},
                                 json={"title": "Adventure", "release_date": "2023-01-29"})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_get_movies(self):
        res = self.client().get("/movies",
                                headers={'Authorization': f'{ASSISTANT_TOKEN}'})

        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_actors(self):
        res = self.client().get("/actors", headers={'Authorization': f'{ASSISTANT_TOKEN}'})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_patch_actors(self):
        res = self.client().patch("/actor/2",
                                  headers={'Authorization': PRODUCER_TOKEN},
                                  json={"name": "Jean P ", "age": "32", "gender": "male"})
        data = json.loads(res.data)
        print(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["updated"])

    def test_patch_movie(self):
        res = self.client().patch("/movie/2", headers={'Authorization': PRODUCER_TOKEN},
                                  json={"title": "New Titanic", "release_date": "2023-01-19"})
        data = json.loads(res.data)
        print(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["updated"])

    def test_404_delete(self):
        res = self.client().delete("/movie/11111", headers={'Authorization': f'{PRODUCER_TOKEN}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_404_delete_actor(self):
        res = self.client().delete("/actor/112313", headers={'Authorization': f'{DIRECTOR_TOKEN}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_actor(self):
        deleteid = "3"
        res = self.client().delete("/actor/" + deleteid, headers={'Authorization': f'{DIRECTOR_TOKEN}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_movie(self):
        deleteid = "3"
        res = self.client().delete("/movie/" + deleteid, headers={'Authorization': f'{PRODUCER_TOKEN}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
