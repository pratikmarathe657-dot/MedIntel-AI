import chromadb



# =====================================
# CHROMA DATABASE
# =====================================


CHROMA_PATH = "chroma_db"



client = chromadb.PersistentClient(
    path=CHROMA_PATH
)






# =====================================
# COLLECTION HANDLER
# =====================================


def get_collection(chat_id):


    collection_name = (
        f"chat_{chat_id}"
    )


    collection = client.get_or_create_collection(

        name=collection_name

    )


    return collection







# =====================================
# STORE EMBEDDINGS
# =====================================


def store_embeddings(

    chat_id,
    chunks,
    embeddings

):


    collection = get_collection(

        chat_id

    )



    ids = []

    documents = []

    metadatas = []




    for index, chunk in enumerate(chunks):


        ids.append(

            f"{chat_id}_{index}"

        )



        # -----------------------------
        # Extract text
        # -----------------------------

        if isinstance(chunk, dict):


            text = chunk.get(

                "text",

                ""

            )


            page = chunk.get(

                "page"

            )


        else:


            text = str(chunk)

            page = None




        documents.append(text)



        metadatas.append({

            "chat_id": chat_id,

            "page": page

        })





    # -----------------------------
    # Store vectors
    # -----------------------------

    collection.add(

        ids=ids,

        documents=documents,

        embeddings=embeddings,

        metadatas=metadatas

    )



    print(

        "Stored embeddings for:",

        chat_id

    )


    return True







# =====================================
# SEARCH EMBEDDINGS
# =====================================


def search(

    chat_id,

    query_embedding,

    n_results=5

):


    try:


        collection_name = (

            f"chat_{chat_id}"

        )



        # Do not create collection
        # during search

        collection = client.get_collection(

            name=collection_name

        )



        result = collection.query(

            query_embeddings=[

                query_embedding

            ],

            n_results=n_results

        )



        formatted_results = []



        documents = result.get(

            "documents",

            []

        )


        metadatas = result.get(

            "metadatas",

            []

        )



        if documents:


            docs = documents[0]


            metas = (

                metadatas[0]

                if metadatas

                else []

            )



            for i,text in enumerate(docs):


                page = None



                if i < len(metas):


                    page = metas[i].get(

                        "page"

                    )



                formatted_results.append({

                    "text": text,

                    "page": page

                })



        return formatted_results




    except Exception as e:


        print(

            "SEARCH ERROR:",

            e

        )


        return []








# =====================================
# DELETE CHAT COLLECTION
# =====================================


def delete_collection(chat_id):


    collection_name = (

        f"chat_{chat_id}"

    )



    try:


        client.delete_collection(

            name=collection_name

        )


        print(

            "Deleted Chroma collection:",

            collection_name

        )


        return True




    except Exception as e:


        print(

            "DELETE COLLECTION ERROR:",

            e

        )


        return False