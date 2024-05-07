from django.contrib.auth import \
    get_user_model  # Importe la fonction get_user_model pour obtenir le modèle utilisateur actuel
from django.test import SimpleTestCase, TestCase  # Importe les classes de test Django
from django.urls import reverse  # Importe la fonction reverse pour la résolution d'URLs


class HomePageTests(SimpleTestCase):  # Définit une classe de test pour la page d'accueil
    def test_home_page_status_code(self):  # Méthode de test pour vérifier le code d'état de la page d'accueil
        response = self.client.get('/')  # Effectue une requête GET à l'URL de la page d'accueil
        self.assertEqual(response.status_code, 200)  # Vérifie que le code d'état de la réponse est 200 (OK)

    def test_view_url_by_name(self):  # Méthode de test pour vérifier l'URL de la vue par son nom
        response = self.client.get(reverse('home'))  # Effectue une requête GET à l'URL de la vue d'accueil
        self.assertEqual(response.status_code, 200)  # Vérifie que le code d'état de la réponse est 200 (OK)

    def test_view_uses_correct_template(self):  # Méthode de test pour vérifier l'utilisation du bon modèle
        response = self.client.get(reverse('home'))  # Effectue une requête GET à l'URL de la vue d'accueil
        self.assertEqual(response.status_code, 200)  # Vérifie que le code d'état de la réponse est 200 (OK)
        self.assertTemplateUsed(response, 'home.html')  # Vérifie que le modèle utilisé est 'home.html'


class SignupPageTests(TestCase):  # Définit une classe de test pour la page d'inscription
    username = 'newuser'  # Nom d'utilisateur pour le test
    email = 'newuser@email.com'  # Adresse e-mail pour le test

    def test_signup_page_status_code(self):  # Méthode de test pour vérifier le code d'état de la page d'inscription
        response = self.client.get('/users/signup/')  # Effectue une requête GET à l'URL de la page d'inscription
        self.assertEqual(response.status_code, 200)  # Vérifie que le code d'état de la réponse est 200 (OK)

    def test_view_url_by_name(self):  # Méthode de test pour vérifier l'URL de la vue par son nom
        response = self.client.get(reverse('signup'))  # Effectue une requête GET à l'URL de la vue d'inscription
        self.assertEqual(response.status_code, 200)  # Vérifie que le code d'état de la réponse est 200 (OK)

    def test_view_uses_correct_template(self):  # Méthode de test pour vérifier l'utilisation du bon modèle
        response = self.client.get(reverse('signup'))  # Effectue une requête GET à l'URL de la vue d'inscription
        self.assertEqual(response.status_code, 200)  # Vérifie que le code d'état de la réponse est 200 (OK)
        self.assertTemplateUsed(response, 'signup.html')  # Vérifie que le modèle utilisé est 'signup.html'

    def test_signup_form(self):  # Méthode de test pour vérifier le formulaire d'inscription
        new_user = get_user_model().objects.create_user(  # Crée un nouvel utilisateur
            self.username, self.email)  # en utilisant le nom d'utilisateur et l'adresse e-mail
        self.assertEqual(get_user_model().objects.all().count(), 1)  # Vérifie qu'un seul utilisateur existe
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)  # Vérifie le nom d'utilisateur
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)  # Vérifie l'adresse e-mail
