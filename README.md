# Thomas deBlaquiere's Personal Portfolio Web App

![Screenshot](https://storage.googleapis.com/thomasd9e.appspot.com/website/Portfolio.png)

## Project Description

This web app serves as a personal portfolio for Thomas deBlaquiere, showcasing his skills, experience, and projects. It includes a CustomUser class for user creation, login/logoff capabilities, and protected views. The app also features the "CFB Assistant" project, demonstrating the integration of ChatGPT with a knowledge base to create a subject matter expert chatbot.

## Installation and Deployment

1. Clone the repository:
   ```bash
   git clone https://github.com/tdwebdesign/thomasd9e.git
   ```

2. Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. Update environment variables:
   - Create a `.env` file in the project directory or set the necessary environment variables for:
     - Database configuration: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
     - Debug mode: `DEBUG`
     - Secret key: `SECRET_KEY`
     - OpenAI API key: `OPENAI_API_KEY`

4. Acquire an OpenAI API key from [openai.com](https://openai.com) to interact with the API.

5. Initialize gcloud with your project information for deployment.

## Dependencies

This project is built using Python Django and utilizes a PostgreSQL database. It interfaces with OpenAI through its API, requiring an API key. All required dependencies are listed in the `requirements.txt` file in the project directory.

## Database Setup

Database configuration is handled through environmental variables. Make sure to set the necessary variables (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT) to establish a connection with the PostgreSQL database. Django handles database migrations, so follow the usual Django workflow for migrations.

## Environment Variables

Environmental variables are managed using the `dotenv` Python package. Apart from the database variables, the app requires the following environment variables to be set:
- `DEBUG`: Set to `True` for development and `False` for production.
- `SECRET_KEY`: Django secret key for secure sessions.
- `OPENAI_API_KEY`: OpenAI API key for interacting with the ChatGPT API.

## Static Files and Media

Static files and media are served using a CDN. Use the `collectstatic` command to collect and serve the static files.

## Testing

This project uses Django's built-in test framework for testing purposes. You can easily run the tests using the following command:
```bash
python manage.py test
```
This command will discover and execute all the test cases in your Django application.

## How to Run

To run the app locally, use the following command:
```bash
python manage.py runsslserver
```

## Deployment Instructions

1. Run `gcloud init` and provide your project information.
2. Deploy the app using:
   ```bash
   gcloud app deploy
   ```

## Contact Information

For any inquiries or feedback, please contact Thomas deBlaquiere at tdwebdesignmsu@yahoo.com.

