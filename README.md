# Laboratory Reservation System

## Autors
- Thomas PAZZÉ
- Léo BERNARD
- Nino SAUVAGEOT

## Description
Introducing the Laboratory Room Reservation System tailored for CreStic. This innovative system streamlines the process of reserving laboratory spaces, offering researchers a seamless platform to schedule and manage their experimental work.

## Requirements
- Python 3.9.x

### Project setup
1. In the project's root directory, create a virtual environment
    ```shell
    $ python -m venv venv
    ```
2. Activate the environment
    - If in a Linux environment
        ```shell
        source venv/bin/activate
        ```
    - If in a Windows environment
        ```shell
        venv\Scripts\activate
        ```
3. Install the dependencies
    ```shell
    pip install -r requirements.txt
    ```
4. Migrate the models
    ```shell
    python manage.py migrate
    ```
5. Create a superuser account. If you log in using this in the website, you'll be able to add rooms that the hotel offers.
    ```shell
    python manage.py createsuperuser
    ```

### Running the project
1. Run the server
    ```shell
    python manage.py runserver
    ```
You should now be able to access the project on `localhost:8000`


---
### Disclaimer
Project was originally forked from https://github.com/c3n7/hotel-reservation
