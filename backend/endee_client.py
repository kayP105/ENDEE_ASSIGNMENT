from endee import Endee, Precision
from endee.exceptions import ConflictException, NotFoundException
from backend.config import INDEX_NAME, EMBEDDING_DIM



def get_index():
    client = Endee()

    try:
        # Try to create index (safe if it doesn't exist)
        client.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            space_type="cosine",
            precision=Precision.INT8D
        )
    except ConflictException:
        # Index name exists — this is fine
        pass

    try:
        # Try to fetch the index
        return client.get_index(INDEX_NAME)
    except NotFoundException:
        # Index metadata exists but files are missing → recreate
        client.delete_index(INDEX_NAME)

        client.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            space_type="cosine",
            precision=Precision.INT8D
        )

        return client.get_index(INDEX_NAME)
