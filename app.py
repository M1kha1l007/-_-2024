import os
import threading
from pyngrok import ngrok
from flask import Flask, render_template, request, make_response
import requests, base64
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from generate_image import generate_image


os.environ["FLASK_ENV"] = "development"

app = Flask(__name__)
port = 5000

#Setting an auth token allows us to open multiple tunnels at the same time
ngrok.set_auth_token("2Wmx2exUH6e5PAIeQOXEckaXvVs_4hWoY1YztkxBJcZYtmBB4")

# Open a ngrok tunnel to the HTTP server
public_url = ngrok.connect(port).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

# Update any base URLs to use the public ngrok URL
app.config["BASE_URL"] = public_url


app = Flask(__name__)
data = [["Формат А3, вертикальный", (3508, 4961)],
        ['Формат А4 (два изображения на листе, вертикальный', (2480, 3508)],
        ['горизонтальный', (1920, 1080)],
        [
            'горизонтальный, нижняя четверть (около 190 px) не занимается текстом или другими важными элементами,предусмотреть отступы сверху и слева около60 px до текста и других элементов',
            (1200, 593)],
        [
            '(горизонтальный) 72 dpi, предусмотреть отступы сверху, снизу, слева и справа около 60 px до текста и других элементов',
            (1200, 520)],
        [
            '(вертикальный), без текста, однотонное пространство в левом верхнем углу для размещения логотипа (не менее 10% от высоты изображения)',
            (700, 1080)],
        ["72 dpi, одно доминирующее тематическое изображение без надписей и мелких элементов", (1084, 585)]]
data2 = ['Плакат А3', 'Листовка А5', 'Скринсейвер', 'Баннер (кликабельный)', 'Баннер (кликабельный)',
         'Иллюстрация к новости', 'Иллюстрация на анонс']
data3 = ['Информационные доски', 'настольные демонстрационные системы (тейбл-тенты)',
         'Экраны блокировки персональных компьютеров', 'Интранет-портал', 'Дайджест новостей (e-mail рассылка)',
         'ТВ-панель', 'Информационное сообщение']



# @app.route("/")
@app.route('/', methods=['GET', 'POST'])
def home():
    title = 'Home'
    if request.method == 'POST':
        # name = request.form
        prmt1 = request.form['prm1']
        num = request.form['e']
        print(prmt1, num)
        prompt = f'Сгенерируй изображение в формате {data2[int(num) - 1]}; носителем для которого является {data3[int(num) - 1]}, с текстовыми вставками, которые отображают это событие: {prmt1}; требования по оформлению: {data[int(num) - 1][0]}'
        size = data[int(num) - 1][1]
        print(prompt, size)
        w, h = size[0], size[1]

        generate_image(prompt, 'static/image.jpg', w, h)

        return render_template('main.html', title=title, src='static/image.jpg', width=w, height=h)
    return render_template('main.html', title=title)


threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()