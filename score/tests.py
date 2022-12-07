from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import datetime
from .models import *
from django.urls import reverse


class TeamTests(TestCase):
    image = open("test_img.png", "rb")

    @classmethod
    def setUpTestData(cls):
        cls.team = Team.objects.create(
            name="team1",
            thumbnail=SimpleUploadedFile(
                cls.image.name, cls.image.read(), content_type="image/jpeg"
            ),
        )

    def test_team_model(self):
        self.assertEqual(self.team.name, "team1")
        self.assertEqual(
            self.team.thumbnail.read(),
            open("test_img.png", "rb").read(),
        )
        self.assertEqual(str(self.team), "team1")


class PlayerTests(TestCase):
    image = open("test_img.png", "rb")
    image2 = open("test_img.png", "rb")

    @classmethod
    def setUpTestData(cls):

        cls.team = Team.objects.create(
            name="team1",
            thumbnail=SimpleUploadedFile(
                cls.image.name, cls.image.read(), content_type="image/jpeg"
            ),
        )

        cls.player = Player.objects.create(
            name="player1",
            image=SimpleUploadedFile(
                cls.image2.name, cls.image2.read(), content_type="image/jpeg"
            ),
            team=cls.team,
        )

    def test_player_model(self):
        self.assertEqual(self.player.name, "player1")
        self.assertEqual(
            self.player.image.read(),
            open("test_img.png", "rb").read(),
        )

        self.assertEqual(self.player.team, self.team)
        self.assertEqual(self.player.team.name, "team1")


class MatchTests(TestCase):
    image = open("test_img.png", "rb")
    date = datetime.datetime.now(tz=timezone.utc)

    @classmethod
    def setUpTestData(cls):

        cls.team1 = Team.objects.create(
            name="team1",
            thumbnail=SimpleUploadedFile(
                cls.image.name, cls.image.read(), content_type="image/jpeg"
            ),
        )

        cls.team2 = Team.objects.create(
            name="team2",
            thumbnail=SimpleUploadedFile(
                cls.image.name, cls.image.read(), content_type="image/jpeg"
            ),
        )

        cls.match = Match.objects.create(
            team1=cls.team1,
            team2=cls.team2,
            start_date=cls.date,
            end_date=cls.date,
        )

    def test_match_model(self):
        self.assertEqual(self.match.team1, self.team1)
        self.assertEqual(self.match.team2, self.team2)
        self.assertEqual(self.match.team1.name, "team1")
        self.assertEqual(self.match.team2.name, "team2")
        self.assertEqual(self.match.start_date, self.date),

        self.assertEqual(
            self.match.end_date,
            self.date,
        )

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "team1")
        self.assertContains(response, "team2")

    def test_home_url_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_update_url_name(self):
        response = self.client.get(reverse("update_score"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update_score.html")


class ScoreTests(TestCase):
    image = open("test_img.png", "rb")
    date = datetime.datetime.now(tz=timezone.utc)

    @classmethod
    def setUpTestData(cls):
        cls.team1 = Team.objects.create(
            name="team1",
            thumbnail=SimpleUploadedFile(
                cls.image.name, cls.image.read(), content_type="image/jpeg"
            ),
        )

        cls.team2 = Team.objects.create(
            name="team2",
            thumbnail=SimpleUploadedFile(
                cls.image.name, cls.image.read(), content_type="image/jpeg"
            ),
        )

        cls.match = Match.objects.create(
            team1=cls.team1,
            team2=cls.team2,
            start_date=cls.date,
            end_date=cls.date,
        )

        cls.player = Player.objects.create(
            name="player1",
            image=SimpleUploadedFile(
                cls.image.name, cls.image.read(), content_type="image/jpeg"
            ),
            team=cls.team1,
        )

        cls.score = Score.objects.create(match=cls.match, player=cls.player, score=23)

    def test_score_model(self):
        self.assertEqual(self.score.match, self.match)
        self.assertEqual(self.score.player, self.player)
        self.assertEqual(self.score.score, 23)
        self.assertEqual(self.score.match.team1, self.team1)
        self.assertEqual(self.score.match.team2, self.team2)
        self.assertEqual(self.score.player.name, "player1")

    def test_update_score_view(self):
        response = self.client.post(
            reverse("update_score"),
            {"match": self.match.id, "player": self.player.id, "score": 4},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Score.objects.last().score, 27)
        self.assertEqual(Score.objects.last().match, self.match)
        self.assertEqual(Score.objects.last().player, self.player)
