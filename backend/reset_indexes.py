from endee import Endee

def delete_all_indexes():
    client = Endee("http://localhost:8080")

    indexes = client.list_indexes()
    if not indexes:
        print("No indexes to delete.")
        return

    for idx in indexes:
        client.delete_index(name=idx)
        print(f"Deleted index: {idx}")

    print("All indexes deleted.")

if __name__ == "__main__":
    delete_all_indexes()
