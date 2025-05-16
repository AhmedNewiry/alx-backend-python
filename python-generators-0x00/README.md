```markdown
# Python Generators: Streaming Data from MySQL

This project demonstrates the use of Python generators to stream data efficiently from a MySQL database (`ALX_prodev`) in the context of the `alx-backend-python` curriculum.

## Repository Structure
- **Repository**: `alx-backend-python`
- **Directory**: `python-generators-0x00`
- **Files**:
  - `seed.py`: Sets up the `ALX_prodev` database and `user_data` table, populating it with `user_data.csv`.
  - `0-stream_users.py`: Generator to stream `user_data` rows one by one.
  - `1-batch_processing.py`: Generator to fetch and process `user_data` in batches, filtering users over 25.
  - `2-lazy_paginate.py`: Generator for lazy pagination of `user_data`.
  - `4-stream_ages.py`: Generator to stream ages and compute average age memory-efficiently.
  - `README.md`: This file.

## Prerequisites
- **MySQL**: Running locally (host: `localhost`, user: `root`, password: empty or configured).
- **Python**: 3.8+ with a virtual environment.
- **Dependencies**:
  ```bash
  pip install mysql-connector-python
  ```
- **CSV File**: `user_data.csv` with columns `user_id`, `name`, `email`, `age`.

## Setup
1. **Start MySQL**:
   ```bash
   sudo service mysql start
   ```
2. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install mysql-connector-python
   ```
4. **Prepare CSV**: Ensure `user_data.csv` is in the project directory.
5. **Run Setup**:
   ```bash
   ./0-main.py
   ```

## Tasks
1. **Task 0: Database Setup** (`seed.py`)
   - Sets up `ALX_prodev` database and `user_data` table (`user_id`, `name`, `email`, `age`).
   - Populates with `user_data.csv`, skipping duplicates.
   - Run: `./0-main.py`

2. **Task 1: Stream Users** (`0-stream_users.py`)
   - Generator `stream_users()` yields rows one by one.
   - Uses one loop.
   - Run: `./1-main.py`

3. **Task 2: Batch Processing** (`1-batch_processing.py`)
   - Generator `stream_users_in_batches(batch_size)` fetches batches.
   - `batch_processing(batch_size)` filters users over 25.
   - Uses two loops.
   - Run: `./2-main.py | head -n 5`

4. **Task 3: Lazy Pagination** (`2-lazy_paginate.py`)
   - Generator `lazy_paginate(page_size)` yields pages using `paginate_users`.
   - Uses one loop.
   - Run: `./3-main.py | head -n 7`

5. **Task 4: Memory-Efficient Aggregation** (`4-stream_ages.py`)
   - Generator `stream_user_ages()` yields ages.
   - `calculate_average_age()` computes average age without SQL `AVERAGE`.
   - Uses two loops.
   - Run: `python3 4-stream_ages.py`

## Notes
- **Database**: MySQL, unlike the PostgreSQL-based `alx-airbnb-database`.
- **Performance**: Generators ensure memory efficiency for large datasets (~10,000+ rows).
- **Error Handling**: Scripts handle MySQL and file errors gracefully.
- **Constraints**: Adheres to loop limits and generator requirements.

```