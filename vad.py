import tensorflow as tf
import os
import time
import cv2

images_list = []

dir_path = r"/home/ramachandra_babu/data"
if dir_path is not None:
    images_in_dir = [os.path.join(dir_path, f)
                     for f in os.listdir(dir_path) if f.endswith('.jpg')]
    # Append images in the directory to images_list
    images_list += images_in_dir


if not images_list:
    print("images_list is empty. Nothing to predict. Exiting!")
    exit(0)


model_path = r"/media/ramachandra_babu/Local Disk/rd/model_3_batch_16/1538145105"
predictor_model = tf.contrib.predictor.from_saved_model(model_path)

class_list_f = os.path.join(model_path, "classes.txt")
with open(class_list_f) as f:
    classes_str_list = f.readlines()

# Remove whitespace characters.
classes_str_list = [class_name.strip() for class_name in classes_str_list]
classes_str_list.sort()
def visualize(image_path, class_name, probability):
    """
    Desc:
        This function displays the image whose class being predicted.
        The predicted class and probability is written on the image for
        easy visualization.

    Args:
        image_path: File path of the image being predicted.
        class_name: Class name predicted by the AI model.
        probability: Probability predicted for the class by the AI model.

    Returns:
        Nothing (None value, not meant to be caught).

    """
    # Strings to display over the image.
    class_string = "Class : " + class_name
    prob_string = "Prob: " + str(probability)

    font = cv2.FONT_HERSHEY_SIMPLEX

    # The predicted image.
    img = cv2.imread(image_path, 1)

    # Write the predicted class, the image.
    cv2.putText(img,
                class_string,
                (10, 20),
                font, 0.7,
                (255, 0, 0), 1,
                cv2.LINE_AA)

    # Write the probability predicted, on the image.
    cv2.putText(img,
                prob_string,
                (10, 45),
                font, 0.7,
                (255, 0, 0), 1,
                cv2.LINE_AA)

    # Display the image for the specified time delay. This delay
    # value can be varied using '-t' CLI option.
    # If 0 is passed as the delay value, it will wait indefinitely
    # till some Key is pressed.
    cv2.imshow('predicted_image', img)
    cv2.waitKey(5000)

    cv2.destroyAllWindows()


for i in range(len(images_list)):
    image = tf.read_file(images_list[i])
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize_images(image, [640, 480])

    with tf.Session() as sess:
        # Uncomment the below line for measuring time.
        # start_time = time.clock()

        # Convert the tensor object to NumPy array for feeding to the
        # predictor.
        prediction = predictor_model({"input": sess.run(image)})

        # Uncomment the below line for measuring time.
        # print("Approx. time taken for prediction : ",
        #       time.clock() - start_time)

    # Un-comment the below for debugging.
    # print("prediction = ", prediction)

    # The label predicted by the model
    predicted_class = prediction['classes'][0]

    # Probability of the predicted model.
    probability = prediction['probabilities'][0][predicted_class]

    b=print("Predicted_class for {} is: {}".format(
        images_list[i],
        classes_str_list[predicted_class]))
    c = print("Probability predicted for the class: ", probability)
    res =visualize(images_list[i],
              classes_str_list[predicted_class],
              probability)