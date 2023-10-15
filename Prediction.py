#!/usr/bin/env python
# coding: utf-8

# In[1]:


#get_ipython().system('pip install tensorflow google-cloud-storage')


# In[6]:


import tensorflow as tf
from google.cloud import storage
from sklearn import datasets
from sklearn.model_selection import train_test_split
from google.cloud import storage
import os
# 1. Sample dataset and preprocessing
data = datasets.load_iris()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Define a simple Neural Network model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(4,)),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 3. Train the model
model.fit(X_train, y_train, epochs=10)

# 4. Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {accuracy}")

# 5. Save the model
model_save_path = "saved_model/my_model"
model.save(model_save_path)

# 6. Upload the saved model to GCP bucket
bucket_name =  "mybucket_004788"

# Set up GCS client
client = storage.Client()
bucket = client.bucket(bucket_name)

# Upload all files in the saved directory
for root, _, files in os.walk(model_save_path):
    for file in files:
        local_file = os.path.join(root, file)
        blob_path = os.path.relpath(local_file, start=model_save_path)
        blob = bucket.blob(f"{model_save_path}/{blob_path}")
        blob.upload_from_filename(local_file)

print(f"Model uploaded to {bucket_name}/{model_save_path}.")



# In[ ]:




