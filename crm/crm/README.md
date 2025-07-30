# CRM GraphQL Backend

## Setup

1. **Install Redis**:
   ```bash
   sudo apt install redis-server
   sudo systemctl start redis
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Add cron jobs**:
   ```bash
   python manage.py crontab add
   ```
