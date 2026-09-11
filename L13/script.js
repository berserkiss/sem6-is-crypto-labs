// Класс для работы с текстовой стеганографией
class TextSteganography {
    constructor() {
        this.initializeEventListeners();
        this.currentMethod = 'kerning';
    }

    // Инициализация обработчиков событий
    initializeEventListeners() {
        // Переключение вкладок
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Кодирование кернинга
        document.getElementById('encode-k').addEventListener('click', () => {
            this.encodeKerning();
        });

        // Декодирование кернинга
        document.getElementById('decode-k').addEventListener('click', () => {
            this.decodeKerning();
        });

        // Кодирование длины строки
        document.getElementById('encode-ll').addEventListener('click', () => {
            this.encodeLineLength();
        });

        // Декодирование длины строки
        document.getElementById('decode-ll').addEventListener('click', () => {
            this.decodeLineLength();
        });

        // Генерация контейнера для kerning
        document.getElementById('generate-cover-k').addEventListener('click', () => {
            this.generateCoverTextK();
        });

        // Генерация контейнера для line-length
        document.getElementById('generate-cover-ll').addEventListener('click', () => {
            this.generateCoverTextLL();
        });
    }

    // Переключение между вкладками
    switchTab(tabName) {
        this.currentMethod = tabName;
        
        // Убираем активный класс со всех кнопок и контента
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

        // Добавляем активный класс к выбранной вкладке
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        document.getElementById(tabName).classList.add('active');
    }

    // Преобразование текста в бинарную строку (UTF-8, поддержка Unicode)
    textToBinary(text) {
        const encoder = new TextEncoder();
        const bytes = encoder.encode(text);
        return Array.from(bytes).map(byte => byte.toString(2).padStart(8, '0')).join('');
    }

    // Преобразование бинарной строки в текст (UTF-8, поддержка Unicode)
    binaryToText(binary) {
        const bytes = [];
        for (let i = 0; i < binary.length; i += 8) {
            const byte = binary.substr(i, 8);
            if (byte.length === 8) {
                bytes.push(parseInt(byte, 2));
            }
        }
        const decoder = new TextDecoder();
        return decoder.decode(new Uint8Array(bytes));
    }

    // Кодирование с использованием кернинга
    encodeKerning() {
        const coverText = document.getElementById('cover-text-k').value;
        const secretMessage = document.getElementById('secret-message-k').value;
        const baseKerning = parseInt(document.getElementById('kerning-value').value);
        const modificationValue = parseInt(document.getElementById('modification-value-k').value);

        if (!coverText || !secretMessage) {
            this.showNotification('Пожалуйста, введите текст-контейнер и секретное сообщение', 'error');
            return;
        }

        // Преобразуем секретное сообщение в бинарную строку
        const binaryMessage = this.textToBinary(secretMessage);
        // Добавляем маркер конца сообщения
        const messageWithEndMarker = binaryMessage + '00000000';
        // Разбиваем текст на символы (корректно для Unicode)
        const chars = Array.from(coverText);
        if (chars.length < messageWithEndMarker.length) {
            this.showNotification('Текст-контейнер слишком короткий для скрытия данного сообщения', 'error');
            return;
        }
        let encodedHTML = '';
        for (let i = 0; i < chars.length; i++) {
            const bit = i < messageWithEndMarker.length ? messageWithEndMarker[i] : '0';
            const kerning = bit === '1' ? baseKerning + modificationValue : baseKerning;
            const isModified = bit === '1';
            encodedHTML += `<span class="encoded-char${isModified ? ' modified' : ''}" style="margin-right: ${kerning}px;">${chars[i]}</span>`;
        }
        document.getElementById('encoded-text-k').innerHTML = encodedHTML;
        
        this.updateAnalysis(binaryMessage, 'kerning');
        this.showNotification('Текст успешно закодирован!', 'success');
    }

    // Декодирование кернинга
    decodeKerning() {
        const encodedElement = document.getElementById('encoded-text-k');
        const baseKerning = parseInt(document.getElementById('kerning-value').value);
        const modificationValue = parseInt(document.getElementById('modification-value-k').value);
        if (!encodedElement.children.length) {
            this.showNotification('Сначала закодируйте текст', 'error');
            return;
        }
        let binaryMessage = '';
        const chars = encodedElement.children;
        for (let i = 0; i < chars.length; i++) {
            const kerning = parseFloat(chars[i].style.marginRight);
            const threshold = baseKerning + modificationValue / 2;
            const bit = kerning > threshold - 0.5 ? '1' : '0';
            binaryMessage += bit;
            if (binaryMessage.endsWith('00000000')) {
                binaryMessage = binaryMessage.slice(0, -8);
                break;
            }
        }
        try {
            const decodedMessage = this.binaryToText(binaryMessage);
            document.getElementById('decoded-message-k').textContent = decodedMessage;
            this.showNotification('Сообщение успешно декодировано!', 'success');
        } catch (error) {
            document.getElementById('decoded-message-k').textContent = 'Ошибка декодирования';
            this.showNotification('Ошибка при декодировании сообщения', 'error');
        }
    }

    // Кодирование с использованием длины строки
    encodeLineLength() {
        const coverText = document.getElementById('cover-text-ll').value;
        const secretMessage = document.getElementById('secret-message-ll').value;
        const baseLineLength = parseInt(document.getElementById('line-length-value').value);
        const modificationValue = parseInt(document.getElementById('modification-value-ll').value);

        if (!coverText || !secretMessage) {
            this.showNotification('Пожалуйста, введите текст-контейнер и секретное сообщение', 'error');
            return;
        }

        // Преобразуем секретное сообщение в бинарную строку
        const binaryMessage = this.textToBinary(secretMessage);
        // Добавляем маркер конца сообщения
        const messageWithEndMarker = binaryMessage + '00000000';

        // Разбиваем текст на строки
        const lines = coverText.split('\n');
        if (lines.length < messageWithEndMarker.length) {
            this.showNotification('Текст-контейнер должен содержать больше строк для скрытия данного сообщения', 'error');
            return;
        }

        let encodedHTML = '';
        for (let i = 0; i < lines.length; i++) {
            const bit = i < messageWithEndMarker.length ? messageWithEndMarker[i] : '0';
            const lineLength = bit === '1' ? baseLineLength + modificationValue : baseLineLength;
            const isModified = bit === '1';
            
            // Обрезаем или дополняем строку до нужной длины
            let processedLine = lines[i];
            if (processedLine.length > lineLength) {
                processedLine = processedLine.substring(0, lineLength);
            } else if (processedLine.length < lineLength) {
                processedLine = processedLine.padEnd(lineLength, ' ');
            }
            
            encodedHTML += `<div class="encoded-line${isModified ? ' modified' : ''}" style="max-width: ${lineLength}ch;">${processedLine}</div>`;
        }
        document.getElementById('encoded-text-ll').innerHTML = encodedHTML;
        
        this.updateAnalysis(binaryMessage, 'line-length');
        this.showNotification('Текст успешно закодирован!', 'success');
    }

    // Декодирование длины строки
    decodeLineLength() {
        const encodedElement = document.getElementById('encoded-text-ll');
        const baseLineLength = parseInt(document.getElementById('line-length-value').value);
        const modificationValue = parseInt(document.getElementById('modification-value-ll').value);
        if (!encodedElement.children.length) {
            this.showNotification('Сначала закодируйте текст', 'error');
            return;
        }
        let binaryMessage = '';
        const lines = encodedElement.children;
        for (let i = 0; i < lines.length; i++) {
            const lineLength = parseInt(lines[i].style.maxWidth);
            const threshold = baseLineLength + modificationValue / 2;
            const bit = lineLength > threshold - 0.5 ? '1' : '0';
            binaryMessage += bit;
            if (binaryMessage.endsWith('00000000')) {
                binaryMessage = binaryMessage.slice(0, -8);
                break;
            }
        }
        try {
            const decodedMessage = this.binaryToText(binaryMessage);
            document.getElementById('decoded-message-ll').textContent = decodedMessage;
            this.showNotification('Сообщение успешно декодировано!', 'success');
        } catch (error) {
            document.getElementById('decoded-message-ll').textContent = 'Ошибка декодирования';
            this.showNotification('Ошибка при декодировании сообщения', 'error');
        }
    }

    // Генерация контейнера для kerning (по числу битов)
    generateCoverTextK() {
        const secretMessage = document.getElementById('secret-message-k').value;
        if (!secretMessage) {
            this.showNotification('Введите секретное сообщение!', 'error');
            return;
        }
        const binaryMessage = this.textToBinary(secretMessage);
        const totalBits = binaryMessage.length + 8; // +8 для маркера конца
        // Генерируем строку из totalBits символов (например, a, b, c ...)
        const alphabet = 'abcdefghijklmnopqrstuvwxyz';
        let chars = '';
        for (let i = 0; i < totalBits; i++) {
            chars += alphabet[i % alphabet.length];
        }
        document.getElementById('cover-text-k').value = chars;
        this.showNotification('Контейнер сгенерирован!', 'success');
    }

    // Генерация контейнера для line-length (по числу битов)
    generateCoverTextLL() {
        const secretMessage = document.getElementById('secret-message-ll').value;
        if (!secretMessage) {
            this.showNotification('Введите секретное сообщение!', 'error');
            return;
        }
        const binaryMessage = this.textToBinary(secretMessage);
        const totalBits = binaryMessage.length + 8; // +8 для маркера конца
        // Генерируем строки для кодирования
        let lines = [];
        for (let i = 1; i <= totalBits; i++) {
            lines.push(`Строка ${i} для кодирования бита ${i}`);
        }
        document.getElementById('cover-text-ll').value = lines.join('\n');
        this.showNotification('Контейнер сгенерирован!', 'success');
    }

    // Обновление анализа и статистики
    updateAnalysis(binaryMessage, method) {
        // Статистика кодирования
        const stats = {
            'Общее количество битов': binaryMessage.length,
            'Количество единиц': (binaryMessage.match(/1/g) || []).length,
            'Количество нулей': (binaryMessage.match(/0/g) || []).length,
            'Соотношение 1/0': ((binaryMessage.match(/1/g) || []).length / (binaryMessage.match(/0/g) || []).length).toFixed(2),
            'Метод кодирования': this.getMethodName(method)
        };

        let statsHTML = '';
        for (const [key, value] of Object.entries(stats)) {
            statsHTML += `<p><strong>${key}:</strong> ${value}</p>`;
        }
        document.getElementById('encoding-stats').innerHTML = statsHTML;

        // Визуализация битов
        let bitHTML = '';
        for (let i = 0; i < binaryMessage.length; i++) {
            const bit = binaryMessage[i];
            bitHTML += `<div class="bit ${bit === '1' ? 'one' : 'zero'}" title="Бит ${i+1}: ${bit}">${bit}</div>`;
        }
        document.getElementById('bit-visualization').innerHTML = bitHTML;
    }

    // Получение названия метода
    getMethodName(method) {
        const names = {
            'kerning': 'Кернинг',
            'line-length': 'Длина строки'
        };
        return names[method] || method;
    }

    // Дополнительные утилиты
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        if (type === 'success') {
            notification.style.background = 'linear-gradient(135deg, #4CAF50, #45a049)';
        } else if (type === 'error') {
            notification.style.background = 'linear-gradient(135deg, #f44336, #da190b)';
        } else {
            notification.style.background = 'linear-gradient(135deg, #2196F3, #0b7dda)';
        }

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Добавляем CSS анимации для уведомлений
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Инициализация приложения
document.addEventListener('DOMContentLoaded', () => {
    const steganography = new TextSteganography();
    
    // Добавляем глобальную переменную для доступа к методам
    window.steganography = steganography;
    
    console.log('Приложение стеганографии инициализировано');
}); 