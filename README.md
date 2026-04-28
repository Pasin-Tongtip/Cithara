# Set up instruction

1️⃣ First, you need to install Django and the required libraries.

```
python -m pip install Django requests python-dotenv google-auth
```

2️⃣ Go to your terminal and cd into your repository.

Then, run the command below.

```
git clone https://github.com/Pasin-Tongtip/Cithara.git
```

3️⃣ cd into Cithara repository by running:

```
cd Cithara
```

4️⃣ Create your environment file by create a file named .env at the root of the project:

5️⃣ Add your API key:

```
SUNO_API_KEY=your_actual_key_here
```

6️⃣ Set up database by running:

```
python manage.py migrate
```

7️⃣ Run the server:

```
python manage.py runserver
```

8️⃣ Go to this [link](http://127.0.0.1:8000/cithara/login/)

9️⃣ Login with your google account.


# Running In Mock Mode

1️⃣ Set USE_MOCK_GENERATOR = True in your settings.py (at line 126)

2️⃣ You can generate the song now 🫡


# Running In SUNO Mode

1️⃣ Ensure your SUNO API key is in the .env file

2️⃣ Set USE_MOCK_GENERATOR = False in your settings.py (at line 126)

3️⃣ You can generate the song now 🫡


# Justification

In the original design, the Mood class has only Sad and Happy, and the Occasion class has only Birthday, Wedding and Party.

Now I add Calm and Energetic into the Mood class, and I add Studying into the Occasion class. 

By adding more choices into those classes, the song creator will have more choices and can create more meaningful song. 
