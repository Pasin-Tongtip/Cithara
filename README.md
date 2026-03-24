# Set up instruction

1️⃣ First, you need to install Django.

```
python -m pip install Django
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
4️⃣ create admin access

```
python manage.py migrate

python manage.py createsuperuser
```

5️⃣ run the server

```
python manage.py runserver
```

6️⃣ go to this [link](http://127.0.0.1:8000/admin/)

7️⃣ login with the username and password you set in step 4️⃣.


# Justification

In the original design, the Mood class has only Sad and Happy, and the Occasion class has only Birthday, Wedding and Party.

Now I add Calm and Energetic into the Mood class, and I add Studying into the Occasion class. 

By adding more choices into those classes, the song creator will have more choices and can create more meaningful song. 
