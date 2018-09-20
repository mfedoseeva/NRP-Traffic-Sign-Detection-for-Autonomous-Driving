##
## TensorFlow object detection, based on:
## https://github.com/GoogleCloudPlatform/tensorflow-object-detection-example
##
# internal TensorFlow state variables to persist
@nrp.MapVariable("tensorflow_venv", initial_value="/home/bbpnrsoa/.opt/tensorflow_venv")
@nrp.MapVariable("object_detection_api", initial_value="/home/bbpnrsoa/.opt/models/research")
@nrp.MapVariable("model_path", initial_value="/home/bbpnrsoa/.opt/graph_def")
@nrp.MapVariable("detection_threshold", initial_value=0.9)
@nrp.MapVariable("detection_graph", initial_value=None)
@nrp.MapVariable("sess", initial_value=None)
@nrp.MapVariable("category_index", initial_value=None)
@nrp.MapVariable("bridge", initial_value=None)
@nrp.MapVariable("sign", initial_value=None, scope=nrp.GLOBAL)
# input generators to drive the Braitenberg brain
# @nrp.MapSpikeSource("left_eye", nrp.brain.sensors[slice(0, 3, 2)], nrp.poisson)
# @nrp.MapSpikeSource("right_eye", nrp.brain.sensors[slice(1, 4, 2)], nrp.poisson)
# subscribe to images from the robot
@nrp.MapRobotSubscriber("camera", Topic('/husky/camera', sensor_msgs.msg.Image))
# publish an annotated image as output of this transfer function
@nrp.Neuron2Robot(Topic('/detections', sensor_msgs.msg.Image))
def object_detection(t, tensorflow_venv, object_detection_api, model_path, detection_threshold, detection_graph, sess, category_index, bridge, sign, camera): #, left_eye, right_eye):
    from PIL import Image, ImageDraw
    import numpy
    # initialize the TensorFlow Object Detection session and store it as needed
    if detection_graph.value is None:

        # import TensorFlow in the NRP, update this path for your local installation
        try:
            import site
            site.addsitedir(tensorflow_venv.value + '/lib/python2.7/site-packages')
            import tensorflow as tf
        except:
            clientLogger.info("Unable to import TensorFlow, did you change the path in the transfer function?")
            raise

        # configure Object Detection environment
        import sys

        # paths to saved model states, update these paths if different in your local installation
        MODEL_BASE = object_detection_api.value
        sys.path.append(MODEL_BASE)
        sys.path.append(MODEL_BASE + '/object_detection')
        sys.path.append(MODEL_BASE + '/slim')

        PATH_TO_CKPT = model_path.value + '/frozen_inference_graph.pb'
        PATH_TO_LABELS = model_path.value + '/label_map.pbtxt'

        # initialize the detection graph
        import object_detection.utils.label_map_util as label_map_util
        #from utils import label_map_util
        detection_graph.value = tf.Graph()
        with detection_graph.value.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
                sess.value = tf.Session(graph=detection_graph.value)

        # create internal label and category mappings
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map,
                                                                    max_num_classes=4,
                                                                    use_display_name=True)
        category_index.value = label_map_util.create_category_index(categories)

        # OpenCV bridge for ROS <-> CV image conversion
        from cv_bridge import CvBridge, CvBridgeError
        bridge.value = CvBridge()

        # initialized, start searching
        sign.value = ''

    # no image received yet, do nothing
    if camera.value is None:
        return

    # convert the ROS image to an OpenCV image and Numpy array
    cv_image = bridge.value.imgmsg_to_cv2(camera.value, "rgb8")
    numpy_image = np.expand_dims(cv_image, axis=0)

    # run the actual detection
    image_tensor = detection_graph.value.get_tensor_by_name('image_tensor:0')
    boxes = detection_graph.value.get_tensor_by_name('detection_boxes:0')
    scores = detection_graph.value.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.value.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.value.get_tensor_by_name('num_detections:0')

    (boxes, scores, classes, num_detections) = sess.value.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: numpy_image})

    boxes, scores, classes, num_detections = map(
        np.squeeze, [boxes, scores, classes, num_detections])

    # annotate detections on the image
    pil_image = Image.fromarray(cv_image)
    detections = []
    closest_sign = {'name': '', 'square': -1}

    for i in range(num_detections):

        # only accept high enough detection scores
        if scores[i] < detection_threshold.value: continue

        name = category_index.value[classes[i]]['name']
        # log the detection at timestamp
        clientLogger.info(t, name, scores[i])
        detections.append(name)

        # annotate the image with boxes
        draw = ImageDraw.Draw(pil_image)
        im_width, im_height = pil_image.size
        ymin, xmin, ymax, xmax = boxes[i]

        (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                      ymin * im_height, ymax * im_height)
        draw.line([(left, top), (left, bottom), (right, bottom),
                   (right, top), (left, top)], width=int(scores[i]*10)-4, fill='red')

        square = (xmax - xmin) * (ymax - ymin)
        if closest_sign['square'] < square:
            closest_sign['square'] = square
            closest_sign['name'] = name

    clientLogger.info("Closest sign:", closest_sign['name'])
    sign.value = closest_sign['name']

    # publish a ROS image with annotations
    return bridge.value.cv2_to_imgmsg(numpy.array(pil_image), "rgb8")

