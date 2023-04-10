# Simple Similar Image Search Engine MVP

This is a simple image search engine MVP that leverages [Weaviate](https://weaviate.io/), a vector database that allows you to create and query embeddings with pre-trained deep learning models such as ResNet-50 to vectorize images.

## Getting Started

1. Create a virtual environment and install the dependencies by running the following commands:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Spin up the database by running the following command:

    ```bash
    docker-compose up -d
    ```

3. Run the script to add the images in the `images` folder to the database then query the database for the image nearest to the prompt image, `foo.png`:

    ```bash
    python -dir images -prompt foo.png
    ```
