import argparse
import os
from base64 import b64decode, b64encode
from pathlib import Path

from rich.console import Console
import weaviate


console = Console()


def create_class(dir: str, client: weaviate.Client) -> str:
    client.schema.get()

    class_obj = {
        'class': (class_name := Path(dir).stem.title()),
        'vectorizer': 'img2vec-neural',
        'vectorIndexType': 'hnsw',
        'moduleConfig': {'img2vec-neural': {'imageFields': ['image']}},
        'properties': [{'name': 'image', 'dataType': ['blob']}, {'name': 'text', 'dataType': ['string']}],
    }
    client.schema.create_class(class_obj)

    return class_name


def load_imgs(dir: str, class_name: str, client: weaviate.Client) -> None:
    for root, _, files in os.walk(dir):
        for file in files:
            if file == '.DS_Store':
                continue
            with open(os.path.join(root, file), 'rb') as meme_file:
                client.data_object.create({'image': b64encode(meme_file.read()).decode('utf-8'), 'text': file}, class_name)


def nearest_image_query(class_name: str, client: weaviate.Client, prompt_img: str) -> str:
    if os.path.exists(result_path := f'{class_name}-{Path(prompt_img).stem}.png'):
        os.remove(result_path)

    with open(result_path, 'wb') as file:
        file.write(
            b64decode(
                client.query.get(class_name, ['image'])
                .with_near_image({'image': prompt_img})
                .with_limit(1)
                .do()['data']['Get'][class_name][0]['image']
            )
        )

    return result_path


def cli() -> tuple[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument(f'-{(var:="dir")}', dest=var, type=str, required=True, help="Path to directory")
    parser.add_argument(f'-{(var:="prompt")}', dest=var, type=str, required=True, help="Path to prompt file")
    args = parser.parse_args()
    return args.dir, args.prompt


def main() -> None:
    dir, prompt = cli()

    client = weaviate.Client(
        url='http://localhost:8080',
    )

    class_name = create_class(dir, client)

    load_imgs(dir, class_name, client)

    console.print(f'Nearest image to {nearest_image_query(class_name, client, prompt)}')


if __name__ == '__main__':
    main()
