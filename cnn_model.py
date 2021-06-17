def train():
    import matplotlib.pyplot as plt
    from keras.models import Sequential
    from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout
    from keras.preprocessing.image import ImageDataGenerator
    from keras import optimizers,  backend as K
    K.set_image_data_format('channels_first')

    # Initialing the CNN
    classifier = Sequential()

    # Convolution Layer
    classifier.add(Convolution2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu', padding='same'))
    # MaxPooling Layer
    classifier.add(MaxPooling2D((2, 2), padding='same'))
    # 2nd convolution layer
    classifier.add(Convolution2D(32, (3, 3), activation='relu', padding='same'))
    classifier.add(MaxPooling2D((2, 2), padding='same'))
    # 3rd Convolution Layer
    classifier.add(Convolution2D(64, (3, 3), activation='relu', padding='same'))
    classifier.add(MaxPooling2D((2, 2), padding='same'))
    # Flattening Layer
    classifier.add(Flatten())
    # Fully Connected Layer
    classifier.add(Dense(256, activation='relu'))
    classifier.add(Dropout(0.5))
    classifier.add(Dense(26, activation='softmax'))

    # Compiling The CNN
    classifier.compile(optimizer=optimizers.SGD(lr=0.01), loss='categorical_crossentropy', metrics=['accuracy'])

    # Fitting the CNN to the image
    train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1./255)

    training_set = train_datagen.flow_from_directory('data/training_set', target_size=(64, 64), batch_size=32, class_mode='categorical')

    test_set = test_datagen.flow_from_directory('data/test_set', target_size=(64, 64), batch_size=32, class_mode='categorical')

    model = classifier.fit_generator(training_set, steps_per_epoch=800, epochs=25, validation_data=test_set, validation_steps=6500)

    # Saving the model
    classifier.save('Trained_model.h5')

    '''
    print(model.history.keys())
    print(model.history.values())
    '''

    # plot accuracy vs epochs
    plt.plot(model.history['accuracy'])
    plt.plot(model.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # plot loss vs epochs
    plt.plot(model.history['loss'])
    plt.plot(model.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
