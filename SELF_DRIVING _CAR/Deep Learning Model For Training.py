from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras import regularizers
from keras.models import model_from_json
from keras.models import load_model





classifier = Sequential()

classifier.add(Convolution2D(filters =32 , kernel_size = 3, input_shape = (64,48,3), activation = 'elu', padding = "valid"))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

classifier.add(Convolution2D(filters =32 , kernel_size = 3, activation = 'elu', padding = "valid"))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

classifier.add(Convolution2D(filters =64 , kernel_size = 3, activation = 'elu', padding = "valid"))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

classifier.add(Flatten())


classifier.add(Dense(units= 128, activation = 'elu', kernel_regularizer=regularizers.l2(0.001), activity_regularizer = regularizers.l1(0.001)))
classifier.add(Dense(units= 8, activation = 'softmax'))

classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])


from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator()
test_datagen = ImageDataGenerator()

training_set = train_datagen.flow_from_directory(
                                                'datanew/training_set',
                                                target_size=(64, 48),
                                                batch_size=32,
                                                class_mode='categorical', 
                                                shuffle = True,
                                                )

test_set = test_datagen.flow_from_directory(
                                            'datanew/test_set',
                                            target_size=(64, 48),
                                            batch_size=50,
                                            class_mode='categorical', 
                                            shuffle = True,
                                            )


classifier.fit_generator(
                        training_set,
                        steps_per_epoch=500,
                        epochs=20,
                        validation_data=test_set,
                        validation_steps=100
                        )
                

training_set.class_indices

model_json = classifier.to_json()
with open("./model2.json","w") as json_file:
  json_file.write(model_json)

classifier.save_weights("./model2.h5")
print("saved model..! ready to go.")
