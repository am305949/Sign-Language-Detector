def create(ges_name):
    import cv2
    import numpy as np
    import os

    def create_folder(folder_name):
        if not os.path.exists('./data/training_set/' + folder_name):
            os.mkdir('./data/training_set/' + folder_name)
        if not os.path.exists('./data/test_set/' + folder_name):
            os.mkdir('./data/test_set/' + folder_name)

    def capture_images(ges_name):
        create_folder(str(ges_name))

        cam = cv2.VideoCapture(0)

        cv2.namedWindow("test")

        img_counter = 0
        t_counter = 1
        training_set_image_name = 1
        test_set_image_name = 1
        listImage = [1, 2, 3, 4, 5]

        for loop in listImage:
            while True:
                ret, frame = cam.read()
                frame = cv2.flip(frame, 1)

                img = cv2.rectangle(frame, (425, 100), (625, 300), (0, 255, 0), thickness=2, lineType=8, shift=0)

                # get hsv values
                file = open('hsv_values.txt')
                loaded = file.read()
                h_low, h_high, s_low, s_high, v_low, v_high = int(loaded.split()[0]), int(loaded.split()[1]), int(
                    loaded.split()[2]), int(loaded.split()[3]), int(loaded.split()[4]), int(loaded.split()[5])
                lower_blue = np.array([h_low, s_low, v_low])
                upper_blue = np.array([h_high, s_high, v_high])

                imcrop = img[102:298, 427:623]
                hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, lower_blue, upper_blue)

                result = cv2.bitwise_and(imcrop, imcrop, mask=mask)

                cv2.putText(frame, str(img_counter), (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (127, 127, 255))
                cv2.imshow("test", frame)
                cv2.imshow("mask", mask)
                cv2.imshow("result", result)

                if cv2.waitKey(1) == ord('c'):

                    if t_counter <= 350:
                        img_name = "./data/training_set/" + str(ges_name) + "/{}.png".format(training_set_image_name)
                        save_img = cv2.resize(mask, (64, 64))
                        cv2.imwrite(img_name, save_img)
                        print("{} written!".format(img_name))
                        training_set_image_name += 1

                    if t_counter > 350 and t_counter <= 400:
                        img_name = "./data/test_set/" + str(ges_name) + "/{}.png".format(test_set_image_name)
                        save_img = cv2.resize(mask, (64, 64))
                        cv2.imwrite(img_name, save_img)
                        print("{} written!".format(img_name))
                        test_set_image_name += 1
                        if test_set_image_name > 250:
                            break

                    t_counter += 1
                    if t_counter == 401:
                        t_counter = 1
                    img_counter += 1

                elif cv2.waitKey(1) == 27:
                    break

            if test_set_image_name > 250:
                break

        cam.release()
        cv2.destroyAllWindows()

    capture_images(ges_name)
