def extract_keywords(topic):
    from keybert import KeyBERT
    from sentence_transformers import SentenceTransformer, util
    import sqlite3

    kw_model = KeyBERT()
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    # topic = "Python"
    topic_embedding = embedding_model.encode(topic, convert_to_tensor=True)

    # Connect to your database
    conn = sqlite3.connect("zoom_chat.db")
    cursor = conn.cursor()

    # Fetch all messages
    cursor.execute("SELECT id, message FROM chat_data")
    rows = cursor.fetchall()

    # Analyze each message
    for row_id, message in rows:
        # Extract keywords from the message
        keywords = kw_model.extract_keywords(message, keyphrase_ngram_range=(1, 2), stop_words='english', use_maxsum=True, top_n=2)
        
        relevant_keywords = []
        for kw, _ in keywords:
            kw_embedding = embedding_model.encode(kw, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(kw_embedding, topic_embedding).item()

            # Consider similar if similarity > 0.5
            if similarity > 0.1:
                relevant_keywords.append(kw)

        # Join keywords and update DB
        joined = ", ".join(set(relevant_keywords))
        cursor.execute("UPDATE chat_data SET matched_keywords = ? WHERE id = ?", (joined, row_id))
        if relevant_keywords:
            print(relevant_keywords)

    conn.commit()
    conn.close()
    print("✅ Keywords related to topic stored in `matched_keywords` column.")

