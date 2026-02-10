from endee import Endee, Precision
from endee.exceptions import ConflictException, NotFoundException
from backend.config import INDEX_NAME, EMBEDDING_DIM



def get_index():
    client = Endee()

    try:
        client.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            space_type="cosine",
            precision=Precision.INT8D
        )
    except ConflictException:
        pass

    try:
        return client.get_index(INDEX_NAME)
    except NotFoundException:
        client.delete_index(INDEX_NAME)

        client.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            space_type="cosine",
            precision=Precision.INT8D
        )

        return client.get_index(INDEX_NAME)
