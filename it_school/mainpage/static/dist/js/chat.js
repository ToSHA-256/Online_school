const roomName = '{{ room_name }}';
const user = '{{ user }}';

// Функция для генерации случайного тёмного цвета
function getRandomDarkColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Объект для хранения цветов пользователей
const userColors = {};

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data.message;
    const author = data.author; // Получаем автора сообщения из данных

    // Получаем цвет пользователя из объекта userColors или генерируем новый цвет
    let userColor = userColors[author];
    if (!userColor) {
        userColor = getRandomDarkColor();
        userColors[author] = userColor;
    }

    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const timestamp = hours + ':' + minutes;
    const messageWithTimestamp = '<div style="border: 1px solid #ccc; background-color: ' + userColor + '; color: #fff; padding: 10px; border-radius: 10px; margin-bottom: 10px;">' +
        '<pre><strong>' + author + '</strong>: ' + message + '</pre>' +
        '<p style="font-size: 12px; color: #888;">' + timestamp + '</p>' +
        '</div>';
    const chatLog = document.querySelector('#chat-log');
    chatLog.innerHTML += messageWithTimestamp;
    chatLog.scrollTop = chatLog.scrollHeight; // Прокручиваем чат вниз
};

document.querySelector('#chat-input').addEventListener('keyup', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        const messageInputDom = document.querySelector('#chat-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message,
            'author': user  // Отправляем имя автора сообщения
        }));
        messageInputDom.value = '';
    }
});

document.querySelector('#chat-message-submit').addEventListener('click', function(e) {
    const messageInputDom = document.querySelector('#chat-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'author': user  // Отправляем имя автора сообщения
    }));
    messageInputDom.value = '';
});