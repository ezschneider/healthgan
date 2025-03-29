# HealthGAN

HealthGAN is a research-oriented project focused on generating synthetic, privacy-preserving health time series data using Generative Adversarial Networks (GANs). The main goal is to produce realistic yet anonymized sequences from diabetes patient records, enabling safe data sharing and robust model training.

---

## 🚀 Features

- Synthetic time series generation using GANs
- Real-world diabetes dataset with glucose, insulin, meals, and event codes
- Dockerized development environment with Python 3.12, Cython, and Jupyter
- Fast dependency management using [`uv`](https://github.com/astral-sh/uv)

---

## 💠 Development Setup

### Requirements

- Docker
- Docker Compose

### Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/healthgan.git
   cd healthgan
   ```

2. Extract the dataset:
   ```bash
   unzip diabetes.zip
   cd diabetes
   uncompress diabetes-data.tar.Z
   tar -xvf diabetes-data.tar
   ```

3. Build and run the container:
   ```bash
   docker-compose up --build
   ```

4. Open Jupyter Notebook in your browser:
   ```
   http://localhost:8888
   ```

---

## 📦 Dependencies

Defined in [`pyproject.toml`](./pyproject.toml). Key packages include:

- `cython`
- `numpy`, `pandas`, `scikit-learn`, `scipy`
- `notebook`

---

## 📁 Project Structure

```
healthgan/
├── Dockerfile             # Python 3.12 + uv + Jupyter
├── docker-compose.yml     # Container orchestration
├── pyproject.toml         # Project dependencies
├── notebooks/             # Jupyter notebooks and experiments
└── README.md              # This file
```

---

## 📌 Dataset Info

The project uses diabetes patient event logs consisting of timestamped events like:

- Blood glucose measurements
- Insulin doses
- Meal and activity logs

After downloading and unzipping the `diabetes.zip`, navigate into the extracted folder and also unzip the `diabetes-data.tar.Z` to access the full dataset.

---

## 📖 License

MIT License — feel free to use and adapt.

