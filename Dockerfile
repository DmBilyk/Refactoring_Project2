FROM python:3.11-slim

WORKDIR /app

# Встановлюємо Java і утиліти
RUN apt-get update && apt-get install -y \
    openjdk-17-jre \
    wget \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо SonarScanner
RUN wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip \
    && unzip sonar-scanner-cli-5.0.1.3006-linux.zip \
    && mv sonar-scanner-5.0.1.3006-linux /opt/sonar-scanner \
    && ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/local/bin/sonar-scanner \
    && rm sonar-scanner-cli-5.0.1.3006-linux.zip

# Копіюємо залежності та встановлюємо їх
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проєкт
COPY . .

# Змінні середовища
ENV PYTHONUNBUFFERED=1

# Відкриваємо порт
EXPOSE 8000

# Команда за замовчуванням — міграція + запуск
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
