from services.embedding_service import create_query_embedding
from services.vector_db import search



# =====================================
# RETRIEVE RELEVANT DOCUMENT CHUNKS
# =====================================

def retrieve_chunks(
    chat_id: str,
    question: str
):

    try:


        # --------------------------------
        # Create embedding for user query
        # --------------------------------

        query_embedding = create_query_embedding(

            question

        )



        # --------------------------------
        # Search inside selected chat
        # --------------------------------

        results = search(

            chat_id,

            query_embedding

        )



        print(

            "Retrieved Results:",

            len(results)

            if results

            else 0

        )



        # --------------------------------
        # No matching chunks
        # --------------------------------

        if not results:


            return {

                "context":"",

                "pages":[]

            }





        context = []

        pages = set()



        # --------------------------------
        # Extract text + pages
        # --------------------------------

        for item in results:



            if not item:

                continue



            text = item.get(

                "text",

                ""

            )



            if text:


                context.append(

                    text

                )




            page = item.get(

                "page"

            )



            if page is not None:


                pages.add(

                    page

                )






        return {


            "context":

                "\n\n".join(context),



            "pages":

                sorted(

                    list(pages)

                )

        }





    except Exception as e:


        print(

            "RETRIEVAL ERROR:",

            e

        )


        return {


            "context":"",


            "pages":[]

        }